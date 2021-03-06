#!/usr/bin/env python

'''The setup script.'''

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['click~=8.0.0', 'requests~=2.25.1', 'tinyrpc~=1.0.4']

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest>=3',
    'requests-mock~=1.9.2',
]

setup(
    author='Eli Gothill',
    author_email='eli.gothill@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='A lightweight Python client for Radix.',
    install_requires=requirements,
    license='MIT license',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['pyradix', 'radix'],
    name='pyradix-dlt',
    packages=find_packages(include=['pyradix', 'pyradix.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/gothill/pyradix-dlt',
    version='0.0.1',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'pyradix=pyradix.cli:start',
        ]
    },
)
