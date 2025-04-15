# !/usr/bin/env python
"""
Setup script for PObjects package
"""

from setuptools import setup
import os
description = open( os.path.join( os.path.dirname( __file__ ),
                                  'PObjects',
                                  'README.md'),
                    'r').read()
setup(
    name = "PObjects",
    packages = ["PObjects"],
    include_package_data = True,
    package_data = {
        "PObjects":[]
        },
    version = "2.0.0",
    description = "Set of Python classes encapsulating physical objects",
    author = "W. Ekkehard Blanz",
    author_email = "Ekkehard.Blanz@gmail.com",
    url = "https://github.com/Ekkehard/PObjects.git",
    keywords = ["Physical Computing", "Engineering", "SI Units"],
    install_requires=[
        "setuptools", 
        "gpiod >= 2.2"],
    license='LICENSE.md',
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: release 2.0.0",
        "Intended Audience :: Physicists and engineers",
        "License :: Apache License",
        "Operating System :: Linux :: Windows :: Mac OS",
        "Topic :: computing with physical objects",
        ],
    long_description = description
    )
 
