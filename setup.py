import setuptools

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
    url="https://github.com/tevnpowers/text-studio",
    packages=['text_studio'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
)
