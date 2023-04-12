from pathlib import Path
import pytest
from src.lexer import QPLexer
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
        "t10",
        "t11",
        "t12",
        "t13",
        "t14",
        "t15",
        "t16",
        "t17",
        "t18",
        "t19",
        "t20",
    ],
)
def test_lexer(test_name, capfd):
    input_path, expected_path = resolve_test_files(test_name, Path(__file__).parent.absolute())

    m = QPLexer()
    with open(input_path) as f_in, open(expected_path) as f_ex:
        m.scan(f_in.read())
        captured = capfd.readouterr()
        expect = f_ex.read()
    assert captured.out == expect
