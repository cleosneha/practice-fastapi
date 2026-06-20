# Pydantic: `model_dump()` vs `model_dump(mode="json")` vs `model_dump_json()`

## Example Model

```python
from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4, UUID

class Product(BaseModel):
    id: UUID
    created_at: datetime

product = Product(
    id=uuid4(),
    created_at=datetime.now()
)
```

## `model_dump()`

Returns a normal Python dictionary.

```python
product.model_dump()
```

Output:

```python
{
    "id": UUID(...),
    "created_at": datetime(...)
}
```

Use when you want to work with Python objects.

---

## `model_dump(mode="json")`

Returns a JSON-friendly dictionary.

```python
product.model_dump(mode="json")
```

Output:

```python
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2026-06-20T21:05:30"
}
```

Use when sending API responses or saving JSON data.

---

## `model_dump_json()`

Returns a JSON string.

```python
product.model_dump_json()
```

Output:

```python
'{"id":"550e8400-e29b-41d4-a716-446655440000","created_at":"2026-06-20T21:05:30"}'
```

Use when you need actual JSON text.

---

## Quick Comparison

| Method                    | Returns            |
| ------------------------- | ------------------ |
| `model_dump()`            | Python dict        |
| `model_dump(mode="json")` | JSON-friendly dict |
| `model_dump_json()`       | JSON string        |

### Easy Memory Trick

```python
model_dump()
```

➡️ Model → Dict

```python
model_dump(mode="json")
```

➡️ Model → JSON-safe Dict

```python
model_dump_json()
```

➡️ Model → JSON String
