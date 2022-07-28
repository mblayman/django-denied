from setuptools import find_packages, setup

setup(
    name="django-denied",
    version="0.1",
    url="https://github.com/mblayman/django-denied",
    license="MIT",
    author="Matt Layman",
    author_email="matthewlayman@gmail.com",
    description="An authorization system based exclusively on allow lists",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
