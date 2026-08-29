def chunk_text(
    text: str,
    max_chars: int = 12000,
    overlap: int = 500,
) -> list[str]:

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = min(
            start + max_chars,
            len(text),
        )

        chunk = text[start:end]

        chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks