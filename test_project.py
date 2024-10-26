from project import (
    read_file,
    split_name_age,
    find_drop_missing_values,
    find_explicit_duplicates,
    drop_explicit_duplicates,
    remove_extra_spaces_and_characters_data,
    age_data,
    total_info,
    visualization,
    save_to_csv,
)
import pytest
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    test_read_file()
    test_split_name_age()
    test_find_drop_missing_values()
    test_find_explicit_duplicates()
    test_drop_explicit_duplicates()
    test_remove_extra_spaces_and_characters_data()
    test_age_data()
    test_total_info()
    test_visualization()
    test_save_to_csv()


def test_read_file():
    # Apply the test function
    result = read_file()
    # Check if result is a DataFrame object
    assert isinstance(result, pd.DataFrame)
    # Check if length of DataFrame equal 105
    assert len(result) == 105
    # Check columns names
    assert list(result.columns) == ["Column1", "Column2"]
    # Check values
    assert result.iloc[0, 0] == "DONATELLO (1386-1466)"
    assert result.iloc[0, 1] == "  EARLY RENAISSANCE"

def test_split_name_age():
    # Create a data to test
    sample_data = pd.DataFrame(
        {"Column1": ["DONATELLO (1386-1466)"], "Column2": ["EARLY RENAISSANCE"]}
    )
    # Expected result after applying the function
    expected_result = pd.DataFrame(
        {
            "Name": ["DONATELLO"],
            "Birth": ["1386"],
            "Death": ["1466"],
            "Movement": ["EARLY RENAISSANCE"],
        }
    )
    # Apply the test function
    result1 = split_name_age(sample_data)
    # Check if result1 is a DataFrame object
    assert isinstance(result1, pd.DataFrame)
    # Strip leading and trailing spaces near name
    result1 = result1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    # Check if the actual result matches the expected result
    pd.testing.assert_frame_equal(result1, expected_result)


def test_find_drop_missing_values():
    # Create a data to test
    sample_data = pd.DataFrame(
        {
            "Name": ["fra filippo lippi", "Albrecht Durer", "Alessandro BOTTICELLi"],
            "Birth": ["c.1406", "1471", "1445"],
            "Death": ["1469", "1528", "1510"],
            "Movement": ["EARLY RENAISSANCE", None, "EARLY RENAISSANCE"],
        }
    )
    # Expected result after applying the function
    expected_result = pd.DataFrame(
        {
            "Name": ["fra filippo lippi", "Alessandro BOTTICELLi"],
            "Birth": ["c.1406", "1445"],
            "Death": ["1469", "1510"],
            "Movement": ["EARLY RENAISSANCE", "EARLY RENAISSANCE"],
        }
    )
    # Apply the test function
    result2 = find_drop_missing_values(sample_data)
    # Check if result2 is a DataFrame object
    assert isinstance(result2, pd.DataFrame)
    # Check if the actual result matches the expected result
    assert result2.equals(expected_result)


def test_find_explicit_duplicates(capsys):
    # Create a data to test
    sample_data = pd.DataFrame(
        {
            "Name": ["Titian", "Titian"],
            "Birth": ["c.1485", "c.1485"],
            "Death": ["1576", "1576"],
            "Movement": ["HIGH RENAISSANCE", "HIGH RENAISSANCE"],
        }
    )
    # Apply the test function
    explicit_duplicates_count, explicit_duplicates = find_explicit_duplicates(
        sample_data
    )
    # Check if output is correct
    captured = capsys.readouterr()
    explicit_duplicates_count = sample_data.duplicated().sum()
    assert f"We have {explicit_duplicates_count} explisit duplicates" in captured.out
    if explicit_duplicates_count > 0:
        assert "Explicit duplicates are:" in captured.out
        assert (
            sample_data[sample_data.duplicated(keep=False)].to_string() in captured.out
        )
    else:
        assert "Explicit duplicates did't find" in captured.out
    # Check return values
    assert explicit_duplicates_count == sample_data.duplicated().sum()
    assert explicit_duplicates is None or isinstance(explicit_duplicates, pd.DataFrame)


def test_drop_explicit_duplicates():
    # Create a data to test
    sample_data = pd.DataFrame(
        {
            "Name": ["Titian", "Titian"],
            "Birth": ["c.1485", "c.1485"],
            "Death": ["1576", "1576"],
            "Movement": ["HIGH RENAISSANCE", "HIGH RENAISSANCE"],
        }
    )
    # Apply the test function
    result3 = drop_explicit_duplicates(sample_data)
    # Check if result3 is a DataFrame object
    assert isinstance(result3, pd.DataFrame)
    # Check if all duplicates were dropped
    assert len(result3) == len(sample_data.drop_duplicates())
    # Check if indexes were reseted
    assert result3.index.equals(pd.RangeIndex(len(result3)))
    # Check if our DataFrame isn't empty
    assert not result3.empty


def test_remove_extra_spaces_and_characters_data():
    # Create a data to test
    sample_data = pd.DataFrame(
        {
            "index": [0, 1, 2, 3],
            "Name": [
                "fra filippo lippi",
                "    Leon Battista Alberti    ",
                "Filippino        Lippi",
                "Alessandro BOTTICELLi",
            ],
            "Birth": ["c.1406", "1404", "1457", "1445"],
            "Death": ["1469", "1472", "1504", "1510"],
            "Movement": [
                "EARLY RENAISSANCE",
                "EARLY RENAISSANCE",
                "HIGH RENAISSANCE",
                "EARLY RENAISSANCE",
            ],
        }
    )
    # Apply the test function
    result4 = remove_extra_spaces_and_characters_data(sample_data)
    # Check if result4 is a DataFrame object
    assert isinstance(result4, pd.DataFrame)
    # Check if leading and trailing spaces from all raws were stripped
    assert result4["Name"][1] == "Leon Battista Alberti"
    # Check if extra whitespaces between first name and last name were removed
    assert result4["Name"][2] == "Filippino Lippi"
    # Check if any characters before numbers at "Birth" column were removed
    assert result4["Birth"][0] == 1406
    # Check if types in columns "Birth" and "Death" are integer
    assert result4["Birth"].dtype == int
    assert result4["Death"].dtype == int
    # Check if all text in lowercase and words are titled
    assert result4["Name"][3] == "Alessandro Botticelli"


def test_age_data():
    # Create a data to test
    sample_data = pd.DataFrame(
        {
            "Name": ["Donatello", "Albrecht Durer"],
            "Birth": [1386, 1471],
            "Death": [1466, 1528],
            "Movement": ["EARLY RENAISSANCE", "HIGH RENAISSANCE"],
        }
    )
    # Apply the test function
    result5 = age_data(sample_data)
    # Check if result5 is a DataFrame object
    assert isinstance(result5, pd.DataFrame)
    # Check if column "Age" was added
    assert "Age" in result5.columns
    # Check if column  "Movement" is at the end of table
    assert result5.columns[-1] == "Movement"
    # Check if column "Name" is sorted alphabetically
    assert result5["Name"].tolist() == ["Albrecht Durer", "Donatello"]
    # Check if values in column "Age" are correct
    assert result5["Age"].tolist() == [57, 80]


def test_total_info(capsys):
    # Create a data to test
    sample_data = pd.DataFrame(
        {
            "Name": ["Donatello", "Albrecht Durer"],
            "Birth": [1386, 1471],
            "Death": [1466, 1528],
            "Movement": ["EARLY RENAISSANCE", "HIGH RENAISSANCE"],
        }
    )
    # Apply the test function
    result6 = total_info(sample_data)
    # Check if result6 is a DataFrame object
    assert isinstance(result6, pd.DataFrame)
    # Check if output is correct
    captured = capsys.readouterr()
    # Check return values
    assert f"{result6.info()}" in captured.out
    assert f"{result6.describe()}" in captured.out


def test_visualization(capsys):
    # Create a data for testing
    sample_data = pd.DataFrame(
        {
            "Name": ["Donatello", "Albrecht Durer", "Raphael"],
            "Birth": [1386, 1471, 1483],
            "Death": [1466, 1528, 1520],
            "Age": [80, 57, 37],
            "Movement": ["EARLY RENAISSANCE", "HIGH RENAISSANCE", "HIGH RENAISSANCE"],
        }
    )
    # Apply the test function
    result7 = visualization(sample_data)
    # Check if result7 is a DataFrame object
    assert isinstance(result7, pd.DataFrame)
    # Check if output is correct
    captured = capsys.readouterr()
    assert "Count Artists by Movement:" in captured.out
    assert "Count Artists by Age:" in captured.out
    # Check if the function generates a plot file
    assert os.path.exists("demo_visualisation_movement.png")


def test_save_to_csv(tmp_path):
    # Create a data to test
    sample_data = pd.DataFrame(
        {
            "Name": ["Donatello", "Albrecht Durer", "Raphael"],
            "Birth": [1386, 1471, 1483],
            "Death": [1466, 1528, 1520],
            "Age": [80, 57, 37],
            "Movement": ["EARLY RENAISSANCE", "HIGH RENAISSANCE", "HIGH RENAISSANCE"],
        }
    )
    # Create temporary directory to save a CSV file
    temp_dir = tmp_path / "/workspaces/141852833/project/test_output"
    temp_dir.mkdir()
    # Path to the saved CSV file
    csv_file_path = temp_dir / "/workspaces/141852833/project/test_data.csv"
    # Apply the test function with temporary data
    save_to_csv(sample_data, csv_file_path)
    # Check if the CSV file was created
    assert csv_file_path.is_file()
    # Check if contents of the CSV file matches the expected data
    loaded_data = pd.read_csv(csv_file_path)
    pd.testing.assert_frame_equal(sample_data, loaded_data)
    # Clean up temporary directory after test and remove temporary file
    temp_dir.rmdir()
    os.remove(csv_file_path)


if __name__ == "__main__":
    main()


