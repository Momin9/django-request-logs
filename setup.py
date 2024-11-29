from setuptools import setup, find_packages

# Read the content of README.md for long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="django-request-logs",
    version="1.0.0",
    author="Momin Ali",
    author_email="mominalikhoker589@gmail.com",
    description="A Django application for logging and displaying HTTP requests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/momin9/django-request-logs",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=4.2.14",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
    python_requires='>=3.8',
)
