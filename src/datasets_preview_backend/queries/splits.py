from typing import List

from datasets import load_dataset_builder
from datasets.utils.streaming_download_manager import StreamingDownloadManager

from datasets_preview_backend.exceptions import Status400Error, Status404Error


def get_splits(dataset: str, config: str) -> List[str]:
    try:
        builder = load_dataset_builder(dataset, name=config)
    except FileNotFoundError as err:
        raise Status404Error("The dataset config could not be found.") from err
    except ValueError as err:
        if str(err).startswith(f"BuilderConfig {config} not found."):
            raise Status404Error("The dataset config could not be found.") from err
        else:
            raise Status400Error(
                "The split names could not be parsed from the dataset config."
            ) from err
    except Exception as err:
        raise Status400Error(
            "The split names could not be parsed from the dataset config."
        ) from err

    if builder.info.splits is None:
        # try to get them from _split_generators
        # should not be necessary once https://github.com/huggingface/datasets/issues/2743 is fixed
        try:
            splits = [
                split_generator.name
                for split_generator in builder._split_generators(
                    StreamingDownloadManager(base_path=builder.base_path)
                )
            ]
        except Exception as err:
            raise Status400Error(
                "The split names could not be parsed from the dataset config."
            ) from err
    else:
        splits = list(builder.info.splits.keys())
    return {"dataset": dataset, "config": config, "splits": splits}