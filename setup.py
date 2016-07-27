#!/usr/bin/env python3
import setuptools

setuptools.setup(
    name="pythonwars",
    version="1.0.0",
    description="A curses interface for CodeWars",
    url="https://github.com/8Banana/PythonWars",
    author="8Banana",
    install_requires=["requests",
                      "inflection",
                      "Pygments",
                      "mistune",
                      "tabulate",
                      "colorama"],
    packages=["pythonwars"]
)
