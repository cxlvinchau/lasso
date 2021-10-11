from distutils.core import setup
import setuptools

with open("requirements.txt") as file:
      requirements = file.readlines()

setup(name="lasso",
      version="0.1dev",
      author="Calvin Chau",
      author_email="calvin.chau@tum.de",
      package_dir={"": "src"},
      packages = setuptools.find_packages(where="lasso"),
      python_requires=">=3.7",
      install_requires=requirements,
      include_package_data=True
      )