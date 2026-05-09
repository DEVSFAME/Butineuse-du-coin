#!/usr/bin/env python3
"""
Phase 2: Navbar Glassmorphism - Header-01 Design Implementation
==============================================================
Implements scroll-aware navbar with glassmorphism effect on all 6 pages.

Features:
  - Scroll = 0: transparent background, white text, logo-clair.png
  - Scroll > 50px: rgba(255,255,255,0.85) + backdrop-filter: blur(20px)
                    + box-shadow + dark text + logo-foncé.png
  - Smooth transition: all 0.3s ease
  - Mobile compatible (preserves hamburger menu)

Target pages: index.html, products.html, about-us.html, blog.html,
              blog/blog-post.html, products/product.html
"""

import re
import os

BASE = "."
FILES = [
    "index.html",
    "products.html",
    "about-us.html",
    "blog.html",
    "blog/blog-post.html",
    "products/product.html",
]

# ── CSS to inject (before </head>) ──────────────────────────────────────────
GLASSMORPHISM_CSS = """<!-- Phase 2: Navbar Glassmorphism CSS -->
<style>
  /* ── Initial state (scroll = 0) ── */
  .navbar2_component {
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    transition: background 0.3s ease,
                box-shadow 0.3s ease,
                backdrop-filter 0.3s ease,
                -webkit-backdrop-filter 0.3s ease,
                border-color 0.3s ease;
  }

  .navbar2_component .navbar2_link,
  .navbar2_component .navbar2_dropdwn-toggle,
  .navbar2_component .navbar2_button-wrapper {
    color: #ffffff;
    transition: color 0.3s ease;
  }

  .navbar2_component .navbar2_logo-image {
    transition: opacity 0.2s ease;
  }

  /* ── Scrolled state (scroll > 50px) ── */
  .navbar2_component.scrolled {
    background: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08),
                0 4px 12px rgba(0, 0, 0, 0.04);
    border-bottom: 1px solid rgba(0, 0, 0, 0.06) !important;
  }

  .navbar2_component.scrolled .navbar2_link,
  .navbar2_component.scrolled .navbar2_dropdwn-toggle,
  .navbar2_component.scrolled .navbar2_button-wrapper {
    color: #0d0901;
  }

  /* ── Link hover effect ── */
  .navbar2_component.scrolled .navbar2_link:hover {
    color: var(--_primitives---colors--sun, #fbac0c);
  }

  /* ── Dropdown chevron color inheritance ── */
  .navbar2_component .navbar2_dropdwn-toggle svg path {
    transition: fill 0.3s ease;
  }

  /* ── Button in navbar ── */
  .navbar2_component .button.is-alternate {
    transition: color 0.3s ease, border-color 0.3s ease;
  }

  .navbar2_component.scrolled .button.is-alternate {
    color: #0d0901;
    border-color: #0d0901;
  }
</style>"""

# ── JS to inject (before </body>) ───────────────────────────────────────────
GLASSMORPHISM_JS = """<!-- Phase 2: Navbar Glassmorphism Scroll Behavior -->
<script>
  (function() {
    var nav = document.querySelector('.navbar2_component');
    var logoImg = document.querySelector('.navbar2_logo-image');
    if (!nav || !logoImg) return;

    var LOGO_LIGHT = 'images/logo-clair.png';
    var LOGO_DARK = 'logo-fonce.png';
    var SCROLL_THRESHOLD = 50;

    function onScroll() {
      var scrolled = window.scrollY > SCROLL_THRESHOLD;
      if (scrolled) {
        nav.classList.add('scrolled');
        if (logoImg.getAttribute('src') !== LOGO_DARK) {
          logoImg.setAttribute('src', LOGO_DARK);
        }
      } else {
        nav.classList.remove('scrolled');
        if (logoImg.getAttribute('src') !== LOGO_LIGHT) {
          logoImg.setAttribute('src', LOGO_LIGHT);
        }
      }
    }

    // Set initial state
    onScroll();

    // Listen for scroll with passive flag for performance
    window.addEventListener('scroll', onScroll, { passive: true });
  })();
</script>"""

# ── Main injection logic ─────────────────────────────────────────────────────

def inject_into_page(filepath):
    """Inject CSS and JS into a single HTML page."""
    if not os.path.exists(filepath):
        print(f"  [SKIP] {filepath} not found")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1) Inject CSS before </head>
    head_close_pattern = re.compile(r'</head>', re.IGNORECASE)
    if not head_close_pattern.search(content):
        print(f"  [WARN] {filepath}: no </head> found, skipping CSS injection")
    else:
        # Only inject if not already present
        if 'Phase 2: Navbar Glassmorphism CSS' not in content:
            content = head_close_pattern.sub(
                '\n' + GLASSMORPHISM_CSS + '\n</head>', content, count=1
            )
            print(f"  [CSS] Injected glassmorphism CSS into {filepath}")
        else:
            print(f"  [CSS] Already present in {filepath}, skipping")

    # 2) Inject JS before </body>
    body_close_pattern = re.compile(r'</body>', re.IGNORECASE)
    if not body_close_pattern.search(content):
        print(f"  [WARN] {filepath}: no </body> found, skipping JS injection")
    else:
        if 'Phase 2: Navbar Glassmorphism Scroll' not in content:
            content = body_close_pattern.sub(
                '\n' + GLASSMORPHISM_JS + '\n</body>', content, count=1
            )
            print(f"  [JS]  Injected scroll behavior JS into {filepath}")
        else:
            print(f"  [JS]  Already present in {filepath}, skipping")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    else:
        print(f"  [INFO] {filepath}: no changes needed")
        return True


# ── Run ───────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("PHASE 2: Navbar Glassmorphism - Header-01 Design")
    print("=" * 60)

    success = 0
    for fname in FILES:
        fpath = os.path.join(BASE, fname)
        print(f"\nProcessing: {fname}")
        if inject_into_page(fpath):
            success += 1

    print(f"\n{'=' * 60}")
    print(f"Done. {success}/{len(FILES)} pages processed successfully.")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()