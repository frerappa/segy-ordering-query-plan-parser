import pytest
from pathlib import Path
from src.parser import QPParser
from tests.utils import resolve_test_files
from io import StringIO  # Python 3



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
    ],
)
# capfd will capture the stdout/stderr outputs generated during the test
def test_semantic(test_name, capfd):
    input_path, expected_path = resolve_test_files(test_name, Path(__file__).parent.absolute())

    parser = QPParser()
    with open(input_path) as f_in, open(expected_path) as f_ex:
        temp_out = StringIO()
        ast = parser.parse_text(f_in.read())
        ast.show(temp_out, showcoord=True)
        expect = f_ex.read()
    assert temp_out.getvalue() == expect
