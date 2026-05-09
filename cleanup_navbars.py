#!/usr/bin/env python3
"""Remove duplicate navbar link blocks - keep only the first complete set of 6 links."""
import re
import os

BASE = "."
FILES = ["products.html", "about-us.html", "blog.html", "blog/blog-post.html", "products/product.html", "index.html"]

TARGET_SET = [
    '<a href="index.html" class="navbar2_link w-nav-link">Accueil</a>',
    '<a href="products.html" class="navbar2_link w-nav-link">Boutique</a>',
    '<a href="about-us.html" class="navbar2_link w-nav-link">À Propos</a>',
    '<a href="#" class="navbar2_link w-nav-link">Recettes</a>',
    '<a href="#" class="navbar2_link w-nav-link">Musée</a>',
    '<a href="#" class="navbar2_link w-nav-link">Contact</a>',
]

# Regex to match a SINGLE navbar link line (with leading whitespace)
LINK_RE = re.compile(r'[ \t]*<a href="[^"]*" class="navbar2_link w-nav-link">[^<]*</a>')

for fname in FILES:
    fpath = os.path.join(BASE, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    first_link_idx = -1
    last_link_idx = -1
    replaced = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if LINK_RE.fullmatch(line):
            if first_link_idx == -1:
                first_link_idx = len(new_lines)
                # Insert the 6 correct links
                for link in TARGET_SET:
                    new_lines.append('          ' + link)
                replaced = True
                # Skip all consecutive link lines
                while i < len(lines) and LINK_RE.fullmatch(lines[i]):
                    i += 1
                continue
            else:
                # Skip this duplicate link line
                i += 1
                continue
        else:
            new_lines.append(line)
            i += 1
    
    new_content = '\n'.join(new_lines)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    count = new_content.count('class="navbar2_link w-nav-link"')
    print(f"[{fname}] {count} links (expected 6)")

print("Done")