import os

from typing import Callable, List, Tuple
from itertools import zip_longest
from wcwidth import wcswidth

from PyTabFy.PyTEnums import Alignment, StringFunctions, TableFitMode, StringSlicingMode, StringLengthValidation
from PyTabFy.PyTCore.Types import TableData
from PyTabFy.PyTCore.Exceptions import OversizedTableException
from PyTabFy.PyTConfigs import TableConfigs
from PyTabFy.PyTCore.Warnings import InvalidDataWarning, WarningLevel
from PyTabFy.PyTUtils import (
    get_item_from_idx_or_zero,
    get_item_from_obj_at_idx, 
    reduce_strings_length, 
    reduce_string_length, 
    get_visual_width,
    match_parity, 
    
)


class TableBuilder():

    def __init__(self, configs: TableConfigs) -> None:
        self.configs = configs

        # 'TableBuilder' Attributes
        self.columns_width:                    List[int]
        self.max_columns_width:                List[int]
        self.max_columns_left_padding_values:  List[int] 
        self.max_columns_right_padding_values: List[int]


    def build(self, *, data: TableData) -> TableData:
        slicing_mode: StringSlicingMode= self.configs.string_slicing_mode
        length_validation: StringLengthValidation = self.configs.string_lenght_validation

        if not self.configs.enable_multiline:

            # Reduce the title string with the specified config
            if data.table_title_data.has_raw_data():

                if data.table_title_data.raw_data_is_empty_string():
                    formatted_title = (' ', )

                formatted_title = reduce_string_length(
                    string=data.table_title_data._raw_data,
                    delimiter=self.configs.title_delimiter,
                    length=self.configs.max_title_string_lenght,
                    slicing_mode=self.configs.string_slicing_mode,
                    length_validation=self.configs.string_lenght_validation,
                )

                data.table_title_data.insert_formatted_title_row_data(formatted_title)
        

            # Reduce all header strings with the specified config
            max_lengths: List[int] = self.configs.max_header_strings_lenght
            delimiters: List[str] = self.configs.headers_delimiters

            if data.table_header_data is not None:
                for header_row in data.table_header_data.__iter__():

                    formatted_header_row = reduce_strings_length(
                        strings=header_row,
                        lengths=max_lengths,
                        delimiters=delimiters,
                        slicing_mode=slicing_mode,
                        length_validation=length_validation,
                        string_replacement_if_none=self.configs.headers_null_str_replacement,
                    )
                
                    data.table_header_data.insert_formatted_header_row_data(formatted_header_row)
                    
            # Reduce all content strings with the specified config
            max_lengths: List[int] = self.configs.max_content_strings_lenght
            delimiters: List[str] = self.configs.contents_delimiters

            if data.table_content_data._raw_data is not None:
                for content_row in data.table_content_data.__iter__():

                    formatted_content_row = reduce_strings_length(
                        strings=content_row,
                        lengths=max_lengths,
                        delimiters=delimiters,
                        slicing_mode=slicing_mode,
                        length_validation=length_validation,
                        string_replacement_if_none=self.configs.contents_null_str_replacement,                        
                    )

                    data.table_content_data.insert_formatted_content_row_data(formatted_content_row)
                    data.table_content_data.insert_multiline_block_range(1)

        else: # Handle a multilines table
            
            # Formats the title
            if data.table_title_data.has_raw_data():
                
                if data.table_title_data.raw_data_is_empty_string():
                    formatted_title = (' ', )

                else: 
                    formatted_title: Tuple[str] = tuple(
                        self.configs.string_break_mode.break_string(
                            string=data.table_title_data._raw_data if data.table_title_data._raw_data else ' ',
                            max_str_size=self.configs.max_title_string_lenght,
                            length_validation=self.configs.string_lenght_validation,
                        )
                    )   

                for string in formatted_title:
                    data.table_title_data.insert_formatted_title_row_data(string)
        

            # Formats the headers
            if data.table_header_data._raw_data is not None:
                for header_row in data.table_header_data.__iter__():

                    formatted_header_row = tuple(
                        self.configs.string_break_mode.break_string(
                            string if string else self.configs.headers_null_str_replacement, 
                            get_item_from_obj_at_idx(self.configs.max_header_strings_lenght, col_idx), 
                            self.configs.string_lenght_validation
                        )
                        for col_idx, string in enumerate(header_row)
                    )

                    transposed_rows = list(zip_longest(*formatted_header_row, fillvalue=''))
                    for transposed_row in transposed_rows:
                        data.table_header_data.insert_formatted_header_row_data(transposed_row)


            # Formats the contents
            if data.table_content_data._raw_data is not None:
                for content_row in data.table_content_data.__iter__():

                    formatted_content_row = tuple(
                        self.configs.string_break_mode.break_string(
                            string if string else self.configs.contents_null_str_replacement, 
                            get_item_from_obj_at_idx(self.configs.max_content_strings_lenght, col_idx), 
                            self.configs.string_lenght_validation
                        )
                        for col_idx, string in enumerate(content_row)
                    )

                    transposed_rows = list(zip_longest(*formatted_content_row, fillvalue=''))
                    for transposed_row in transposed_rows:
                        data.table_content_data.insert_formatted_content_row_data(transposed_row)

                    data.table_content_data.insert_multiline_block_range(len(transposed_rows))


        # The number of columns in the table
        headers_n_cols = data.table_header_data._columns
        contents_n_cols = data.table_content_data._columns
        if headers_n_cols > contents_n_cols:
            n_columns = headers_n_cols
        else:
            n_columns = contents_n_cols

        if headers_n_cols != contents_n_cols:
            _from = 'headers' if headers_n_cols > contents_n_cols else 'contents'
            _dif = 'headers' if headers_n_cols < contents_n_cols else 'contents'
            InvalidDataWarning(
                f'The number of columns inside {_from} are different from {_dif}. This will lead to unexpected bugs.', 
                WarningLevel.WARNING
            )


        self._eval_and_set_max_columns_padding_values(n_columns=n_columns)
        self._eval_and_set_max_columns_width(
            n_columns=n_columns,
            max_title_str_len=data.table_title_data.max_str_len,
            max_header_str_len_for_each_col=data.table_header_data._max_str_len_of_each_col,
            max_content_str_len_for_each_col=data.table_content_data._max_str_len_of_each_col,
        )
        self._eval_and_set_columns_width()
        self.table_width = sum(self.columns_width)


        # If the title is provided, build it
        if data.table_title_data.has_formatted_data():

            # Builds all title rows
            for title_row in data.table_title_data.iter_formatted_data():
                data.set_built_data(
                    'built_table_title',
                    self._build_table_title(title=title_row, table_width=self.table_width),
                )

            # Builds the title border
            built_title_border = self._build_table_border(
                margin=self.configs.margin,
                left_symbol=self.configs.table_symbols.get_value('TITLE_LEFT'),
                right_symbol=self.configs.table_symbols.get_value('TITLE_RIGHT'),
                center_symbol=self.configs.table_symbols.get_value('TITLE_CENTER'),
                chars_symbols=self.configs.table_symbols.get_value('CHARS'),
                column_widths=self.columns_width,
            )

            data.is_title_built = True
            data.set_built_data('built_table_title_border', built_title_border)


        # If the headers are provided, build it.
        if data.table_header_data.has_formatted_data():

            # Builds all headers rows
            for header_row in data.table_header_data._formatted_data:
                data.set_built_data(
                    'built_table_header',
                    self._build_table_header(headers=header_row, column_widths=self.columns_width)
                )
            
            # Builds the header border
            built_header_border = self._build_table_border(
                margin=self.configs.margin,
                left_symbol=self.configs.table_symbols.get_value('HEADER_LEFT'),
                right_symbol=self.configs.table_symbols.get_value('HEADER_RIGHT'),
                center_symbol=self.configs.table_symbols.get_value('HEADER_CENTER'),
                chars_symbols=self.configs.table_symbols.get_value('CHARS'),
                column_widths=self.columns_width
            )

            data.is_header_built = True
            data.set_built_data('built_table_header_border', built_header_border)


        # If the contents are provided, build it.
        if data.table_content_data.has_formatted_data():
            
            # Builds all contents rows
            for content_row in data.table_content_data._formatted_data:
                data.set_built_data(
                    'built_table_contents',
                    self._build_table_content(contents=content_row, column_widths=self.columns_width)
                )

            # Builds the upper contents border
            built_contents_upper_border = self._build_table_border(
                margin=self.configs.margin,
                left_symbol=self.configs.table_symbols.get_value('CONTENT_UPPER_LEFT'),
                right_symbol=self.configs.table_symbols.get_value('CONTENT_UPPER_RIGHT'),
                center_symbol=self.configs.table_symbols.get_value('CONTENT_UPPER_CENTER'),
                chars_symbols=self.configs.table_symbols.get_value('CHARS'),
                column_widths=self.columns_width
            )
            # Builds the lower contents border
            built_contents_lower_border = self._build_table_border(
                margin=self.configs.margin,
                left_symbol=self.configs.table_symbols.get_value('CONTENT_LOWER_LEFT'),
                right_symbol=self.configs.table_symbols.get_value('CONTENT_LOWER_RIGHT'),
                center_symbol=self.configs.table_symbols.get_value('CONTENT_LOWER_CENTER'),
                chars_symbols=self.configs.table_symbols.get_value('CHARS'),
                column_widths=self.columns_width
            )
            # Builds the middle contents border
            built_contents_middle_border = self._build_table_border(
                margin=self.configs.margin,
                left_symbol=self.configs.table_symbols.get_value('CONTENT_MIDDLE_LEFT'),
                right_symbol=self.configs.table_symbols.get_value('CONTENT_MIDDLE_RIGHT'),
                center_symbol=self.configs.table_symbols.get_value('CONTENT_MIDDLE_CENTER'),
                chars_symbols=self.configs.table_symbols.get_value('CHARS'),
                column_widths=self.columns_width
            )

            data.is_contents_built = True
            data.set_built_data('built_table_contents_upper_border', built_contents_upper_border)
            data.set_built_data('built_table_contents_lower_border', built_contents_lower_border)
            data.set_built_data('built_table_contents_middle_border', built_contents_middle_border)
        
        # Builds and set empty border with and without dividers
        data.set_built_data(
            'built_table_empty_border_with_div', 
            self._build_empty_border(self.configs.margin, True, self.columns_width)
        )
        data.set_built_data(
            'built_table_empty_border_without_div', 
            self._build_empty_border(self.configs.margin, False, self.columns_width)
        )

        return data
        

    def _eval_and_set_columns_width(self) -> None:
        assigned_columns_sizes: List[int] = [0] * len(self.max_columns_width)
        for idx in range(len(self.max_columns_width)):

            left_padding_val = get_item_from_obj_at_idx(obj=self.max_columns_left_padding_values, idx=idx)
            right_padding_val = get_item_from_obj_at_idx(obj=self.max_columns_right_padding_values, idx=idx)

            assigned_columns_sizes[idx] = self.max_columns_width[idx] + left_padding_val + right_padding_val + 1

        
        if self.configs.table_fit_mode == TableFitMode.MAX_TABLE_FIT:

            rest = self.configs.max_table_size - sum(assigned_columns_sizes[:-1])

            if rest < assigned_columns_sizes[-1]:
                print("WARNING - - -> The value ['self.max_table_size'] is too small to create a table with these headers and contents!")
                print("WARNING - - -> The value ['self.max_table_size'] wasn't used!")
            else:
                assigned_columns_sizes[-1] = rest
        
        elif self.configs.table_fit_mode == TableFitMode.MIN_TABLE_FIT:

            rest = self.configs.min_table_size - sum(assigned_columns_sizes[:-1])

            if rest < assigned_columns_sizes[-1]:
                print("WARNING - - -> The value ['self.min_table_size'] is too small to create a table with these headers and contents!")
                print("WARNING - - -> The value ['self.min_table_size'] wasn't used!")
            
            elif self.configs.min_table_size > sum(assigned_columns_sizes):
                assigned_columns_sizes[-1] = rest
                
        elif self.configs.table_fit_mode == TableFitMode.DYNAMIC_TABLE_FIT:
            pass # Fit the table

        
        if self.configs.force_alternating_chars_respect:
            for i in range(len(assigned_columns_sizes)):
                assigned_columns_sizes[i] = match_parity(value=assigned_columns_sizes[i], target_parity="even", decrease=False)

        if not self.configs.force_display:

            try:
                col, _ = os.get_terminal_size()
            except OSError:
                col = 1000

            if sum(assigned_columns_sizes) + self.configs.margin + 1 > col:
                raise OversizedTableException(
                    "The table is too big.",
                    [
                        "You should try: ", 
                        "Expand your terminal tab",
                        "reduce 'max_table_size'", 
                        "reduce all paddings values", 
                        "reduce 'margin'", 
                        "set 'enable_multiline' to True",
                    ],
                    "If none of the above fix the issue, you should increase you terminal size or set 'force_display' to True."
                )
        
        self.columns_width = assigned_columns_sizes


    def _eval_and_set_max_columns_width(self, *, 
            n_columns: int,
            max_title_str_len: int,
            max_header_str_len_for_each_col: List[int],
            max_content_str_len_for_each_col: List[int],
        ) -> None:
        
        max_columns_width: List[int] = []

        for i in range(n_columns):
            max_columns_width.append(
                max(
                    get_item_from_idx_or_zero(max_header_str_len_for_each_col, i), 
                    get_item_from_idx_or_zero(max_content_str_len_for_each_col, i),
                )
            )

        if max_title_str_len > 0:
            # FIXME: Fix the title being out of the table issue in some cases
            # FIXME: Enable multiline to Title
            title_len = max_title_str_len

            if title_len > sum(max_columns_width):
                max_columns_width[-1] = title_len - sum(max_columns_width[0: -1])
            
            # Fix title being out of the table when title_left_padding > title_right_padding
            elif self.configs.title_left_padding > sum(max_columns_width):
                rest = self.configs.title_left_padding - sum(max_columns_width[0: -1])
                max_columns_width[-1] += rest + self.configs.title_right_padding

                # NOTE: Test
                if self.configs.force_alternating_chars_respect:
                    current_parity = "even" if sum(max_columns_width) % 2 == 0 else "odd"
                    max_columns_width[-1] = match_parity(value=max_columns_width[-1], target_parity=current_parity, decrease=False) 
                else:
                    current_parity = "even" if sum(max_columns_width) % 2 == 0 else "odd"
                    max_columns_width[-1] = match_parity(value=max_columns_width[-1], target_parity=current_parity, decrease=False) + 1

        self.max_columns_width = max_columns_width


    def _eval_and_set_max_columns_padding_values(self, n_columns: int) -> None:
        _max_left_paddings: List[int] = []
        _max_right_paddings: List[int] = []
 
        for idx in range(n_columns):
            header_left_padding = get_item_from_obj_at_idx(self.configs.header_left_paddings, idx)
            header_right_padding = get_item_from_obj_at_idx(self.configs.header_right_paddings, idx)
            content_left_padding = get_item_from_obj_at_idx(self.configs.content_left_paddings, idx)
            content_right_padding = get_item_from_obj_at_idx(self.configs.content_right_paddings, idx)

            if header_left_padding > content_left_padding:
                _max_left_paddings.append(header_left_padding)
            else: 
                _max_left_paddings.append(content_left_padding)

            if header_right_padding > content_right_padding:
                _max_right_paddings.append(header_right_padding)
            else: 
                _max_right_paddings.append(content_right_padding)

        self.max_columns_left_padding_values = _max_left_paddings
        self.max_columns_right_padding_values = _max_right_paddings


    def _build_empty_border(self, margin: int, keep_columns: bool, columns_width: List[int]) -> str:
        built_empty_border: str = ' ' * margin

        div: str = self.configs.table_symbols.get_value('DIV')
        if keep_columns:
            built_empty_border += div + div.join(' ' * (width - 1) for width in columns_width) + div
        else:
            built_empty_border += div + ' ' * (sum(columns_width) - 1) + div

        return built_empty_border


    def _build_table_border(self, 
            margin: int, 
            left_symbol: str,
            right_symbol: str,
            center_symbol: str,
            chars_symbols: List[str],
            column_widths: List[int], 
        ) -> str:
        
        def get_char(index: int) -> str:
            return get_item_from_obj_at_idx(
                obj=chars_symbols,
                idx=index,
            )
 
        table_border: str = ' ' * margin + left_symbol
        for width in column_widths:
            for n in range(width - 1): 
                table_border += get_char(n % 2)

            table_border += center_symbol if center_symbol else get_char(n + 1 % 2)
        
        table_border = table_border[0: -1]
        table_border += right_symbol

        return table_border
    

    def _build_table_title(self, title: str, table_width: int) -> str:

        table_title: str = ' ' * self.configs.margin + self.configs.table_symbols.get_value('DIV')
  
        table_title += self._format_string(
            string=title,
            col_width=table_width,
            left_padding=self.configs.title_left_padding,
            right_padding=self.configs.title_right_padding,
            alignment=self.configs.title_alignment,
            func=self.configs.title_string_function
        )

        table_title += self.configs.table_symbols.get_value('DIV')

        return table_title


    def _build_table_header(self, headers: List[str], column_widths: List[int]) -> str:
        table_headers: str = ' ' * self.configs.margin + self.configs.table_symbols.get_value('DIV')
        
        for idx, string in enumerate(headers):
            func: Callable[[str], str] = get_item_from_obj_at_idx(
                obj=self.configs.header_strings_function, 
                idx=idx,
            )
            
            visual_width: int = get_visual_width(string)
            rest_of_visual_width: int = 0
            if visual_width != len(string):
                rest_of_visual_width = visual_width - len(string)
            

            col_width: int = column_widths[idx] - rest_of_visual_width
            left_padding: int = get_item_from_obj_at_idx(obj=self.configs.header_left_paddings, idx=idx)
            right_padding: int = get_item_from_obj_at_idx(obj=self.configs.header_right_paddings, idx=idx)
            alignment: Alignment = get_item_from_obj_at_idx(obj=self.configs.header_alignments, idx=idx)

            table_headers += self._format_string(
                string=string, 
                col_width=col_width,
                left_padding=left_padding,
                right_padding=right_padding,
                alignment=alignment,
                func=func,
            )

            table_headers += self.configs.table_symbols.get_value('DIV')

        return table_headers
    

    def _build_table_content(self, contents: List[str], column_widths: List[int]) -> List[str]:
        table_content: str = ' ' * self.configs.margin + self.configs.table_symbols.get_value('DIV')

        for idx, string in enumerate(contents):
            
            func: Callable[[str], str] = get_item_from_obj_at_idx(
                obj=self.configs.content_strings_function, 
                idx=idx,
            )

            visual_width: int = get_visual_width(string)
            rest_of_visual_width: int = 0
            if visual_width != len(string):
                rest_of_visual_width = visual_width - len(string)
        

            col_width: int = column_widths[idx] - rest_of_visual_width
            left_padding: int = get_item_from_obj_at_idx(obj=self.configs.content_left_paddings, idx=idx)
            right_padding: int = get_item_from_obj_at_idx(obj=self.configs.content_right_paddings, idx=idx)
            alignment: Alignment = get_item_from_obj_at_idx(obj=self.configs.content_alignments, idx=idx)

            table_content += self._format_string(
                string=string, 
                col_width=col_width,
                left_padding=left_padding,
                right_padding=right_padding,
                alignment=alignment,
                func=func,
            )

            table_content += self.configs.table_symbols.get_value('DIV')
                
        return table_content
        

    def _format_string(
            self,
            string: str,
            col_width: int,
            left_padding: int,
            right_padding: int,
            alignment: Alignment,
            func: StringFunctions,
        ) -> str:

        # Apply a function to the string
        if func is not None:
            string = func.apply(string)

        # Adjust width removing paddings values
        col_width -= (1 + left_padding + right_padding)  
        
        if alignment == Alignment.LEFT:
            string = string.ljust(col_width)
        elif alignment == Alignment.RIGHT:
            string = string.rjust(col_width)
        elif alignment == Alignment.CENTER:
            string = string.center(col_width) 
        
        formated_string = (' ' * left_padding) + string + (' ' * right_padding)
        return formated_string
