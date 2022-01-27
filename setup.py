from distutils.core import setup
from distutils import util
from pathlib import Path
import sys

if __name__ == "__main__":
    
    # package paths
    jwtPath = util.convert_path("jwt")

    # get version file
    versionPath = Path().cwd() / "jwt/version.py"

    main_ns = {}

    with open(str(versionPath)) as ver_file:
        exec(ver_file.read(), main_ns)

    # get long description
    longDescription = (Path().cwd() / "README.md").read_text()

    # running setup
    setup(
        name="jwt",
        version=main_ns['__version__'],
        description="Collection of functions to create JWT (signed)",
        long_description=longDescription,
        long_description_content_type="text/markdown",
        author="Daniel Kiermeier",
        author_email="d.kiermeier@layers-of-life.com",
        url="https://github.com/No9005/jwt",
        license="MIT",
        package_dir={
            "jwt":jwtPath
        },
        packages=["jwt"],
        install_requires=['Authlib']
    )