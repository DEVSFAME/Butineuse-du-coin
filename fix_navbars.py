#!/usr/bin/env python3
"""Fix navbar inconsistencies across all pages before applying header-01 redesign."""

import re
import os

BASE = "/Users/yacinehida/Desktop/COPIE-SITE/Les butineuses du coin copie/les-butineuses-du-coin"

# Target files
FILES = [
    "products.html",
    "blog.html",
    "blog/blog-post.html",
    "products/product.html",
    "about-us.html",
    "index.html",
]

# --- French navbar links (uniform across all pages) ---
# Order: Accueil | Boutique | À Propos | Recettes | Musée | Contact | dropdown FR
NEW_NAV_LINKS = """          <a href="index.html" class="navbar2_link w-nav-link">Accueil</a>
          <a href="products.html" class="navbar2_link w-nav-link">Boutique</a>
          <a href="about-us.html" class="navbar2_link w-nav-link">À Propos</a>
          <a href="#" class="navbar2_link w-nav-link">Recettes</a>
          <a href="#" class="navbar2_link w-nav-link">Musée</a>
          <a href="#" class="navbar2_link w-nav-link">Contact</a>"""

# English nav links pattern (to detect and replace)
EN_LINKS_PATTERN = re.compile(
    r'(<a href="[^"]*" class="navbar2_link w-nav-link">(?:Shop|About|Recipe|Museum|Contact)</a>\s*)+',
    re.DOTALL
)

# FR links pattern (less strict, catches index.html variations)
FR_LINKS_PATTERN = re.compile(
    r'(<a href="[^"]*" class="navbar2_link w-nav-link">(?:Boutique|À Propos|Accueil|Recettes|Savoir-Faire|Musée|Contact)</a>\s*)+',
    re.DOTALL
)

# Logo SVG placeholder pattern (very long SVG in w-embed div)
LOGO_SVG_PATTERN = re.compile(
    r'<div class="navbar2_logo w-embed"><svg[^>]*>.*?</svg></div>',
    re.DOTALL
)

# Correct logo for each page (clair for index, foncé for others - but we'll unify to clair)
NEW_LOGO = """<div class="navbar2_logo-image-wrapper"><img src="images/logo-clair.png" alt="Les Butineuses du Coin Logo" class="navbar2_logo-image"></div>"""

# Dropdown defaults
OLD_DROPDOWN_EN = '<div class="navbar2_dropdwn-toggle w-dropdown-toggle">\n              <div>EN</div>'
NEW_DROPDOWN_FR = '<div class="navbar2_dropdwn-toggle w-dropdown-toggle">\n              <div>FR</div>'

OLD_DROPDOWN_OPTIONS = '<a href="#" class="navbar2_dropdown-link w-dropdown-link">English</a>\n              <a href="#" class="navbar2_dropdown-link w-dropdown-link">Francais</a>'
NEW_DROPDOWN_OPTIONS = '<a href="#" class="navbar2_dropdown-link w-dropdown-link">Anglais</a>\n              <a href="#" class="navbar2_dropdown-link w-dropdown-link">Français</a>'

for filename in FILES:
    filepath = os.path.join(BASE, filename)
    if not os.path.exists(filepath):
        print(f"SKIP: {filepath} not found")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # 1. Replace EN nav links with FR nav links
    if EN_LINKS_PATTERN.search(content):
        content = EN_LINKS_PATTERN.sub(NEW_NAV_LINKS, content, count=1)
        print(f"[{filename}] Replaced EN links with FR links")

    # 2. Also fix index.html which has FR links but wrong ones (Savoir-Faire, no Accueil, Boutique->#)
    if filename == "index.html":
        # Fix index.html specifically: replace its FR links with the uniform ones
        content = FR_LINKS_PATTERN.sub(NEW_NAV_LINKS, content, count=1)
        print(f"[{filename}] Replaced existing FR links with uniform set")

    # 3. Fix about-us.html specific issues
    if filename == "about-us.html":
        # Fix logo path from logo-foncé.png to images/logo-foncé.png ... actually use logo-clair like others
        content = content.replace('src="logo-foncé.png"', 'src="images/logo-clair.png"')
        # Also add missing Accueil link if needed
        if '>Accueil<' not in content.split('navbar2_menu')[1].split('</nav>')[0] if 'navbar2_menu' in content else True:
            # Re-run FR pattern replacement to ensure uniformity
            content = FR_LINKS_PATTERN.sub(NEW_NAV_LINKS, content, count=1)
            print(f"[{filename}] Ensured uniform FR nav links")

    # 4. Replace SVG placeholder logos with real image logo
    content = LOGO_SVG_PATTERN.sub(NEW_LOGO, content, count=1)

    # 5. Fix dropdown default to FR
    content = content.replace(OLD_DROPDOWN_EN, NEW_DROPDOWN_FR)

    # 6. Fix dropdown options
    content = content.replace(OLD_DROPDOWN_OPTIONS, NEW_DROPDOWN_OPTIONS)
    # Also fix if partly fixed already
    content = content.replace(
        '<a href="#" class="navbar2_dropdown-link w-dropdown-link">Anglais</a>\n              <a href="#" class="navbar2_dropdown-link w-dropdown-link">Francais</a>',
        NEW_DROPDOWN_OPTIONS
    )

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[{filename}] ✓ Written")
    else:
        print(f"[{filename}] No changes needed")

print("\n✅ All navbars fixed!")