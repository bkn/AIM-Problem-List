from setuptools import setup, find_packages

setup(
    name = "aimauth",
    version = "0.1",
    url = 'https://github.com/benoitc/aimpl',
    license = 'BSD',
    description = "aim.",
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['distribute', 'restkit'],
)
