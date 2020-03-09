import setuptools

PROJECT_URLS = {
    "Bug Tracker": "https://github.com/tevnpowers/text-studio/issues",
    "Documentation": "https://github.com/tevnpowers/text-studio/tree/master/docs",
    "Source Code": "https://github.com/tevnpowers/text-studio",
}

DOWNLOAD_URL = "https://pypi.org/project/text-studio/#files"

with open("text_studio/README.md", "r") as fh:
    long_description = fh.read()

short_description = "Python package that powers the TextStudio development environment where users can explore, process, model, and visualize textual data."

setuptools.setup(
    name="text-studio",
    version="0.0.1-alpha",
    author="Tev'n Powers",
    author_email="tevnpowers@gmail.com",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url=DOWNLOAD_URL,
    project_urls=PROJECT_URLS,
    url="https://github.com/tevnpowers/text-studio",
    packages=["text_studio"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
)
