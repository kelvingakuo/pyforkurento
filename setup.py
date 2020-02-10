import setuptools

with open("README.md", "r") as fh:
    long_description  =  fh.read()

setuptools.setup(
    name = "pyforkurento",
    version = "0.1.3",
    description = "A Python client for Kurento Media Server",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/kelvingakuo/pyforkurento",
    author = "Kelvin Gakuo",
    author_email = "kelvingakuo@gmail.com",
    license = "MIT",
    packages = setuptools.find_packages(),
    install_requires = [
      "websocket-client>=0.57.0"
    ],
    zip_safe = False
)