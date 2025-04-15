## Make Implementation: make shared libraries and install a Python package
##
## @version    1.2.0
##
## @par Purpose
##             This is the Makefile in a source Python package directory.  It
##             allows to build shared C/C++ libraries that the package might
##             need as well as the installation of the package with the site
##             packages for the current user in the current Conda environment.
##
## @par Synopsis
##             make all        to make C/C++ source libraries if present
##             make default    same as all
##             make shared     same as all
##             make docs       to make the Doxygen documentation of this package
##             make check      to run the Unit Tests of this package
##             make clean      to clean up temporary files
##             make distclean  to clean up everything that was built
##             make package    to bundle a package into a tar ball
##             make install    to install the package
##             make uninstall  to uninstall the package
##             make help       to print helpful information
##             make Version    to display the Version information
##
## @par Comments
##             This Makefile supports sub-packages, which are stored in
##             sub-directories of the main directory in which this Makefile
##             resides.  All files in these sub-directories will be installed.
##             Files that should not be installed are easiest kept in separate
##             sub-directories, which can then be excluded in a customize.mak
##             file.  Also files without the extension .py in the main directory
##             will never be installed (with the exception of requirements.txt).
##             The Makefile also supports building shared libraries.  For this,
##             the source of the shared (C or C++) libraries and their Python
##             API must be in sub-directories of the directory where this
##             Makefile resides and contain a Makefile that can build a "shared"
##             target, whereby the resulting shared libraries must be placed in
##             the directory where this Makefile resides.  Details are left to
##             the Makefile in the sub-directory for the libraries, which is
##             usually libMakefile from the same author as this Makefile.
##             Library directories will not be installed, only the resulting
##             shared libraries.  All sub-directories with a Makefile are
##             considered library subdirectories (unless excluded in
##             customize.mak) In addition, this Makefile supports the execution
##             of Unit Tests.  These Unit Tests are a set of Python scripts
##             starting with "test_" - Unit Test scripts are not installed.
##             Lastly, the Makefile supports the generation of Doxygen
##             documentation, which will be placed in the sub-directory docs;
##             all Python scripts are included in the generation of this
##             documentation.  The documentation will not be installed unless
##             instructed to do so in the customize.mak file.
## @par
##             The installation will be done in the "activated" Conda
##             environment (if applicable).  For this Makefile to find the
##             installation directory, numpy must be installed.
## @par
##             This Makefile also supports the flags MDEBUG and LATEX that can
##             be used to either print additional debug information for this
##             Makefile or to switch on additional LaTeX documentation for the
##             target docs - otherwise only html documentation is generated.
##             Both flags can be given in addition to the target as
##                   <TAG>=ON
##             i.e. to generate additional LaTeX documentation
##                   make docs LATEX=ON
##
## @par Known Bugs
##             None
##
## @author     W. Ekkehard Blanz <Ekkehard.Blanz@gmail.com> (C) 2022-2023
##
## @copyright  See COPYING file that comes with this distribution
##
##

# File history:
#       Date        | Author         | Modification
#  -----------------+----------------+------------------------------------------
#   Thu Nov 23 2022 | Ekkehard Blanz | created
#   Mon Nov 28 2022 | Ekkehard Blanz | fixed rsync issues on Mac
#   Thu Dec 09 2022 | Ekkehard Blanz | now allows several shared libraries to be
#                   |                | built
#   Tue May 16 2023 | Ekkehard Blanz | fixed unnecessary error message
#   Thu Sep 29 2023 | Ekkehard Blanz | now also runs under Msys2 in Windows
#                   |                |

## @cond

.PHONY: default all shared docs clean distclean check install uninstall help package

onePound := \#
twoPounds := \#\#

# We need the name of the current Makefile for the help target
yoursTruly := $(CURDIR)/$(lastword $(MAKEFILE_LIST))

# function to escape blanks
escapeBlanks = $(strip $(subst $(empty) $(empty),\ ,$1))

# these are the tools that are the same across all platforms
LS      := ls
LN      := ln -fs
MV      := mv -f
CAT     := cat
RM      := rm -rf
GREP    := grep
SED     := sed
AWK     := awk
HEAD    := head
MKDIR   := mkdir -p

# determin which platform (Windows, Linux, or Mac) and which OS (Windows or
# Cygwin) we are running under and define fn to be able to do
# $(call fn,$(MY_FILENAME))
ifneq "$(findstring Windows, $(OS))" ""
    ifeq "$(CYGPATH)" ""
        $(info The CYGPATH environment variable is not set.)
        $(error Please run setupWinArduino before making anything.)
    endif
    CYGPATH := $(subst \,/,$(CYGPATH))
	
    ifneq "$(findstring CYGWIN, $(shell uname))" ""
	    # we are running under cygwin
        SHELL := /bin/bash
    else ifneq "$(findstring x86_64, $(shell uname -rs))" ""
        # we aree running under Msys2
        SHELL := /bin/bash
    else
        # even though we require cygwin to be installed, we do not require that
        # this Makefile is called from a cygwin shell, it can be windows as well
        SHELL := $(CYGPATH)/bin/bash.exe
    endif
    ifeq "" "$(wildcard $(SHELL))"
        $(error Cygwin installation does not contain bash shell)
    endif
    fn       = $(subst \,/,$1)
    installed = $(firstword $(strip $(if $(suffix $1),\
        $(call lastword,$(notdir $(shell which $1))), \
        $(strip $(call lastword,$(notdir $(shell which $1.bat 2>/dev/null))) \
        $(call lastword,$(notdir $(shell which $1.exe 2>/dev/null)))))))
    # prevent the backslash from acting as a line-continuation character
    SEPCHAR := \$(empty)
    CP      := cp -fuvr
    PYTHON  := py
else ifeq "$(shell uname)" "Linux"
    SHELL   := /bin/bash
    fn       = $(call escapeBlanks,$1)
    SEPCHAR := /
    CP      := cp -fuvr
    installed = $(notdir $(shell which $1))
    PYTHON  := $(call installed,python3)
else ifeq "$(shell uname)" "Darwin"
    SHELL   := /opt/homebrew/bin/bash
    fn       = $(call escapeBlanks,$1)
    SEPCHAR := /
    CP      := rsync -rogpuLvW
    installed = $(notdir $(shell which $1))
    PYTHON  := $(call installed,python3)
endif

DOXYGEN := $(call installed,doxygen)

ifeq "setup.py" "$(wildcard setup.py)"
    PackageName := $(strip $(shell grep "name " setup.py | xargs | \
                                cut -d " " -f 3 | \
                                sed 's/\(.*\),/\1 /'))
    Version := $(strip $(shell grep "version " setup.py | xargs | \
                            cut -d " " -f 3 | \
                            sed 's/\(.*\),/\1 /') )
    TarName := $(PackageName)-$(Version).tar.gz
else
    PackageName := $(shell echo $${PWD$(twoPounds)*/})
endif

# We assume that every directory that contains a Makefile is a Library directory
# that does not get installed - only the resulting shared library does
LibDirs := $(dir $(shell $(LS) */Makefile 2> /dev/null ))

# all other directories, other than the "usual suspects," are considered
# sub-packages
SubPackages := $(filter-out $(LibDirs) doc/ __pycache__/,$(shell $(LS) -d */))
# remove the training slash
SubPackages := $(subst /,,$(SubPackages))

# we won't install the test scripts indicated by starting with test_*.py
TestScripts := $(wildcard test_*.py)

# We take all other scripts for installation
Scripts := $(filter-out $(TestScripts),$(wildcard *.py))

# Libraries may come into existence later - so no := assignment
Libraries = $(strip $(wildcard *.so) $(wildcard *.dll))

# we determine the installation location by figuring out where numpy resides
# if it is not installed, we have a problem
InstallDir := $(shell $(PYTHON) -m pip show numpy | $(GREP) Location | \
                $(SED) '-e s/Location: //')$(SEPCHAR)$(PackageName)$(SEPCHAR)
InstallDir := $(call fn,$(InstallDir))
ifeq "$(InstallDir)" "$(SEPCHAR)$(PackageName)$(SEPCHAR)"
    $(error numpy must be installed for this makefile to work)
endif

Docfiles := $(strip $(Scripts) $(foreach d,$(SubPackages),$(wildcard $(d)*py)))

# Without the quotes, it sometimes doesn't work - very strange
DOXYFILE := "docs/Doxyfile"

ifneq "$(LATEX)" ""
    SedLaTeXcommand :=
else
    SedLaTeXcommand := -e 's/^GENERATE_LATEX *=.*/GENERATE_LATEX = NO/g'
endif

SpecialFiles := $(strip $(wildcard requirements.txt) $(wildcard README.md))

InstallCandidates = $(strip $(SubPackages) $(Scripts) $(Libraries) \
                            $(SpecialFiles))

PREINSTALL    :=
POSTINSTALL   :=
PREUNINSTALL  :=
POSTUNINSTALL :=


# -------------------------> Customization Section <----------------------------
# If any of the previously defined variables are not acceptable, they can be
# redefined here or in the customize.mak file.
#LibDirs := $(filter-out tools,$(LibDirs))
#Scripts := $(filter-out workScript.py,$(Scripts))
# Also, special additional PREINSTALL and POSTINSTALL as well as PREUNINSTALL
# and POSTUNINSTALL options can be specified
#PREINSTALL    :=
#POSTINSTALL   :=
#PREUNINSTALL  :=
#POSTUNINSTALL :=
# There is also a chance to specify a multitude of library names, which makes
# only sense if there is only one library directory
#LIBNAME := im_py_b im_py_w im_py_i im_py_d
# In this case the Makefile in the lib directory is called with LIBNAME set
# to each element in the LIBNAME list in turn
# ----------------------> End of Customization Section <------------------------

ifeq "customize.mak" "$(wildcard customize.mak)"
    include customize.mak
endif

ifneq "$(LIBNAME)" ""
    ifneq "$(words $(LibDirs))" "1"
        $(error LIBNAME can only be specified with single librrary directories)
    endif
endif

ifneq "$(MDEBUG)" ""
    $(info SHELL = $(SHELL))
    $(info SEPCHAR = $(SEPCHAR))
    $(info LIBNAME = $(LIBNAME))
    $(info PackageName = $(PackageName))
    $(info LibDirs = $(LibDirs))
    $(info SubPackages = $(SubPackages))
    $(info TestScripts = $(TestScripts))
    $(info Scripts = $(Scripts))
    $(info Libraries = $(Libraries))
    $(info InstallDir = $(InstallDir))
    $(info InstallCandidates = $(InstallCandidates))
    $(info Docfiles = $(Docfiles))
    $(info SedLaTeXcommand = $(SedLaTeXcommand))
    $(info TarName = $(TarName))
    $(info yoursTruly = $(yoursTruly))
    ifeq "$(MDEBUG)" "STOP"
        $(error exiting as requested...)
    endif
endif

default all shared:
	@if [[ -n "$(LibDirs)" ]]; then \
	    echo "Making shared libraries in $(LibDirs) ..."; \
	fi
	@for dir in $(LibDirs); do \
	    if [[ -z "$(LIBNAME)" ]]; then \
	        if "$(MAKE)" -C $$dir shared; then \
	            echo ""; \
		    else \
		        break; \
		    fi; \
	    else \
	        for lib in $(LIBNAME); do \
				echo "making" $$lib; \
	            if "$(MAKE)" -C $$dir shared LIBNAME=$$lib; then echo ""; \
	            else break; \
	            fi; \
	            if "$(MAKE)" -C $$dir clean; then echo ""; \
	            else break; \
	            fi; \
	        done; \
	    fi; \
	done

clean:
	@echo "Cleaning up temporary and backup files..."
	$(RM) *~
	$(RM) build
	@for dir in $(LibDirs); do \
	    if "$(MAKE)" -C $$dir $@; then echo ""; \
	    else break; \
	    fi; \
	done
	@for dir in $(SubPackages); do \
	    cd $$dir; \
	    $(RM) *~; \
	    cd ..; \
	done

distclean: clean
	@echo "Cleaning up everything that was ever built..."
	$(RM) $(Libraries)
	$(RM) *.egg-info
	$(RM) dist
	@for dir in $(LibDirs); do \
	    if "$(MAKE)" -C $$dir $@; then echo ""; \
	    else break; \
	    fi; \
	done

docs: $(DOXYFILE) $(Docfiles)
	@echo "Making Doxygen documentation..."
	@echo $(InstallCandiates)
	$(DOXYGEN) $(DOXYFILE)
	@if [ -d docs/html ]; then \
	    $(LN) $(PWD)/docs/html/index.html $(PWD)/docs/index.html; \
	fi
	@if [ -d docs/latex ]; then \
	    $(MAKE) -C docs/latex all; \
	fi

install: default
	@echo "Installing package $(PackageName)..."
	$(PREINSTALL)
	@if ! [[ -e __init__.py ]]; then \
        echo ERROR: File __init__.py is missing; \
        exit 1; \
    fi
	@if ! [[ -e requirements.txt ]]; then \
        echo ERROR: File requirements.txt is missing; \
        exit 1; \
    fi
	@if ! [[ -e setup.py ]]; then \
        echo WARNING: File setup.py is missing; \
    fi
	@if ! [[ -e README.md ]]; then \
        echo WARNING: File README.md is missing; \
    fi
	@$(MKDIR) $(InstallDir)
	@for file in $(InstallCandidates); do \
	    $(CP) $$file $(InstallDir).; \
	done
	$(POSTINSTALL)

uninstall:
	@echo "Uninstalling package $(PackageName)..."
	$(PREUNINSTALL)
	$(RM) $(InstallDir)
	$(POSTUNINSTALL)

check:
	@echo "Running Unit Tests for package $(PackageName)..."
	@for s in $(TestScripts); do \
	    $(PYTHON) $$s; \
	done

package: setup.py MANIFEST.in dist/$(TarName)

help:
	@NUM=`$(GREP) "^\# File history" $(yoursTruly) -n | \
	      $(AWK) -F: '{print $$1}'`;\
	let "NUM--"; \
	$(HEAD) -n $$NUM $(yoursTruly) | \
            $(SED) -e 's/^##//g' \
                   -e 's/@par //g' \
                   -e 's/@par/ /g' \
                   -e 's/^ @/ /g'

Version:
	@echo "Versions:"
	@echo "pythonPackageMakefile" \
        `$(GREP) '@version' $(yoursTruly) | $(AWK) '{print $$3;exit}'`
	@echo "GNU make" $(MAKE_VERSION)
	@$(PYTHON) -V


$(DOXYFILE):
	@if [ -z "$(DOXYGEN)" ]; then \
	     echo "Error: doxygen needs to be installed to make docs"; \
	else \
	    if [ ! -d docs ]; then \
	        mkdir docs; \
        fi; \
        $(DOXYGEN) -g - | \
        $(SED) -e 's/^PROJECT_NAME *=.*/PROJECT_NAME = $(PackageName)/g' \
               -e 's/^OUTPUT_DIRECTORY *=.*/OUTPUT_DIRECTORY = docs/g' \
               -e 's|^INPUT *=.*|INPUT = $(Docfiles)|g' \
               $(SedLaTeXcommand) \
        > $(DOXYFILE); \
    fi

dist/$(TarName): *.py *.md requirements.txt setup.py docs/html/* MANIFEST.in
	@echo creating tar ball for package $@ ...
	$(CP) $(PWD)/setup.py $(PWD)/../setup.py
	$(CP) $(PWD)/MANIFEST.in $(PWD)/../MANIFEST.in
	$(CP) $(PWD)/README.md $(PWD)/../README.md
	cd .. && $(PYTHON) setup.py build
	cd .. && $(PYTHON) setup.py sdist
	$(MV) $(PWD)/../dist $(PWD)
	$(MV) $(PWD)/../build $(PWD)
	$(MV) $(PWD)/../*.egg-info $(PWD)
	$(RM) $(PWD)/../README.md $(PWD)/../setup.py $(PWD)/../MANIFEST.in

## @endcond
