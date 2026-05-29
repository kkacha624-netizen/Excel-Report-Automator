from src.loader import get_fileNames

def test_get_fileNames():
    assert get_fileNames("tests\test_data", ["csv", "xlsx"]) == ["1.csv", "2.xlsx"]
    