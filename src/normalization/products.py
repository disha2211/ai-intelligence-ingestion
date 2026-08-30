from typing import Any

from src.acquisition.models import RawRecord
from src.models.canonical import Product
from src.normalization.utils import (
    normalize_url,
)

def normalize_product(
    record: RawRecord,
) -> Product:

    data: dict[str, Any] = record.payload

    name = (
        data.get("name")
        or data.get("title")
        or ""
    ).strip()

    description = (
        data.get("description")
        or ""
    ).strip()

    url = normalize_url(
        data.get("url")
        or data.get("website")
        or record.source_url
    )

    if url is None:
        raise ValueError(
            f"Product has no valid URL: {name}"
        )
    features = (
        data.get("features_use_cases")
        or data.get("features")
        or data.get("use_cases")
        or []
    )

    if isinstance(features, str):
        features = [features]

    features = [
        str(feature).strip()
        for feature in features
        if str(feature).strip()
    ]

    return Product(
        name=name,
        description=description,
        url=url,
        source=record.source_name,
        category=(
            data.get("category")
            or data.get("categories")
        ),
        features_use_cases=features,
        pricing=(
            data.get("pricing")
            or data.get("pricing_model")
        ),
        company=(
            data.get("company")
            or data.get("developer")
        ),
        github_url=data.get(
            "github_url"
            or None
        ),
    )