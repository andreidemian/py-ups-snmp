from setuptools import setup, find_packages

setup(
    name="snmpDevices",
    version="0.1.0",
    packages=find_packages(),
    # If it has dependencies, list them here:
    install_requires=[
        "pysnmp==7.1.16"
    ]
)