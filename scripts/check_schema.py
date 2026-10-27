"""Validate the complete JSON Schema, in addition to the dependency-free JS checks."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

root = Path(__file__).resolve().parents[1]
schema = json.loads((root / "data/catalog.schema.json").read_text())
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema, format_checker=FormatChecker())
errors = list(validator.iter_errors(json.loads((root / "data/catalog.json").read_text())))
for error in errors:
    print(f"{list(error.path)}: {error.message}")
if errors:
    raise SystemExit(1)
print("JSON Schema validation passed.")
