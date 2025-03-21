from typing import List, Optional, Union

from PyTabFy.PyTEnums import Alignment
from PyTabFy.PyTConfigs import TableConfigs
from PyTabFy.PyTCore.Types import TableData
from PyTabFy.PyTCore.Tables.Core import BaseTable


class LeftAlignedTable(BaseTable):
    """'LeftAlignedTable' always use 'Alignment.LEFT' as the default Alignment"""

    def __init__(self, custom_configs: Optional[TableConfigs] = None) -> None:
        super().__init__(custom_configs)

        # NOTE: Overrides the default alignment values
        self.configs.title_alignment    = Alignment.LEFT
        self.configs.header_alignments  = [Alignment.LEFT, ]
        self.configs.content_alignments = [Alignment.LEFT, ]
       

    def build(self, /, data: TableData, **kwargs) -> 'BaseTable':
        if kwargs:
            # NOTE: Overrides alignment values
            kwargs['title_alignment']    = Alignment.LEFT
            kwargs['header_alignments']  = [Alignment.LEFT, ]
            kwargs['content_alignments'] = [Alignment.LEFT, ]
            
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
