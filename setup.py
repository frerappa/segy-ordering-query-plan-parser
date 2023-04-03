from setuptools import find_packages, setup

setup(
    name="segyqp",
    version="0.1",
    python_requires=">=3.9",
    install_requires=["pytest", "pathlib", "timeout_decorator", "pytest-timeout"],
    packages=(
        find_packages() +
        find_packages(where="./lib/sly")
    ),)
