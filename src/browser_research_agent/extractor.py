from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import TypedDict, cast
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from browser_research_agent.models import EvidenceSnippet

_WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+.#-]{1,}")
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
_BLOCK_TAGS = ["p", "li", "blockquote", "article", "section", "td"]
_STOP_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "about",
    "find",
    "research",
    "evidence",
    "company",
    "offers",
    "offer",
    "page",
    "site",
    "their",
    "reporting",
    "team",
    "teams",
    "buyer",
    "buyers",
    "need",
    "needs",
}


@dataclass(frozen=True)
class ExtractedPage:
    title: str | None
    description: str | None
    canonical_url: str | None
    text: str
    links: list[str]
    headings: list[str] = field(default_factory=list)


class SnippetCandidate(TypedDict):
    text: str
    before: str | None
    after: str | None


def normalize_terms(text: str) -> list[str]:
    terms: list[str] = []
    seen: set[str] = set()
    for raw_word in _WORD_RE.findall(text):
        term = _stem_term(raw_word.lower().strip("-_."))
        if len(term) < 3 or term in _STOP_WORDS or term in seen:
            continue
        seen.add(term)
        terms.append(term)
    return terms


def extract_page(html: str, base_url: str) -> ExtractedPage:
    soup = BeautifulSoup(html, "html.parser")
    for node in soup(["script", "style", "noscript", "svg", "nav", "header", "footer"]):
        node.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else None
    desc_node = soup.find("meta", attrs={"name": "description"})
    raw_description = desc_node.get("content") if desc_node else None
    description = cast(str, raw_description).strip() if isinstance(raw_description, str) else None
    canonical_node = soup.find("link", attrs={"rel": "canonical"})
    raw_canonical = canonical_node.get("href") if canonical_node else None
    canonical = cast(str, raw_canonical).strip() if isinstance(raw_canonical, str) else None

    headings = [_clean_text(node.get_text(" ")) for node in soup.find_all(["h1", "h2", "h3"])]
    headings = [heading for heading in headings if heading]
    blocks = [_clean_text(node.get_text(" ")) for node in soup.find_all(_BLOCK_TAGS)]
    blocks = [block for block in blocks if len(block) >= 20]
    if not blocks:
        blocks = [_clean_text(soup.get_text(" "))]
    text_parts = [part for part in [title, description, *headings] if part]
    for start, block in enumerate(blocks):
        text_parts.append(block)
        if start + 1 < len(blocks):
            text_parts.append(f"{block} {blocks[start + 1]}")
    text = "\n".join(_dedupe_preserve_order(text_parts))

    raw_links = [a.get("href") for a in soup.find_all("a")]
    links = sorted(
        {
            urljoin(base_url, href)
            for href in raw_links
            if isinstance(href, str) and not href.startswith(("mailto:", "tel:", "javascript:"))
        }
    )

    return ExtractedPage(
        title=title,
        description=description or None,
        canonical_url=urljoin(base_url, canonical) if canonical else None,
        text=text,
        links=links,
        headings=headings,
    )


def extract_evidence(objective: str, page_text: str, limit: int = 8) -> list[EvidenceSnippet]:
    terms = normalize_terms(objective)
    if not terms or not page_text:
        return []

    weighted_terms = Counter(terms)
    snippets: list[EvidenceSnippet] = []
    seen_text: set[str] = set()
    candidates = _candidate_snippets(page_text)
    for index, candidate in enumerate(candidates):
        candidate_text = candidate["text"]
        lowered_words = set(normalize_terms(candidate_text))
        matched = sorted({term for term in weighted_terms if term in lowered_words})
        if not matched:
            continue
        snippet_text = candidate_text[:700]
        dedupe_key = re.sub(r"\W+", " ", snippet_text.lower()).strip()
        if dedupe_key in seen_text:
            continue
        seen_text.add(dedupe_key)
        coverage = sum(weighted_terms[term] for term in matched) / max(1, len(weighted_terms))
        density = len(matched) / max(8, len(lowered_words))
        length_bonus = 0.12 if 80 <= len(candidate_text) <= 360 else 0.04
        snippets.append(
            EvidenceSnippet(
                text=snippet_text,
                score=round(min(1.0, (0.82 * coverage) + density + length_bonus), 4),
                matched_terms=matched,
                source=_infer_source(index),
                context_before=candidate["before"],
                context_after=candidate["after"],
            )
        )

    return sorted(snippets, key=lambda item: (item.score, len(item.matched_terms)), reverse=True)[
        :limit
    ]


def _candidate_snippets(page_text: str) -> list[SnippetCandidate]:
    raw_candidates: list[str] = []
    for block in page_text.splitlines():
        block = _clean_text(block)
        if len(block) < 30:
            continue
        raw_candidates.append(block)
        parts = [part.strip() for part in _SENTENCE_RE.split(block) if part.strip()]
        if len(parts) <= 1:
            continue
        raw_candidates.extend(part for part in parts if len(part) >= 40)

    candidates: list[SnippetCandidate] = []
    for index, text in enumerate(raw_candidates):
        candidates.append(
            {
                "text": text,
                "before": raw_candidates[index - 1] if index > 0 else None,
                "after": raw_candidates[index + 1] if index + 1 < len(raw_candidates) else None,
            }
        )
    return candidates


def _infer_source(index: int) -> str:
    if index == 0:
        return "title_or_meta"
    if index <= 2:
        return "heading_or_summary"
    return "body"


def _clean_text(text: str) -> str:
    return " ".join(text.split())


def _dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def _stem_term(term: str) -> str:
    if term.endswith("ies") and len(term) > 4:
        return f"{term[:-3]}y"
    if term.endswith("ing") and len(term) > 6:
        return term[:-3]
    if term.endswith("s") and not term.endswith("ss") and len(term) > 3:
        return term[:-1]
    return term
