# sphinx-autodoc2 快速开始

+ `pdm add sphinx-autodoc2`

+ Add `autodoc2` to the extensions list in your `conf.py` file 
```conf
extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "autodoc2",
    "sphinx.ext.napoleon",
]
autodoc2_packages = [
    "../src/my_package",
]
```
+ `index.rst`加入：
```conf
   apidocs/index
```
+ `make html`
