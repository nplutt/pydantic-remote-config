from setuptools import find_packages, setup


setup(
    name="pydantic_remote_config",
    version="0.1.0",
    description=(
        "Utility to fetch configuration values from remote sources "
        "that integrates with Pydantic settings models"
    ),
    author="Nick Plutt",
    author_email="nplutt@gmail.com",
    license="MIT",
    url="https://github.com/nplutt/pydantic-remote-config",
    project_urls={"Source Code": "https://github.com/nplutt/pydantic-remote-config/"},
    keywords="pydantic remote config settings",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["pydantic"],
    extras_require={
        "aws": ["boto3"],
        "dev": ["black", "isort", "tox", "mypy", "pytest", "pytest-cov", "tox-asdf"],
    },
)
