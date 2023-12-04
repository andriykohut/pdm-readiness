# pdm-readiness

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

```sh
pdm readiness 3.12
Supported dependencies (5):
 ✓ whitenoise (2.21)
 ✓ python-dotenv (2.21)
 ✓ django-cors-headers (2.21)
 ✓ celery (2.21)
 ✓ azure-identity (2.21)
Update required (2):
 ⬆ Django (4.2.7 -> 5.0)
 ⬆ django-filter (23.3 -> 23.4)
Unsupported dependencies (5):
 ✗ certifi (2023.11.17) supported versions: 3.6, 3.7, 3.8, 3.9, 3.10, 3.11
 ✗ djangorestframework-camel-case (1.4.2) supported versions: 3.6, 3.7, 3.8, 3.9, 3.10
 ✗ requests (2.31.0) supported versions: 3.7, 3.8, 3.9, 3.10, 3.11
 ✗ opentelemetry-api (1.21.0) supported versions: 3.7, 3.8, 3.9, 3.10, 3.11
 ✗ pycparser (2.21) supported versions: 2.7, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10
Missing metadata (2):
 ⚠ channels-redis (4.1.0)
 ⚠ pyodbc (5.0.1)
```