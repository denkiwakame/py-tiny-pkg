# 📦 py-tiny-pkg
[![test](https://github.com/denkiwakame/py-tiny-pkg/actions/workflows/test.yml/badge.svg)](https://github.com/denkiwakame/py-tiny-pkg/actions/workflows/test.yml)
[![publish](https://github.com/denkiwakame/py-tiny-pkg/actions/workflows/pub.yml/badge.svg)](https://github.com/denkiwakame/py-tiny-pkg/actions/workflows/pub.yml)
[![PyPI version](https://badge.fury.io/py/tinypkg.svg)](https://badge.fury.io/py/tinypkg)

- a tiny packaging example that only has a [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) w/[setuptools 🔨](https://github.com/pypa/setuptools)
- 🎉 setuptools [v61.0.0](https://github.com/pypa/setuptools/releases/tag/v61.0.0) is released with experimental support for `pyproject.toml`
  - see https://discuss.python.org/t/help-testing-experimental-features-in-setuptools/

### 🦾 motivation
- we can find lots of packaging examples with `poetry`, `pdm`, etc., but hard to find examples with the standard `setuptools` based on the latest PEP supports.

### ✔️ confirmed versions
- `Ubuntu 20.04` `Mac OS X 11.6.4`
- `python 3.7.*, 3.8.*, 3.9.*`
- `pip 22.0.4+`

### ⬇️ install locally
- clone this repo
- `$ pip install .` or `$ pip install .[dev]` (for testing)
- `$ pip show tinypkg`

```
Name: tinypkg
Version: 0.0.0
Summary: a tiny package example w/setuptools
Home-page: github.com/denkiwakame/tiny-pkg
Author: denkiwakame
Author-email: denkivvakame@gmail.com
License: MIT License
        Copyright (c) 2022 denkiwakame
        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:
        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.
        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
Location: ...
Requires: requests
```

### 👩‍🔧 testing
- `$ pip install .[dev]`
- `$ python -m pytest --cov`

### :octocat: install from GitHub.com
- `pip install git+https://github.com/denkiwakame/py-tiny-pkg`

### 📝 editable install (-e)

```
ERROR: Project file:///../tiny-py-pkg has a 'pyproject.toml' and its build backend is missing the 'build_editable' hook. Since it does not have a 'setup.py' nor a 'setup.cfg', it cannot be installed in editable mode. Consider using a build backend that supports PEP 660.
```

- workaround: **locate `setup.py` that contains the following lines:** and then `$ pip install -e .`

```python
from setuptools import setup
setup()
```

- in near future, editable install will work on projets that only have a `pyproject.toml`
  - 📑 PEP660 https://peps.python.org/pep-0660/
  - pip 21.1+ supports `build_editable` hook https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/#editable-installation
  - setuptools support (wip) https://github.com/pypa/setuptools/issues/2816

### ❓ How can I manage ext_modules ?
- `pyproject.toml` does not strictly intend to replace `setup.py` .
- If you need to build C/C++ extension modules w/[pybind11](https://github.com/pybind/pybind11) or something, write the following `setup.py` (dynamic config) alongside with the `pyproject.toml` (metadata file).

```python
import subprocess
import os
import sys

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def build_extension(self, ext):
        cfg = "Debug" if self.debug else "Release"  # TODO
        extdir = os.path.abspath(os.path.dirname(
            self.get_ext_fullpath(ext.name)))
        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",
        ]
        build_args = []
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(
            ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp
        )
setup(
    ext_modules=[CMakeExtension("bindings")],
    cmdclass={"build_ext": CMakeBuild},
)
```


### 📦 publish to PyPI
- use [pypa/build](https://github.com/pypa/build), a simple PEP 517 frontend and [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)
  - https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/

### 📚 Refernces
#### pyproject.toml
- https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/

#### build-system
- 📑 PEP 517 https://www.python.org/dev/peps/pep-0517/
  - setuptools support https://setuptools.pypa.io/en/latest/build_meta.html
- 📑 PEP 518 https://www.python.org/dev/peps/pep-0518/

#### metadata
- 📑 PEP 621 https://peps.python.org/pep-0621/
  - setuptools support (wip) https://github.com/pypa/setuptools/issues/1688
  - experimental release https://discuss.python.org/t/help-testing-experimental-features-in-setuptools/13821

#### linter support for pyproject.toml
- black (supported)
- isort (supported)
- mypy (supported) https://github.com/python/mypy/issues/5205
- flake8 https://github.com/PyCQA/flake8/issues/234
  - pyproject-flake8 https://github.com/csachs/pyproject-flake8
