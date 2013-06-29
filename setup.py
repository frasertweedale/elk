from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='elk',
    version='0.1',
    author='Fraser Tweedale',
    author_email='frase@frase.id.au',
    description='Moose-like object system for Python',
    long_description=readme,
    url='https://github.com/frasertweedale/elk',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
    ],
    packages=find_packages()
)
