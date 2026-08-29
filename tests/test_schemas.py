from datetime import datetime, timezone

from src.models.schemas import (
    ProductContent,
    ProductEntity,
    PricingModel,
    Source,
    StartupContent,
    StartupEntity,
)


def test_startup_schema():
    record = StartupEntity(
        source=Source(
            name="Example Source",
            url="https://example.com/startup"
        ),
        content=StartupContent(
            entityName="OpenAI",
            employeeCount=1000,
        ),
        collectedAt=datetime.now(timezone.utc),
    )

    assert record.recordType == "STARTUP"
    assert record.content.entityName == "OpenAI"


def test_product_pricing_enum():
    record = ProductEntity(
        source=Source(
            name="Example Source",
            url="https://example.com/product"
        ),
        content=ProductContent(
            startupName="OpenAI",
            pricingModel=PricingModel.FREEMIUM,
        ),
        collectedAt=datetime.now(timezone.utc),
    )

    assert record.content.pricingModel == PricingModel.FREEMIUM