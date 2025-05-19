from setuptools import setup, find_packages

setup(
    name='sxm2py',
    version='0.1',
    packages=find_packages(),
    install_requires=['numpy'],
    entry_points={
        'console_scripts': [
            'sxm2py = sxm2py.run:main',
        ],
    },
)
