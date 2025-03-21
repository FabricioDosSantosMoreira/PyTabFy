import copy
import os 

from wcwidth import wcswidth

from typing import Any, Iterable, List, Optional, Literal, Union


def match_parity(
        *,
        value: int, 
        target_parity: Literal["even", "odd"],
        decrease: Optional[bool] = False,
    ) -> int:
    """
    Adjusts an integer to match a specified parity (even or odd).

    Parameters:
    value (int): The integer value to be adjusted.
    target_parity (Literal["even", "odd"]): The desired parity of the result.
    decrease (Optional[bool]): If True and adjustment is needed, decrease the value by 1 
                               to achieve the desired parity. If False or not specified, 
                               increase the value by 1 to achieve the desired parity.

    Returns:
    int: The adjusted integer with the specified parity.
    """

    # Determine the current parity of 'value'.
    current_parity = "even" if value % 2 == 0 else "odd"

    # If the current parity does not match the target parity, adjust the value.
    if current_parity != target_parity:
        if decrease:
            return value - 1  # Decrease the value by 1 to change its parity.
        
        return value + 1  # Increase the value by 1 to change its parity.

    
    return value  # 'value' already has the desired parity.


def categorize_contents(
        contents: Union[List[str], List[List[str]]], 
        identifiers: Optional[List[str]] = None,
        do_deepcopy: Optional[bool] = True
    ) -> List[List[str]]:
    """
    Categorize a list of contents by assigning an identifier to each content item.
    
    Args:
        contents (List[str]): A list of strings representing the content to be categorized.
        identifiers (Optional[List[str]]): A list of strings representing identifiers for each content item.
                                           If not provided, identifiers will be generated as incremental numbers
                                           starting from 1.
    
    Returns:
        List[List[str]]: A list of lists, where each inner list contains an identifier and the corresponding content.
                        The format is [[identifier1, content1], [identifier2, content2], ...].
    """
    if do_deepcopy:
        contents = copy.deepcopy(contents)
        identifiers = copy.deepcopy(identifiers) if identifiers else None


    # If 'identifiers' isn't provided.
    if not identifiers:

        identifiers = []
        for n in range(1, len(contents) + 1):
            # Assign default 'identifiers' based on the indices of 'contents', starting from 1
            identifiers.append(str(n))
        

    # Initialize an empty list to store the categorized contents.
    categorized_contents: List = []
    for i, content in enumerate(contents): 

        if isinstance(content, list):
            content.insert(0, identifiers[i])
            categorized_contents.append(content)
        else:
            # Append a list containing the identifier and the content.
            categorized_contents.append([identifiers[i], str(content)])

    return categorized_contents


def get_item_from_obj_at_idx(obj: Iterable[Any], idx: int) -> Any:
    if idx < len(obj):
        return obj[idx]
    else:
        return obj[-1]


def get_item_from_idx_or_zero(obj: Iterable[Any], idx: int) -> Union[Any, int]:
    try:
        return obj[idx]
    except IndexError:
        return 0
            

def get_terminal_width(*, multiplier: float, default: Optional[int] = 80) -> int:
    """Get the terminal width adjusted by a multiplier."""

    try:
        val = int(os.get_terminal_size()[0] * multiplier)
        return val
    except OSError:
        return default


def get_terminal_height(*, multiplier: float, default: Optional[int] = 80) -> int:
    """Get the terminal height adjusted by a multiplier."""

    try:
        val = int(os.get_terminal_size()[1] * multiplier)
        return val
    except OSError:
        return default


def get_visual_width(string: str) -> int:
    """Calculate the visual width of a given string.

    This function determines the visual width of a string, accounting for the 
    differences between ASCII and NON-ASCII characters. NON-ASCII characters 
    may have different widths when displayed compared to ASCII characters.

    Args:
        string (str): The string to calculate the visual width.

    Returns:
        int: The visual width of the string.
    """     
        
    # Check if all characters in the string are ASCII
    if string.isascii():
        return len(string)
    else:
        return wcswidth(string)
