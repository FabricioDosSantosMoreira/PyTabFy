from wcwidth import wcswidth

from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, Union
from PyTabFy.PyTUtils import get_visual_width
from PyTabFy.PyTUtils.validation import validate_obj_type


class TwoCharsList():

    def __init__(self, char_a: str, char_b: Optional[str] = None) -> None:
        if not isinstance(char_a, str) or wcswidth(char_a) != 1:
            raise ValueError("'char_a' must be a single 'str' and it's visual width must be equal to 1!")
        if char_b is not None:
            if not isinstance(char_b, str) or wcswidth(char_b) != 1:
                raise ValueError("'char_b' must be a single 'str' and it's visual width must be equal to 1!")

        self._value: List[str] = [char_a] if char_b is None else [char_a, char_b]
        self._is_alternating_chars: bool = char_b is not None
  

    def is_alternating_chars(self) -> bool:
        """Return whether the list has two alternating characters."""
        return self._is_alternating_chars
    

    def get_chars(self) -> List[str]:
        """Return the list with two characters."""
        return self._value


    def __str__(self) -> str:
        if self.is_alternating_chars():
            return f"['{self._value[0]}', '{self._value[1]}']"
        else:
            return f"['{self._value[0]}', 'None']"
        

    def __repr__(self) -> str:
        return self.__str__()


class Node():

    def __init__(self, value: Any) -> None:
        self.value: Any = value
        self.next: Any = None


class LinkedList():

    def __init__(self) -> None:
        self.head: Any = None
        self.tail: Any = None
        self.size: int = 0


    def insert(self, value: Any) -> None:
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            assert self.tail is not None 
            self.tail.next = new_node
            self.tail = new_node 

        self.size += 1

    
    def len(self) -> int:
        return self.size
    

    def get(self, index):
        if index >= self.size:
            raise IndexError()
        
        if index == -1:
            return self.tail.value

        current = self.head
        for _ in range(index):
            current = current.next
        return current.value


    def set(self, index, value):
        if index < 0 or index >= self.size:
            raise IndexError()

        current = self.head
        for _ in range(index):
            current = current.next
        current.value = value


    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __str__(self):
        return "«" + " -> ".join(str(value) for value in self) + "»"
    





class TableData():

    class TableContentData():

        def __init__(self) -> None:
            self._raw_data: LinkedList[List[str]] = LinkedList()
            self._formatted_data: LinkedList[Tuple[str]] = LinkedList()

            self._max_str_len_of_each_col: List[int] = []
            self._columns: int = 0
 
            self.multiline_block_range: List[int] = []
        
        
        def insert_multiline_block_range(self, n: int) -> None:
            self.multiline_block_range.append(n)


        def set_raw_data(self, contents: Iterable[Iterable[str]]) -> 'TableContentData':
            # Doesn't allow empty contents
            if contents is None:
                raise ValueError('')

            if not isinstance(contents, (list, tuple)):
                raise ValueError("Contents must be a 'List' or 'Tuple' type!")
            
            for idx, row in enumerate(self._raw_data):
                if not all(isinstance(cell, str) for cell in row):
                    raise ValueError(f"All elements in row {idx} must be of type 'str'!")

            
            self._raw_data = LinkedList()
            for content_row in contents:
                if content_row is None:
                    raise ValueError('')
                
                self._raw_data.insert(content_row)
        
            self._columns = len(contents[0] if contents else [])
            self._max_str_len_of_each_col = [0 for _ in range(self._columns)]

            return self
        

        def insert_formatted_content_row_data(self, formatted_content_row: Tuple[str]) -> None:
            self._formatted_data.insert(formatted_content_row)

            col_idx: int = 0
            for string in formatted_content_row:
                visual_width = get_visual_width(string)

                if visual_width > self._max_str_len_of_each_col[col_idx]:
                    self._max_str_len_of_each_col[col_idx] = visual_width

                col_idx += 1


        def __iter__(self) -> Generator[List[str], None, None]:
            if self._raw_data:
                yield from self._raw_data


        def _show(self) -> None:
            print(self._raw_data)
            print(self._columns)
            print(self._max_str_len_of_each_col)


        def has_formatted_data(self) -> bool:
            return True if self._formatted_data.size > 0 else False


    class TableHeaderData():

        def __init__(self) -> None:
            self._raw_data = LinkedList()
            self._formatted_data: LinkedList[str] = LinkedList()

            self._max_str_len_of_each_col: List[int] = []
            self._columns: int = 0


        def set_raw_data(self, data: Iterable[str]) -> None:
            
            validate_obj_type(
                obj=data, 
                obj_type=(list, tuple), 
                obj_name='headers', 
                nullable=True, # Allow empty title
            )

            for inner_data in data:
                validate_obj_type(
                    obj=inner_data, 
                    obj_type=str, 
                    obj_name='headers', 
                    nullable=True,
                ) 

            if data is not None:
                self._raw_data.insert(data)

                self._columns = len(data)
                self._max_str_len_of_each_col = [0 for _ in range(self._columns)]

                # If this happens the headers is an empty iterable.
                # FIXME: Raise an error
                if self._columns == 0:
                    raise ValueError('')




        def insert_formatted_header_row_data(self, formatted_header_row: Tuple[str]) -> None:
            self._formatted_data.insert(formatted_header_row)

            col_idx: int = 0
            
            for string in formatted_header_row:
                visual_width = get_visual_width(string)

                if visual_width > self._max_str_len_of_each_col[col_idx]:
                    self._max_str_len_of_each_col[col_idx] = visual_width        

                col_idx += 1


        def __iter__(self) -> Generator[List[str], None, None]:
            if self._raw_data:
                yield from self._raw_data


        def _show(self) -> None:
            print(self._raw_data)
            print(self._columns)
            print(self._max_str_len_of_each_col)

        
        def has_formatted_data(self) -> bool:
            return True if self._formatted_data.size > 0 else False


    class TableTitleData():

        def __init__(self) -> None:
            self._raw_data: str = None
            self._formatted_data: LinkedList[str] = LinkedList()
            
            self.max_str_len: int = 0


        def set_raw_title_data(self, data: str) -> None:
            validate_obj_type(
                obj=data, 
                obj_type=str, 
                obj_name='title', 
                nullable=True,  # Allow empty title
            )

            self._raw_data = data


        def insert_formatted_title_row_data(self, data: str) -> None:
            self._formatted_data.insert(data)

            visual_width = get_visual_width(data)
            if visual_width > self.max_str_len:
                self.max_str_len = visual_width

        
        def has_raw_data(self) -> bool:
            if self._raw_data is None and not self.raw_data_is_empty_string():
                return False
            return True
        

        def raw_data_is_empty_string(self) -> bool:
            if self._raw_data == '':
                return True
            return False


        def has_formatted_data(self) -> bool:
            return True if self._formatted_data.size > 0 else False
        

        def iter_formatted_data(self) -> Generator[str, None, None]:
            yield from self._formatted_data


    def __init__(self) -> None:

        # Unbuilt Table Data
        self.table_title_data = self.TableTitleData()
        self.table_header_data  = self.TableHeaderData()
        self.table_content_data = self.TableContentData()

        # Built Table Data Info
        self._built_data: Dict[str, Any] = {
            'built_table_title':                    [],
            'built_table_header':                   [],
            'built_table_contents':                 [],
            'built_table_title_border':             None,
            'built_table_header_border':            None,
            'built_table_contents_upper_border':    None,
            'built_table_contents_lower_border':    None,
            'built_table_contents_middle_border':   None,
            'built_table_empty_border_with_div':    None,
            'built_table_empty_border_without_div': None,
        }
    
        # Built Table Info
        self.is_title_built:    bool = False
        self.is_header_built:   bool = False
        self.is_contents_built: bool = False

        self.MAIN_KEYS: List[str] = [
            'built_table_title',
            'built_table_header',
            'built_table_contents',
        ]


    def set_data_from_list(self, *, 
            title: Optional[str], 
            headers: Optional[List[str]], 
            contents: Optional[List[List[str]]]
        ) -> 'TableData':
        
        self.table_title_data.set_raw_title_data(title)
        self.table_header_data.set_raw_data(headers)
        self.table_content_data.set_raw_data(contents)

        return self


    def set_built_data(self, key: str, value: str) -> None:

        if key in self.MAIN_KEYS:
            self._built_data[key].append(value)
        else:
            self._built_data[key] = value

    def get_built_data(self, key: str) -> Optional[Union[str, List[str], List[List[str]]]]:
        return self._built_data.get(key)
 