import json
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def contains_files(path: Path, suffixes: set[str]) -> bool:
    return path.is_dir() and any(
        candidate.is_file()
        and candidate.suffix in suffixes
        and candidate.stat().st_size > 0
        for candidate in path.rglob("*")
    )


def main() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    npm_private = package.get("private") is True
    publication_authorized = (
        pyproject.get("tool", {})
        .get("szl", {})
        .get("publication-authorized")
    ) is True
    classifiers = pyproject.get("project", {}).get("classifiers", [])
    pypi_upload_blocked = "Private :: Do Not Upload" in classifiers

    if package.get("version") != pyproject.get("project", {}).get("version"):
        raise SystemExit("npm and Python package versions differ")

    source_present = any(
        contains_files(path, {".js", ".mjs", ".py", ".ts", ".tsx"})
        for path in (ROOT / "src", ROOT / "alloyscape_tribe_sdk")
    )
    tests_present = contains_files(
        ROOT / "tests", {".js", ".mjs", ".py", ".ts", ".tsx"}
    )

    if publication_authorized:
        if npm_private:
            raise SystemExit("authorized publication conflicts with npm private=true")
        if pypi_upload_blocked:
            raise SystemExit("authorized publication conflicts with the PyPI upload block")
        if not source_present or not tests_present:
            raise SystemExit("publication requires implementation source and tests")
    else:
        if not npm_private:
            raise SystemExit("scaffold must keep npm private=true")
        if not pypi_upload_blocked:
            raise SystemExit("scaffold must keep the PyPI upload block")

    print(
        "publication gate valid: "
        f"authorized={publication_authorized}, source={source_present}, "
        f"tests={tests_present}, pypi_blocked={pypi_upload_blocked}"
    )


if __name__ == "__main__":
    main()
