import json
import jsonschema
from pathlib import Path


class ValidationError(Exception):
    pass


def validate_memory(memory: dict) -> None:
    schema_path = Path(__file__).parent.parent.parent / "schema" / "memory_schema.json"
    
    if not schema_path.exists():
        raise ValidationError(f"Schema file not found: {schema_path}")
    
    with open(schema_path, "r") as f:
        schema = json.load(f)
    
    try:
        jsonschema.validate(instance=memory, schema=schema)
    except jsonschema.ValidationError as e:
        raise ValidationError(f"Memory validation failed: {e.message}") from e
    except jsonschema.SchemaError as e:
        raise ValidationError(f"Invalid schema: {e.message}") from e