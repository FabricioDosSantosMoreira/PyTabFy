from pathlib import Path

from PyTabFy.PyTCore.Types import TableData
from PyTabFy.PyTConfigs import TableConfigs


class TableLogger():

    def __init__(self, configs: TableConfigs) -> None:
        self.configs = configs


    def log_table(self, *, data: TableData, file_path: Path, border_between_content: bool) -> None:

        if not file_path.is_absolute():
            raise FileNotFoundError('Invalid file_path to TableLogger(). Not absolute')
        
        if not file_path.name:
            raise FileNotFoundError('Invalid file_path to TableLogger(). Missing name')
        
        if not file_path.suffix:
            raise FileNotFoundError('Invalid file_path to TableLogger(). Missing suffix')
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with file_path.open('w', encoding='utf-8') as txt:
            
            txt.write("NOTE:\n")
            txt.write("\t-> If your table is misaligned or broke:\n")
            txt.write("\t\t-> Consider using either `MS Gothic with regular style` or `M Plus Code 1 with regular styles` as font\n")
            txt.write("\t\t-> Consider using notepad++ to open the table. ('Don't forget to change fonts')\n")
            txt.write('\t\t-> You can try different monospaced fonts and programs!\n\n')

            txt.write('\t-> There are a few limitations with non-ascii chars for the log table\n')
            txt.write('\tPlease consider reporting any errors.\n\n')

            # Writes the built title
            if data.is_title_built:
                txt.write(data.get_built_data('built_table_title_border') + '\n')
                [txt.write(data.get_built_data('built_table_empty_border_without_div') + '\n') for _ in range(self.configs.upper_title_empty_border_size)]
                for string in data.get_built_data('built_table_title'):
                    txt.write(string + '\n')
                [txt.write(data.get_built_data('built_table_empty_border_without_div') + '\n') for _ in range(self.configs.lower_title_empty_border_size)]

            # Writes the built header
            if data.is_header_built:
                txt.write(data.get_built_data('built_table_header_border') + '\n')
                [txt.write(data.get_built_data('built_table_empty_border_with_div') + '\n') for _ in range(self.configs.upper_header_empty_border_size)]
                for string in data.get_built_data('built_table_header'):
                    txt.write(string + '\n')
                [txt.write(data.get_built_data('built_table_empty_border_with_div') + '\n') for _ in range(self.configs.lower_header_empty_border_size)]

            # Writes the built contents
            if data.is_contents_built is not None:
                txt.write(data.get_built_data('built_table_contents_upper_border') + '\n')

                built_contents_len = len(data.get_built_data('built_table_contents')) 

                block_count = 0
                for block in (data.table_content_data.multiline_block_range):
                    [txt.write(data.get_built_data('built_table_empty_border_with_div') + '\n') for _ in range(self.configs.upper_content_empty_border_size)]
                    
                    for i in range(block_count, block + block_count):
                        txt.write(data.get_built_data('built_table_contents')[i] + '\n') 
                    
                    [txt.write(data.get_built_data('built_table_empty_border_with_div') + '\n') for _ in range(self.configs.lower_content_empty_border_size)]

                    block_count += block

                    if border_between_content and block_count <= built_contents_len - 1:
                        txt.write(data.get_built_data('built_table_contents_middle_border') + '\n')

                txt.write(data.get_built_data('built_table_contents_lower_border') + '\n')

            print(f'Table saved in: {file_path}')
