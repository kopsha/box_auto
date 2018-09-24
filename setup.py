import setuptools

with open("readme.md", "r") as file_handle:
    long_description = file_handle.read()

setuptools.setup(
    name="box_auto",
    version="0.0.1",
    author="Florin Ciurcanu",
    author_email="florin.ciurcanu@gmail.com",
    description="BoxCore communication API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kopsha/box_auto",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: GNU General Public License",
        "Operating System :: OS Independent",
    ],
)
