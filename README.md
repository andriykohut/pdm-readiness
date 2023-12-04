# pdm-readiness

A `pdm` plugin to check if your project dependencies support new Python versions.

> [!NOTE]  
> Many packages may still work just fine with newer Python versions, but they are not officially supported by the
> package maintainers. This plugin only checks the metadata of the packages. Version classifiers are used to determine
> if package officially supports a Python version.

## Installation

```bash
pdm self add pdm-readiness
```

## Usage

```bash
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
 ⚠ pyodbc (5.0.1)
```