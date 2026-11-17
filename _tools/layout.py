#!/usr/bin/env python3
"""Refresh the shared <head> assets, header/nav and footer in every page.

Each index.html contains marker comments; everything between a marker pair is
regenerated with the correct relative paths for that page's depth, and the nav
link for the current page gets aria-current="page".

    python3 _tools/layout.py

Edit NAV / HEADER / FOOTER below, then re-run. Safe to run repeatedly.
"""
import hashlib
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (label, site path, children)
NAV = [
    ("Home", "", []),
    ("People", "people/", [("Current", "people/current/"), ("Visiting", "people/visiting/"), ("Past", "people/past/")]),
    ("Research", "research/", []),
    ("Workshop", "workshop/", [("2026", "workshop/2026/"), ("2025", "workshop/2025/")]),
    ("Seminar", "seminar/", []),
]

# ?v= is a hash of the file, so browsers fetch the new copy after every change
# instead of reusing a cached one (GitHub Pages caches for 10 minutes).
HEAD = """<link rel="icon" type="image/png" href="{r}assets/img/favicon.png">
  <link rel="stylesheet" href="{r}assets/css/style.css?v={css_v}">
  <script src="{r}assets/js/nav.js?v={js_v}" defer></script>
  <script src="{r}assets/js/lightbox.js?v={lb_v}" defer></script>"""

HEADER = """<header class="site-header">
    <div class="container">
      <a class="brand" href="{home}">
        <img src="{r}assets/img/logo/gspel-logo.png" width="600" height="197" alt="GSPE Lab">
        <span class="brand-text">
          <span class="brand-name">Global Strategy &amp; Political Economy Lab</span>
          <span class="brand-sub">KDI School of Public Policy and Management</span>
        </span>
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav class="site-nav" id="site-nav" aria-label="Main">
        <ul>
{items}
        </ul>
      </nav>
    </div>
  </header>"""

FOOTER = """<footer class="site-footer">
    <div class="container">
      <img src="{r}assets/img/logo/gspel-mark.png" width="240" height="240" alt="">
      <p><strong>Global Strategy &amp; Political Economy Lab</strong>
        KDI School of Public Policy and Management<br>
        263 Namsejong-ro, Sejong-si 30149, Republic of Korea</p>
      <p class="footer-contact"><strong>Contact</strong>
        <a href="mailto:gspel.kdis@gmail.com">gspel.kdis@gmail.com</a></p>
    </div>
  </footer>"""


def href(target, r, home):
    return (r + target) if target else home


def link(label, target, page, r, home, cls=""):
    attrs = f' href="{href(target, r, home)}"'
    if target == page:
        attrs += ' aria-current="page"'
    elif cls:
        attrs += f' class="{cls}"'
    return f"<a{attrs}>{label}</a>"


def render_nav(page, r, home):
    out = []
    pad = " " * 10
    for label, target, children in NAV:
        if not children:
            out.append(f"{pad}<li>{link(label, target, page, r, home)}</li>")
            continue
        in_section = page.startswith(target) and page != target
        out.append(f'{pad}<li class="has-dropdown">')
        out.append(f"{pad}  {link(label, target, page, r, home, 'current-section' if in_section else '')}")
        out.append(f'{pad}  <button class="dropdown-toggle" aria-expanded="false" aria-label="{label} submenu">&#9662;</button>')
        out.append(f'{pad}  <ul class="dropdown">')
        for clabel, ctarget in children:
            out.append(f"{pad}    <li>{link(clabel, ctarget, page, r, home)}</li>")
        out.append(f"{pad}  </ul>")
        out.append(f"{pad}</li>")
    return "\n".join(out)


def replace_block(html, name, content, path):
    pattern = re.compile(rf"(<!-- layout:{name} -->)(.*?)(<!-- /layout:{name} -->)", re.S)
    if not pattern.search(html):
        raise SystemExit(f"{path}: missing <!-- layout:{name} --> markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n  {content}\n  {m.group(3)}", html)


def pages():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith((".", "_")) and d != "assets")
        if "index.html" in filenames:
            yield os.path.relpath(os.path.join(dirpath, "index.html"), ROOT)


def version(rel_path):
    with open(os.path.join(ROOT, rel_path), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def main():
    css_v = version("assets/css/style.css")
    js_v = version("assets/js/nav.js")
    lb_v = version("assets/js/lightbox.js")
    for path in pages():
        page = os.path.dirname(path)
        page = page + "/" if page else ""
        r = "../" * page.count("/")
        home = r or "./"
        full = os.path.join(ROOT, path)
        with open(full, encoding="utf-8") as f:
            html = f.read()
        html = replace_block(html, "head", HEAD.format(r=r, css_v=css_v, js_v=js_v, lb_v=lb_v), path)
        html = replace_block(html, "header", HEADER.format(r=r, home=home, items=render_nav(page, r, home)), path)
        html = replace_block(html, "footer", FOOTER.format(r=r), path)
        with open(full, "w", encoding="utf-8") as f:
            f.write(html)
        print("updated", path)


if __name__ == "__main__":
    main()
