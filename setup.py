from setuptools import setup

with open("README.MD", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

VERSION = "0.2.0"
GITHUB = "https://github.com/nerdguyahmad/qord"
DOCUMENTATION = "https://qord.readthedocs.io"
LICENSE = "MIT"

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.readlines()

    while "\n" in REQUIREMENTS:
        REQUIREMENTS.remove("\n")

PACKAGES = [
    "qord",
    "qord.core",
    "qord.events",
    "qord.flags",
    "qord.models",
]

setup(
    name="qord",
    author="nerdguyahmad",
    version=VERSION,
    license=LICENSE,
    url=GITHUB,
    project_urls={
        "Documentation": DOCUMENTATION,
        "Issue tracker": GITHUB + "/issues",
    },
    description='[WIP] Python library for Discord API based around asyncio.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=REQUIREMENTS,
    packages=PACKAGES,
    python_requires='>=3.8.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ]
)