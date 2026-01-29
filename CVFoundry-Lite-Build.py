import argparse
from dataclasses import dataclass
from datetime import datetime
import hashlib
from pathlib import Path
from typing import Any, Optional

import yaml
from jinja2 import Environment, FileSystemLoader


DEFAULT_CANONICAL_PATH = "CVFoundry-Lite-Canonical.yml"
DEFAULT_CONFIG_PATH = "CVFoundry-Lite-Config.yml"
DEFAULT_TEMPLATE_NAME = "CVFoundry-Lite-Jinja.j2"


def _load_yaml_file(path: str) -> Any:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"Failed to parse YAML: {path} ({e})") from e


def _get_in(d: Any, path: str) -> Any:
    cur = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _require(d: Any, path: str) -> Any:
    v = _get_in(d, path)
    if v is None:
        raise ValueError(f"Missing required field: {path}")
    return v


def _as_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _as_dict(value: Any) -> dict:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    return {}


def _slugify_filename(value: str) -> str:
    s = " ".join(str(value).split()).strip()
    out: list[str] = []
    for ch in s:
        if ch.isalnum():
            out.append(ch)
        elif ch in (" ", "-", "_", "."):
            out.append(" ")
    s2 = " ".join("".join(out).split())
    return s2


def _format_month_year(dt: datetime) -> str:
    return dt.strftime("%b %Y")


def fmt_date(value: Optional[str], date_format: str = "mmm yyyy") -> str:
    if value is None:
        return ""
    s = str(value).strip()
    if s == "":
        return ""
    if s.lower() == "present":
        return "Present"

    try:
        if len(s) == 4 and s.isdigit():
            dt = datetime(int(s), 1, 1)
        elif len(s) == 10 and s[4] == "-" and s[7] == "-":
            dt = datetime.strptime(s, "%Y-%m-%d")
        else:
            dt = datetime.strptime(s, "%Y-%m")
    except Exception:
        # If parsing fails, return raw input rather than breaking the build.
        return s

    if date_format == "mmm yy":
        return dt.strftime("%b %y")
    if date_format == "mmm yyyy":
        return dt.strftime("%b %Y")
    if date_format == "yyyy":
        return dt.strftime("%Y")

    return _format_month_year(dt)


@dataclass(frozen=True)
class BuildMeta:
    product: str
    version: str
    date: str
    hash: str

    @property
    def hash_short(self) -> str:
        return self.hash[:10]


def _compute_content_hash(paths: list[Path]) -> str:
    h = hashlib.sha256()
    for p in paths:
        try:
            rel = str(p.as_posix()).encode("utf-8")
            h.update(rel)
            h.update(b"\0")
            h.update(p.read_bytes())
            h.update(b"\0")
        except Exception:
            continue
    return h.hexdigest()


def _build_meta(*, canonical_path: str, config_path: str, template_path: str) -> BuildMeta:
    paths = [Path(canonical_path), Path(config_path), Path(template_path), Path(__file__)]
    content_hash = _compute_content_hash([p for p in paths if p.exists()])
    return BuildMeta(
        product="cvfoundry-lite",
        version="0.1.0",
        date=datetime.now().strftime("%Y-%m-%d"),
        hash=content_hash,
    )


def _validate_and_normalize(canonical: Any, config: Any) -> tuple[dict, dict]:
    if not isinstance(canonical, dict):
        raise ValueError("Canonical YAML must be a mapping/object")
    if not isinstance(config, dict):
        raise ValueError("Config YAML must be a mapping/object")

    personal = _as_dict(_require(canonical, "personal"))
    _require(personal, "name")
    _require(personal, "headline")

    theme = _as_dict(_require(config, "theme"))
    layout = _as_dict(_require(config, "layout"))

    # Theme defaults
    fonts = _as_dict(theme.get("fonts"))
    colors = _as_dict(theme.get("colors"))
    density = _as_dict(theme.get("density"))

    theme["fonts"] = {
        "body": str(fonts.get("body") or "system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif"),
        "mono": str(fonts.get("mono") or "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"),
    }

    theme["colors"] = {
        "background": str(colors.get("background") or "#ffffff"),
        "text": str(colors.get("text") or "#0f172a"),
        "muted": str(colors.get("muted") or "#475569"),
        "subtle": str(colors.get("subtle") or "#94a3b8"),
        "border": str(colors.get("border") or "#e2e8f0"),
        "primary": str(colors.get("primary") or "#2563eb"),
    }

    def _to_int(v: Any, default: int) -> int:
        try:
            return int(v)
        except Exception:
            return default

    def _to_float(v: Any, default: float) -> float:
        try:
            return float(v)
        except Exception:
            return default

    theme["density"] = {
        "line_height": _to_float(density.get("line_height"), 1.25),
        "section_gap_px": _to_int(density.get("section_gap_px"), 14),
        "item_gap_px": _to_int(density.get("item_gap_px"), 8),
    }

    layout_norm = {
        "page_width_px": _to_int(layout.get("page_width_px"), 900),
        "left_column_width_pct": _to_int(layout.get("left_column_width_pct"), 34),
        "show_footer_build_info": bool(layout.get("show_footer_build_info") or False),
    }

    formatting = _as_dict(config.get("formatting"))
    date_format = str(formatting.get("date_format") or "mmm yyyy")

    features = _as_dict(config.get("features"))
    features_norm = {
        "show_summary": bool(features.get("show_summary") if "show_summary" in features else True),
        "show_projects": bool(features.get("show_projects") if "show_projects" in features else True),
        "show_certifications": bool(features.get("show_certifications") if "show_certifications" in features else True),
        "show_interests": bool(features.get("show_interests") if "show_interests" in features else True),
        "show_skill_categories": bool(
            features.get("show_skill_categories") if "show_skill_categories" in features else True
        ),
    }

    # Canonical normalization
    personal_norm = {
        "name": str(personal.get("name") or ""),
        "headline": str(personal.get("headline") or ""),
        "location": str(personal.get("location") or ""),
        "email": str(personal.get("email") or ""),
        "phone": str(personal.get("phone") or ""),
        "links": [],
    }

    for link in _as_list(personal.get("links")):
        if not isinstance(link, dict):
            continue
        label = str(link.get("label") or "").strip()
        url = str(link.get("url") or "").strip()
        if label and url:
            personal_norm["links"].append({"label": label, "url": url})

    summary = [str(s).strip() for s in _as_list(canonical.get("summary")) if str(s).strip()]

    skills_in = _as_list(canonical.get("skills"))
    skills: list[dict] = []
    for s in skills_in:
        if not isinstance(s, dict):
            continue
        cat = str(s.get("category") or "").strip()
        items = [str(i).strip() for i in _as_list(s.get("items")) if str(i).strip()]
        if cat and items:
            skills.append({"category": cat, "items": items})

    def _norm_entries(entries: Any, required_fields: list[str]) -> list[dict]:
        out: list[dict] = []
        for e in _as_list(entries):
            if not isinstance(e, dict):
                continue
            for f in required_fields:
                if not str(e.get(f) or "").strip():
                    raise ValueError(f"Entry missing required field: {f}")
            out.append(e)
        return out

    experience_raw = _as_list(canonical.get("experience"))
    experience: list[dict] = []
    for r in experience_raw:
        if not isinstance(r, dict):
            continue
        company = str(r.get("company") or "").strip()
        role = str(r.get("role") or "").strip()
        if not company or not role:
            raise ValueError("Each experience entry requires company and role")
        highlights = [str(h).strip() for h in _as_list(r.get("highlights")) if str(h).strip()]
        tags = [str(t).strip() for t in _as_list(r.get("tags")) if str(t).strip()]
        experience.append(
            {
                "company": company,
                "location": str(r.get("location") or "").strip(),
                "role": role,
                "start_date": str(r.get("start_date") or "").strip(),
                "end_date": str(r.get("end_date") or "").strip(),
                "highlights": highlights,
                "tags": tags,
            }
        )

    projects_raw = _as_list(canonical.get("projects"))
    projects: list[dict] = []
    for p in projects_raw:
        if not isinstance(p, dict):
            continue
        name = str(p.get("name") or "").strip()
        if not name:
            continue
        bullets = [str(b).strip() for b in _as_list(p.get("bullets")) if str(b).strip()]
        projects.append(
            {
                "name": name,
                "role": str(p.get("role") or "").strip(),
                "link": str(p.get("link") or "").strip(),
                "bullets": bullets,
            }
        )

    education = []
    for e in _as_list(canonical.get("education")):
        if not isinstance(e, dict):
            continue
        school = str(e.get("school") or "").strip()
        degree = str(e.get("degree") or "").strip()
        if not school or not degree:
            continue
        details = [str(d).strip() for d in _as_list(e.get("details")) if str(d).strip()]
        education.append(
            {
                "school": school,
                "degree": degree,
                "location": str(e.get("location") or "").strip(),
                "start_date": str(e.get("start_date") or "").strip(),
                "end_date": str(e.get("end_date") or "").strip(),
                "details": details,
            }
        )

    certifications = []
    for c in _as_list(canonical.get("certifications")):
        if not isinstance(c, dict):
            continue
        name = str(c.get("name") or "").strip()
        issuer = str(c.get("issuer") or "").strip()
        if not name:
            continue
        certifications.append({"name": name, "issuer": issuer, "date": str(c.get("date") or "").strip()})

    extras = _as_dict(canonical.get("extras"))
    extras_norm = {
        "interests": [str(i).strip() for i in _as_list(extras.get("interests")) if str(i).strip()],
    }

    normalized = {
        "personal": personal_norm,
        "summary": summary,
        "skills": skills,
        "experience": experience,
        "projects": projects,
        "education": education,
        "certifications": certifications,
        "extras": extras_norm,
    }

    cfg_norm = {
        "theme": theme,
        "layout": layout_norm,
        "features": features_norm,
        "date_format": date_format,
    }

    return normalized, cfg_norm


def _default_output_name(person_name: str) -> str:
    safe = _slugify_filename(person_name)
    if safe == "":
        safe = "Resume"
    return f"CVFoundry-Lite-{safe}.html"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", default=DEFAULT_CANONICAL_PATH)
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--template", default=DEFAULT_TEMPLATE_NAME)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    canonical_path = str(args.canonical)
    config_path = str(args.config)
    template_path = str(args.template)

    canonical = _load_yaml_file(canonical_path)
    config = _load_yaml_file(config_path)

    data, cfg = _validate_and_normalize(canonical, config)

    build_meta = _build_meta(
        canonical_path=canonical_path,
        config_path=config_path,
        template_path=template_path,
    )

    template_parent = str(Path(template_path).parent) if str(Path(template_path).parent) != "." else "."
    env = Environment(loader=FileSystemLoader(template_parent), autoescape=True)
    env.filters["fmt_date"] = fmt_date

    tpl = env.get_template(Path(template_path).name)

    out_html = tpl.render(
        personal=data["personal"],
        summary=data["summary"],
        skills=data["skills"],
        experience=data["experience"],
        projects=data["projects"],
        education=data["education"],
        certifications=data["certifications"],
        extras=data["extras"],
        theme=cfg["theme"],
        layout=cfg["layout"],
        features=cfg["features"],
        date_format=cfg["date_format"],
        build_meta={
            "product": build_meta.product,
            "version": build_meta.version,
            "date": build_meta.date,
            "hash": build_meta.hash,
            "hash_short": build_meta.hash_short,
        },
    )

    out_path = Path(args.output) if args.output else Path(_default_output_name(data["personal"]["name"]))
    out_path.write_text(out_html, encoding="utf-8")
    print(f"Generated {out_path}")


if __name__ == "__main__":
    main()
