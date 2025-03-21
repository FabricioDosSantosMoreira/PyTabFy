from typing import Dict, List, Tuple


def get_version(version: Tuple[int, int, int, str]) -> str:
    string = 'v' + '.'.join(str(value) for value in version[0:-1])
    if version[-1] != 'null':
        string += f'-{str(version[-1])}'

    return string


def build_ascii_art() -> List[str]:
    from PyTabFy import version_tuple

    base_art_msg: List[str] = [
        r" _____    _______    _     ______               ",
        r"|  __ \  |__   __|  | |   |  ____|              ",
        r"| |__) |   _| | __ _| |__ | |__ _   _           ",
        r"|  ___/ | | | |/ _` | '_ \|  __| | | |          ",
        r"| |   | |_| | | (_| | |_) | |  | |_| |   __   __",
        r"|_|    \__, |_|\__,_|_.__/|_|   \__, |   \ \ / /",
        r"        __/ |                    __/ |    \ V / ",
        r"       |___/                    |___/      \_/  ",
    ]

    for idx, value in enumerate(version_tuple):
        if isinstance(value, int):
            ascii_art: List[str] = get_ascii_number_art(value)

            min_empty_spaces: int = 0
            inversed_string = ascii_art[-1][::-1].split(' ')

            for i in range(len(inversed_string)):
                if inversed_string[i] == '':
                    min_empty_spaces += 1
                else:
                    break
            
            if min_empty_spaces > 1:
                ascii_art[-1] = ascii_art[-1][0: -min_empty_spaces]

            for i in range(6):
                base_art_msg[-(6 - i)] += ascii_art[i]

            if idx < 2:
                base_art_msg[-1] += ' ■ ' + ' ' * (min_empty_spaces - 2)

            for i in range(5):
                max_str_len: int = max(len(string) for string in base_art_msg)

                for i in range(len(base_art_msg)):
                    base_art_msg[i] = base_art_msg[i].ljust(max_str_len)
             
     
        elif isinstance(value, str) and value != 'null':
            ascii_art: List[str] = get_ascii_word_art(value)
            
            start: int = len(ascii_art)
            if start > 6:
                for i in range(len(ascii_art) - 6):
                    base_art_msg.append('')
                
            max_str_len: int = max(len(string) for string in base_art_msg)

            for i in range(len(base_art_msg)):
                base_art_msg[i] = base_art_msg[i].ljust(max_str_len + 1)

            for i in range(len(ascii_art)):
                base_art_msg[-(start - i)] += ascii_art[i]

    return base_art_msg


def get_ascii_word_art(string: str) -> List[str]:
    
    words: Dict[str, List[str]] = {
        'alpha': [
            r"       _       _           ",
            r"      | |     | |          ",
            r"  __ _| |_ __ | |__   __ _ ",
            r" / _` | | '_ \| '_ \ / _` |",
            r"| (_| | | |_) | | | | (_| |",
            r" \__,_|_| .__/|_| |_|\__,_|",
            r"        | |                ",
            r"        |_|                ",
        ],
        'beta': [
            r" _          _         ",
            r"| |        | |        ",
            r"| |__   ___| |_  __ _ ",
            r"| '_ \ / _ \ __|/ _` |",
            r"| |_) |  __/ |_| (_| |",
            r"|_.__/ \___|\__|\__,_|",
        ],
    }

    return words.get(string, ['', '', '', '', '', ''])


def get_ascii_number_art(n: int) -> List[str]:

    numbers: Dict[int, List[str]] = {
        1: [
            " __ ", 
            "/_ |", 
            " | |", 
            " | |", 
            " | |", 
            " |_|",                    
        ], 
        2: [
            " ___  ", 
            "|__ \ ", 
            "   ) |", 
            "  / / ", 
            " / /_ ", 
            "|____|",
        ],
        3: [
            " ____  ", 
            "|___ \ ", 
            "  __) |", 
            " |__  <", 
            " ___) |",
            "|____/ ",
        ],
        4: [
            " _  _   ", 
            "| || |  ", 
            "| || |_ ", 
            "|__   _|", 
            "   | |  ", 
            "   |_|  ",
        ],
        5: [
            " _____ ", 
            "| ____|", 
            "| |__  ", 
            "|___ \ ", 
            " ___) |", 
            "|____/ ",
        ],
        6: [
            "   __   ", 
            "  / /   ", 
            " / /__  ", 
            "| '__ \ ", 
            "| (__) |", 
            " \____/ ",
        ],
        7: [
            " ______ ", 
            "|____  |", 
            "    / / ",
            "   / /  ", 
            "  / /   ", 
            " /_/    ",
        ],
        8: [
            "  ____  ", 
            " / __ \ ", 
            "| (__) |", 
            " > __ < ", 
            "| (__) |", 
            " \____/ "
        ],
        9: [
            "  ____  ", 
            " / __ \ ", 
            "| (__) |", 
            " \__, / ", 
            "   / /  ", 
            "  /_/   ",
        ],
        0: [
            "  ___  ", 
            " / _ \ ", 
            "| | | |", 
            "| | | |", 
            "| |_| |", 
            " \___/ ",
        ],
    }

    art: List[str] = ['' for _ in range(6)]
    
    for digit in split_digits(n):
        for i in range(6):
            art[i] += numbers[digit][i]

    return art


def split_digits(n: int) -> List[int]:
    return [int(d) for d in str(n)]
