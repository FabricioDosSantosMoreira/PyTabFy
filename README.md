# 📌 PyTabFy

PyTabFy is a module in development that allows users to build customizable tables. Its primary goal is to transform raw data into visually appealing and organized tables. The module was built to take into account ASCII and Non-ASCII characters (for example CJK characters, which have larger width than normal characters).


# 🖼 Gallery:
|                          |  
|--------------------------|
| ![T1](./Docs/img/T1.png) | 
| ![T2](./Docs/img/T2.png) | 


# 📦 Installation
You can install PyTabFy using:

```bash
pip install pytabfy
```

# 🔨 Build
If you prefer to build PyTabFy manually, follow these steps:

```bash
# Clone this repository:
git clone https://github.com/FabricioDosSantosMoreira/PyTabFy.git

# Change directory:
cd PyTabFy

# Normal install 
python -m pip install .
make install

# Editable install
python -m pip install -e .
make install-editable
```


# 🚀 Getting Started

## Examples:
You can start by running the examples of PytabFy:

Option 1 - Running `examples.py` directly
```bash
python -m PyTabFy.Examples.examples   
```

Option 2 - Importing specific examples
```python
from PyTabFy.Examples import (
    left_aligned_table_example, 
    right_aligned_table_example, 
    center_aligned_table_example, 
    multi_lines_table_example,
    log_table_example,
)
from PyTabFy.Dummy import get_not_only_ascii_movie_data


multi_lines_table_example()
multi_lines_table_example(get_not_only_ascii_movie_data)
```


## Building Your Own Table

To create a custom table, follow this example:

```python
# Importing necessary modules
from pathlib import Path
import sys

from PyTabFy.PyTUtils import get_terminal_width
from PyTabFy.PyTConfigs import TableConfigs
from PyTabFy.PyTCore.Types import TableData
from PyTabFy.PyTCore.Tables import (
    DefaultTable,
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

# Defining a custom configuration class
class CustomConfigs(TableConfigs):
    
    # NOTE: The __init__() method and calling super().__init__() are required!
    def __init__(self) -> None:
        super().__init__()

        # NOTES:
        # - You don't need to manually set each configuration, as PyTabFy provides defaults.
        # - Some configurations can influence the behavior of others.
        # - For all configuration variables that are lists:
        #     - They cannot be empty; at least one value must be provided.
        #     - Each list index corresponds to the respective table section index.
        #     - If the table section index exceeds the list length, the last value is used.

        # Defining the fitting mode for the table
        self.table_fit_mode = TableFitMode.DYNAMIC_TABLE_FIT

        # Defining the min and max table size
        # NOTE: Only used if TableFitMode.MAX_TABLE_FIT or MIN_TABLE_FIT are enable
        self.min_table_size = get_terminal_width(multiplier=0.75) # Minimum table width (75% of terminal width)
        self.max_table_size = get_terminal_width(multiplier=0.95) # Maximum table width (95% of terminal width)

        # Defining the symbols for the table
        self.table_symbols  = TableSymbols.DEFAULT_MIXED

        # Defining how strings will be validated
        # NOTE: Use WCSWIDTH if your data contains non-ASCII characters
        self.string_lenght_validation = StringLengthValidation.WCSWIDTH  

        # Defining the maximum string length for different sections
        self.max_title_string_lenght    = sys.maxsize
        self.max_header_strings_lenght  = [50, ] # Each list item corresponds to a header index
        self.max_content_strings_lenght = [30, ] # Each list item corresponds to a content index

        # Defining how the data is sliced (dependent on max string length)
        self.string_slicing_mode = StringSlicingMode.STRING_END
        self.string_break_mode   = StringBreakMode.BREAK_DYNAMIC

        # Defining delimiters for truncated data
        self.title_delimiter     = '...'
        self.headers_delimiters  = ['...', ] # Each list item corresponds to a header index
        self.contents_delimiters = ['...', ] # Each list item corresponds to a content index
        
        # Defining string replacement for empty data values
        self.headers_null_str_replacement = 'NULL'
        self.contents_null_str_replacement = 'NULL'

        # Defining the alignment settings for each section of the table
        self.title_alignment    = Alignment.CENTER
        self.header_alignments  = [Alignment.CENTER, ] # Each list item corresponds to a header index
        self.content_alignments = [Alignment.LEFT, ]   # Each list item corresponds to a content index

        # Defining functions applied to strings in each section
        self.title_string_function = StringFunctions.STR_KEEP_AS_IS
        self.header_strings_function = [StringFunctions.STR_UPPER, ] # Each list item corresponds to a header index
        self.content_strings_function = [StringFunctions.STR_LOWER, ] # Each list item corresponds to a content index

        # Defining padding settings for the table
        self.title_left_padding     = 1
        self.title_right_padding    = 1
        self.header_left_paddings   = [1, ] # Each list item corresponds to a header index
        self.header_right_paddings  = [1, ] # Each list item corresponds to a header index
        self.content_left_paddings  = [1, ] # Each list item corresponds to a content index
        self.content_right_paddings = [1, ] # Each list item corresponds to a content index

        # Defining empty borders for better table visualization
        self.upper_title_empty_border_size = 2
        self.lower_title_empty_border_size = 2
        self.upper_header_empty_border_size = 1
        self.lower_header_empty_border_size = 1
        self.upper_content_empty_border_size = 0 
        self.lower_content_empty_border_size = 0 

        # Ensures border character alternation is respected in some TableSymbols
        self.force_alternating_chars_respect = True 

        # Displays the table even if it's broken
        self.force_display = True 

        # Outer margin for the table
        self.margin = 1

        # Enables multiline tables, affecting several configurations
        self.enable_multiline = True


# Defining the data
title = 'PyTabFy README.md Table Example'
headers = ["Header 0", "Header 1", "Header 2"]
contents = [
    ["Content [0][0]", "Content [1][0]", "Content [2][0]"], 
    ["Content [0][1]", "Content [1][1]", "Content [2][1]"], 
    ["Content [0][2]", "Content [1][2]", "Content [2][2]"],
]

data = TableData().set_data_from_list(title=title, headers=headers, contents=contents)

# Defining the table and building it
custom_configs = CustomConfigs()
table = DefaultTable(custom_configs=custom_configs) # NOTE: Using a custom_configs is optional 
table.build(data)
    
# Using different methods on the table
table.display(border_between_content=False)
print('\n\n')

# NOTE: The display_and_select() method prompts the user to select an content starting from 1
selection = table.display_and_select(index=0, border_between_content=True)
print(f"You selected: {selection}")
print('\n\n')

selection = table.display_and_select(select_full_content=True, border_between_content=False)
print(f"You selected: {selection}")
print('\n\n')

table.log_table(file_path=Path().home() / 'table.txt', border_between_content=True)
print('\n\n')
```
