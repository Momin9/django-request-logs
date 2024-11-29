from setuptools import setup, find_packages

setup(
    name="request-logs",
    version="1.0.1",
    author="Momin Ali",
    author_email="mominalikhoker589@gmail.com",
    description="A Django application for logging and displaying HTTP requests.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/momin9/django-request-logs",
    packages=find_packages(),  # This ensures the `request_logs` package is included
    include_package_data=True,
    install_requires=[
        "django>=4.2.14",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
