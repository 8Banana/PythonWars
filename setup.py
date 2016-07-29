#!/usr/bin/env python3
import setuptools

setuptools.setup(
    name="pythonwars",
    version="1.0.0",
    description="A curses interface for CodeWars",
    url="https://github.com/8Banana/PythonWars",
    author="8Banana",
    install_requires=["requests>=2.10.0",
                      "inflection>=0.3.1",
                      "Pygments>=2.1.3",
                      "mistune>=0.7.3",
                      "tabulate>=0.7.5",
                      "colorama>=0.3.7"],
    packages=["pythonwars"]
)
