from datetime import date
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class Startup(BaseModel):
    name: str = Field(min_length=1)
    description: str = ""
    url: HttpUrl
    source: str

    industry: str | None = None
    founded_year: int | None = None
    location: str | None = None
    funding_stage: str | None = None
    founders: list[str] = Field(default_factory=list)
    linkedin_url: HttpUrl | None = None


class Product(BaseModel):
    name: str = Field(min_length=1)
    description: str = ""
    url: HttpUrl
    source: str

    category: str | None = None
    features_use_cases: list[str] = Field(
        default_factory=list
    )
    pricing: str | None = None
    company: str | None = None
    github_url: HttpUrl | None = None


class ResearchPaper(BaseModel):
    title: str = Field(min_length=1)
    authors: list[str] = Field(
        default_factory=list
    )
    abstract: str = ""
    url: HttpUrl
    source: str

    published_date: date | None = None
    github_url: HttpUrl | None = None
    github_stars: int | None = None