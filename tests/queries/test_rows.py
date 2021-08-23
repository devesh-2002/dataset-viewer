import pytest

from datasets_preview_backend.queries.rows import (
    Status400Error,
    Status404Error,
    extract_rows,
)


def test_extract_split_rows():
    dataset = "acronym_identification"
    config = None
    split = "train"
    num_rows = 100
    extract = extract_rows(dataset, config, split, num_rows)
    assert "dataset" in extract and extract["dataset"] == dataset
    assert "config" in extract and extract["config"] == config
    assert "split" in extract and extract["split"] == split
    assert "rows" in extract
    rows = extract["rows"]
    assert len(rows) == num_rows
    assert rows[0]["tokens"][0] == "What"


def test_extract_split_rows_num_rows():
    dataset = "acronym_identification"
    config = None
    split = "train"
    num_rows = 20
    extract = extract_rows(dataset, config, split, num_rows)
    rows = extract["rows"]
    assert len(rows) == 20
    assert rows[0]["tokens"][0] == "What"


def test_extract_unknown_dataset():
    with pytest.raises(Status404Error):
        extract_rows("doesnotexist", None, "train", 100)
    with pytest.raises(Status404Error):
        extract_rows("AConsApart/anime_subtitles_DialoGPT", None, "train", 100)


def test_extract_unknown_config():
    with pytest.raises(Status404Error):
        extract_rows("glue", "doesnotexist", "train", 100)
    with pytest.raises(Status404Error):
        extract_rows("glue", None, "train", 100)
    with pytest.raises(Status404Error):
        extract_rows("TimTreasure4/Test", None, "train", 100)


def test_extract_unknown_split():
    with pytest.raises(Status404Error):
        extract_rows("glue", "ax", "train", 100)


def test_extract_bogus_config():
    with pytest.raises(Status400Error):
        extract_rows("Valahaar/wsdmt", None, "train", 10)
    with pytest.raises(Status400Error):
        extract_rows("nateraw/image-folder", None, "train", 10)


def test_extract_not_implemented_split():
    with pytest.raises(Status400Error):
        extract_rows("ade_corpus_v2", "Ade_corpus_v2_classification", "train", 10)


def test_tar_gz_extension():
    with pytest.raises(Status400Error):
        extract_rows("air_dialogue", "air_dialogue_data", "train", 10)