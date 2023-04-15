from pathlib import Path
import pytest
from src.extended.lexer import QPLexerExtended
from tests.utils import resolve_test_files


@pytest.mark.parametrize(
    "test_name",
    [
        "t01",
        "t02",
        "t03",
        "t04",
        "t05",
        "t06",
        "t07",
        "t08",
        "t09",
        "t10"
    ],
)
def test_lexer(test_name, capfd):
    input_path, expected_path = resolve_test_files(test_name, Path(__file__).parent.absolute())

    m = QPLexerExtended()
    with open(input_path) as f_in, open(expected_path) as f_ex:
        m.scan(f_in.read())
        captured = capfd.readouterr()
        expect = f_ex.read()
    assert captured.out == expect
