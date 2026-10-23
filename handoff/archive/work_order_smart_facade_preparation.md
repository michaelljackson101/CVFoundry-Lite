---
source: CV-Foundry
target: CVFoundry-Lite
type: architectural_recommendation
priority: medium
created_at: 2026-07-04T13:20:00-04:00
---

# Architectural Recommendation: The Smart Facade Pattern for Future LLM Integration

## Context
During the recent `LLM-Registry` remediation effort in the main `CV-Foundry` repository, a critical architectural best practice was discovered regarding dependency management and repository autonomy. 

We noticed in `ui.py` (Tab: Deconstructor) that `CVFoundry-Lite` has a placeholder for a future feature: 
*"This feature is currently a placeholder. In the future, this will dispatch a request to Prompt-Foundry or LLM-Registry to analyze the sample text and synthesize a working Jinja2 (`.j2`) layout..."*

## The Threat: Dependency Bloat
When `CVFoundry-Lite` eventually implements this LLM integration, the naive approach would be to import `LLM-Registry` and utilize the heavy, pre-instantiated SDK clients (`openai`, `google-genai`, or `langchain`) it offers. 
Doing so would force `CVFoundry-Lite` to add these unstable, rapidly changing SDK packages to its `requirements.txt`. This would violate the core ethos of `CVFoundry-Lite` being a lightweight, fast, and resilient generator.

## The Recommendation: The "Smart Facade"
When it comes time to build the Template Deconstructor feature, `CVFoundry-Lite` MUST adopt the **Smart Facade** pattern.

1. **Extract Metadata Only**: Use `llm_registry.client.resolver.get_optimal_llm(task_profile="reasoning")` strictly to retrieve the routing metadata (`api_key`, `base_url`, `resolved_model`, `provider_name`).
2. **Native Implementation**: Do NOT use the `client` object returned by the registry. Do NOT add `openai` or `langchain` to your `requirements.txt`. Instead, use Python's built-in `urllib.request` to manually construct the HTTP POST payload to the LLM endpoint using the retrieved credentials.

By following this pattern, `CVFoundry-Lite` will remain perfectly lean and immune to upstream SDK breaking changes, while still achieving full compliance with the ecosystem's centralized model routing and credential governance policies.
