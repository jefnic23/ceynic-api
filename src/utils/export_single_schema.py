# export_single_schema.py
import sys
import json
import importlib.util
from pathlib import Path

def strip_titles(schema: dict) -> dict:
    """
    Remove 'title' metadata fields from all properties in JSON Schema,
    including nested definitions, to avoid unnecessary type aliases
    in the generated TypeScript code.
    """
    def clean(obj: any):
        if isinstance(obj, dict):
            # Remove 'title' only from individual property definitions
            if 'type' in obj or 'anyOf' in obj or 'oneOf' in obj or 'allOf' in obj:
                obj.pop('title', None)
            # Recurse into all nested values
            return {k: clean(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean(item) for item in obj]
        return obj

    return clean(schema)

py_file = Path(sys.argv[1])
class_name = sys.argv[2]
schema_path = Path(sys.argv[3])

spec = importlib.util.spec_from_file_location("mod", str(py_file))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
cls = getattr(mod, class_name)

if getattr(cls, '__frontend_export__', False):
    schema = strip_titles(cls.model_json_schema())
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    with open(schema_path, "w") as f:
        json.dump(schema, f, indent=4)
