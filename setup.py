#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from setuptools import setup, find_packages
from docs import getVersion


# Variables ===================================================================
changelog = open('CHANGELOG.rst').read()
long_description = "\n\n".join([
    open('README.rst').read(),
    changelog
])


# Actual setup definition =====================================================
setup(
    name='edeposit.amqp.aleph_link_export',
    version=getVersion(changelog),
    description="Subsystem for updating Edeposit's links in Aleph.",
    long_description=long_description,
    url='https://github.com/edeposit/edeposit.amqp.aleph_link_export/',

    author='Edeposit team',
    author_email='edeposit@email.cz',

    classifiers=[
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Developers',

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",

        "License :: OSI Approved :: MIT License",
    ],
    license='MIT',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['edeposit', 'edeposit.amqp'],

    zip_safe=False,
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines(),

    test_suite='py.test',
    tests_require=["pytest"],
    extras_require={
        "test": [
            "pytest",
        ],
        "docs": [
            "sphinx",
            "sphinxcontrib-napoleon",
        ]
    },
)
