# CVFoundry-Lite

CVFoundry-Lite is a tiny, local-first resume generator designed for a modern workflow:

- **One resume “source of truth”**: `CVFoundry-Lite-Canonical.yml`
- **One config** (colors, fonts, toggles): `CVFoundry-Lite-Config.yml`
- **One build command** generates a **self-contained HTML resume** you can share: `CVFoundry-Lite-<Your Name>.html`

It’s aimed at friends/family who want a better system than manually editing and archiving Word/PDF variants.

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

The build script validates and normalizes inputs to reduce template breakage.

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

## Troubleshooting

- **`./bootstrap.sh: Permission denied`**
  - Run `bash bootstrap.sh`.

- **YAML errors**
  - If the build fails, read the error message (it includes the missing field or parsing issue).

