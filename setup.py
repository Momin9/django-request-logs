from setuptools import setup, find_packages

setup(
    name="django_requests_loger",               # PyPI package name
    version="1.1.9",
    author="Momin Ali",
    author_email="mominalikhoker589@gmail.com",
    description="A Django application for logging and displaying HTTP requests.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/momin9/django-request-logs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "django>=4.2.14",
        "django-environ",
    ],
    license="MIT",
)
