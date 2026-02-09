#!/usr/bin/env python3
"""Generate a lightweight review report from provided test files."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class ReviewFinding:
    category: str
    message: str


@dataclass
class ReviewReport:
    file_path: Path
    findings: List[ReviewFinding]

    def to_markdown(self) -> str:
        if not self.findings:
            return f"## {self.file_path}\nNo issues detected."

        lines = [f"## {self.file_path}"]
        for finding in self.findings:
            lines.append(f"- **{finding.category}:** {finding.message}")
        return "\n".join(lines)


def load_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def analyze_content(path: Path, content: str) -> ReviewReport:
    findings: List[ReviewFinding] = []
    stripped = content.strip()

    if not stripped:
        findings.append(
            ReviewFinding("Content", "File is empty or contains only whitespace.")
        )
        return ReviewReport(path, findings)

    if "TODO" in content or "FIXME" in content:
        findings.append(
            ReviewFinding("Notes", "Contains TODO/FIXME markers to review.")
        )

    if "assert" not in content:
        findings.append(
            ReviewFinding(
                "Coverage",
                "No assertions found; consider adding assertions to validate behavior.",
            )
        )

    if "print(" in content:
        findings.append(
            ReviewFinding(
                "Signal",
                "Print statements detected; they can mask failures in automated runs.",
            )
        )

    if "@pytest.mark.skip" in content or "skip(" in content:
        findings.append(
            ReviewFinding(
                "Skip",
                "Skipped tests detected; ensure skips are justified and documented.",
            )
        )

    return ReviewReport(path, findings)


def collect_reports(paths: Iterable[Path]) -> List[ReviewReport]:
    reports: List[ReviewReport] = []
    for path in paths:
        if not path.exists():
            reports.append(
                ReviewReport(
                    path,
                    [ReviewFinding("Missing", "File does not exist.")],
                )
            )
            continue
        content = load_file(path)
        reports.append(analyze_content(path, content))
    return reports


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an automated review report for test files."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("test file")],
        help="Paths to test files (defaults to ./test file).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    reports = collect_reports(args.paths)
    output = ["# Automated Review Report", ""]
    for report in reports:
        output.append(report.to_markdown())
        output.append("")
    print("\n".join(output).strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
