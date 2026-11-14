# GSPE Lab website

Static site for the Global Strategy & Political Economy Lab (KDI School), hosted on GitHub Pages. Plain HTML/CSS/JS — no build step, no framework.

## Structure

Clean URLs: each page is a folder with its own `index.html`.

```
index.html                  About (Home): tagline, lab intro, wall photo, upcoming workshop, About the Lab (01/02)
people/index.html           People landing — links to Current, Visiting, Past
people/current/index.html   Current members (Faculty subsection; add a Student subsection when there are current students)
people/visiting/index.html  Visiting scholars (faculty-style bio + "is visiting" note)
people/past/index.html      Past members (Student Assistants, each with a "helped organize" note)
research/index.html         Collaborative Research (working papers with abstracts, work in progress)
workshop/index.html         Workshop intro, table of workshops (2027 upcoming, 2026, 2025), photo grid
workshop/2026/index.html    2026 program (presenter names link to personal websites) + poster preview
workshop/2025/index.html    2025 program + poster preview
seminar/index.html          KDI School Research Seminar Series talks hosted by lab members, by year (newest first)
assets/pdf/                 Workshop poster PDFs (copied from _source)
assets/img/posters/         Poster page previews, rendered with `gs -sDEVICE=png16m -r110` then `sips --resampleWidth 1000`
assets/css/style.css        Shared styles (all pages)
assets/js/nav.js            Mobile menu + dropdown toggles
assets/img/hero.jpg         Home wall photo (from _source/Workshop/select_photos/main.jpeg)
assets/img/workshop/        Workshop grid photos (from select_photos/1–6)
assets/img/people/          Headshots (slug names, e.g. dongil-lee.jpg)
assets/img/logo/            Original logo files + web copies gspel-logo.png (header) and gspel-mark.png (footer)
assets/img/favicon.png      From logo/small_logo_white.png
_tools/layout.py            Regenerates the shared head/header/nav/footer in every page
_source/                    Raw materials: bios, posters, papers, original photos
_config.yml                 Jekyll config (excludes CLAUDE.md; _source/ and _tools/ are excluded automatically)
```

`_source/` holds the original People/, Research/, Workshop/ folders. They were moved there because macOS is case-insensitive, so `People/` and `people/` cannot coexist. Never link to files in `_source/` from the site.

## Shared layout (header, nav, footer)

Every page has three marker pairs: `<!-- layout:head -->`, `<!-- layout:header -->`, `<!-- layout:footer -->`. Do not hand-edit inside them. To change the nav, footer (address/contact), logo, or favicon, edit `NAV` / `HEADER` / `FOOTER` in `_tools/layout.py` and run:

```
python3 _tools/layout.py
```

It fixes relative paths for each page's depth and sets `aria-current="page"` (and `current-section` on the dropdown parent). New pages: copy an existing page (keep the markers), then re-run the script — it picks up every `index.html` outside `_*`, `.*` and `assets/`.

## Conventions

- **Relative links only.** Link to folders (`workshop/2026/`), not `index.html`.
- **Contact email:** gspel.kdis@gmail.com. **Address:** 263 Namsejong-ro, Sejong-si 30149, Republic of Korea.
- **Images:** never use originals. Make web copies with `sips` at JPEG quality ~80:
  - hero: `sips -s format jpeg -s formatOptions 80 --resampleWidth 2000 SRC --out assets/img/hero.jpg`
  - grid photos: `--resampleWidth 1200`
  - headshots: `-Z 600`
  Set `width`/`height` attributes on `<img>` to the output dimensions.
- **Faculty bios** follow one pattern: (1) "Name is [title] at the KDI School of Public Policy and Management." (2) research, (3) education, (4) "Personal website" link. Refer to people by surname unless their pronouns are given.
- **Seminars:** date and time, title, speaker linked to their personal website, (affiliation). Leave out the room and the host.
- **Workshop programs:** copy names, affiliations and titles exactly as printed on the posters (`_source/Workshop/<year>/…poster.pdf`). Mark anything unreadable `[CHECK]`. Each panel: label + name, then presenter name (linked to their personal website), (affiliation), title. When adding a year: new `workshop/<year>/` page, add it to `NAV` in `_tools/layout.py`, and update the table in `workshop/index.html`.

## Local preview

Folder links need a web server (opening files directly shows directory listings):

```
python3 -m http.server 8000   # then open http://localhost:8000/
```
