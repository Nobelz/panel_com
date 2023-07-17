import pathlib
import setuptools

from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='panel_com_g2',
    version='0.2',
    description='Panel controller rewrite for Reiser\'s Generation 2 Panels.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Nobelz/panel_com',
    author='Nobel Zhou',
    author_email='nxz157@case.edu',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    project_urls={
        'Issue Tracker': 'https://github.com/Nobelz/panel_com/issues',
    }
)