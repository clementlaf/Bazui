from setuptools import setup, find_packages

setup(
    name="bazui",
    version="0.1.0",
    description="A simple UI library for Python apps based on pygame",
    author="Clément Lafond",
    author_email="clafond8@gmail.com",
    url="https://github.com/clementlaf/Bazui",  # Optional: link to your repo
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pygame-ce==2.5.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.12.0",
        "Operating System :: OS Independent",
    ],
)


# build by running "pip install -e path_to/Bazui"
# this will install the package in editable mode, allowing you to make changes to the code without reinstalling it
# and the package will be available for import in your Python environment
