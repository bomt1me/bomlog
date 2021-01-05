"""setup.py """


from pathlib import Path
from setuptools import setup, find_namespace_packages


REQUIREMENTS = [
    "bom-configuration",
]


setup(
    name="bom-logger",
    version="1.0.2",
    description="config",
    long_description=Path("README.md").read_text(),
    author="Calvin Spring",
    url="https://github.com/bomt1me/bomlog",
    packages=find_namespace_packages("src"),
    namespace_packages=["bom"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=REQUIREMENTS,
    setup_requires=[],
)
