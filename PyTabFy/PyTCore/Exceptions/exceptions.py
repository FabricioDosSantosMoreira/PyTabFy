from typing import List, Union


class PyTabFyException(Exception):
    """
    Base exception for all errors in PyTabFy.
    """
    def __init__(self, from_class: str, *args: Union[List[str], str]) -> None:
        super().__init__(*args)

        self.args: Union[List[str], str] = args
        self.from_class: str = from_class


    def __str__(self) -> str:
        args_length: int = len(self.args)

        formatted_string: str = '\033[96m' + f"\n\n\n\n\t■ {self.from_class}:" + '\033[0m'

        # Formats the Exception __str__()
        for i, arg in enumerate(self.args):

            if i + 1 == args_length:
                formatted_string += '\033[96m' + "\n\t│\n\t└─────> "
            else:
                formatted_string += '\033[96m' + "\n\t│\n\t├─────> "
            
            if isinstance(arg, list):
                if i + 1 == args_length:
                    formatted_string += f"\n\t\t".join(arg)
                else:
                    formatted_string += f"\n\t│\t".join(arg)
            else:
                formatted_string += arg 

        return formatted_string + "\n\033[0m"
   

class OversizedTableException(PyTabFyException):

    def __init__(self, *args: Union[List[str], str]) -> None:
        super().__init__(__class__.__name__, *args)


class BuildTableException(PyTabFyException):

    def __init__(self, *args: Union[List[str], str]) -> None:
        super().__init__(__class__.__name__, *args)


class InvalidConfigurationException(PyTabFyException):

    def __init__(self, *args: Union[List[str], str]) -> None:
        super().__init__(__class__.__name__, *args)


class ColumnMismatchException(PyTabFyException):

    def __init__(self, *args: Union[List[str], str]) -> None:
        super().__init__(__class__.__name__, *args)
