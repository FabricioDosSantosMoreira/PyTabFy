from typing import List, Optional, Union

from PyTabFy.PyTUtils import read_int
from PyTabFy.PyTConfigs import TableConfigs
from PyTabFy.PyTCore.Types import TableData


class TablePrinter():

    def __init__(self, configs: TableConfigs) -> None:
        self.configs = configs


    def display(self, *, data: TableData, border_between_content: Optional[bool] = False) -> None:
        # Displays the built title
        if data.is_title_built:
            print(data.get_built_data('built_table_title_border'))
            [print(data.get_built_data('built_table_empty_border_without_div')) for _ in range(self.configs.upper_title_empty_border_size)]
            for string in data.get_built_data('built_table_title'):
                print(string)
            [print(data.get_built_data('built_table_empty_border_without_div')) for _ in range(self.configs.lower_title_empty_border_size)]


        # Displays the built header
        if data.is_header_built:
            print(data.get_built_data('built_table_header_border'))
            [print(data.get_built_data('built_table_empty_border_with_div')) for _ in range(self.configs.upper_header_empty_border_size)]
            for string in data.get_built_data('built_table_header'):
                print(string)
            [print(data.get_built_data('built_table_empty_border_with_div')) for _ in range(self.configs.lower_header_empty_border_size)]

        # Displays the built contents
        if data.is_contents_built:
            print(data.get_built_data('built_table_contents_upper_border'))

            built_contents_len = len(data.get_built_data('built_table_contents'))

            block_count = 0
            for block in (data.table_content_data.multiline_block_range):
                [print(data.get_built_data('built_table_empty_border_with_div')) for _ in range(self.configs.upper_content_empty_border_size)]
                
                for i in range(block_count, block + block_count):
                    print(data.get_built_data('built_table_contents')[i]) 
                
                [print(data.get_built_data('built_table_empty_border_with_div')) for _ in range(self.configs.lower_content_empty_border_size)]

                block_count += block

                if border_between_content and block_count <= built_contents_len - 1:
                    print(data.get_built_data('built_table_contents_middle_border'))

            print(data.get_built_data('built_table_contents_lower_border'))

        return
            

    def display_and_select(self, *, 
            data: TableData,
            index: int,
            input_msg: str,
            select_full_content: bool,
            border_between_content: bool,
        ) -> Union[List[str], str, int]:

        while True:
            self.display(border_between_content=border_between_content)

            selection = read_int(msg=input_msg)
            if selection == -1:  # Exception from 'read_int()', return -1.
                return -1
            
            # Return a string based on the selected content and its 'index'.
            if data.table_content_data._raw_data.size > (selection - 1) >= 0: 
                if index >= data.table_content_data._columns:
                    # If index is greater than the table column we set to the last column
                    index = -1

                if select_full_content is True:
                    return data.table_content_data._raw_data.get(selection - 1)
                else:
                    return str(data.table_content_data._raw_data.get(selection - 1)[index])            
            else:
                print("\nWarning - - -> Selection wasn't valid. Please, Try again.")
