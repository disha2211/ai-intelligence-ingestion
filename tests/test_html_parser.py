from datetime import datetime, timezone

from src.models.schemas import RawDocument
from src.parsers.html import HTMLParser


def test_html_parser():

    html = """
    <html>
        <head>
            <title>AI Startup Raises Funding</title>

            <meta
                name="description"
                content="An AI startup raised funding."
            />

            <script type="application/ld+json">
            {
                "@context": "https://schema.org",
                "@type": "NewsArticle",
                "headline": "AI Startup Raises Funding",
                "datePublished": "2026-08-29T10:30:00Z"
            }
            </script>
        </head>

        <body>

            <header>
                Navigation
            </header>

            <main>
                <h1>AI Startup Raises Funding</h1>

                <p>
                    The startup announced a new funding round.
                </p>
            </main>

            <footer>
                Copyright
            </footer>

            <script>
                console.log("remove me");
            </script>

        </body>
    </html>
    """

    raw = RawDocument(
        source_name="Test Source",
        source_url="https://example.com/article",
        fetched_at=datetime.now(timezone.utc),
        status_code=200,
        content_type="text/html",
        raw_html=html,
        content_hash="abc123",
    )

    parser = HTMLParser()

    result = parser.parse(raw)

    assert result.title == "AI Startup Raises Funding"

    assert (
        result.description
        == "An AI startup raised funding."
    )

    assert (
        "The startup announced"
        in result.text
    )

    assert "console.log" not in result.text

    assert "Copyright" not in result.text

    assert result.published_at is not None