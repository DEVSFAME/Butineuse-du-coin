#!/usr/bin/env python3
"""Final cleanup: ensure exactly 6 properly formatted navbar links on all pages."""
import re
import os

BASE = "."
FILES = ["products.html", "about-us.html", "blog.html", "blog/blog-post.html", "products/product.html", "index.html"]

NEW_BLOCK = """          <a href="index.html" class="navbar2_link w-nav-link">Accueil</a>
          <a href="products.html" class="navbar2_link w-nav-link">Boutique</a>
          <a href="about-us.html" class="navbar2_link w-nav-link">À Propos</a>
          <a href="#" class="navbar2_link w-nav-link">Recettes</a>
          <a href="#" class="navbar2_link w-nav-link">Musée</a>
          <a href="#" class="navbar2_link w-nav-link">Contact</a>"""

LINK_LINE_RE = re.compile(r'^\s*<a href="[^"]*" class="navbar2_link w-nav-link">[^<]*</a>.*$', re.MULTILINE)

for fname in FILES:
    fpath = os.path.join(BASE, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the <nav> menu opening
    nav_pattern = re.compile(r'(<nav\s+[^>]*class="navbar2_menu\s[^"]*"[^>]*>)')
    nav_match = nav_pattern.search(content)
    if not nav_match:
        print(f"[{fname}] No nav found, skipping")
        continue
    
    nav_start = nav_match.end()
    
    # Find dropdown start after the links
    dropdown_pattern = re.compile(r'<div\s+[^>]*class="navbar2_menu-dropdown\s')
    dropdown_match = dropdown_pattern.search(content, nav_start)
    if not dropdown_match:
        print(f"[{fname}] No dropdown found, skipping")
        continue
    
    link_section_end = dropdown_match.start()
    
    # Extract the link section
    link_section = content[nav_start:link_section_end]
    
    # Remove ALL link lines from that section
    cleaned_section = LINK_LINE_RE.sub('', link_section)
    
    # Remove any blank lines left over
    cleaned_section = re.sub(r'\n\s*\n\s*\n', '\n', cleaned_section)
    cleaned_section = re.sub(r'\n\s*\n', '\n', cleaned_section)
    cleaned_section = cleaned_section.strip('\n')
    
    # Rebuild: nav_open + NEW_BLOCK + cleaned_section (should be empty or whitespace) + rest
    before = content[:nav_start]
    after = content[link_section_end:]
    
    new_content = before + '\n' + NEW_BLOCK + '\n' + after
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    count = new_content.count('class="navbar2_link w-nav-link"')
    print(f"[{fname}] {count} links")

print("Done")