from setuptools import find_packages, setup

PACKAGE_NAME = "cloudstoragetui"

setup(
    name=PACKAGE_NAME,
    packages=find_packages(exclude=["tests"]),
    install_requires=[package for package in open("requirements.txt").read().split("\n")],
    entry_points={
        "console_scripts": [
            f"cloudstoragetui = {PACKAGE_NAME}.main:main",
        ]
    },
    package_data={"": ["*.txt", "*.cfg"]},
    include_package_data=True,
)
