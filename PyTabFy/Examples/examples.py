import sys
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from PyTabFy.PyTCore.Exceptions import PyTabFyException
from PyTabFy.PyTUtils import get_terminal_width
from PyTabFy.Dummy import (
    get_only_ascii_book_data, 
    get_only_ascii_movie_data,
    get_not_only_ascii_book_data, 
    get_not_only_ascii_movie_data, 
)
from PyTabFy.PyTConfigs import TableConfigs
from PyTabFy.PyTCore.Types import TableData
from PyTabFy.PyTCore.Tables import (
    DefaultTable,
    LeftAlignedTable,
    RightAlignedTable,
    CenterAlignedTable, 
)
from PyTabFy.PyTEnums import (
    Alignment, 
    TableSymbols, 
    TableFitMode, 
    StringBreakMode,
    StringFunctions, 
    StringSlicingMode, 
    StringLengthValidation, 
)


def center_aligned_table_example(
        DummyDataFunc: Optional[Callable[[], Tuple[str, List[str], List[List[str]]]]] = None
    ) -> None:
    """
    Displays a center-aligned table using custom configuration settings.

    This function builds and displays a table with title, headers and contents. 
    The data for the table can either be fetched using a provided callable 
    function or defaults to book data. 

    ### Args:
        - `DummyDataFunc (Callable[[], Tuple[str, List[str], List[List[str]]]], Optional):`
            Any function found inside the module `PyTabFy.Dummy`. If not provided, 
            the `get_only_ascii_book_data` function is used as the default.
 
    ### Returns:
        - `None`

    ### How To:
        - `center_aligned_table_example()`
        - `center_aligned_table_example(get_not_only_ascii_movie_data)`
    """

    if DummyDataFunc is None:
        title, headers, contents = get_only_ascii_book_data()
    else:
        title, headers, contents = DummyDataFunc()

    title = 'Center Aligned Table Example Using ' + title

    
    class CustomConfigs(TableConfigs):
        
        def __init__(self) -> None:
            super().__init__()

            self.table_fit_mode = TableFitMode.DYNAMIC_TABLE_FIT
            self.table_symbols  = TableSymbols.DEFAULT_MIXED
            self.min_table_size = get_terminal_width(multiplier=0.75)
            self.max_table_size = get_terminal_width(multiplier=0.95)

            self.string_lenght_validation = StringLengthValidation.WCSWIDTH  
            self.string_slicing_mode      = StringSlicingMode.STRING_END

            self.title_delimiter =     '...'
            self.headers_delimiters =  ['...', ]
            self.contents_delimiters = ['...', ]

            self.max_title_string_lenght    = sys.maxsize
            self.max_header_strings_lenght  = [sys.maxsize, ]
            self.max_content_strings_lenght = [30, ]

            self.title_string_function    = StringFunctions.STR_TITLE
            self.header_strings_function  = [StringFunctions.STR_UPPER, ]
            self.content_strings_function = [StringFunctions.STR_KEEP_AS_IS, ]

            self.title_left_padding     = 1
            self.title_right_padding    = 1
            self.header_left_paddings   = [1, ]
            self.header_right_paddings  = [1, ]
            self.content_left_paddings  = [1, ]
            self.content_right_paddings = [1, ]

            self.upper_title_empty_border_size = 2
            self.lower_title_empty_border_size = 2
            self.upper_header_empty_border_size = 1
            self.lower_header_empty_border_size = 1
            self.upper_content_empty_border_size = 0 
            self.lower_content_empty_border_size = 0 

            self.force_alternating_chars_respect = True
            self.margin = 1

    custom_configs = CustomConfigs()
    
    data = TableData().set_data_from_list(title=title, headers=headers, contents=contents)
    table = CenterAlignedTable(custom_configs=custom_configs)

    table.build(data)
    table.display(border_between_content=False)


def left_aligned_table_example(
        DummyDataFunc: Optional[Callable[[], Tuple[str, List[str], List[List[str]]]]] = None
    ) -> None:
    """
    Displays a left-aligned table using custom configuration settings.

    This function builds and displays a table with title, headers and contents. 
    The data for the table can either be fetched using a provided callable 
    function or defaults to book data. 

    ### Args:
        - `DummyDataFunc (Callable[[], Tuple[str, List[str], List[List[str]]]], Optional):`
            Any function found inside the module `PyTabFy.Dummy`. If not provided, 
            the `get_not_only_ascii_book_data` function is used as the default.

    ### Returns:
        - `None`

    ### How To:
        - `left_aligned_table_example()`
        - `left_aligned_table_example(get_not_only_ascii_movie_data)`
    """

    if DummyDataFunc is None:
        title, headers, contents = get_not_only_ascii_book_data()
    else:
        title, headers, contents = DummyDataFunc()

    title = 'Left Aligned Table Example Using ' + title


    class CustomConfigs(TableConfigs):
        
        def __init__(self) -> None:
            super().__init__()  

            self.table_fit_mode = TableFitMode.MAX_TABLE_FIT
            self.table_symbols  = TableSymbols.DEFAULT_EQUAL
            self.min_table_size = get_terminal_width(multiplier=0.75)
            self.max_table_size = get_terminal_width(multiplier=0.95)

            self.string_lenght_validation = StringLengthValidation.WCSWIDTH  
            self.string_slicing_mode      = StringSlicingMode.STRING_END

            self.title_delimiter =     '...'
            self.headers_delimiters =  ['...', ]
            self.contents_delimiters = ['...', ]

            self.max_title_string_lenght    = sys.maxsize
            self.max_header_strings_lenght  = [sys.maxsize, ]
            self.max_content_strings_lenght = [sys.maxsize, 20, ]

            self.title_string_function    = StringFunctions.STR_TITLE
            self.header_strings_function  = [StringFunctions.STR_UPPER, ]
            self.content_strings_function = [StringFunctions.STR_KEEP_AS_IS, ]

            self.title_left_padding     = 1
            self.title_right_padding    = 1
            self.header_left_paddings   = [1, ]
            self.header_right_paddings  = [1, ]
            self.content_left_paddings  = [1, ]
            self.content_right_paddings = [1, ]

            self.upper_title_empty_border_size = 2
            self.lower_title_empty_border_size = 2
            self.upper_header_empty_border_size = 1
            self.lower_header_empty_border_size = 1
            self.upper_content_empty_border_size = 0 
            self.lower_content_empty_border_size = 0 

            self.force_alternating_chars_respect = False
            self.margin = 1

    custom_configs = CustomConfigs()

    data = TableData().set_data_from_list(title=title, headers=headers, contents=contents)
    table = LeftAlignedTable(custom_configs=custom_configs)

    table.build(data)
    table.display(border_between_content=False)


def right_aligned_table_example(
        DummyDataFunc: Optional[Callable[[], Tuple[str, List[str], List[List[str]]]]] = None
    ) -> None:
    """
    Displays a right-aligned table using custom configuration settings.

    This function builds and displays a table with title, headers and contents. 
    The data for the table can either be fetched using a provided callable 
    function or defaults to movie data. 

    ### Args:
        - `DummyDataFunc (Callable[[], Tuple[str, List[str], List[List[str]]]], Optional):`
            Any function found inside the module `PyTabFy.Dummy`. If not provided, 
            the `get_only_ascii_movie_data` function is used as the default.

    ### Returns:
        - `None`

    ### How To:
        - `right_aligned_table_example()`
        - `right_aligned_table_example(get_not_only_ascii_movie_data)`
    """

    if DummyDataFunc is None:
        title, headers, contents = get_only_ascii_movie_data()
    else:
        title, headers, contents = DummyDataFunc()

    title = 'Right Aligned Table Example Using ' + title


    class CustomConfigs(TableConfigs):
        
        def __init__(self) -> None:
            super().__init__()
            
            self.table_fit_mode = TableFitMode.MAX_TABLE_FIT
            self.table_symbols  = TableSymbols.DEFAULT_DASH
            self.min_table_size = get_terminal_width(multiplier=0.75)
            self.max_table_size = get_terminal_width(multiplier=0.95)

            self.string_lenght_validation = StringLengthValidation.WCSWIDTH  
            self.string_slicing_mode      = StringSlicingMode.STRING_END
            
            self.title_delimiter =     '...'
            self.headers_delimiters =  ['...', ]
            self.contents_delimiters = ['...', ]

            self.max_title_string_lenght    = sys.maxsize
            self.max_header_strings_lenght  = [sys.maxsize, ]
            self.max_content_strings_lenght = [20, ]

            self.title_string_function    = StringFunctions.STR_TITLE
            self.header_strings_function  = [StringFunctions.STR_UPPER, ]
            self.content_strings_function = [StringFunctions.STR_KEEP_AS_IS, ]
            
            self.title_left_padding     = 1
            self.title_right_padding    = 1
            self.header_left_paddings   = [1, ]
            self.header_right_paddings  = [1, ]
            self.content_left_paddings  = [1, ]
            self.content_right_paddings = [1, ]

            self.upper_title_empty_border_size = 2
            self.lower_title_empty_border_size = 2
            self.upper_header_empty_border_size = 1
            self.lower_header_empty_border_size = 1
            self.upper_content_empty_border_size = 0 
            self.lower_content_empty_border_size = 0 

            self.force_alternating_chars_respect = False
            self.margin = 1
            
    custom_configs = CustomConfigs()

    data = TableData().set_data_from_list(title=title, headers=headers, contents=contents)
    table = RightAlignedTable(custom_configs=custom_configs)

    table.build(data)
    table.display(border_between_content=False)


def multi_lines_table_example(
        DummyDataFunc: Optional[Callable[[], Tuple[str, List[str], List[List[str]]]]] = None
    ) -> None:
    """
    Displays a multiline table using custom configuration settings.

    This function builds and displays a table with title, headers and contents. 
    The data for the table can either be fetched using a provided callable 
    function or defaults to movie data. 

    ### Args:
        - `DummyDataFunc (Callable[[], Tuple[str, List[str], List[List[str]]]], Optional)`:
            Any function found inside the module `PyTabFy.Dummy`. If not provided, 
            the `get_not_only_ascii_movie_data` function is used as the default.

    ### Returns:
        - `None`

    ### How To:
        - `multi_lines_table_example()`
        - `multi_lines_table_example(get_not_only_ascii_movie_data)`
    """

    if DummyDataFunc is None:
        title, headers, contents = get_not_only_ascii_movie_data()
    else:
        title, headers, contents = DummyDataFunc()

    title = 'Multiline Table Example Using ' + title


    class CustomConfigs(TableConfigs):
        
        def __init__(self) -> None:
            super().__init__()
            
            self.table_fit_mode = TableFitMode.DYNAMIC_TABLE_FIT
            self.table_symbols  = TableSymbols.DEFAULT_CLI
            self.min_table_size = get_terminal_width(multiplier=0.75)
            self.max_table_size = get_terminal_width(multiplier=0.95)

            self.string_lenght_validation = StringLengthValidation.WCSWIDTH  
            self.string_break_mode        = StringBreakMode.BREAK_DYNAMIC

            self.title_delimiter =     '...'
            self.headers_delimiters =  ['...', ]
            self.contents_delimiters = ['...', ]

            self.max_title_string_lenght    = sys.maxsize
            self.max_header_strings_lenght  = [sys.maxsize]
            self.max_content_strings_lenght = [sys.maxsize, sys.maxsize, 10, ]

            self.title_string_function    = StringFunctions.STR_TITLE
            self.header_strings_function  = [StringFunctions.STR_UPPER, ]
            self.content_strings_function = [StringFunctions.STR_KEEP_AS_IS, ]

            self.title_alignment    = Alignment.CENTER
            self.header_alignments  = [Alignment.CENTER, ]
            self.content_alignments = [
                Alignment.LEFT, Alignment.LEFT, Alignment.LEFT, Alignment.LEFT, Alignment.CENTER, Alignment.CENTER
            ]
            
            self.title_left_padding     = 1
            self.title_right_padding    = 1
            self.header_left_paddings   = [1, ]
            self.header_right_paddings  = [1, ]
            self.content_left_paddings  = [1, ]
            self.content_right_paddings = [1, ]

            self.upper_title_empty_border_size   = 2
            self.lower_title_empty_border_size   = 2
            self.upper_header_empty_border_size  = 1
            self.lower_header_empty_border_size  = 1
            self.upper_content_empty_border_size = 0
            self.lower_content_empty_border_size = 0

            self.force_alternating_chars_respect = False
            self.enable_multiline = True

            self.margin = 1
            
    custom_configs = CustomConfigs()

    data = TableData().set_data_from_list(title=title, headers=headers, contents=contents)
    table = DefaultTable(custom_configs=custom_configs)

    table.build(data)
    table.display(border_between_content=True)


def log_table_example(
        DummyDataFunc: Optional[Callable[[], Tuple[str, List[str], List[List[str]]]]] = None,
        file_path: Optional[Path] = Path.home() / 'Documents' / 'table.txt'
    ) -> None:
    """
    Log a multiline table using custom configuration settings.

    This function builds and log a table with title, headers and contents. 
    The data for the table can either be fetched using a provided callable 
    function or default to movie data. 

    ### Args:
        - `DummyDataFunc (Callable[[], Tuple[str, List[str], List[List[str]]]], Optional):`
            Any function found inside the module `PyTabFy.Dummy`. If not provided, 
            the `get_only_ascii_movie_data` function is used as the default.

        - `file_path (Path, Optional):`
            The full path to save the table. If not provided, `Path.home() / 'Documents' / 'table.txt'` 
            is used as the default.

    ### Returns:
        - `None`

    ### How To:
        - `log_table_example()`
        - `log_table_example(file_path='C:/Users/Public/table.txt', get_not_only_ascii_movie_data)`
    """

    if DummyDataFunc is None:
        title, headers, contents = get_only_ascii_movie_data()
    else:
        title, headers, contents = DummyDataFunc()

    title = 'Log Table Example Using ' + title


    class CustomConfigs(TableConfigs):
        
        def __init__(self) -> None:
            super().__init__()
            
            self.table_fit_mode = TableFitMode.MAX_TABLE_FIT
            self.table_symbols  = TableSymbols.DEFAULT_MIXED
            self.max_table_size = 120

            self.string_lenght_validation = StringLengthValidation.BUILT_IN_LEN  
            self.string_break_mode        = StringBreakMode.BREAK_DYNAMIC

            self.max_title_string_lenght    = sys.maxsize
            self.max_header_strings_lenght  = [sys.maxsize, ]
            self.max_content_strings_lenght = [sys.maxsize, ]

            self.title_string_function    = StringFunctions.STR_TITLE
            self.header_strings_function  = [StringFunctions.STR_UPPER, ]
            self.content_strings_function = [StringFunctions.STR_KEEP_AS_IS, ]

            self.title_alignment    = Alignment.CENTER
            self.header_alignments  = [Alignment.CENTER, ]
            self.content_alignments = [Alignment.LEFT, Alignment.CENTER, Alignment.CENTER]
            
            self.title_left_padding     = 1
            self.title_right_padding    = 1
            self.header_left_paddings   = [1, ]
            self.header_right_paddings  = [1, ]
            self.content_left_paddings  = [1, ]
            self.content_right_paddings = [1, ]

            self.upper_title_empty_border_size   = 1
            self.lower_title_empty_border_size   = 1
            self.upper_header_empty_border_size  = 0
            self.lower_header_empty_border_size  = 0
            self.upper_content_empty_border_size = 0 
            self.lower_content_empty_border_size = 0 

            self.force_alternating_chars_respect = True
            self.force_display = True # FIXME
            self.margin = 0
            
    custom_configs = CustomConfigs()

    data = TableData().set_data_from_list(title=title, headers=headers, contents=contents)
    table = DefaultTable(custom_configs=custom_configs)

    table.build(data)
    table.log_table(file_path=file_path, border_between_content=True)


# NOTE: You can directly execute this file
if __name__ == '__main__':

    if get_terminal_width(multiplier=1) < 120:
        raise PyTabFyException(
            'PyTabFy.Examples', 
            [
                'If you are seeing this, you directly executed examples.py with a small terminal tab', 
                'Please, expand your terminal tab!',
                f'Terminal tab size = {get_terminal_width(multiplier=1)}. Expected >= 120'
            ]
        )

    left_aligned_table_example()
    print('\n\n')
    right_aligned_table_example()
    print('\n\n')
    center_aligned_table_example()
    print('\n\n')
    multi_lines_table_example()
    print('\n\n')
    log_table_example(get_not_only_ascii_book_data)
    print('\n\n')

    # NOTE: Other Examples:
    # from PyTabFy.Dummy import get_not_only_ascii_movie_data
    
    #center_aligned_table_example(get_not_only_ascii_movie_data)
    #left_aligned_table_example(get_not_only_ascii_movie_data)
    #right_aligned_table_example(get_not_only_ascii_movie_data)
    #multi_lines_table_example(get_not_only_ascii_movie_data)
