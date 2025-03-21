from pathlib import Path
from typing import List, Optional, Union

from PyTabFy.PyTConfigs import TableConfigs
from PyTabFy.PyTCore.Types import TableData
from PyTabFy.PyTCore.Tables.Core import BaseTable


class DefaultTable(BaseTable):
    """'DefaultTable' is the default implementation of 'BaseTable'"""

    def __init__(self, custom_configs: Optional[TableConfigs] = None) -> None:
        super().__init__(custom_configs)


    def build(self, /, data: TableData, **kwargs) -> 'BaseTable':
        if kwargs:
            self.configs.update_attributes(**kwargs)

        return super().build(data=data)
    

    def display(self, *, border_between_content: Optional[bool] = None) -> None:
        return super().display(border_between_content=border_between_content)
    

    def display_and_select(self, *, 
            index: Optional[int] = None, 
            input_msg: Optional[int] = None, 
            select_full_content: Optional[bool] = None, 
            border_between_content: Optional[bool] = None,
        ) -> Union[int, str, List[str]]:
    
        return super().display_and_select(
            index=index, 
            input_msg=input_msg, 
            select_full_content=select_full_content, 
            border_between_content=border_between_content
        )
    

    def log_table(self, *, file_path: Path, border_between_content: bool, **kwargs) -> None:
        if kwargs:
            self.configs.update_attributes(**kwargs)

        return super().log_table(
            file_path=file_path, 
            border_between_content=border_between_content
        )
