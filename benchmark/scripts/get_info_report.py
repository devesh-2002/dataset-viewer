import json
import logging
import time

import typer
from datasets import disable_progress_bar
from serialize import deserialize_dataset_name

from datasets_preview_backend.queries.info import get_info

# remove any logs
logging.disable(logging.CRITICAL)
disable_progress_bar()


def get_info_report(dataset: str):
    try:
        t = time.process_time()
        info = get_info(dataset)["info"]
        return {
            "dataset": dataset,
            "info": info,
            "success": True,
            "exception": None,
            "message": None,
            "cause": None,
            "cause_message": None,
            "elapsed_seconds": time.process_time() - t,
        }
    except Exception as err:
        return {
            "dataset": dataset,
            "info": None,
            "success": False,
            "exception": type(err).__name__,
            "message": str(err),
            "cause": type(err.__cause__).__name__,
            "cause_message": str(err.__cause__),
            "elapsed_seconds": time.process_time() - t,
        }


def main(serialized_dataset_name: str, filename: str):
    report = get_info_report(deserialize_dataset_name(serialized_dataset_name))
    with open(filename, "w") as f:
        json.dump(report, f)


if __name__ == "__main__":
    typer.run(main)