from setuptools import setup, find_packages

setup(
    name="intervallum",
    version="0.0.1",

    description="Intervallum - package for interval computations",

    url="https://github.com/wol4aravio/Intervallum",

    author="Panovskiy Valentin",
    author_email="panovskiy.v@yandex.ru",

    license="MIT License",

    classifiers=[
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],

    keywords="",

    packages=find_packages(exclude=['intervallum.tests']),

    install_requires=[]

)
