from .lib0 import Lib0
from .exceptions import ExpliciteTypeError, ConstantAssignmentError


class TypedVar:
    def __init__(self, obj: Lib0, type: type, default: any):
        self._obj = obj
        self._type = type
        self._default = default

    def __getattr__(self, name):
        if name.startswith("_"):
            return super().__getattr__(name)
        elif name not in self._obj:
            self._obj.__setitem__(name, Lib0(self._default, PRESERVE_NONE=True, TYPE_LOCKED=True))
    
    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        elif isinstance(value, self._type):
            if name not in self._obj:
                self._obj[name] = Lib0(value, PRESERVE_NONE=True, TYPE_LOCKED=True)
            elif name in self._obj and isinstance(self._obj[name]._data, self._type):
                self._obj[name] = Lib0(value, PRESERVE_NONE=True, TYPE_LOCKED=True)
            else:
                raise ExpliciteTypeError(f"Expected {name} object to be of type int, got {type(self._obj[name]._data)}")
        else:
            raise ExpliciteTypeError(f"Expected the assignment of {name} to be of type int, got {type(value)}")


class ConstVars:
    def __init__(self, obj: Lib0):
        self._obj = obj
        self._meta = {
            "typelocked": True,
            "childtype": None,
            "const": True
        }

    def __getattr__(self, name):
        if name.startswith("_"):
            return super().__getattr__(name)
        elif name not in self._obj:
            raise ConstantAssignmentError(f"Cannot assign a constant without value to the non-existing variable '{name}'")
        else:
            raise ConstantAssignmentError(f"Cannot assign a constant without value to the existing variable '{name}'")

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            if name not in self._obj:
                self._obj[name] = Lib0(value, PRESERVE_NONE=True, CONST=True)
            elif name in self._obj:
                if self._obj[name]._meta["const"]:
                    raise ConstantAssignmentError(f"Cannot reassign constant '{name}'")
                else:
                    self._obj[name]._data = value
                    self._obj[name]._meta["const"] = True
            else:
                raise ConstantAssignmentError(f"Cannot assign a constant to the existing variable '{name}'")
        


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

    Const = ConstVars(OBJ)

    return Int, Float, Str, Tuple, List, Dict, Bool, Range, Byte, Const
            
    
