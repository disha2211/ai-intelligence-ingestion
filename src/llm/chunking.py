# src/llm/chunking.py

def chunk_text(
    text: str,
    *,
    max_chars: int = 12000,
    overlap: int = 500,
) -> list[str]:

    if not text:
        return []

    if len(text) <= max_chars:
        return [text]

    if overlap >= max_chars:
        raise ValueError(
            "overlap must be smaller than max_chars"
        )

    chunks: list[str] = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(
            start + max_chars,
            text_length,
        )

        chunks.append(
            text[start:end]
        )

        if end >= text_length:
            break

        start = end - overlap

    return chunks