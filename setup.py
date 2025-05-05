from setuptools import setup, find_packages

setup(
    name="pim_activation",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "aiohttp",
        "azure-identity",
        "PyJWT",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'activate_pims=pim_activation.activatePIMs:main',
        ],
    },
)