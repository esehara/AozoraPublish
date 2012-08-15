try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

dependencies = [
            'BeautifulSoup >= 3.2.1',
            'nose >= 1.0.0',
        ]
setup(
    name='AozoraPublish',
    version='0.0.1',
    packages=['aozorapublish',],
    install_requires=dependencies)
