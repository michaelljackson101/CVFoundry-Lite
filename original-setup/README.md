# original-setup

This folder contains a **golden copy** of the core CVFoundry-Lite files as originally shipped.

It exists for one reason: if you (or an AI assistant) accidentally break your working files while experimenting, you can restore the project to a known-good baseline by copying files from here back to the repo root.

## What’s in here

- `CVFoundry-Lite-Build.py`
- `CVFoundry-Lite-Jinja.j2`
- `CVFoundry-Lite-Config.yml`
- `CVFoundry-Lite-Canonical.yml` (starter sample)
- `requirements.txt`
- `bootstrap.sh`

## Reset guidance

Be careful:
- Resetting `CVFoundry-Lite-Canonical.yml` will overwrite your resume content.

Typical reset (safe):
- restore build/template/config
- keep your canonical file
