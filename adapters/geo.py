"""Growth OS adapter: GEO (Generative Engine Optimization) prober — PROTOCOL STUB.

GEO measures whether AI assistants (ChatGPT, Gemini, Claude, Perplexity) mention
or cite a brand when a user asks a buying-intent question. There is no single
official "AI visibility" API, so Growth OS defines an open protocol instead:

    1. Generate a set of realistic prompts from the brand's ICP + category
       (done here — real, deterministic).
    2. Send each prompt to one or more LLM "probers" (bring your own key).
    3. Parse each answer for brand mention, citation link, sentiment,
       competitors named, and rank/position.
    4. Aggregate into a share-of-voice baseline the orchestrator can track.

v0.1 ships step 1 for real and leaves steps 2-4 as a documented `probe()` stub,
because probing spends tokens and needs user-supplied model keys. The prompt
generator is usable today to seed a manual GEO audit.

Optional env once probing is implemented:
    GEO_PROBERS               # csv, e.g. "openai,anthropic,perplexity,gemini"
    OPENAI_API_KEY / ANTHROPIC_API_KEY / PERPLEXITY_API_KEY / GEMINI_API_KEY

Docs: docs/integrations/geo.md
"""

from __future__ import annotations

from typing import Any

# Prompt archetypes that surface brand mentions in AI answers. Buying-intent,
# comparison, and recommendation questions are where citations actually happen.
_PROMPT_TEMPLATES = [
    "What are the best tools for {category}?",
    "I need {job_to_be_done}. What software should I use?",
    "What is the best alternative to {competitor}?",
    "Compare the top {category} platforms for a {icp_role}.",
    "Which {category} tool is best for {icp_segment}?",
    "Is {brand} any good for {job_to_be_done}?",
    "What do people recommend for {job_to_be_done} in 2026?",
    "Cheapest reliable {category} tool for a small team?",
    "Which {category} tools integrate with {integration}?",
    "What are experts saying about {brand} vs {competitor}?",
]


def generate_queries(
    brand: str,
    category: str,
    icp_role: str = "founder",
    icp_segment: str = "small business",
    job_to_be_done: str = "growing my business",
    competitors: list[str] | None = None,
    integration: str = "your existing stack",
) -> dict[str, Any]:
    """Build a deterministic set of GEO probe prompts from ICP inputs.

    Real and usable today: feed the output into any AI assistant by hand, or wait
    for probe() to automate it.
    """
    competitors = competitors or ["a leading competitor"]
    primary_competitor = competitors[0]

    prompts: list[str] = []
    for template in _PROMPT_TEMPLATES:
        prompts.append(
            template.format(
                brand=brand,
                category=category,
                icp_role=icp_role,
                icp_segment=icp_segment,
                job_to_be_done=job_to_be_done,
                competitor=primary_competitor,
                integration=integration,
            )
        )
    # De-duplicate while preserving order.
    seen: set[str] = set()
    unique = [p for p in prompts if not (p in seen or seen.add(p))]

    return {
        "adapter": "geo",
        "command": "generate_queries",
        "brand": brand,
        "category": category,
        "competitors": competitors,
        "count": len(unique),
        "prompts": unique,
    }


def probe(
    brand: str,
    category: str,
    probers: list[str] | None = None,
    **icp_kwargs: Any,
) -> dict[str, Any]:
    """Run generated prompts against LLM probers and score brand visibility.

    STUB in v0.1 — probing spends tokens and needs user-supplied model keys.

    Planned pipeline:
        for prompt in generate_queries(...).prompts:
            for prober in probers:            # openai / anthropic / perplexity / gemini
                answer = call_model(prober, prompt)
                score  = parse(answer) -> {
                    "mentioned": bool, "cited_url": str | None,
                    "sentiment": "pos|neu|neg",
                    "competitors_named": [...], "rank": int | None }
        aggregate -> {
            "share_of_voice": float,          # % of prompts where brand appears
            "citation_rate": float,           # % with a real link to brand
            "by_prober": { prober: {...} },
            "competitor_share": { name: float } }

    Returns that aggregate dict once implemented.
    """
    raise NotImplementedError(
        "GEO probing is a v0.1 protocol stub — it spends tokens and needs your own "
        "model keys. Use geo generate_queries to seed a manual audit, or implement "
        "probe() per docs/integrations/geo.md."
    )


COMMANDS = {
    "generate_queries": generate_queries,
    "probe": probe,
}
