#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    setup for py_tracker_iou package
"""

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'numpy',
]

setup(
    name='py_tracker_iou',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description="PyTrackerIou package",
    long_description=readme,
    author="Taras Lishchenko",
    author_email='taras.lishchenko@gmail.com',
    url='https://github.com/jackersson/py-tracker-iou.git',
    packages=[
        'py_tracker_iou',
    ],
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=True,
    keywords='py_tracker_iou',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ]
)
