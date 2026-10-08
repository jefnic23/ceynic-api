import ast
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
SCHEMA_DIR = PROJECT_ROOT.parent / "ceynic" / "src" / "lib" / "schemas"
TYPES_DIR = PROJECT_ROOT.parent / "ceynic" / "src" / "lib" / "interfaces"


def find_decorated_classes(file_path: Path) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(file_path))

    decorated = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if any(getattr(decorator, "id", None) == "frontend" for decorator in node.decorator_list):
                decorated.append(node.name)
    return decorated


def export_json_schema(py_file: Path, class_name: str, schema_path: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "src.utils.export_single_schema",
            str(py_file),
            class_name,
            str(schema_path),
        ],
        check=True,
        cwd=PROJECT_ROOT,
    )


def convert_schema_to_ts(json2ts: str, schema_path: Path, ts_path: Path) -> None:
    ts_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            json2ts,
            "-i",
            str(schema_path),
            "-o",
            str(ts_path),
            "--additionalProperties",
            "false",
        ],
        check=True,
    )
    print(f"Generated: {ts_path.resolve()}")


def generate_frontend_models(
    src_dir: Path = SRC_DIR,
    schema_dir: Path = SCHEMA_DIR,
    types_dir: Path = TYPES_DIR,
) -> None:
    json2ts = shutil.which("json2ts")
    if json2ts is None:
        raise RuntimeError(
            "json2ts must be installed. Instructions can be found here: "
            "https://www.npmjs.com/package/json-schema-to-typescript"
        )
    for py_file in src_dir.rglob("*.py"):
        decorated = find_decorated_classes(py_file)
        for class_name in decorated:
            schema_path = schema_dir / f"{class_name}.json"
            ts_path = types_dir / f"{class_name}.d.ts"
            export_json_schema(py_file, class_name, schema_path)
            convert_schema_to_ts(json2ts, schema_path, ts_path)


def main() -> None:
    generate_frontend_models()


if __name__ == "__main__":
    main()
