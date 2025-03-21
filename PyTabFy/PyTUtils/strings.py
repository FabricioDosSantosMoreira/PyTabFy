from typing import Iterable, Optional, Tuple

from PyTabFy.PyTEnums import StringLengthValidation, StringSlicingMode
from PyTabFy.PyTUtils import get_item_from_obj_at_idx


def reduce_strings_length(
        strings: Iterable[str],
        lengths: Iterable[int],
        delimiters: Iterable[str],
        slicing_mode: StringSlicingMode,
        length_validation: StringLengthValidation,
        string_replacement_if_none: Optional[str] = '',
    ) -> Tuple[str]:
    """_summary_

    Args:
        strings (List[str]): _description_
        lengths (List[int]): _description_
        delimiters (List[str]): _description_
        slicing_mode (StringSlicingMode): _description_
        length_validation (StringLengthValidation): _description_

    Returns:
        Tuple[Tuple[str, int]]: A Tuple of Tuple, containing the reduced string and its length based on 'length_validation'
    """

    # Pre-process lengths and delimiters to avoid repeated function calls
    lengths = [get_item_from_obj_at_idx(lengths, idx) for idx in range(len(strings))]
    delimiters = [get_item_from_obj_at_idx(delimiters, idx) for idx in range(len(strings))]

    return tuple(
        reduce_string_length(
            string=sub_string,
            length=lengths[idx],
            delimiter=delimiters[idx],
            slicing_mode=slicing_mode,
            length_validation=length_validation,
            string_replacement_if_none=string_replacement_if_none
        )
        for idx, sub_string in enumerate(strings)
    )


def reduce_string_length(
        string: str,
        length: int,
        delimiter: str,
        slicing_mode: StringSlicingMode,
        length_validation: StringLengthValidation,
        string_replacement_if_none: Optional[str] = ''
    ) -> Tuple[str]:

    if string is None or string == '':
        string = string_replacement_if_none

    # Check if 'length' is greater or equal to 'string_length'. If so, return the string unaltered.
    string_length = StringLengthValidation.length_of(string, length_validation)
    if length >= string_length:  
        return string

    str_slice_index: int = 0
    if length_validation == StringLengthValidation.BUILT_IN_LEN:
        str_slice_index = length - len(delimiter)

    elif length_validation == StringLengthValidation.WCSWIDTH:
        current_width: int = StringLengthValidation.length_of(delimiter, length_validation)

        if slicing_mode == StringSlicingMode.STRING_START: 
            _string = reversed(string)
        elif slicing_mode == StringSlicingMode.STRING_END:
            _string = string

        for idx, char in enumerate(_string):
            current_width += StringLengthValidation.char_length(char)
            if current_width > length:
                str_slice_index = idx
                break

    # Return the sliced 'string' with the 'delimiter'
    if slicing_mode == StringSlicingMode.STRING_START: 
        string = delimiter + string[-str_slice_index:]
    elif slicing_mode == StringSlicingMode.STRING_END:
        string = string[:str_slice_index] + delimiter

    return string
