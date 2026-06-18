#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["packaging", "rich-click", "rich"]
# ///
"""Compute the next CalVer prerelease version. Pure function: version in, version out.

Versioning rules (current version vs. today), per issue #1192:
  - new year/month            -> reset to current YYYY.M.1a1
  - same YYYY.M, prerelease   -> bump the a/b serial, keep the letter
  - same YYYY.M, final        -> next minor, start at a1
Output is always a prerelease (a/b suffix). Only the new version is printed to
stdout; the workflow handles reading the latest tag and creating the release.

Use `uv run --script` so uv installs the inline deps below instead of the
surrounding project environment:

    uv run --script .github/scripts/publish_prerelease.py bump 2026.6.1b1
    uv run --script .github/scripts/publish_prerelease.py selftest
"""
from __future__ import annotations

from datetime import date

import rich_click as click
from packaging.version import Version
from rich.console import Console
from rich.table import Table

console = Console(stderr=True)


def next_version(latest: Version, today: date) -> str:
    """Apply the issue #1192 rules. Always returns a prerelease string."""
    if (latest.major, latest.minor) != (today.year, today.month):
        return f"{today.year}.{today.month}.1a1"
    if latest.is_prerelease:
        letter, n = latest.pre  # ("a" | "b", N)
        return f"{today.year}.{today.month}.{latest.micro}{letter}{n + 1}"
    return f"{today.year}.{today.month}.{latest.micro + 1}a1"


@click.group()
def cli() -> None:
    """Compute CalVer prerelease versions."""


@cli.command()
@click.argument("current")
def bump(current: str) -> None:
    """Print the next prerelease version after CURRENT (e.g. 2026.6.1b1)."""
    click.echo(next_version(Version(current), date.today()))


@cli.command()
def selftest() -> None:
    """Run offline checks of the version rules."""
    today = date(2026, 6, 17)
    cases = {
        "2026.6.1b1": "2026.6.1b2",     # continue beta serial
        "2026.6.1a1": "2026.6.1a2",     # continue alpha serial
        "2026.6.1a9": "2026.6.1a10",    # double-digit serial
        "2026.6.1b10": "2026.6.1b11",   # double-digit beta serial
        "2026.6.1": "2026.6.2a1",       # final -> next minor, a1
        "2026.6.10": "2026.6.11a1",     # double-digit minor final
        "2026.5.4a2": "2026.6.1a1",     # prior month -> reset to today
        "2025.12.3a4": "2026.6.1a1",    # prior year -> reset to today
    }
    table = Table(title=f"Version rules (today = {today})")
    table.add_column("result")
    table.add_column("latest", style="cyan")
    table.add_column("next")
    table.add_column("expected", style="dim")

    failures = 0
    for current, want in cases.items():
        got = next_version(Version(current), today)
        ok = got == want
        failures += not ok
        result = "[green]✓ OK[/]" if ok else "[red]✗ FAIL[/]"
        table.add_row(result, current, f"[green]{got}[/]" if ok else f"[red]{got}[/]", want)

    console.print(table)
    if failures:
        raise click.ClickException(f"{failures} failure(s)")
    console.print("[bold green]ALL PASS[/]")


if __name__ == "__main__":
    cli()
