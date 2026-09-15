import os
import glob
from pathlib import Path

# Base asset filenames
SCHOOL_LOGO_FILE = 'GCIS_logo.svg'
UNBOXED_LOGO_FILE = 'unboxed_logo.svg'

APP_FOOTER_HTML_TEMPLATE = '''    <footer class="site-footer">
        <img src="{unboxed_path}" alt="Unboxed Logo">
        <span>Crafted for our classroom using Unboxed</span>
    </footer>'''

CSS_SNIPPET = '''
        .site-footer {
            text-align: center;
            margin-top: 40px;
            padding: 25px 20px;
            font-size: 0.85rem;
            color: var(--subtext-color);
            background-color: var(--card-bg);
            border-top: 1px solid var(--border-color);
            transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
        }

        .site-footer img {
            height: 24px;
            vertical-align: middle;
            margin-right: 6px;
        }'''

def get_relative_prefix(filepath):
    # Calculate relative path back to root depending on depth
    path = Path(filepath)
    depth = len(path.parts) - 1  # root files have depth 1 (filename) -> parts: ('index.html',)
    if depth == 1:
        return ""
    else:
        return "../" * (depth - 1)

def update_html_files():
    html_files = glob.glob('**/*.html', recursive=True)
    
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        modified = False
        prefix = get_relative_prefix(filepath)
        
        school_logo_src = f'{prefix}assets/{SCHOOL_LOGO_FILE}'
        unboxed_logo_src = f'{prefix}assets/{UNBOXED_LOGO_FILE}'
        
        school_logo_html = f'<img src="{school_logo_src}" alt="School Logo" style="height: 40px; vertical-align: middle; margin-right: 10px;">'
        app_footer_html = APP_FOOTER_HTML_TEMPLATE.format(unboxed_path=unboxed_logo_src)

        # 1. Clean up old/broken logo insertions if any exist from previous runs, then re-insert properly
        # (Or handle safe insertion into nav-brand)
        if '<a href' in content and 'alt="School Logo"' not in content:
            content = content.replace(
                '<a href="../../index.html" class="nav-brand">',
                f'<a href="../../index.html" class="nav-brand">{school_logo_html}'
            )
            content = content.replace(
                '<a href="index.html" class="nav-brand">',
                f'<a href="index.html" class="nav-brand">{school_logo_html}'
            )
            modified = True

        # 2. Inject CSS rules into <style> if .site-footer isn't already there
        if '</style>' in content and '.site-footer' not in content:
            content = content.replace('</style>', f'{CSS_SNIPPET}\n    </style>')
            modified = True

        # 3. Inject site-footer before </body> if not already present
        if '</body>' in content and 'class="site-footer"' not in content:
            content = content.replace('</body>', f'{app_footer_html}\n</body>')
            modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")
        else:
            print(f"Skipped (already updated): {filepath}")

if __name__ == '__main__':
    update_html_files()