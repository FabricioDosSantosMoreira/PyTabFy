from typing import Any, Iterable, Optional, Type, Tuple, Union, get_args, get_origin


from PyTabFy.PyTUtils import get_item_from_obj_at_idx

def validate_obj_type(
        obj: Union[object, Iterable[object]], 
        obj_type: Union[Type, Tuple[Type]], 
        obj_name: Optional[str] = 'object',
        nullable: Optional[bool] = False,
    ) -> None:

    if nullable is True and obj is None:
        return
    
    def obj_isinstance(obj: object, obj_type: type, obj_name: str) -> None:
        if obj_type == bool or obj_type == int:
            bool_int_validation = type(obj) != obj_type
        else:
            bool_int_validation = False

        # NOTE: isinstance doesn't work with bool and int. That's why i used 'type(obj) != obj_type'
        if not isinstance(obj, obj_type) or bool_int_validation: 
            raise TypeError(
                f"\n\n\t"
                f"TypeError - - -> |{obj_name}| Should be of Type |{obj_type}| but got |{type(obj)}|\n\n\t"
                f"obj       = {obj!r}\n\t"
                f"type(obj) = {type(obj)}\n\t"
                f"obj_type  = {obj_type}\n\t"
                f"obj_name  = {obj_name}\n\t"
            )
    
    obj_type_origin = get_origin(obj_type)
    obj_type_args = get_args(obj_type)
    
    if obj_type_origin is None and obj_type_args == ():
        if obj_type is Any:
            return
        
        obj_isinstance(obj, obj_type, obj_name)
    else:
        if obj_type_origin is Union:
            raise ValueError('Unsuported!')
        
        obj_isinstance(obj, obj_type_origin, obj_name)

        if obj_type_args is not None and obj_type_args != (): 
            if isinstance(obj, dict):
                for key, value in obj.items():
                    # NOTE: Validates the key type and the value type
                    validate_obj_type(key, obj_type_args[0], str(obj_name + f'[{key.__repr__()}]'), nullable)
                    validate_obj_type(value, obj_type_args[1], str(obj_name + f'[{key.__repr__()}]'), nullable)
            else:
                for idx, inner_obj in enumerate(obj):
                    inner_arg = get_item_from_obj_at_idx(obj=obj_type_args, idx=idx) 
                    validate_obj_type(inner_obj, inner_arg, f"{obj_name}[{idx}]", nullable)
                           