# src/acquisition/huggingface_sources.py

from src.acquisition.huggingface import (
    HuggingFaceSource,
)


huggingface_models = HuggingFaceSource(
    entity_type="AI_MODEL",
    endpoint="models",
    source_name="huggingface_models",
)


huggingface_datasets = HuggingFaceSource(
    entity_type="DATASET",
    endpoint="datasets",
    source_name="huggingface_datasets",
)