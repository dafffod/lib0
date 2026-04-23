# Lib0 — Python Dynamic Attribute Wrapper

Lib0 is a Python wrapper class that provides JavaScript-style dot notation access to nested data structures. It automatically handles missing nested keys, supports full Python operator compatibility, and adds optional variable metadata like type locking and constants.

---

## Part 1 — The Basics

### Installation

Copy `lib0_package/` into your project and import from it:

```python
from lib0_package import Lib0, dict2lib0, lib02dict, SetExplicitTypes
```

---

### Creating a Lib0 object

```python
# Empty object (acts as an empty dict)
obj = Lib0()

# From a value
obj = Lib0(42)
obj = Lib0("hello")
obj = Lib0([1, 2, 3])

# From a flat dict
obj = Lib0({"x": 1, "y": 2})

# From a nested dict — use R=True to recursively wrap all levels
obj = Lib0({"a": {"b": {"c": 3}}}, R=True)
print(obj.a.b.c)  # 3
```

> **Important:** `Lib0(nested_dict)` only wraps the top level. Use `R=True` for full recursive wrapping of multidimensional dicts.

---

### Attribute access

Lib0 objects support dot notation for reading and writing attributes. Missing keys are auto-created as empty Lib0 objects.

```python
obj = Lib0()

obj.name = "lib0"
obj.config.host = "localhost"   # auto-creates config as empty Lib0
obj.config.port = 8080

print(obj.name)         # lib0
print(obj.config.host)  # localhost
```

---

### Bracket access

```python
obj = Lib0()
obj["x"] = 10
print(obj["x"])         # 10

# Works on lists and strings too
obj = Lib0([10, 20, 30])
print(obj[1])           # 20
print(obj[0:2])         # [10, 20]
```

---

### Type conversions

#### Mutation methods — modify the object in place, return `self` for chaining

```python
obj = Lib0("42")
obj._int()              # obj._data is now 42
obj._float()            # obj._data is now 42.0
obj._str()._int()       # chaining: "42.0" → 42
```

#### Conversion methods — return the converted value without modifying the object

```python
obj = Lib0("42")
print(obj.int())        # 42
print(obj.float())      # 42.0
print(obj.str())        # "42"
print(obj.bool())       # True
```

#### Python built-in conversions

```python
obj = Lib0("42")
print(int(obj))         # 42
print(float(obj))       # 42.0
print(str(obj))         # "42"
print(bool(obj))        # True
```

---

### Operators

All standard Python operators are supported and transparently unwrap the inner value:

```python
a = Lib0(10)
b = Lib0(3)

print(a + b)    # 13
print(a - b)    # 7
print(a * b)    # 30
print(a / b)    # 3.333...
print(a // b)   # 3
print(a % b)    # 1
print(a ** b)   # 1000
print(a > b)    # True
print(a == 10)  # True

a += 5          # a._data becomes 15
```

---

### Container operations

```python
obj = Lib0({"a": 1, "b": 2})
print(len(obj))         # 2
print("a" in obj)       # True
del obj.a

for key in obj:
    print(key)          # b
```

---

### Dict ↔ Lib0 conversion

```python
from lib0_package import dict2lib0, lib02dict

data = {"server": {"host": "localhost", "port": 8080}}

# dict → Lib0 (recursive, preferred over R=True for complex cases)
obj = dict2lib0(data)
print(obj.server.host)  # localhost

# Lib0 → dict
back = lib02dict(obj)
print(back)             # {"server": {"host": "localhost", "port": 8080}}

# Round-trip is lossless
assert data == lib02dict(dict2lib0(data))
```

> `dict2lib0` and `lib02dict` are the "raw" way to do recursive conversions. For simple cases, `Lib0(data, R=True)` is equivalent.

---

## Part 2 — Edge Cases & Advanced Usage

### `PRESERVE_NONE`

By default, `Lib0(None)` creates an empty dict `{}`. Use `PRESERVE_NONE=True` to actually store `None`:

```python
obj = Lib0(None)                        # _data = {}
obj = Lib0(None, PRESERVE_NONE=True)    # _data = None
```

---

### Mutable vs immutable inner types

Lib0 respects the mutability of its inner value:

```python
# Mutable — item assignment works
obj = Lib0([1, 2, 3])
obj[0] = 99             # OK

# Immutable — raises TypeError
obj = Lib0("hello")
obj[0] = "H"            # TypeError: str does not support item assignment

obj = Lib0((1, 2, 3))
obj[0] = 99             # TypeError: tuple does not support item assignment
```

---

### Auto-creation behavior

Accessing a missing key on a dict-backed Lib0 silently creates it as an empty Lib0:

```python
obj = Lib0()
x = obj.nonexistent     # creates obj.nonexistent = Lib0()
obj.a.b.c = "deep"      # creates the full chain
```

This is intentional for ergonomic nested writes, but be careful when checking for key existence — reading a key creates it.

---

### `dict()` with recursive unwrap

```python
obj = Lib0({"a": {"b": 1}}, R=True)

obj.dict()      # returns top-level dict only (shallow)
obj.dict(R=True)  # returns fully unwrapped nested dict via lib02dict
```

---

### Context manager

```python
with Lib0() as session:
    session.user.id = 123
    session.user.name = "John"
# __exit__ is a no-op, but the pattern is supported
```

---

### Error types

| Exception | When |
|---|---|
| `Lib0Error` | General access or operation failure |
| `TypeLockedError` | Assignment violates a type lock |
| `ConstantAssignmentError` | Reassignment of a constant |

---

## Part 3 — Explicit Types

Explicit types are variable metadata constraints baked into Lib0 objects. They allow you to enforce C-like type safety directly in Python using a clean syntax.

### Concept

A `TypedVar` object acts as a **typed variable initializer** for a shared Lib0 environment. The syntax mirrors C-style declarations:

```
int a = 3;       →    Int.a = 3
float b = 3.14;  →    Float.b = 3.14
```

---

### `SetExplicitTypes` — quick setup

```python
from lib0_package import Lib0, SetExplicitTypes

env = Lib0()
Int, Float, Str, Tuple, List, Dict, Bool, Range, Byte, Const = SetExplicitTypes(env)

Int.a = 3           # creates env.a = 3, type-locked to int
Float.b = 3.14      # creates env.b = 3.14, type-locked to float
Str.c = "hello"     # creates env.c = "hello", type-locked to str

print(env.a)        # 3
print(env.b)        # 3.14
```

All 10 generators share the same `env` object — it is the variable environment.

---

### Type locking

Once a variable is created through a typed initializer, its type cannot change:

```python
Int.a = 3
Int.a = 10      # OK — same type
Int.a = "ten"   # TypeLockedError: Expected assignment of 'a' to be int, got str
```

Mutation methods (`._int()`, `._float()`, etc.) also respect type locks:

```python
# If env.a is type-locked to int:
env.a._float()  # TypeLockedError: Cannot convert int to float. Type is locked.
```

---

### Default values

Accessing an uninitialised typed variable auto-initialises it with the type's default:

```python
Int.x           # creates env.x = 0
Float.y         # creates env.y = 0.0
Str.z           # creates env.z = ""
Bool.flag       # creates env.flag = False
```

---

### Constants

Constants are type-locked AND cannot be reassigned after creation:

```python
Const.MAX_RETRIES = 5
Const.API_URL = "https://api.example.com"

Const.MAX_RETRIES = 10  # ConstantAssignmentError: Cannot reassign constant 'MAX_RETRIES'
```

Reading a constant that doesn't exist raises `ConstantAssignmentError` — constants must always be initialised with a value.

---

### Manual Lib0 creation with metadata

You can create type-locked or constant Lib0 objects directly without using the typed initializers:

```python
# Type-locked
x = Lib0(42, TYPE_LOCKED=True)
x._data = "oops"    # This bypasses the lock — always go through __setattr__

# Constant
y = Lib0(100, CONST=True)

# Planned — type-locked collection (child type enforcement, not yet implemented)
z = Lib0([1, 2, 3], TYPE_LOCKED=True, CHILD_TYPE=int)
# CHILD_TYPE will enforce that every element of the list must be of type int
```

---

### Custom `TypedVar`

You can create your own typed initializer for any type, including custom classes:

```python
from lib0_package import Lib0
from lib0_package.explicite_types import TypedVar

env = Lib0()
MyClass = TypedVar(env, MyCustomClass, MyCustomClass())

MyClass.obj = MyCustomClass(...)    # OK
MyClass.obj = "wrong"               # ExpliciteTypeError
```

---

### Summary table

| Feature | Syntax | Behaviour |
|---|---|---|
| Typed variable | `Int.a = 3` | Type-locked to `int`, default `0` |
| Constant | `Const.a = 3` | Type-locked + cannot reassign |
| Type mutation block | `env.a._float()` | Blocked if type-locked |
| Planned: child type | `CHILD_TYPE=int` | Will enforce element types in collections |
