from setuptools import setup

setup(
    name='host',
    version='0.1.0',
    py_modules=['host'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'host = host:server',
        ],
    },
)