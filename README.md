# pdm-readiness

[![PyPI version](https://badge.fury.io/py/pdm-readiness.svg)](https://pypi.org/project/pdm-readiness/)
![Github Actions](https://github.com/pdm-project/pdm/workflows/Tests/badge.svg)

A `pdm` plugin to check if your project dependencies support specific Python version.

> [!NOTE]  
> Many packages may still work just fine even when they are not listed as supported.
> This plugin only checks the metadata provided by the package authors, so it is not
> a guarantee that the package will work or not.

## Synopsis

The readiness report is divided into 4 sections:

- **Supported dependencies** - currently locked dependencies that support the target Python version.
- **Update required** - currently locked dependencies that do not support the target Python version, but have newer versions that do.
- **Unsupported** - dependencies: the most recent version of the dependency does not support the target Python version.
- **Missing metadata** - the package does not provide metadata about the supported Python versions.

Plugins uses [PyPI JSON API](https://warehouse.pypa.io/api-reference/json.html) to get the metadata.
It looks at classifiers like `Programming Language :: Python :: 3.12` to determine which versions are supported.

## Installation

```sh
pdm self add pdm-readiness
```

## Usage

Run `pdm readiness <python_version>` in the root of your pdm project.

Example output:
![image](https://github.com/andriykohut/pdm-readiness/assets/3106616/60b7985f-0cc6-4124-8abe-878690a9d89a)
