from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from urllib.parse import urlparse

from dateutil.parser import parse as parse_date

from browser_research_agent.extractor import ExtractedPage, normalize_terms
from browser_research_agent.models import EvidenceSnippet, ScoreBreakdown

_DATE_RE = re.compile(
    r"\b(?:20\d{2}|19\d{2})[-/.](?:0?[1-9]|1[0-2])[-/.](?:0?[1-9]|[12]\d|3[01])\b|\b(?:20\d{2}|19\d{2})\b"
)
_CREDIBILITY_TERMS = {
    "about",
    "contact",
    "privacy",
    "terms",
    "security",
    "compliance",
    "customers",
    "case studies",
    "documentation",
    "docs",
    "whitepaper",
    "report",
    "citations",
}
_HIGH_TRUST_TLDS = {"gov", "edu"}


@dataclass(frozen=True)
class ScoringRubric:
    description: str
    weights: dict[str, float]
    interpretation: dict[str, float]


SCORE_RUBRIC = ScoringRubric(
    description="Transparent weighted scoring for ranking captured web evidence; not a hidden quality claim.",
    weights={"relevance": 0.5, "credibility": 0.35, "freshness": 0.15},
    interpretation={"strong": 0.72, "review": 0.45, "weak": 0.0},
)


def score_page(
    url: str, objective: str, page: ExtractedPage, evidence: list[EvidenceSnippet]
) -> ScoreBreakdown:
    relevance_reasons: list[str] = []
    credibility_reasons: list[str] = []
    freshness_reasons: list[str] = []
    relevance, relevance_details = _score_relevance(objective, page, evidence, relevance_reasons)
    credibility, credibility_details = _score_credibility(url, page, credibility_reasons)
    freshness, freshness_details = _score_freshness(page.text, freshness_reasons)
    confidence = _score_confidence(page, evidence, freshness_details)
    total = round(
        (SCORE_RUBRIC.weights["relevance"] * relevance)
        + (SCORE_RUBRIC.weights["credibility"] * credibility)
        + (SCORE_RUBRIC.weights["freshness"] * freshness),
        4,
    )
    return ScoreBreakdown(
        relevance=round(relevance, 4),
        credibility=round(credibility, 4),
        freshness=round(freshness, 4),
        confidence=confidence,
        total=total,
        reasons=[*relevance_reasons, *credibility_reasons, *freshness_reasons],
        relevance_reasons=relevance_reasons,
        credibility_reasons=credibility_reasons,
        freshness_reasons=freshness_reasons,
        weights=SCORE_RUBRIC.weights,
        details={
            "relevance": relevance_details,
            "credibility": credibility_details,
            "freshness": freshness_details,
            "confidence": {
                "score": confidence,
                "basis": "metadata, evidence, and detected-date completeness",
            },
        },
    )


def _score_relevance(
    objective: str,
    page: ExtractedPage,
    evidence: list[EvidenceSnippet],
    reasons: list[str],
) -> tuple[float, dict[str, object]]:
    terms = set(normalize_terms(objective))
    if not terms:
        return 0.0, {"matched_terms": [], "keyword_score": 0.0, "evidence_score": 0.0}
    haystack_terms = set(
        normalize_terms(" ".join([page.title or "", page.description or "", page.text]))
    )
    matched = {term for term in terms if term in haystack_terms}
    keyword_score = len(matched) / len(terms)
    evidence_score = min(1.0, sum(item.score for item in evidence[:5]) / 2.5)
    if matched:
        reasons.append(f"Matched objective terms: {', '.join(sorted(matched)[:8])}")
    if evidence:
        reasons.append(f"Extracted {len(evidence)} evidence snippets")
    return min(1.0, (0.55 * keyword_score) + (0.45 * evidence_score)), {
        "matched_terms": sorted(matched),
        "objective_terms": sorted(terms),
        "keyword_score": round(keyword_score, 4),
        "evidence_score": round(evidence_score, 4),
        "evidence_count": len(evidence),
    }


def _score_credibility(
    url: str, page: ExtractedPage, reasons: list[str]
) -> tuple[float, dict[str, object]]:
    parsed = urlparse(url)
    is_https = parsed.scheme == "https"
    score = 0.15 if is_https else 0.0
    if is_https:
        reasons.append("HTTPS source")
    suffix = parsed.netloc.split(".")[-1].lower()
    high_trust_tld = suffix in _HIGH_TRUST_TLDS
    if high_trust_tld:
        score += 0.25
        reasons.append(f"High-trust .{suffix} domain")
    text = page.text.lower()
    matched_signals = sorted(term for term in _CREDIBILITY_TERMS if term in text)
    signal_score = min(0.4, 0.06 * len(matched_signals))
    score += signal_score
    if matched_signals:
        reasons.append(f"Credibility signals: {', '.join(matched_signals[:6])}")
    outbound_domains = {urlparse(link).netloc for link in page.links if urlparse(link).netloc}
    outbound_score = min(0.2, len(outbound_domains) / 50)
    score += outbound_score
    if outbound_domains:
        reasons.append(f"References {len(outbound_domains)} distinct linked domains")
    return min(1.0, score), {
        "https": is_https,
        "high_trust_tld": high_trust_tld,
        "credibility_signals": matched_signals,
        "outbound_domain_count": len(outbound_domains),
        "signal_score": round(signal_score, 4),
        "outbound_score": round(outbound_score, 4),
    }


def _score_freshness(text: str, reasons: list[str]) -> tuple[float, dict[str, object]]:
    candidates = _DATE_RE.findall(text[:20000])
    dates: list[datetime] = []
    for candidate in candidates[:25]:
        try:
            parsed = parse_date(candidate, fuzzy=True)
        except (ValueError, OverflowError):
            continue
        if 1990 <= parsed.year <= datetime.now(tz=UTC).year + 1:
            dates.append(parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed)
    if not dates:
        reasons.append("No explicit freshness date found")
        return 0.35, {"newest_date": None, "age_days": None, "date_candidates": []}
    newest = max(dates)
    age_days = max(0, (datetime.now(tz=UTC) - newest).days)
    if age_days <= 365:
        score = 1.0
    elif age_days <= 1095:
        score = 0.7
    else:
        score = 0.4
    reasons.append(f"Newest detected date: {newest.date().isoformat()}")
    return score, {
        "newest_date": newest.date().isoformat(),
        "age_days": age_days,
        "date_candidates": [date.date().isoformat() for date in sorted(dates, reverse=True)[:5]],
    }


def _score_confidence(
    page: ExtractedPage, evidence: list[EvidenceSnippet], freshness_details: dict[str, object]
) -> float:
    score = 0.2
    if page.title:
        score += 0.15
    if page.description:
        score += 0.1
    if page.text and len(page.text) >= 100:
        score += 0.2
    if evidence:
        score += 0.2
    if page.links:
        score += 0.05
    if freshness_details.get("newest_date"):
        score += 0.1
    return round(min(1.0, score), 4)
