from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, field_validator, model_validator


class ResearchConfig(BaseModel):
    """Validated runtime config for one research run."""

    objective: str = Field(min_length=3)
    urls: list[str] = Field(min_length=1)
    out_dir: Path = Path("artifacts/run")
    headless: bool = True
    timeout_ms: int = Field(default=30_000, ge=1_000, le=120_000)
    max_pages: int | None = Field(default=None, ge=1)
    include_screenshots: bool = True
    user_agent: str | None = None
    report: str = Field(default="markdown", pattern="^(markdown|none)$")

    @field_validator("objective")
    @classmethod
    def objective_must_not_be_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("objective must not be blank")
        return stripped

    @field_validator("urls")
    @classmethod
    def urls_must_not_be_blank(cls, value: list[str]) -> list[str]:
        normalized = [url.strip() for url in value if url.strip()]
        if not normalized:
            raise ValueError("at least one URL is required")
        return normalized

    @model_validator(mode="after")
    def apply_max_pages(self) -> ResearchConfig:
        if self.max_pages is not None:
            self.urls = self.urls[: self.max_pages]
        return self
