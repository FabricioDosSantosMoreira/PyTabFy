from typing import List, Optional, Tuple
from random import randint


def generate_dummy_data(
        cols: int, 
        rows: int, 
        allow_empty_data: Optional[bool] = True,
        empty_data_chance: Optional[int] = 3
    ) -> Tuple[str, List[str], List[List[str]]]:
    """
    Generates valid dummy data to use as TableData.

    ### Args:
        - `cols (int):`
            - summary: 'Number of columns.'
            - example: '3'

        - `rows (int):`
            - summary: 'Number of rows.'
            - example: '5'

        - `allow_empty_data (bool) (default: True)`
            - summary: 'Whether to allow empty fields.'
            - example: 'True'
        
        - `empty_chance (int) (default: 3 | 1 in 3 chance):`
            - summary: 'Probability of an empty field.'
            - example: '2'

    ### Returns:
        - `Tuple[str, List[str], List[List[str]]]:`
            - `Title (str):` The table title
            - `Headers (List[str]):` The table headers
            - `Contents (List[List[str]]):` The table contents

    ### How To:
        - `title, headers, contents = generate_dummy_data(cols=3, rows=6, allow_empty_data=True, empty_data_chance=2)`
    """

    def maybe_empty(value: str) -> str:
        return '' if allow_empty_data and randint(1, empty_data_chance) == 1 else value

    title: str = 'Dummy Data'
    headers: List[str] = [
        maybe_empty(f'Header {[c]}') for c in range(cols)
    ]
    contents: List[List[str]] = [
        [maybe_empty(f'Content {[r]}{[c]}') for c in range(cols)] for r in range(rows)
    ]

    return (title, headers, contents)


def get_not_only_ascii_movie_data() -> Tuple[str, List[str], List[List[str]]]:
    """
    Obtain a collection of movie data containing ascii and non-ascii values.
    
    ### Returns:
        - `Tuple[str, List[str], List[List[str]]]:`
            - `title (str):` The table title
            - `headers (List[str]):` The table headers
            - `contents (List[List[str]]):` The table contents

    ### How To:
        - `title, headers, contents = get_not_only_ascii_movie_data()`
    """

    title: str = "Not Only ASCII Movie Data"
    headers: List[str] = ["Original Title", "English Title", "Director", "Genre", "Year", "Country"]
    contents: List[List[str]] = [
        ["重慶森林", "Chungking Express", "Wong Kar-wai", "Romance/Drama", "1994", "China"],
        ["墮落天使", "Fallen Angels", "Wong Kar-wai", "Crime/Drama", "1995", "China"],
        ["ラブレター", "Love Letter", "Shunji Iwai", "Romance/Drama", "1998", "Japan"],
        ["ワンダフルライフ", "After Life", "Hirokazu Kore-eda", "Drama/Fantasy", "1999", "Japan"],
        ["リリイ・シュシュのすべて", "All About Lily Chou-Chou", "Shunji Iwai", "Drama", "2002", "Japan"],
        ["올드보이", "Oldboy", "Park Chan-wook", "Thriller/Action", "2003", "South Korea"],
        ["スウィングガールズ", "Swing Girls", "Shinobu Yaguchi", "Comedy/Music", "2004", "Japan"],
        ["リンダ リンダ リンダ", "Linda Linda Linda", "Nobuhiro Yamashita", "Comedy/Drama", "2005", "Japan"],
        ["기생충", "Parasite", "Bong Joon-ho", "Thriller/Drama", "2019", "South Korea"],
        ["ドライブ・マイ・カー", "Drive My Car", "Ryusuke Hamaguchi", "Drama", "2021", "Japan"],
        ["부산행", "Train To Busan", "Yeon Sang-ho", "Horror/Action", "2016", "South Korea"],
        ["ゴジラ-1.0", "Godzilla Minus One", "Takashi Yamazaki", "Sci-Fi/Action", "2023", "Japan"],
    ]

    return (title, headers, contents)


def get_only_ascii_movie_data() -> Tuple[str, List[str], List[List[str]]]:
    """
    Obtain a collection of movie data containing only ascii values.
    
    ### Returns:
        - `Tuple[str, List[str], List[List[str]]]:`
            - `title (str):` The table title
            - `headers (List[str]):` The table headers
            - `contents (List[List[str]]):` The table contents

    ### How To:
        - `title, headers, contents = get_only_ascii_movie_data()`
    """

    title: str = "Only ASCII Movie Data"
    headers: List[str] = ["Original Title", "Director", "Genre", "Year", "Country"]
    contents: List[List[str]] = [
        ["The Breakfast Club", "John Hughes", "Comedy/Drama", "1985", "United States"],
        ["Good Morning, Vietnam", "Barry Levinson", "Comedy/Drama", "1987", "United States"],
        ["Dead Poets Society", "Peter Weir", "Drama", "1989", "United States"],
        ["Pulp Fiction", "Quentin Tarantino", "Crime/Drama", "1994", "United States"],
        ["Forrest Gump", "Robert Zemeckis", "Drama/Romance", "1994", "United States"],
        ["Le Fabuleux Destin d'Amélie Poulain", "Jean-Pierre Jeunet", "Romantic Comedy", "2001", "France"],
        ["Eternal Sunshine of the Spotless Mind", "Michel Gondry", "Romance/Sci-Fi", "2004", "United States"],
        ["Bridge to Terabithia", "Gábor Csupó", "Fantasy/Drama", "2007", "United States"],
        ["Inception", "Christopher Nolan", "Sci-Fi/Thriller", "2010", "United States"],
        ["Submarine", "Richard Ayoade", "Comedy/Drama", "2010", "United Kingdom"],
        ["Rango", "Gore Verbinski", "Animation/Comedy", "2011", "United States"],
        ["The Perks of Being a Wallflower", "Stephen Chbosky", "Drama/Romance", "2012", "United States"],
        ["Interstellar", "Christopher Nolan", "Sci-Fi/Drama", "2014", "United States"],
        ["Whiplash", "Damien Chazelle", "Drama", "2014", "United States"],
        ["La Dame dans l'auto avec des lunettes et un fusil", "Joann Sfar", "Thriller", "2015", "France"],
        ["Arrival", "Denis Villeneuve", "Sci-Fi/Drama", "2016", "United States"],
        ["Anon", "Andrew Niccol", "Sci-Fi/Thriller", "2018", "United States"],
        ["Frida - Viva la Vida", "Giovanni Troilo", "Documentary", "2019", "Italy"],
        ["Jojo Rabbit", "Taika Waititi", "Comedy/Drama", "2019", "United States"],
        ["1917", "Sam Mendes", "War/Drama", "2019", "United Kingdom"],
        ["Tenet", "Christopher Nolan", "Sci-Fi/Action", "2020", "United States"],
        ["The Map of Tiny Perfect Things", "Ian Samuels", "Romantic Fantasy", "2021", "United States"],
        ["Aftersun", "Charlotte Wells", "Drama", "2022", "United Kingdom"],
        ["Oppenheimer", "Christopher Nolan", "Biographical/Drama", "2023", "United States"],
    ]   

    return (title, headers, contents)


def get_not_only_ascii_book_data() -> Tuple[str, List[str], List[List[str]]]:
    """
    Obtain a collection of book data containing ascii and non-ascii values.
    
    ### Returns:
        - `Tuple[str, List[str], List[List[str]]]:`
            - `title (str):` The table title
            - `headers (List[str]):` The table headers
            - `contents (List[List[str]]):` The table contents

    ### How To:
        - `title, headers, contents = get_not_only_ascii_book_data()`
    """

    title: str = "Not Only ASCII Book Data"
    headers: List[str] = ["Original Title", "English Title", "Writer", "Genre", "Year", "Country"]
    contents: List[List[str]] = [
        ["孫子兵法", "The Art of War", "Sun Tzu", "Military Strategy/Philosophy", "5c. BCE", "China"],
        ["雪国", "Snow Country", "Yasunari Kawabata", "Romance/Drama", "1947", "Japan"],
        ["人間失格", "No Longer Human", "Osamu Dazai", "Fiction/Autobiographical", "1948", "Japan"],
        ["金閣寺", "The Temple of the Golden Pavilion", "Yukio Mishima", "Fiction/Philosophical", "1956", "Japan"],
        ["ノルウェイの森", "Norwegian Wood", "Haruki Murakami", "Romance/Drama", "1987", "Japan"],
        ["白夜行", "Journey Under the Midnight Sun", "Keigo Higashino", "Mystery/Suspense", "1999", "Japan"],
        ["夜は短し歩けよ乙女", "The Night is Short, Walk on Girl", "Tomihiko Morimi", "Fantasy/Romance", "2006", "Japan"],
        ["채식주의자", "The Vegetarian", "Han Kang", "Drama/Psychological", "2007", "South Korea"],
        ["三体", "The Three-Body Problem", "Liu Cixin", "Science Fiction", "2008", "China"],
        ["兄弟", "Brothers", "Yu Hua", "Drama/Historical", "2005", "China"],
        ["火花", "Spark", "Naoki Matayoshi", "Contemporary Fiction", "2015", "Japan"],
        ["請回答1988", "Reply 1988", "Lee Woo-jung", "Drama/Slice of Life", "2015", "South Korea"],   
    ]

    return (title, headers, contents)


def get_only_ascii_book_data() -> Tuple[str, List[str], List[List[str]]]:
    """
    Obtain a collection of book data containing only ascii values.
    
    ### Returns:
        - `Tuple[str, List[str], List[List[str]]]:`
            - `title (str):` The table title
            - `headers (List[str]):` The table headers
            - `contents (List[List[str]]):` The table contents

    ### How To:
        - `title, headers, contents = get_only_ascii_book_data()`
    """

    title: str = "Only ASCII Book Data"
    headers: List[str] = ["Original Title", "Writer", "Genre", "Year", "Country"]
    contents: List[List[str]] = [
        ["White Nights", "Fyodor Dostoevsky", "Romantic Fiction", "1848", "Russia"],
        ["Crime and Punishment", "Fyodor Dostoevsky", "Psychological Fiction", "1866", "Russia"],
        ["Thus Spoke Zarathustra", "Friedrich Nietzsche", "Philosophy/Fiction", "1883", "Germany"],
        ["The Sad End of Policarpo Quaresma", "Lima Barreto", "Political Fiction", "1915", "Brazil"],
        ["Brave New World", "Aldous Huxley", "Dystopian/Science Fiction", "1932", "United Kingdom"],
        ["Animal Farm", "George Orwell", "Political Satire/Allegory", "1945", "United Kingdom"],
        ["The Myth of Sisyphus", "Albert Camus", "Philosophy/Essay", "1942", "France"],
        ["The Rebel", "Albert Camus", "Philosophy/Essay", "1951", "France"],
        ["Fahrenheit 451", "Ray Bradbury", "Dystopian/Science Fiction", "1953", "United States"],
        ["1984", "George Orwell", "Dystopian/Political Fiction", "1949", "United Kingdom"],
        ["Happy Death", "Albert Camus", "Philosophical Fiction", "1971", "France"],
        ["The Hour of the Star", "Clarice Lispector", "Fiction/Existentialism", "1977", "Brazil"],
        ["The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "Science Fiction/Comedy", "1979", "United Kingdom"],
        ["Cosmos", "Carl Sagan", "Science/Non-Fiction", "1980", "United States"],
        ["Ockham's Razor", "Gilberto Freyre", "Philosophy/Non-Fiction", "1983", "Brazil"],
        ["Dirk Gently's Holistic Detective Agency", "Douglas Adams", "Science Fiction/Mystery", "1987", "United Kingdom"],
        ["Chaos: Making a New Science", "James Gleick", "Science/Non-Fiction", "1987", "United States"],
        ["A Brief History of Time", "Stephen Hawking", "Science/Non-Fiction", "1988", "United Kingdom"],
        ["The Demon-Haunted World", "Carl Sagan", "Science/Skepticism", "1995", "United States"],
        ["The Universe in a Nutshell", "Stephen Hawking", "Science/Non-Fiction", "2001", "United Kingdom"],
        ["Peripherals", "William Gibson", "Science Fiction", "2014", "Canada"],
        ["The Order of Time", "Carlo Rovelli", "Science/Non-Fiction", "2017", "Italy"],
    ]

    return (title, headers, contents)
