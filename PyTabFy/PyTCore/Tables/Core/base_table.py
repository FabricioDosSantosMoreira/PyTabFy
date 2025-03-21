from pathlib import Path
from typing import List, Optional, Union


from PyTabFy.PyTCore.Tables.Core import TableLogger, TablePrinter, TableBuilder
from PyTabFy.PyTCore.Exceptions import BuildTableException, PyTabFyException
from PyTabFy.PyTConfigs import TableConfigs
from PyTabFy.PyTCore.Types import TableData


class BaseTable(TableBuilder, TablePrinter, TableLogger):
    """Base implementation of a Table"""

    def __init__(self, custom_configs: Optional[TableConfigs] = None) -> None:
        self.configs: TableConfigs = TableConfigs()
        self.data: TableData = TableData()
        
        # If custom configs are provided and valid, set them
        if custom_configs is not None:
            self._verify_custom_configs(custom_configs)
            self.configs.set_custom_configs(custom_configs)
        else:
            self.configs.set_default_configs()


        self.is_built: bool = False
        TableBuilder.__init__(self, configs=self.configs)
        TablePrinter.__init__(self, configs=self.configs)
        TableLogger.__init__(self, configs=self.configs)


    def _verify_custom_configs(self, custom_configs: TableConfigs) -> None:
        try:
            custom_configs._was_class_initialized
        except AttributeError:
            raise PyTabFyException(
                'Invalid custom_configs instance',
                'Ensure that your custom config class correctly inherits from TableConfigs',
                'Ensure that you are overriding the __init__() method and using super().__init__()', 
                'Please see TableConfigs docs!'
            )


    def _verify_is_table_built(self) -> None:
        if not self.is_built:
            raise BuildTableException(
                "Table wasn't built. Use table.build(data) first."
            )

        return


    def build(self, *, data: TableData) -> 'BaseTable':
        self.data = super().build(data=data)
        self.is_built = True

        return self
    

    def display(self, *, border_between_content: bool) -> None:
        self._verify_is_table_built()
        
        if border_between_content is None:
            border_between_content = False

        return super().display(data=self.data, border_between_content=border_between_content)


    def display_and_select(self, *, 
            index: int, 
            input_msg: str, 
            select_full_content: bool, 
            border_between_content: bool
        ) -> Union[int, str, List[str]]:

        self._verify_is_table_built()
        
        if index is None:
            index = 0
        if input_msg is None:
            input_msg = " " * self.configs.margin + '└─────────────> Insert an option: '
        if select_full_content is None:
            select_full_content = False
        if border_between_content is None:
            border_between_content = False

        return super().display_and_select(
            data=self.data,
            index=index, 
            input_msg=input_msg, 
            select_full_content=select_full_content,
            border_between_content=border_between_content,
        )
    

    def log_table(self, *, file_path: Path, border_between_content: bool) -> None:
        self._verify_is_table_built()
        
        return super().log_table(
            data=self.data, 
            file_path=file_path, 
            border_between_content=border_between_content, 
        )
    