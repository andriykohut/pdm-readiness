from argparse import Namespace
from unittest import mock

import pytest
import responses

from pdm.project import Project
from pdm.models.requirements import Requirement

from pdm_readiness import ReadinessCommand


@pytest.fixture
def project(tmp_path):
    project = mock.MagicMock(spec=Project)
    project.get_dependencies.return_value = {
        "foo": Requirement("foo"),
        "bar": Requirement("bar"),
    }
    project.lockfile.exists.return_value = True
    project.lockfile.__getitem__.side_effect = lambda _: [
        {"name": "foo", "version": "1.0.0"},
        {"name": "bar", "version": "2.0.0"},
    ]
    return project


@responses.activate
def test_readiness(capsys, project):
    responses.add(
        responses.GET,
        "https://pypi.org/pypi/foo/json",
        json={
            "info": {
                "version": "1.0.0",
                "classifiers": [
                    "Programming Language :: Python :: 3.9",
                    "Programming Language :: Python :: 3.8",
                ],
            }
        },
    )
    responses.add(
        responses.GET,
        "https://pypi.org/pypi/bar/json",
        json={
            "info": {
                "version": "2.0.0",
                "classifiers": [
                    "Programming Language :: Python :: 3.9",
                    "Programming Language :: Python :: 3.8",
                ],
            }
        },
    )
    cmd = ReadinessCommand()
    cmd.handle(project, Namespace(python_version="3.9"))
    out, err = capsys.readouterr()
    assert "Supported dependencies (2):" in out
    assert "✓ foo (2.0.0)"
    assert "✓ bar (2.0.0)"
    assert not err
