from .lib0 import Lib0
from .exceptions import ExpliciteTypeError


class TypedVar:
    def __init__(self, obj: Lib0, type: type, default: any):
        self._obj = obj
        self._type = type
        self._default = default
        self._meta = {
            "typelocked": True,
            "childtype": None
        }

    def __getattr__(self, name):
        if name.startswith("_"):
            return super().__getattr__(name)
        if name not in self._obj:
            self._obj.__setitem__(name, Lib0(self._default, PRESERVE_NONE=True, META=self._meta))
    
    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
            return None
        if isinstance(value, self._type):
            if name not in self._obj:
                self._obj[name] = Lib0(value, PRESERVE_NONE=True, META=self._meta)
            elif name in self._obj and isinstance(self._obj[name]._data, self._type):
                self._obj[name] = Lib0(value, PRESERVE_NONE=True, META=self._meta)
            else:
                raise ExpliciteTypeError(f"Expected {name} object to be of type int, got {type(self._obj[name]._data)}")
        else:
            raise ExpliciteTypeError(f"Expected the assignment of {name} to be of type int, got {type(value)}")




def SetExplicitTypes(OBJ: Lib0) -> tuple:
    """
    Create a Lib0 state with explicit type conversions for all values.
    Args:
        - OBJ: The target Lib0 object
    Returns:
        - A tuple of Lib0 objects to create OBJ attributes with explicit types.
    """
    # Create typed variable creators for every type
    Int = TypedVar(OBJ, int, 0)
    Float = TypedVar(OBJ, float, 0.0)
    Str = TypedVar(OBJ, str, "")
    Tuple = TypedVar(OBJ, tuple, ())
    List = TypedVar(OBJ, list, [])
    Dict = TypedVar(OBJ, dict, {})
    Bool = TypedVar(OBJ, bool, False)
    Range = TypedVar(OBJ, range, range(0))
    Byte = TypedVar(OBJ, bytes, b"")
    Bytearray = TypedVar(OBJ, bytearray, bytearray(b""))

    return Int, Float, Str, Tuple, List, Dict, Bool, Range, Byte,
            
    
