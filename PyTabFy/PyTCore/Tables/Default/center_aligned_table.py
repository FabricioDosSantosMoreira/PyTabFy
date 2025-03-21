from typing import List, Optional, Union

from PyTabFy.PyTEnums import Alignment
from PyTabFy.PyTConfigs import TableConfigs
from PyTabFy.PyTCore.Types import TableData
from PyTabFy.PyTCore.Tables.Core import BaseTable


class CenterAlignedTable(BaseTable):
    """'CenterAlignedTable' always use 'Alignment.CENTER' as the default Alignment"""

    def __init__(self, custom_configs: Optional[TableConfigs] = None) -> None:
        super().__init__(custom_configs)

        # NOTE: Overrides the default alignment values
        self.configs.title_alignment    = Alignment.CENTER
        self.configs.header_alignments  = [Alignment.CENTER, ]
        self.configs.content_alignments = [Alignment.CENTER, ]
        

    def build(self, /, data: TableData, **kwargs) -> 'BaseTable':
        if kwargs:
            # NOTE: Overrides alignment values
            kwargs['title_alignment']    = Alignment.CENTER
            kwargs['header_alignments']  = [Alignment.CENTER, ]
            kwargs['content_alignments'] = [Alignment.CENTER, ]
            
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
