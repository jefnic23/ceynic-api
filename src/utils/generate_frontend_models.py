import ast
import os
import shutil
import subprocess
import sys
from pathlib import Path


SRC_DIR = Path("src")
SCHEMA_DIR = Path("src/schemas/frontend")
TYPES_DIR = Path("../ceynic/src/lib/interfaces")

def find_decorated_classes(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(file_path))

    decorated = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if any(getattr(d, 'id', None) == 'frontend' for d in node.decorator_list):
                decorated.append(node.name)
    return decorated

def export_json_schema(py_file: Path, class_name: str, schema_path: Path):
    subprocess.run([
        sys.executable, "src/utils/export_single_schema.py",
        str(py_file), class_name, str(schema_path)
    ], check=True)

def convert_schema_to_ts(schema_path: Path, ts_path: Path):
    result = os.system(
        f"json2ts -i {str(schema_path)} -o {str(ts_path)} --additionalProperties false"
    )
    if result != 0:
        print(f"Error generating TypeScript for {schema_path.name}:\n{result.stderr}")
    else:
        print(f"Generated: {ts_path.resolve()}")

def main():
    if " " not in "json2ts" and not shutil.which("json2ts"):
        raise Exception(
            "json2ts must be installed. Instructions can be found here: "
            "https://www.npmjs.com/package/json-schema-to-typescript"
        )
    for py_file in SRC_DIR.rglob("*.py"):
        decorated = find_decorated_classes(py_file)
        for class_name in decorated:
            schema_path = SCHEMA_DIR / f"{class_name}.json"
            ts_path = TYPES_DIR / f"{class_name}.d.ts"
            updated = export_json_schema(py_file, class_name, schema_path)
            if updated or not ts_path.exists():
                convert_schema_to_ts(schema_path, ts_path)

if __name__ == "__main__":
    main()
