import sys

import appdirs
from pyclier.setuptools import read_readme, read_requirements
from setuptools import find_packages, setup

from pyclier_demo import __author__, __email__, __name__, __version__, prog_name

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="Pyclier Demo.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/zhangxianbing/pyclier-demo",
    packages=find_packages(include=[f"{__name__}*"]),
    install_requires=read_requirements(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            f"{prog_name} = {__name__}.cli:main",
        ],
    },
)

# post installation

from pyclier.setuptools import copytree, enable_complete

command = sys.argv[-1]
if command == "install":
    copytree("conf", appdirs.user_config_dir(prog_name))
    enable_complete(prog_name)

    import pip

    pip.main(["install", ".", "-U", "--no-index"])
