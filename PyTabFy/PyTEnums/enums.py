import sys

from enum import Enum
from typing import Any, List, Optional, TypedDict
from wcwidth import wcswidth, wcwidth

from PyTabFy.PyTCore.Types import TwoCharsList


class Alignment(Enum):
    """An Enum for Aligment"""
    
    CENTER: str = 'CENTER'
    RIGHT:  str = 'RIGHT'
    LEFT:   str = 'LEFT'

    def __str__(self) -> str:
        return f"{self.__class__.__name__}.{self.name} = {self.value}"

    def __repr__(self) -> str:
        return self.__str__()
        
    
class TableFitMode(Enum):
    """An Enum for Table Fit Mode"""

    DYNAMIC_TABLE_FIT: str = 'DYNAMIC_TABLE_FIT'
    MAX_TABLE_FIT:     str = 'MAX_TABLE_FIT'
    MIN_TABLE_FIT:     str = 'MIN_TABLE_FIT'

    def __str__(self) -> str:
        return f"{self.__class__.__name__}.{self.name} = {self.value}"

    def __repr__(self) -> str:
        return self.__str__()


class TableSymbols(Enum):
    """An Enum for Table Symbols"""

    class SymbolsDict(TypedDict):
        """A TypedDict for 'TableSymbols' values"""

        # NOTE: Table Border Symbols
        CHARS: TwoCharsList
        DIV:    str  
        LEFT:   str  
        RIGHT:  str  
        CENTER: str  

        # Title Border Symbols
        TITLE_LEFT:   str
        TITLE_RIGHT:  str
        TITLE_CENTER: str

        # Header Border Symbols
        HEADER_LEFT:   str
        HEADER_RIGHT:  str
        HEADER_CENTER: str

        # Content Border Symbols
        CONTENT_UPPER_LEFT:    str
        CONTENT_UPPER_RIGHT:   str
        CONTENT_UPPER_CENTER:  str
        CONTENT_LOWER_LEFT:    str
        CONTENT_LOWER_RIGHT:   str
        CONTENT_LOWER_CENTER:  str
        CONTENT_MIDDLE_LEFT:   str
        CONTENT_MIDDLE_RIGHT:  str
        CONTENT_MIDDLE_CENTER: str

    # NOTE: Avaliable Basic Table Symbols
    DEFAULT_MIXED: SymbolsDict = {'CHARS': TwoCharsList('-', '='),  'DIV': '|', 'LEFT': '+', 'RIGHT': '+', 'CENTER': '+', 'TITLE_CENTER': None}
    DEFAULT_EQUAL: SymbolsDict = {'CHARS': TwoCharsList('=', None), 'DIV': '|', 'LEFT': '+', 'RIGHT': '+', 'CENTER': '+', 'TITLE_CENTER': None}
    DEFAULT_DASH:  SymbolsDict = {'CHARS': TwoCharsList('-', None), 'DIV': '|', 'LEFT': '+', 'RIGHT': '+', 'CENTER': '+', 'TITLE_CENTER': None}
    DEFAULT_DOT:   SymbolsDict = {'CHARS': TwoCharsList('-', None), 'DIV': '|', 'LEFT': '•', 'RIGHT': '•', 'CENTER': '•', 'TITLE_CENTER': None}
    MIXED_BOX:     SymbolsDict = {'CHARS': TwoCharsList('─', '━') , 'DIV': '│', 'LEFT': '┼', 'RIGHT': '┼', 'CENTER': '┼', 'TITLE_CENTER': None}
    LIGHT_BOX:     SymbolsDict = {'CHARS': TwoCharsList('─', None), 'DIV': '│', 'LEFT': '┼', 'RIGHT': '┼', 'CENTER': '┼', 'TITLE_CENTER': None}
    HEAVY_BOX:     SymbolsDict = {'CHARS': TwoCharsList('━', None), 'DIV': '┃', 'LEFT': '╬', 'RIGHT': '╬', 'CENTER': '╬', 'TITLE_CENTER': None}
    
    # NOTE: Avaliable Advanced Table Symbols
    DEFAULT_CLI:   SymbolsDict = {
        'CHARS': TwoCharsList('─', None),
        'DIV': '│',

        'TITLE_LEFT':          '┌', 'TITLE_CENTER':         None, 'TITLE_RIGHT':          '┐',
        'HEADER_LEFT':         '├', 'HEADER_CENTER':         '┬', 'HEADER_RIGHT':         '┤', 
        'CONTENT_UPPER_LEFT':  '├', 'CONTENT_UPPER_CENTER':  '┼', 'CONTENT_UPPER_RIGHT':  '┤',
        'CONTENT_MIDDLE_LEFT': '├', 'CONTENT_MIDDLE_CENTER': '┼', 'CONTENT_MIDDLE_RIGHT': '┤',
        'CONTENT_LOWER_LEFT':  '├', 'CONTENT_LOWER_CENTER':  '┴', 'CONTENT_LOWER_RIGHT':  '┘',
    }

    def is_alternating_chars(self) -> bool:
        return self.value['CHARS'].is_alternating_chars()

    def get_value(self, key: str) -> Any:
        if key == 'CHARS':
            return self.value['CHARS'].get_chars()

        # Tries to get the key value. If not present, falls back to the default value
        if key.endswith('_LEFT'):
            return self.value.get(key, self.value.get('LEFT'))
        if key.endswith('_RIGHT'):
            return self.value.get(key, self.value.get('RIGHT'))
        if key.endswith('_CENTER'):
            return self.value.get(key, self.value.get('CENTER'))
        
        return self.value.get(key)
 

    def __str__(self) -> str:
        representation: str = '{'
        for key, value in self.value.items():
            if key == 'CHARS':
                representation += f"'{key}': {value}, "
            else: 
                representation += f"'{key}': '{value}', " if value is not None else f"'{key}': None"

        representation = representation[0: -2] + '}'

        return f"{self.__class__.__name__}.{self.name} = {representation}"

    def __repr__(self) -> str:
        return self.__str__()
    
    
class StringSlicingMode(Enum):
    """An Enum for String Slicing Mode"""

    STRING_START: str = 'STRING_START'
    STRING_END:   str = 'STRING_END'

    def __str__(self) -> str:
        return f"{self.__class__.__name__}.{self.name} = {self.value}"

    def __repr__(self) -> str:
        return self.__str__()
    

class StringFunctions(Enum):
    """An Enum for String Functions"""

    STR_KEEP_AS_IS: str = 'STR_KEEP_AS_IS'
    STR_UPPER:      str = 'STR_UPPER'
    STR_LOWER:      str = 'STR_LOWER'
    STR_TITLE:      str = 'STR_TITLE'
    
    def apply(self, string: str) -> str:
        if self == self.STR_KEEP_AS_IS:
            return string
        elif self == self.STR_UPPER:
            return string.upper()
        elif self == self.STR_LOWER:
            return string.lower()
        elif self == self.STR_TITLE:
            return string.title()
        
    def __str__(self) -> str:
        return f"{self.__class__.__name__}.{self.name} = {self.value}"

    def __repr__(self) -> str:
        return self.__str__()


class StringLengthValidation(Enum):
    """An Enum for String Length Validation"""

    BUILT_IN_LEN: str = 'BUILT_IN_LEN'
    WCSWIDTH:     str = 'WCSWIDTH'

    @classmethod
    def length_of(cls, string: str, value: 'StringLengthValidation') -> int:
        if value == cls.BUILT_IN_LEN:
            return len(string)
        elif value == cls.WCSWIDTH:
            return wcswidth(string)
    
    @classmethod
    def char_length(cls, char: str) -> int:
        return wcwidth(char)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}.{self.name} = {self.value}"

    def __repr__(self) -> str:
        return self.__str__()


class StringBreakMode(Enum):

    BREAK_DYNAMIC: str = 'BREAK_DYNAMIC'
    BREAK_CHAR:    str = 'BREAK_CHAR'
    BREAK_WORD:    str = 'BREAK_WORD'
    
    
    def break_string(self, string: str, max_str_size: int, length_validation: StringLengthValidation) -> List[str]:
        if self == self.BREAK_DYNAMIC:
            return self._break_dynamic(string, max_str_size, length_validation)
        elif self == self.BREAK_CHAR:
            return self._break_char(string, max_str_size, length_validation)
        elif self == self.BREAK_WORD:
            return self._break_word(string)
        

    def _break_word(self, string: str) -> List[str]:
        return string.split()


    def _break_char(self, string: str, max_str_size: int, length_validation: StringLengthValidation) -> List[str]:
        str_len = StringLengthValidation.length_of(string, length_validation)

        if str_len <= max_str_size:
            return [string]
        
        break_string: List[str] = []
        char_len_sum = 0
        _cont = 1
        
        while string:
            for char in string:
                
                char_len = StringLengthValidation.char_length(char)
                char_len_sum += char_len

                if char_len_sum > max_str_size:
                    _cont = _cont - 1

                if char_len_sum >= max_str_size:
                    break_string.append(string[:_cont])
                    string = string[_cont:]
                    char_len_sum = 0
                    _cont = 0
                else:
                    _cont += 1
    
        return break_string
        

    def _break_dynamic(self, string: str, max_str_size: int, length_validation: StringLengthValidation) -> List[str]:
        """
        Divide uma string em partes com comprimento total menor ou igual ao máximo especificado,
        quebrando palavras maiores que o limite permitido.
        
        :param string: A string que será dividida.
        :param max_str_size: O comprimento máximo permitido para cada segmento.
        :param length_validation: O modo de cálculo do comprimento da string.
        :return: Uma lista de strings divididas.
        """
        def split_large_word(word: str, max_size: int) -> List[str]:
            """Divide uma palavra maior que max_size em pedaços menores."""
            chunks = []
            current_chunk = ""
            for char in word:
                char_len = StringLengthValidation.char_length(char)
                current_chunk_len = StringLengthValidation.length_of(current_chunk, length_validation)
                
                if current_chunk_len + char_len <= max_size:
                    current_chunk += char
                else:
                    chunks.append(current_chunk)
                    current_chunk = char
            
            if current_chunk:
                chunks.append(current_chunk)
            return chunks

        words = string.split()
        splitted_str = []
        current_chunk = ""
        
        for word in words:
            word_len = StringLengthValidation.length_of(word, length_validation)
            chunk_len = StringLengthValidation.length_of(current_chunk, length_validation) if current_chunk else 0

            # Se a palavra cabe no segmento atual, adiciona
            if chunk_len + word_len <= max_str_size - 1:
                current_chunk += (word if not current_chunk else f" {word}")
            else:
                # Adiciona o segmento atual se não estiver vazio
                if current_chunk:
                    splitted_str.append(current_chunk)
                current_chunk = ""

                # Se a palavra for maior que o tamanho máximo, divida
                if word_len > max_str_size:
                    large_chunks = split_large_word(word, max_str_size)
                    splitted_str.extend(large_chunks)
                else:
                    current_chunk = word
        
        # Adiciona o último segmento, se existir
        if current_chunk:
            splitted_str.append(current_chunk)

        return splitted_str
        