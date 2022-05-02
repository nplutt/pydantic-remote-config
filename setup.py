from setuptools import find_packages, setup


setup(
    name="pydantic_remote_config",
    version="0.1.0",
    description="Utility to fetch configuration values from remote source that is compatible with Pydantic models",
    author="Nick Plutt",
    author_email="nplutt@gmail.com",
    license="MIT",
    url="https://github.com/nplutt/pydantic_remote_config",
    project_urls={"Source Code": "https://github.com/nplutt/pydantic_remote_config/"},
    keywords="pydantic remote config settings",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["Jinja2", "pydantic"],
    extras_require={
        "aws": ["boto3"],
        "test": ["pytest", "pytest-cov"],
        "dev": ["black", "isort"],
    },
)
