# KNR Bionik — Strona internetowa / Website

## PL — Instrukcja

### Struktura projektu

```
├── content/          # Treści stron (Markdown + YAML frontmatter)
│   ├── pl/           # Treści po polsku
│   └── en/           # Treści po angielsku
├── data/             # Dane strukturalne (YAML)
│   ├── board.yaml    # Zarząd i opiekun
│   ├── projects.yaml # Projekty (oba języki)
│   ├── achievements.yaml
│   ├── contact.yaml  # Dane kontaktowe, linki social media
│   ├── recruitment.yaml
│   └── stats.yaml    # Statystyki (założone, członkowie, itp.)
├── templates/        # Szablony HTML (Jinja2)
│   ├── index.html    # Strona główna (wszystkie sekcje)
│   └── project.html  # Strona szczegółowa projektu
├── static/           # Pliki statyczne
│   ├── css/custom.css
│   ├── js/main.js
│   └── images/       # Logo i obrazy
├── admin/            # Panel administracyjny (Decap CMS)
│   ├── index.html    # Wejście do panelu
│   └── config.yml    # Konfiguracja CMS (backend GitHub)
├── build.py          # Generator strony statycznej
├── serve.py          # Serwer deweloperski (port 1313)
├── requirements.txt  # Zależności Pythona
└── .github/workflows/deploy.yml  # CI/CD GitHub Pages
```

### Jak uruchomić lokalnie

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build.py        # Buduje stronę do public/
python serve.py        # Serwer na http://localhost:1313
```

### Jak aktualizować treści

**Przez panel admina (zalecane):**
1. Wejdź na `https://<twoja-domena>/admin/`
2. Zaloguj się przez GitHub
3. Edytuj treści w interfejsie graficznym
4. Kliknij „Opublikuj" — CMS commituje zmiany do repozytorium
5. GitHub Actions automatycznie przebuduje stronę

**Ręcznie (przez pliki):**
- **Treści tekstowe** — edytuj pliki `.md` w `content/pl/` i `content/en/`
- **Dane strukturalne** — edytuj pliki `.yaml` w `data/`
- **Projekty** — `data/projects.yaml` — dodaj wpis z polami: `name`, `slug`, `category`, `description`, `details`, `icon`, `gradient`
- **Zarząd** — `data/board.yaml`
- **Kontakt / social media** — `data/contact.yaml`

Po ręcznej edycji:
```bash
python build.py   # Przebuduj
git add . && git commit -m "Aktualizacja treści" && git push
```

### Jak dodać nowy projekt

1. Edytuj `data/projects.yaml`
2. Dodaj wpis w sekcji `pl:` i `en:` z unikalnymi polami `slug`
3. Przebuduj (`python build.py`) — strona projektu wygeneruje się automatycznie

### Jak zmienić wygląd

- **CSS** — `static/css/custom.css` (style niestandardowe)
- **Tailwind** — klasy w `templates/index.html` i `templates/project.html`
- **Kolory marki** — konfiguracja Tailwind w tagach `<script>` w szablonach (brand, navy)
- **Logo** — zamień `static/images/logo_color.svg`

### Deployment

Strona deployowana jest automatycznie przez GitHub Actions na GitHub Pages.
Każdy push na branch `main` uruchamia pipeline:
1. Instaluje zależności Pythona
2. Uruchamia `build.py`
3. Deployuje folder `public/` na GitHub Pages

---

## EN — Instructions

### Project structure

```
├── content/          # Page content (Markdown + YAML frontmatter)
│   ├── pl/           # Polish content
│   └── en/           # English content
├── data/             # Structured data (YAML)
│   ├── board.yaml    # Board members and supervisor
│   ├── projects.yaml # Projects (both languages)
│   ├── achievements.yaml
│   ├── contact.yaml  # Contact info, social media links
│   ├── recruitment.yaml
│   └── stats.yaml    # Stats (founded, members, etc.)
├── templates/        # HTML templates (Jinja2)
│   ├── index.html    # Main page (all sections)
│   └── project.html  # Project detail page
├── static/           # Static assets
│   ├── css/custom.css
│   ├── js/main.js
│   └── images/       # Logo and images
├── admin/            # Admin panel (Decap CMS)
│   ├── index.html    # Panel entry point
│   └── config.yml    # CMS config (GitHub backend)
├── build.py          # Static site generator
├── serve.py          # Dev server (port 1313)
├── requirements.txt  # Python dependencies
└── .github/workflows/deploy.yml  # CI/CD GitHub Pages
```

### How to run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build.py        # Builds site to public/
python serve.py        # Server at http://localhost:1313
```

### How to update content

**Via admin panel (recommended):**
1. Go to `https://<your-domain>/admin/`
2. Log in with GitHub
3. Edit content through the GUI
4. Click "Publish" — the CMS commits changes to the repo
5. GitHub Actions automatically rebuilds the site

**Manually (via files):**
- **Text content** — edit `.md` files in `content/pl/` and `content/en/`
- **Structured data** — edit `.yaml` files in `data/`
- **Projects** — `data/projects.yaml` — add entry with fields: `name`, `slug`, `category`, `description`, `details`, `icon`, `gradient`
- **Board** — `data/board.yaml`
- **Contact / social media** — `data/contact.yaml`

After manual edits:
```bash
python build.py   # Rebuild
git add . && git commit -m "Update content" && git push
```

### How to add a new project

1. Edit `data/projects.yaml`
2. Add an entry under both `pl:` and `en:` sections with a unique `slug`
3. Rebuild (`python build.py`) — project detail page is generated automatically

### How to change appearance

- **CSS** — `static/css/custom.css` (custom styles)
- **Tailwind** — classes in `templates/index.html` and `templates/project.html`
- **Brand colors** — Tailwind config in `<script>` tags in templates (brand, navy)
- **Logo** — replace `static/images/logo_color.svg`

### Deployment

The site is automatically deployed via GitHub Actions to GitHub Pages.
Every push to `main` triggers the pipeline:
1. Installs Python dependencies
2. Runs `build.py`
3. Deploys the `public/` folder to GitHub Pages

### Admin panel notes

- **On production** (GitHub Pages): the admin panel uses the GitHub backend — you log in with GitHub and edits are committed to the repo
- **On localhost**: the `test-repo` backend is used — no authentication required (this is by design for local development). Content shown is demo/empty since it runs in-memory, not connected to actual files. To preview real content locally, edit files directly and run `python build.py`
