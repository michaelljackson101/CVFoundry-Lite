# CVFoundry-Lite

CVFoundry-Lite is a tiny, local-first resume generator designed for a modern workflow:

- **One resume “source of truth”**: `CVFoundry-Lite-Canonical.yml`
- **One config** (colors, fonts, toggles): `CVFoundry-Lite-Config.yml`
- **One build command** generates a **self-contained HTML resume** you can share: `CVFoundry-Lite-<Your Name>.html`

It’s aimed at friends/family who want a better system than manually editing and archiving Word/PDF variants.

## Credit / gratitude (optional)

If you find this useful, a simple “thanks” is always appreciated:

- GitHub: https://github.com/michaelljackson101

If you think it would help someone else, please consider sharing it with a few friends/colleagues who might benefit.

## How to use this repo

Start here:

- `docs/how-to.md` — the guided workflow (includes Mermaid diagrams and AI-assistant prompts)

Core files:

- `CVFoundry-Lite-Canonical.yml` — your resume content (source of truth)
- `CVFoundry-Lite-Config.yml` — theme/options
- `CVFoundry-Lite-Build.py` — build script
- `CVFoundry-Lite-Jinja.j2` — HTML template

## Quickstart

### 1) Install dependencies

```bash
bash bootstrap.sh
source .venv/bin/activate
```

### 2) Build your resume

```bash
bash build.sh
```

Or (manual):

```bash
python CVFoundry-Lite-Build.py
```

You should see something like:

```text
Generated CVFoundry-Lite-John Doe.html
```

Open the HTML file in your browser.

## The AI co-collaboration workflow (why this is better)

Instead of “Resume-final-v7.docx”, you maintain one structured YAML file and regenerate outputs.

- Use an AI assistant to help you:
  - convert your current resume into `CVFoundry-Lite-Canonical.yml`
  - refactor the YAML over time (add experience, wins, certifications)
  - tighten bullets and keep the structure valid

Tip: you can use an AI assistant as a true co-collaborator here—not just Q&A.

- Ask it to propose safe changes to `CVFoundry-Lite-Jinja.j2` (layout) or `CVFoundry-Lite-Config.yml` (theme)
- Apply small changes, rebuild, and iterate
- Keep everything in git so you can review diffs and revert

The build script validates and normalizes inputs to reduce template breakage.

## Templates: create multiple resume layouts (Jinja)

`CVFoundry-Lite-Jinja.j2` is the resume layout. You can make alternate outputs by creating additional templates (for example: short resume, 1-page, landscape) while keeping the same `CVFoundry-Lite-Canonical.yml`.

Example:

```bash
bash build.sh --template CVFoundry-Lite-Jinja-1page.j2 --output "CVFoundry-Lite-1page.html"
```

## Tools like Windsurf

AI-enabled editors can be especially helpful for safe refactors across YAML + Jinja + Python. One example is Windsurf:

- https://windsurf.ai/

## CLI options

```bash
python CVFoundry-Lite-Build.py \
  --canonical CVFoundry-Lite-Canonical.yml \
  --config CVFoundry-Lite-Config.yml \
  --template CVFoundry-Lite-Jinja.j2 \
  --output "CVFoundry-Lite-John Doe.html"
```

## Sharing your resume

The generated HTML is:

- self-contained (inline CSS)
- portable (one file)

You can:

- send it directly as a file
- store it in a private shared folder and share a link
- host it so you have one “always up to date” URL (e.g., GitHub Pages / Netlify)

If you publish publicly, consider removing phone/email or maintaining a “public” canonical variant.

## Reset to a known-good baseline (golden copy)

This repo includes an `original-setup/` folder containing a **golden copy** of the core files as shipped.

Use this if you (or an AI assistant) accidentally break the build script, template, or config while experimenting.

Important:

- Resetting `CVFoundry-Lite-Canonical.yml` will overwrite your resume content.
- Most of the time you only want to reset the build/template/config, and keep your canonical YAML.

Typical safe reset (keep your resume content):

```bash
cp -f original-setup/CVFoundry-Lite-Build.py ./CVFoundry-Lite-Build.py
cp -f original-setup/CVFoundry-Lite-Jinja.j2 ./CVFoundry-Lite-Jinja.j2
cp -f original-setup/CVFoundry-Lite-Config.yml ./CVFoundry-Lite-Config.yml
```

Full reset (including sample canonical):

```bash
cp -f original-setup/CVFoundry-Lite-Canonical.yml ./CVFoundry-Lite-Canonical.yml
```

If you’re using git, the best reset mechanism is still:

- `git status`
- `git diff`
- `git restore <file>`
- `git checkout -- <file>` (older git)

## Troubleshooting

- **`./bootstrap.sh: Permission denied`**
  - Run `bash bootstrap.sh`.

- **YAML errors**
  - If the build fails, read the error message (it includes the missing field or parsing issue).

