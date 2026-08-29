from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class RecordBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schemaVersion: str = "1.0"
    recordType: str

class Source(BaseModel):
    name: str
    url: HttpUrl


class StartupContent(BaseModel):
    entityName: str
    employeeCount: int | None = None


class StartupEntity(BaseModel):
    schemaVersion: str = "1.0"
    recordType: str = "STARTUP"
    source: Source
    content: StartupContent
    collectedAt: datetime

class PricingModel(str, Enum):
    FREE = "FREE"
    FREEMIUM = "FREEMIUM"
    PAID = "PAID"
    ENTERPRISE = "ENTERPRISE"


class ProductContent(BaseModel):
    startupName: str
    pricingModel: PricingModel


class ProductEntity(BaseModel):
    schemaVersion: str = "1.0"
    recordType: str = "PRODUCT"
    source: Source
    content: ProductContent
    collectedAt: datetime

class ResearchPaperContent(BaseModel):
    title: str
    authors: list[str]
    paper_url: HttpUrl
    github_url: HttpUrl | None = None
    github_stars: int | None = None
    published_date: datetime


class ResearchPaperEntity(BaseModel):
    schemaVersion: str = "1.0"
    recordType: str = "RESEARCH_PAPER"
    content: ResearchPaperContent
    collectedAt: datetime

class JobContent(BaseModel):
    company: str
    date: datetime
    is_remote: bool
    role_family: str


class JobEntity(BaseModel):
    schemaVersion: str = "1.0"
    recordType: str = "JOB"
    content: JobContent

class NewsContent(BaseModel):
    title: str
    published_date: datetime
    url: HttpUrl
    source: str
    full_text: str


class NewsEntity(BaseModel):
    schemaVersion: str = "1.0"
    recordType: str = "NEWS"
    content: NewsContent

class RawDocument(BaseModel):
    source_name: str
    source_url: HttpUrl

    fetched_at: datetime

    status_code: int

    content_type: str | None = None

    raw_html: str | None = None
    extracted_text: str | None = None

    content_hash: str

class CleanDocument(BaseModel):
    source_name: str
    source_url: HttpUrl

    fetched_at: datetime

    title: str | None = None
    description: str | None = None

    text: str

    published_at: datetime | None = None

    content_hash: str

class EnrichmentEvidence(BaseModel):
    field: str
    source_url: HttpUrl
    method: str
    confidence: float | None = None

class PaperEnrichment(BaseModel):
    summary: str
    topics: list[str]
    application_area: str | None = None
    github_url: HttpUrl | None = None