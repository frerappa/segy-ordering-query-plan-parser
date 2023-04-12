from pathlib import Path


def resolve_test_files(test_name: str, current_dir: Path):
    input_file = test_name + ".txt"
    expected_file = test_name + ".txt"

    # get absolute path to inputs folder
    input_dir = current_dir / Path('in')
    output_dir = current_dir / Path('out')

    # get input path and check if exists
    input_path = input_dir / Path(input_file)
    assert input_path.exists()

    # get expected test file real path
    expected_path = output_dir / Path(expected_file)
    assert expected_path.exists()

    return input_path, expected_path
