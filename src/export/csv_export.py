import csv
from pathlib import Path

from pydantic import BaseModel


def export_csv(
    records: list[BaseModel],
    path: str,
) -> None:

    if not records:
        return

    output = Path(path)
    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = [
        record.model_dump(mode="json")
        for record in records
    ]

    fieldnames = list(rows[0].keys())

    with output.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(rows)