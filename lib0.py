def dict2lib0(data):
  if isinstance(data, dict):
      return Lib0({k: dict2lib0(v) for k, v in data.items()})
  elif isinstance(data, Lib0):
      return data
  else:
      # wrap every non-dict value into Lib0 so it supports .int(), .float(), etc.
      return Lib0(data)



def lib02dict(lib_obj):
  """
  Recursively convert a Lib0 object into a standard Python dict.
  """
  result = {}
  if not isinstance(lib_obj._data, dict):
      raise TypeError(f"Cannot convert Lib0 with {type(lib_obj._data).__name__} to dict")
  for key, value in lib_obj._data.items():
      if isinstance(value._data, dict):
          result[key] = lib02dict(value)
      else:
          result[key] = value._data
  return result


class Lib0:
  def __init__(self, DATA=None, ROOT=None, PRESERVE_NONE: bool=False, R: bool=False) -> None:
      DATA = {} if DATA is None and not PRESERVE_NONE else (dict2lib0(DATA) if R else DATA)
      if isinstance(DATA, Lib0):
          self._data = DATA._data
      else:
          self._data = DATA
      self._last = None
      self._root = self if ROOT is None else ROOT

  def __getattr__(self, KEY):
      if KEY == "_last":
          return self._root._last
      if hasattr(self._data, KEY):
          return getattr(self._data, KEY)
      if isinstance(self._data, dict):
          if KEY not in self._data:
              # Auto-create a new dict (wrapped by Lib0) if key does not exist
              self._data[KEY] = {}
          value = self._data[KEY]
          if isinstance(value, dict):
              wrapped = Lib0(value, ROOT=self._root)
              self._data[KEY] = wrapped
              return wrapped
          return value
      raise AttributeError(f"No attribute '{KEY}'")

  def __setattr__(self, KEY: str, VALUE) -> None:
      if KEY.startswith('_'):
          super().__setattr__(KEY, VALUE)
      elif isinstance(self._data, dict):
          if isinstance(VALUE, dict):
              self._data[KEY] = Lib0(VALUE, ROOT=self._root)
          elif not isinstance(VALUE, Lib0): 
              self._data[KEY] = Lib0(VALUE, ROOT=self._root, PRESERVE_NONE=True)
          else: # if VALUE is already a Lib0
              self._data[KEY] = VALUE
          object.__setattr__(self._root, '_last', self._data[KEY])
      else:
          raise AttributeError(f"Cannot set attribute '{KEY}' on non-dict value.")

  def __delattr__(self, key) -> None:
      if key.startswith('_'):
          super().__delattr__(key)
      elif isinstance(self._data, dict) and key in self._data:
          del self._data[key]
      else:
          raise AttributeError(f"No such attribute '{key}' to delete.")


  def _int(self):
      try:
          self._data = int(self._data)
          return self
      except (ValueError, TypeError):
          raise TypeError(f"Cannot convert {type(self._data).__name__} to int.")

  def _float(self):
      try:
          self._data = float(self._data)
          return self
      except (ValueError, TypeError):
          raise TypeError(f"Cannot convert {type(self._data).__name__} to float.")

  def _bool(self):
      try:
          self._data = bool(self._data)
          return self
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to bool.")

  def _str(self):
      try:
          self._data = str(self._data)
          return self
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to str.")

  def _list(self):
      try:
          self._data = list(self._data)
          return self
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to list.")

  def _dict(self):
      try:
          self._data = dict(self._data)
          return self
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to dict.")



  # String & Representation
  def __str__(self):
      try:
          return str(self._data)
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to str.")

  def __repr__(self):
      try:
          return repr(self._data)
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to repr.")

  def __format__(self, format_spec):
      try:
          return format(self._data, format_spec)
      except Exception:
          raise TypeError(f"Cannot format {type(self._data).__name__} with format spec '{format_spec}'.")

  # Conversions by attribute
  def str(self):
      try:
          return str(self._data)
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to str.")

  def repr(self):
      try:
          return repr(self)
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to repr.")

  def format(self, format_spec):
      try:
          return format(self._data, format_spec)
      except Exception:
          raise TypeError(f"Cannot format {type(self._data).__name__} with format spec '{format_spec}'.")

  def bool(self):
      try:
          return bool(self._data)
      except Exception:
          return False

  def int(self):
      try:
          return int(self._data)
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to int.")

  def float(self):
      try:
          return float(self._data)
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to float.")

  def complex(self):
      try:
          return complex(self._data)
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to complex.")

  def bytes(self):
      try:
          return bytes(self._data)
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to bytes.")

  def hash(self):
      try:
          return hash(self._data)
      except Exception:
          raise TypeError(f"Cannot hash {type(self._data).__name__}.")

  def list(self):
      try:
          return list(self._data)
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to list.")

  def dict(self, R=False):
      if not R:
          try:
              return dict(self._data)
          except Exception:
              raise TypeError(f"Cannot convert {type(self._data).__name__} to dict.")
      else:
          return lib02dict(self)

  # Conversion by method call
  def __bool__(self):
      try:
          return bool(self._data)
      except Exception:
          return False

  def __int__(self):
      try:
          return int(self._data)
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to int.")

  def __float__(self):
      try:
          return float(self._data)
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to float.")

  def __complex__(self):
      try:
          return complex(self._data)
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to complex.")

  def __bytes__(self):
      try:
          return bytes(self._data)
      except Exception:
          raise TypeError(f"Cannot convert {type(self._data).__name__} to bytes.")

  def __hash__(self):
      try:
          return hash(self._data)
      except Exception:
          raise TypeError(f"Cannot hash {type(self._data).__name__}.")

  # Comparison Operators
  def __eq__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return self._data == other_val
      except Exception:
          raise TypeError(f"Cannot compare {type(self._data).__name__} with {type(other_val).__name__}.")

  def __ne__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return self._data != other_val
      except Exception:
          raise TypeError(f"Cannot compare {type(self._data).__name__} with {type(other_val).__name__}.")

  def __lt__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return self._data < other_val
      except Exception:
          raise TypeError(f"Cannot compare {type(self._data).__name__} with {type(other_val).__name__}.")

  def __le__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return self._data <= other_val
      except Exception:
          raise TypeError(f"Cannot compare {type(self._data).__name__} with {type(other_val).__name__}.")

  def __gt__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return self._data > other_val
      except Exception:
          raise TypeError(f"Cannot compare {type(self._data).__name__} with {type(other_val).__name__}.")

  def __ge__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return self._data >= other_val
      except Exception:
          raise TypeError(f"Cannot compare {type(self._data).__name__} with {type(other_val).__name__}.")

  # Arithmetic Operators
  def __add__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return self._data + other_val
      except Exception:
          raise TypeError(f"Cannot add {type(self._data).__name__} and {type(other_val).__name__}.")

  def __sub__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return self._data - other_val
      except Exception:
          raise TypeError(f"Cannot subtract {type(other_val).__name__} from {type(self._data).__name__}.")

  def __mul__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return self._data * other_val
      except Exception:
          raise TypeError(f"Cannot multiply {type(self._data).__name__} and {type(other_val).__name__}.")

  def __truediv__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return self._data / other_val
      except Exception:
          raise TypeError(f"Cannot divide {type(self._data).__name__} by {type(other_val).__name__}.")

  def __floordiv__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return self._data // other_val
      except Exception:
          raise TypeError(f"Cannot floor divide {type(self._data).__name__} by {type(other_val).__name__}.")

  def __mod__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return self._data % other_val
      except Exception:
          raise TypeError(f"Cannot compute modulus of {type(self._data).__name__} and {type(other_val).__name__}.")

  def __pow__(self, other, modulo=None):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          if modulo is None:
              return pow(self._data, other_val)
          else:
              return pow(self._data, other_val, modulo)
      except Exception:
          raise TypeError(f"Cannot compute power of {type(self._data).__name__} and {type(other_val).__name__}.")

  # Right-side arithmetic operators
  def __radd__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return other_val + self._data
      except Exception:
          raise TypeError(f"Cannot add {type(other_val).__name__} and {type(self._data).__name__}.")

  def __rsub__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return other_val - self._data
      except Exception:
          raise TypeError(f"Cannot subtract {type(self._data).__name__} from {type(other_val).__name__}.")

  def __rmul__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return other_val * self._data
      except Exception:
          raise TypeError(f"Cannot multiply {type(other_val).__name__} and {type(self._data).__name__}.")

  def __rtruediv__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return other_val / self._data
      except Exception:
          raise TypeError(f"Cannot divide {type(other_val).__name__} by {type(self._data).__name__}.")

  def __rfloordiv__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return other_val // self._data
      except Exception:
          raise TypeError(f"Cannot floor divide {type(other_val).__name__} by {type(self._data).__name__}.")

  def __rmod__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return other_val % self._data
      except Exception:
          raise TypeError(f"Cannot compute modulus of {type(other_val).__name__} and {type(self._data).__name__}.")

  def __rpow__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          return pow(other_val, self._data)
      except Exception:
          raise TypeError(f"Cannot compute power of {type(other_val).__name__} and {type(self._data).__name__}.")

  # In-place arithmetic operators
  def __iadd__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          self._data += other_val
          return self
      except Exception:
          raise TypeError(f"Cannot add {type(other_val).__name__} to {type(self._data).__name__}.")

  def __isub__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          self._data -= other_val
          return self
      except Exception:
          raise TypeError(f"Cannot subtract {type(other_val).__name__} from {type(self._data).__name__}.")

  def __imul__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          self._data *= other_val
          return self
      except Exception:
          raise TypeError(f"Cannot multiply {type(self._data).__name__} by {type(other_val).__name__}.")

  def __itruediv__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          self._data /= other_val
          return self
      except Exception:
          raise TypeError(f"Cannot divide {type(self._data).__name__} by {type(other_val).__name__}.")

  def __ifloordiv__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          self._data //= other_val
          return self
      except Exception:
          raise TypeError(f"Cannot floor divide {type(self._data).__name__} by {type(other_val).__name__}.")

  def __imod__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          self._data %= other_val
          return self
      except Exception:
          raise TypeError(f"Cannot compute modulus of {type(self._data).__name__} and {type(other_val).__name__}.")

  def __ipow__(self, other):
      other_val = other._data if isinstance(other, Lib0) else other
      try:
          self._data **= other_val
          return self
      except Exception:
          raise TypeError(f"Cannot compute power of {type(self._data).__name__} and {type(other_val).__name__}.")

  # Unary operators
  def __neg__(self):
      try:
          return -self._data
      except Exception:
          raise TypeError(f"Cannot negate {type(self._data).__name__}.")

  def __pos__(self):
      try:
          return +self._data
      except Exception:
          raise TypeError(f"Cannot apply unary positive to {type(self._data).__name__}.")

  def __abs__(self):
      try:
          return abs(self._data)
      except Exception:
          raise TypeError(f"Cannot compute absolute value of {type(self._data).__name__}.")

  def __invert__(self):
      try:
          return ~self._data
      except Exception:
          raise TypeError(f"Cannot invert {type(self._data).__name__}.")

  # Container methods (if you want to support indexing like dict/list)
  def __len__(self):
      return len(self._data)

  def __getitem__(self, KEY):
      if isinstance(self._data, dict):
          if KEY not in self._data:
              self._data[KEY] = Lib0({}, ROOT=self._root)
          return self._data[KEY]
      elif isinstance(self._data, (list, str, tuple, range, bytes, bytearray)):
          if isinstance(KEY, int) and KEY < len(self._data) and KEY >= -len(self._data):
              return self._data[KEY]
          elif isinstance(KEY, slice):
              return self._data[KEY]
          else:
              raise IndexError(f"Index out of range: {KEY}, length: {len(self._data)}")
      else:
          try:
              return self._data[KEY]
          except Exception:
              raise TypeError(f"Object {self._data} of type {type(self._data).__name__} does not support indexing.")

  def __setitem__(self, KEY, VALUE):
      if isinstance(self._data, dict):
          if isinstance(VALUE, dict):
              self._data[KEY] = Lib0(VALUE, ROOT=self._root)
          elif not isinstance(VALUE, Lib0):
              self._data[KEY] = Lib0(VALUE, ROOT=self._root, PRESERVE_NONE=True)
          else:
              self._data[KEY] = VALUE
          object.__setattr__(self._root, '_last', self._data[KEY])
      elif isinstance(self._data, (list, bytearray)):
          if isinstance(KEY, int) and KEY < len(self._data) and KEY >= -len(self._data):
              self._data[KEY] = VALUE
          elif isinstance(KEY, slice):
              self._data[KEY] = VALUE
          else:
              raise IndexError(f"Index out of range: {KEY}, length: {len(self._data)}")
      else:
          try:
              self._data[KEY] = VALUE
          except Exception:
              raise TypeError(f"Object {self._data} of type {type(self._data).__name__} does not support item assignment.")

  def __delitem__(self, KEY):
      try:
          del self._data[KEY]
      except Exception:
          raise TypeError(f"Object {self._data} of type {type(self._data).__name__} has no item for key: {KEY}")

  def __contains__(self, item):
      try:
          return item in self._data
      except Exception:
          raise TypeError(f"Object {self._data} of type {type(self._data).__name__} does not support 'in' operator.")

  # Iterator support
  def __iter__(self):
      try:
          return iter(self._data)
      except Exception:
          raise TypeError(f"Object {self._data} of type {type(self._data).__name__} is not iterable.")

  # Context management (optional)
  def __enter__(self):
      try:
          return self
      except Exception:
          raise TypeError(f"Object {self._data} of type {type(self._data).__name__} does not support context management.")

  def __exit__(self, exc_type, exc_val, exc_tb):
      pass

  def __round__(self, ndigits=None):
      try:
          # Try to get the underlying float/int value for rounding
          value = self._data
          if ndigits is None:
              return round(value)
          else:
              return round(value, ndigits)
      except Exception:
          # If conversion fails, just return 0 or some fallback value
          return 0




