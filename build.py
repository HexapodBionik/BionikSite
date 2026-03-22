#!/usr/bin/env python3
"""Static site builder for KNR Bionik website."""

import os
import shutil
from pathlib import Path

import frontmatter
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
PUBLIC_DIR = BASE_DIR / "public"
ADMIN_DIR = BASE_DIR / "admin"

# Base URL for GitHub Pages project sites (e.g. "/BionikSite")
# Set via environment variable or leave empty for root deployment
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")

LANGUAGES = ["pl", "en"]
DEFAULT_LANG = "pl"
SECTIONS = ["hero", "about", "projects", "achievements", "recruitment", "contact"]


def load_content(lang):
    """Load all markdown content for a language."""
    content = {}
    lang_dir = CONTENT_DIR / lang
    for section in SECTIONS:
        filepath = lang_dir / f"{section}.md"
        if filepath.exists():
            post = frontmatter.load(str(filepath))
            content[section] = {
                "meta": dict(post.metadata),
                "html": markdown.markdown(post.content, extensions=["extra", "nl2br"]),
                "raw": post.content,
            }
    return content


def load_data():
    """Load all YAML data files."""
    data = {}
    for ext in ("*.yaml", "*.yml"):
        for filepath in DATA_DIR.glob(ext):
            with open(filepath, encoding="utf-8") as f:
                data[filepath.stem] = yaml.safe_load(f)
    return data


def build():
    """Build the full static site."""
    # Clean output
    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)
    PUBLIC_DIR.mkdir(parents=True)

    # Copy static files
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, PUBLIC_DIR / "static")

    # Copy admin files
    if ADMIN_DIR.exists():
        shutil.copytree(ADMIN_DIR, PUBLIC_DIR / "admin")

    # Setup Jinja2
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
    )
    template = env.get_template("index.html")
    project_template = env.get_template("project.html")

    # Load data
    data = load_data()

    # Build each language
    for lang in LANGUAGES:
        content = load_content(lang)
        other_lang = "en" if lang == "pl" else "pl"

        html = template.render(
            lang=lang,
            other_lang=other_lang,
            content=content,
            data=data,
            base_url=BASE_URL,
        )

        if lang == DEFAULT_LANG:
            output_path = PUBLIC_DIR / "index.html"
        else:
            output_dir = PUBLIC_DIR / lang
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / "index.html"

        output_path.write_text(html, encoding="utf-8")
        print(f"  Built: {output_path.relative_to(BASE_DIR)}")

        # Build project detail pages
        if "projects" in data:
            for project in data["projects"].get(lang, []):
                slug = project.get("slug", "")
                if not slug:
                    continue
                details_html = markdown.markdown(
                    project.get("details", ""), extensions=["extra", "nl2br"]
                )
                proj_html = project_template.render(
                    lang=lang,
                    project=project,
                    details_html=details_html,
                    base_url=BASE_URL,
                )
                if lang == DEFAULT_LANG:
                    proj_dir = PUBLIC_DIR / "projects" / slug
                else:
                    proj_dir = PUBLIC_DIR / lang / "projects" / slug
                proj_dir.mkdir(parents=True, exist_ok=True)
                (proj_dir / "index.html").write_text(proj_html, encoding="utf-8")
                print(f"  Built: {(proj_dir / 'index.html').relative_to(BASE_DIR)}")

    print("Build complete!")


if __name__ == "__main__":
    build()
