# CVFoundry-Lite Capability Report

## Purpose
CVFoundry-Lite is a lightweight, dependency-free Markdown and Jinja2-based Resume generator. It serves as a streamlined framework for maintaining a single "canonical" representation of a professional profile (in YAML), rendering it out to various tailored formats using Jinja2 templates.

## Inputs
- `CVFoundry-Lite-Canonical.yml`: The single source of truth for the professional profile.
- `.j2` templates: Specific layouts for outputs (e.g., standard resume, one-pager).

## Outputs
- Rendered `.html` and `.md` outputs tailored to specific roles and styling needs.

## Ecosystem Role
A highly resilient, lightweight alternative to `CV-Foundry`.

## Integrations (Planned)
- Pending: "Template Deconstructor" integration via Prompt-Foundry or LLM-Registry utilizing the "Smart Facade" pattern for dependency-free API calls.
