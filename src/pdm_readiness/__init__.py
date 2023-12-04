import re
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from rich.console import Console
from pdm.core import Core
from pdm.models.versions import Version
from pdm.cli.commands.base import BaseCommand
from pdm.project import Project


def fetch_metadata(dep: str, pinned_version: str) -> tuple[dict, dict]:
    response = requests.get(f"https://pypi.org/pypi/{dep}/json")
    response.raise_for_status()
    latest_data = response.json()
    if latest_data["info"]["version"] != pinned_version:
        response = requests.get(f"https://pypi.org/pypi/{dep}/{pinned_version}/json")
        response.raise_for_status()
        pinned_data = response.json()
        return latest_data, pinned_data
    return latest_data, latest_data


class ReadinessCommand(BaseCommand):
    """Check the readiness of a project for a given Python version."""

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('python_version', help='Python version to check')

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        deps = [d.name for d in project.get_dependencies().values()]
        lockfile = project.lockfile.read()
        pinned_versions = {d["name"]: d["version"] for d in lockfile["package"]}
        console = Console()
        requested_version = Version(options.python_version)
        with console.status("[bold green]Checking dependencies...[/bold green]"):
            with ThreadPoolExecutor(10) as executor:
                metadata_to_dep = {executor.submit(fetch_metadata, dep, pinned_versions[dep.lower()]): dep for dep in deps}
            supported = []
            needs_update = []
            unsupported = []
            unknown = []
            for future in as_completed(metadata_to_dep):
                dep = metadata_to_dep[future]
                latest, pinned = future.result()
                supported_versions_for_pinned = sorted(
                    [Version(c.split("::")[-1].strip()) for c in pinned["info"]["classifiers"] if
                     re.match(r"Programming Language :: Python :: \d\.\d", c)])
                supported_versions_for_latest = sorted(
                    [Version(c.split("::")[-1].strip()) for c in latest["info"]["classifiers"] if
                     re.match(r"Programming Language :: Python :: \d\.\d", c)])
                latest_version = Version(latest["info"]["version"])
                pinned_version = Version(pinned["info"]["version"])
                if requested_version in supported_versions_for_pinned:
                    supported.append((dep, pinned_version, latest_version, supported_versions_for_pinned))
                elif requested_version in supported_versions_for_latest:
                    needs_update.append((dep, pinned_version, latest_version, supported_versions_for_latest))
                elif not supported_versions_for_latest:
                    unknown.append((dep, pinned_version, latest_version, supported_versions_for_latest))
                else:
                    unsupported.append((dep, pinned_version, latest_version, supported_versions_for_latest))
            if supported:
                console.print(f"[bold]Supported dependencies ({len(supported)}):[/bold]")
                for dep, pinned_version, _, supported_versions in supported:
                    console.print(f" [bold green]✓[/bold green] {dep} ({latest_version})")
            if needs_update:
                console.print(f"[bold]Update required ({len(needs_update)}):[/bold]")
                for dep, pinned_version, latest_version, supported_versions in needs_update:
                    console.print(
                        f" [bold green]⬆[/bold green] {dep} ({pinned_version} -> {latest_version})")
            if unsupported:
                console.print(f"[bold]Unsupported dependencies ({len(unsupported)}):[/bold]")
                for dep, pinned_version, latest_version, supported_versions in unsupported:
                    versions_str = ", ".join([str(v) for v in supported_versions])
                    console.print(
                        f" [bold red]✗[/bold red] {dep} ({latest_version}) [dim]supported versions: {versions_str}[/dim]")
            if unknown:
                console.print(f"[bold]Missing metadata ({len(unknown)}):[/bold]")
                for dep, pinned_version, latest_version, supported_versions in unknown:
                    console.print(f" [bold yellow]⚠[/bold yellow] {dep} ({latest_version})")


def readiness(core: Core) -> None:
    core.register_command(ReadinessCommand, "readiness")
