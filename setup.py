from setuptools import setup, find_packages

setup(
        name='automgtic',
        version='0.0.1',
        author='Joar Wandborg',
        author_email='joar [hex 40] wandborg [hex 2e] se',
        url='https://github.com/jwandborg/automgtic',
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            'setuptools',
            'configobj',
            'sqlalchemy',
            'simplejson',
            'poster'],
        license='Apache License v2')
