import sys
from typing import Any, Dict, List, Type, Tuple

from PyTabFy.PyTUtils import get_item_from_obj_at_idx, validate_obj_type, get_terminal_width
from PyTabFy.PyTCore.Exceptions import InvalidConfigurationException
from PyTabFy.PyTCore.Warnings import ConfigWarning, WarningLevel
from PyTabFy.PyTEnums import (
    Alignment,
    TableFitMode, 
    TableSymbols, 
    StringSlicingMode,
    StringLengthValidation, 
    StringFunctions,
    StringBreakMode,
)


class TableConfigs():
    """
    Base Configuration Class for Table Settings.

    **How to Use**:
        - Extend this class to create custom configurations by overriding the `__init__` method.

    **Example**:
        ```python
        from PyTabFy.PyTConfigs import TableConfigs

        class MyCustomTableConfig(TableConfigs):
            def __init__(self) -> None:
                super().__init__()

                # Add custom configuration settings
                self.custom_config_name = "custom_value"
                self.another_config = 42

        # Using the custom configuration
        custom_config = MyCustomTableConfig()
        table = DefaultTable(configs=custom_config)
        ```
    """

    _DEFAULT_CONFIGS: Dict[str, Tuple[Any, Type]] = {

        'table_fit_mode': (TableFitMode.DYNAMIC_TABLE_FIT,      TableFitMode),
        'table_symbols':  (TableSymbols.DEFAULT_MIXED,          TableSymbols),
        'min_table_size': (get_terminal_width(multiplier=0.50), int),
        'max_table_size': (get_terminal_width(multiplier=0.95), int),

        'string_lenght_validation': (StringLengthValidation.BUILT_IN_LEN, StringLengthValidation), 
        'string_slicing_mode':      (StringSlicingMode.STRING_END,        StringSlicingMode), 
        'string_break_mode':        (StringBreakMode.BREAK_DYNAMIC, StringBreakMode),   
        'title_delimiter':          ('...',                                     str),  
        'headers_delimiters':       (['...', ],                           List[str]),
        'contents_delimiters':      (['...', ],                           List[str]),
       
        'headers_null_str_replacement':  ('NULL', str),
        'contents_null_str_replacement': ('NULL', str),

        'title_alignment':    (Alignment.LEFT,     Alignment), 
        'header_alignments':  ([Alignment.LEFT, ], List[Alignment]), 
        'content_alignments': ([Alignment.LEFT, ], List[Alignment]),

        'max_title_string_lenght':    (sys.maxsize,     int), 
        'max_header_strings_lenght':  ([sys.maxsize, ], List[int]), 
        'max_content_strings_lenght': ([sys.maxsize, ], List[int]), 

        'title_string_function':    (StringFunctions.STR_KEEP_AS_IS,     StringFunctions), 
        'header_strings_function':  ([StringFunctions.STR_KEEP_AS_IS, ], List[StringFunctions]), 
        'content_strings_function': ([StringFunctions.STR_KEEP_AS_IS, ], List[StringFunctions]), 

        'title_left_padding':     (1,    int),
        'title_right_padding':    (1,    int),
        'header_left_paddings':   ([1, ], List[int]),
        'header_right_paddings':  ([1, ], List[int]),
        'content_left_paddings':  ([1, ], List[int]),
        'content_right_paddings': ([1, ], List[int]),

        'upper_title_empty_border_size': (1, int),
        'lower_title_empty_border_size': (1, int),
        'upper_header_empty_border_size': (0, int),
        'lower_header_empty_border_size': (0, int),
        'upper_content_empty_border_size': (0, int),
        'lower_content_empty_border_size': (0, int),

        'force_alternating_chars_respect': (False, bool),  
        'force_display':                   (False, bool),
        'enable_multiline':                (False, bool),
        'margin':                          (0,     int),    
    }

    def __init__(self) -> None:
        from PyTabFy import global_configs
        global_configs._display_ascii_art()

        self._was_class_initialized: bool = True

        # NOTE: Table related configs
        self.table_fit_mode: TableFitMode = None  # The fitting method for the table
        self.table_symbols:  TableSymbols = None  # Symbols used in the table
        self.min_table_size: int          = None  # The minimal size of the table
        self.max_table_size: int          = None  # The maximum size of the table

        # NOTE: String related configs
        self.string_lenght_validation: StringLengthValidation = None  # Length validation method applied to all strings
        self.string_slicing_mode:      StringSlicingMode      = None  # Slicing method applied to all strings
        self.title_delimiter:          str                    = None  # Delimiter applied to the title string
        self.headers_delimiters:       List[str]              = None  # Delimiter applied to all header strings
        self.contents_delimiters :     List[str]              = None  # Delimiter applied to all contents strings
      
        # NOTE: Alignment related configs
        self.title_alignment:    Alignment       = None  # Alignment applied to the title
        self.header_alignments:  List[Alignment] = None  # Alignment applied to each header
        self.content_alignments: List[Alignment] = None  # Alignment applied to each content

        # NOTE: Max String Lenght related configs
        self.max_title_string_lenght:    int       = None  # Length applied to the title
        self.max_header_strings_lenght:  List[int] = None  # Lengths applied to header strings
        self.max_content_strings_lenght: List[int] = None  # Lengths applied to content strings

        # NOTE: String Function related configs
        self.title_string_function:    StringFunctions       = None  # Function applied to the title
        self.header_strings_function:  List[StringFunctions] = None  # Functions applied to each header
        self.content_strings_function: List[StringFunctions] = None  # Functions applied to each content

        # NOTE: Paddings related configs
        self.title_left_padding:     int       = None  # Left paddings between the title column
        self.title_right_padding:    int       = None  # Right paddings between the title column
        self.header_left_paddings:   List[int] = None  # Left paddings between the header column
        self.header_right_paddings:  List[int] = None  # Right paddings between the header column
        self.content_left_paddings:  List[int] = None  # Left paddings between the content column
        self.content_right_paddings: List[int] = None  # Right paddings between the content column

        # NOTE: Empty border size related configs
        self.upper_title_empty_border_size:   int = None
        self.lower_title_empty_border_size:   int = None
        self.upper_header_empty_border_size:  int = None
        self.lower_header_empty_border_size:  int = None
        self.upper_content_empty_border_size: int = None
        self.lower_content_empty_border_size: int = None

        # NOTE: Empty string configs
        self.headers_null_str_replacement:  str  = None 
        self.contents_null_str_replacement: str  = None 

        # NOTE: Other configs
        self.force_alternating_chars_respect: bool = None  # Whether to respect the alternating chars or not
        self.force_display:                   bool = None  # Whether to force the display of the table, even if it breaks
        self.enable_multiline:                bool = None  # Whether to enable multiline or not
        self.margin: int  = None  # Margin applied to the table

        self.string_break_mode: StringBreakMode = None
    

    def get_default_config(self, name: str) -> Any:
        value: Any = self._DEFAULT_CONFIGS.get(name, None)[0]

        # NOTE: Overrides the default value for 'force_alternating_chars_respect'
        if name == 'force_alternating_chars_respect':
            if self.table_symbols.is_alternating_chars():
                value = True
            else: 
                value = False

        # NOTE: Overrides the default value for 'max_title_string_lenght'
        if name == 'max_title_string_lenght':
            value = get_terminal_width(multiplier=0.95) - self.title_left_padding - self.title_right_padding

        # NOTE: Overrides the default value for 'max_header_strings_lenght'
        if name == 'max_header_strings_lenght':
            value = [get_terminal_width(multiplier=0.95) - sum(self.header_left_paddings) - sum(self.header_right_paddings)]

        # NOTE: Overrides the default value for 'max_content_strings_lenght'
        if name == 'max_content_strings_lenght':
            value = [get_terminal_width(multiplier=0.95) - sum(self.content_left_paddings) - sum(self.content_right_paddings)]
            
        return value


    def set_default_configs(self) -> None:
        for attr in self.__dir__():
            if attr.startswith('__') or callable(getattr(self, attr)):
                continue
            
            value = self.get_default_config(attr)

            setattr(self, attr, value)
            self.validate_attribute(attr)

        
    def set_custom_configs(self, configs: 'TableConfigs') -> None:
        for attr in self.__dir__():
            if attr.startswith('__') or callable(getattr(self, attr)):
                continue

            if getattr(configs, attr) is not None:
                value = getattr(configs, attr)
            else:
                value = self.get_default_config(attr)
                
            setattr(self, attr, value)
            self.validate_attribute(attr)

        
    def update_attributes(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                self.validate_attribute(key)


    def validate_attribute(self, attr: str) -> None:
        if attr == 'table_symbols':
            validate_obj_type(self.table_symbols, TableSymbols, 'table_symbols')
            validate_obj_type(self.table_symbols.value, Dict[str, Any], 'table_symbols')
       
        elif attr == 'table_fit_mode':
            validate_obj_type(self.table_fit_mode, TableFitMode, 'table_fit_mode')

        elif attr == 'min_table_size':
            validate_obj_type(self.min_table_size, int, 'min_table_size')

            if self.min_table_size <= 0:
                raise InvalidConfigurationException(
                        "The value in 'min_table_size' must be greater than 0."
                )

        elif attr == 'max_table_size':
            validate_obj_type(self.max_table_size, int, 'max_table_size')

            if self.max_table_size <= 0:
                raise InvalidConfigurationException(
                    "The value in 'max_table_size' must be greater than 0."
                )

            if self.max_table_size < self.min_table_size:
                self.max_table_size = self.min_table_size

                ConfigWarning(
                    info="'max_table_size' value must be greater than 'min_table_size'",
                    warning_level=WarningLevel.ERROR,
                    from_class=__class__.__name__,
                )
                ConfigWarning(
                    info="'max_table_size' value was changed to 'min_table_size'",
                    warning_level=WarningLevel.INFO,
                    from_class=__class__.__name__,
                )

        elif attr == 'string_lenght_validation':
            validate_obj_type(self.string_lenght_validation, StringLengthValidation, 'string_lenght_validation')

        elif attr == 'string_slicing_mode':
            validate_obj_type(self.string_slicing_mode, StringSlicingMode, 'string_slicing_mode')
       
        elif attr == 'headers_delimiters':
            validate_obj_type(self.headers_delimiters, List[str], 'headers_delimiters')

        elif attr == 'contents_delimiters':
            validate_obj_type(self.contents_delimiters, List[str], 'contents_delimiters')

        elif attr == 'title_delimiter':
            validate_obj_type(self.title_delimiter, str, 'title_delimiter')

        elif attr == 'title_alignment':
            validate_obj_type(self.title_alignment, Alignment, 'title_alignment')
        
        elif attr == 'header_alignments':
            validate_obj_type(self.header_alignments, List[Alignment], 'header_alignments')

        elif attr == 'content_alignments':
            validate_obj_type(self.content_alignments, List[Alignment], 'content_alignments')

        elif attr == 'max_title_string_lenght':
            validate_obj_type(self.max_title_string_lenght, int, 'max_title_string_lenght')

            # Validating for positive integer
            if self.max_title_string_lenght <= 0:
                raise InvalidConfigurationException("'max_title_string_lenght' must be greater than 0.")
            
            if not self.enable_multiline:
                # Validate for delimiters greater than the string lenght
                if len(self.title_delimiter) >= self.max_title_string_lenght:
                        raise InvalidConfigurationException([
                            f"The length of 'title_delimiter'",
                            f"must be smaller than:",
                            f"'max_title_string_lenght'",
                        ])    

        elif attr == 'max_header_strings_lenght':
            validate_obj_type(self.max_header_strings_lenght, List[int], 'max_header_strings_lenght')
            
            # Validating for positive integers
            for idx, value in enumerate(self.max_header_strings_lenght):
                if value <= 0:
                    raise InvalidConfigurationException(
                        "All values in 'max_header_strings_lenght' must be greater than 0."
                    )
                
                if not self.enable_multiline:
                    # Validate for delimiters greater than the string lenght
                    if len(get_item_from_obj_at_idx(obj=self.headers_delimiters, idx=idx)) >= value:
                        raise InvalidConfigurationException([
                            f"The length of 'headers_delimiters[{idx}]'",
                            f"must be smaller than:",
                            f"'max_header_strings_lenght[{idx}]'",
                        ])    
                
        elif attr == 'max_content_strings_lenght':
            validate_obj_type(self.max_content_strings_lenght, List[int], 'max_content_strings_lenght')
            
            # Validating for positive integers
            for idx, value in enumerate(self.max_content_strings_lenght):
                if value <= 0:
                    raise InvalidConfigurationException(
                        "All values in 'max_content_strings_lenght' must be greater than 0."
                    )
                
                if not self.enable_multiline:
                    # Validate for delimiters greater than the string lenght
                    if len(get_item_from_obj_at_idx(obj=self.contents_delimiters, idx=idx)) >= value:
                        raise InvalidConfigurationException([
                            f"The length of 'contents_delimiters[{idx}]'",
                            f"must be smaller than:",
                            f"'max_content_strings_lenght[{idx}]'",
                        ])

        elif attr == 'title_string_function':
            validate_obj_type(self.title_string_function, StringFunctions, 'title_string_function')

        elif attr == 'header_strings_function':
            validate_obj_type(self.header_strings_function, List[StringFunctions], 'header_strings_function')
        
        elif attr == 'content_strings_function':
            validate_obj_type(self.content_strings_function, List[StringFunctions], 'content_strings_function')

        elif attr == 'title_left_padding':
            validate_obj_type(self.title_left_padding, int, 'title_left_padding')

            # Validating for integers greater or equal to 0
            if self.title_left_padding < 0:
                raise InvalidConfigurationException(
                        "'title_left_padding' must be greater or equal to 0"
                )
            
            if self.force_alternating_chars_respect:
                ConfigWarning(
                    info=f"The value {self.title_left_padding} of 'title_left_padding' may not be complied because all columns must be even",
                    warning_level=WarningLevel.INFO,
                    from_class=__class__.__name__,
                )
       
        elif attr == 'title_right_padding':
            validate_obj_type(self.title_right_padding, int, 'title_right_padding')

            # Validating for integers greater or equal to 0
            if self.title_right_padding < 0:
                raise InvalidConfigurationException(
                        "'title_right_padding' must be greater or equal to 0"
                )

            if self.force_alternating_chars_respect:
                ConfigWarning(
                    info=f"The value {self.title_right_padding} of 'title_right_padding' may not be complied because all columns must be even",
                    warning_level=WarningLevel.INFO,
                    from_class=__class__.__name__,
                )

        elif attr == 'header_left_paddings':
            validate_obj_type(self.header_left_paddings, List[int], 'header_left_paddings')

            # Validating for integers greater or equal to 0
            for idx in range(len(self.header_left_paddings)):
                if self.header_left_paddings[idx] < 0:
                    raise InvalidConfigurationException(
                        "All values in 'header_left_paddings' must be greater than 0."
                    )
                

            if self.force_alternating_chars_respect:
                ConfigWarning(
                    info=f"The values {self.header_left_paddings} of 'header_left_paddings' may not be complied because all columns must be even",
                    warning_level=WarningLevel.INFO,
                    from_class=__class__.__name__,
                )

        elif attr == 'header_right_paddings':
            validate_obj_type(self.header_right_paddings, List[int], 'header_right_paddings')

            # Validating for integers greater or equal to 0
            for idx in range(len(self.header_right_paddings)):
                if self.header_right_paddings[idx] < 0:
                    raise InvalidConfigurationException(
                        "All values in 'header_right_paddings' must be greater than 0."
                    )
                
            if self.force_alternating_chars_respect:
                ConfigWarning(
                    info=f"The values {self.header_right_paddings} of 'header_right_paddings' may not be complied because all columns must be even",
                    warning_level=WarningLevel.INFO,
                    from_class=__class__.__name__,
                )

        elif attr == 'content_left_paddings':
            validate_obj_type(self.content_left_paddings, List[int], 'content_left_paddings')

            # Validating for integers greater or equal to 0
            for idx in range(len(self.content_left_paddings)):
                if self.content_left_paddings[idx] < 0:
                    raise InvalidConfigurationException(
                        "All values in 'content_left_paddings' must be greater than 0."
                    )
                
            if self.force_alternating_chars_respect:
                ConfigWarning(
                    info=f"The values {self.content_left_paddings} of 'content_left_paddings' may not be complied because all columns must be even",
                    warning_level=WarningLevel.INFO,
                    from_class=__class__.__name__,
                )
                    
        elif attr == 'content_right_paddings':
            validate_obj_type(self.content_right_paddings, List[int], 'content_right_paddings')

            # Validating for integers greater or equal to 0
            for idx in range(len(self.content_right_paddings)):
                if self.content_right_paddings[idx] < 0:
                    raise InvalidConfigurationException(
                        "All values in 'content_right_paddings' must be greater than 0."
                    )
            
            if self.force_alternating_chars_respect:
                ConfigWarning(
                    info=f"The values {self.content_right_paddings} of 'content_right_paddings' may not be complied because all columns must be even",
                    warning_level=WarningLevel.INFO,
                    from_class=__class__.__name__,
                )
         
        elif attr == 'force_alternating_chars_respect':
            validate_obj_type(self.force_alternating_chars_respect, bool, 'force_alternating_chars_respect')

        elif attr == 'margin':
            validate_obj_type(self.margin, int, 'margin')

            if self.margin < 0:
                raise InvalidConfigurationException(
                    f"'{attr}' must be greater or equal to 0!"
                )
                
        elif attr == 'string_break_mode':
            validate_obj_type(self.string_break_mode, StringBreakMode, 'string_break_mode')

            if self.string_break_mode == StringBreakMode.BREAK_WORD:
                ConfigWarning(
                    info=f"The value BREAK_WORD of 'string_break_mode' can cause max_strings_lenghts attrs to be disobeyed",
                    warning_level=WarningLevel.INFO,
                    from_class=__class__.__name__,
                )
            

        # Validate empty border sizes
        elif attr in [
            'upper_title_empty_border_size', 
            'lower_title_empty_border_size',
            'upper_header_empty_border_size',
            'lower_header_empty_border_size',
            'upper_content_empty_border_size',
            'lower_content_empty_border_size',
        ]:
            obj: int = self.__getattribute__(attr)

            validate_obj_type(obj=obj, obj_type=int, obj_name=attr)
            if obj < 0:
                raise InvalidConfigurationException(
                    f"'{attr}' must be greater or equal to 0!"
                )
        
        elif attr == 'force_display':
            validate_obj_type(self.force_display, bool, 'force_display')

            if self.force_display:
                ConfigWarning(
                    info=f"Enabling 'force_display' can cause unexpected errors",
                    warning_level=WarningLevel.INFO,
                    from_class=__class__.__name__,
                )

        elif attr == 'enable_multiline':
            validate_obj_type(self.enable_multiline, bool, 'enable_multiline')
            
            if self.enable_multiline:
                ConfigWarning(
                    info="'string_slicing_mode' won't be used because 'enable_multiline' is True",
                    warning_level=WarningLevel.INFO,
                    from_class=__class__.__name__,
                )
                ConfigWarning(
                    info="'string_delimiters' won't be used because 'enable_multiline' is True",
                    warning_level=WarningLevel.INFO,
                    from_class=__class__.__name__,
                )

        elif attr == 'headers_null_str_replacement':
            validate_obj_type(self.headers_null_str_replacement, str, 'headers_null_str_replacement')

        elif attr == 'contents_null_str_replacement':
            validate_obj_type(self.contents_null_str_replacement, str, 'contents_null_str_replacement')


    def __dir__(self) -> List[str]:
        """
        Returns a list of attribute names for the instance, prioritizing certain attributes.

        This method overrides the default `__dir__` to produce an ordered list of attribute names, 
        giving priority to some attributes.

        Returns:
            List[str]: A list of attribute names.
        """

        # NOTE: 'table_symbols', 'force_alternating_chars_respect', 'paddings' and 'enable_multiline' have priority over the rest
        attributes: List[str] = [
            'table_symbols',
            'force_alternating_chars_respect', 
            'enable_multiline',
            'title_left_padding',  
            'title_right_padding',
            'header_left_paddings',  
            'header_right_paddings',  
            'content_left_paddings', 
            'content_right_paddings',

            'table_fit_mode', 
            'min_table_size', 
            'max_table_size',
            'string_lenght_validation',
            'string_slicing_mode',
            'title_delimiter',
            'headers_delimiters',
            'contents_delimiters',
            'title_alignment',  
            'header_alignments', 
            'content_alignments',
            'max_title_string_lenght',  
            'max_header_strings_lenght', 
            'max_content_strings_lenght',
            'title_string_function', 
            'header_strings_function', 
            'content_strings_function',
            'margin',
            'string_break_mode',
            'upper_title_empty_border_size',
            'lower_title_empty_border_size',
            'upper_header_empty_border_size',
            'lower_header_empty_border_size',
            'upper_content_empty_border_size',
            'lower_content_empty_border_size',
            'force_display',     
            'headers_null_str_replacement',
            'contents_null_str_replacement',
            
        ]

        return attributes
