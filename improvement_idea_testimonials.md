# Proposal: Optional Testimonials (CVFoundry-Lite)

## Goal
Add an optional, minimal testimonials capability to the canonical model to capture short quotes from peer/colleague/client, anchored to an experience or win. Do not render by default.

## Non-goals
- No template rendering in MVP
- No complex attribution, names, or organizations
- No long quotes

## Data model
Add [data/testimonials.yml](cci:7://file:///home/jacksonm/CascadeProjects/mlj-resume/data/testimonials.yml:0:0-0:0):

testimonials:
  - id: t_peer_delivery_001
    quote: "Consistently brings clarity, momentum, and calm execution to high-stakes work."
    attribution_public: peer  # allowed: peer | colleague | client
    experience_id: some_experience_id  # optional OR win_id

Rules:
- Required: id, quote, attribution_public
- Optional: experience_id OR win_id (at least one recommended)

## Validation
If [data/testimonials.yml](cci:7://file:///home/jacksonm/CascadeProjects/mlj-resume/data/testimonials.yml:0:0-0:0) exists:
- ensure testimonials is a list
- ensure unique ids
- ensure required fields exist
- ensure experience_id/win_id references exist when provided

## Future (optional)
- profile selection: selected_testimonial_ids + limits
- minimal render: 1 quote max on one-pager, 2 max on resume
