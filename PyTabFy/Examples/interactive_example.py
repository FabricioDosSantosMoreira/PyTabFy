from enum import Enum
from typing import Any

from PyTabFy.PyTUtils import categorize_contents
from PyTabFy.PyTConfigs import TableConfigs
from PyTabFy.PyTCore.Tables import DefaultTable
from PyTabFy.PyTCore.Types import TableData
from PyTabFy.PyTEnums import (
    StringLengthValidation,
    StringSlicingMode, 
    StringFunctions, 
    TableFitMode, 
    TableSymbols,
    Alignment,
)


# TODO: Finish this
def interactive_example() -> None:

    class CustomConfigs(TableConfigs):
        
        def __init__(self) -> None:
            super().__init__()

            self.table_symbols  = TableSymbols.DEFAULT_MIXED
            self.table_fit_mode = TableFitMode.MAX_TABLE_FIT
            
    custom_configs = CustomConfigs()


    def get_enum_value(enum: Enum) -> Any:

        headers = ['Options', 'Enum Values']
        contents = categorize_contents(enum._member_names_)

        data = TableData().set_data(contents=contents, headers=headers)
        option = table.build(data).display_and_select(select_full_content=True)

        enum_name = option[1]
        enum_value = getattr(enum, enum_name)

        return enum_value
    

    while True:
        headers = ['Option', 'Action']
        contents = categorize_contents([
            'Change Table Fit Mode', 
            'Change Table Symbols', 
            'Change String Lenght Validation',
            'Change String Slicing Mode',
            'Change Title String Function',
            'Change Header Strings Function',
            'Change Content Strings Function',
            'Quit',
        ])

        title = 'PyTabFy Interactive Example'

        table = DefaultTable(custom_configs=custom_configs)
        data = TableData().set_data(contents=contents, headers=headers, title=title)
        option = table.build(data).display_and_select()

        if option == '1':
            custom_configs.table_fit_mode = get_enum_value(TableFitMode)
        elif option == '2':
            custom_configs.table_symbols = get_enum_value(TableSymbols)
        elif option == '3':
            custom_configs.str = get_enum_value(StringLengthValidation)
        elif option == '4':
            custom_configs.string_slicing_mode = get_enum_value(StringSlicingMode)
        elif option == '5':
            custom_configs.title_string_function = get_enum_value(StringFunctions)
        elif option == '6':
            custom_configs.header_strings_function = [get_enum_value(StringFunctions)]
        elif option == '7':
            custom_configs.content_strings_function = [get_enum_value(StringFunctions)]
        elif option == '8':
            quit()

if __name__ == '__main__':
    interactive_example()
