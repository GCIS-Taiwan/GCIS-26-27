import os
import glob
from pathlib import Path
import re

SCHOOL_LOGO_FILE = 'GCIS_logo.svg'
UNBOXED_LOGO_FILE = 'unboxed_logo.svg'

APP_FOOTER_HTML_TEMPLATE = '    <footer class="site-footer">\n        <img src="{unboxed_path}" alt="Unboxed Logo">\n        <span>Crafted for our classroom using Unboxed</span>\n    </footer>'

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
    path = Path(filepath)
    depth = len(path.parts) - 1
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
        
        new_school_logo_tag = f'<img src="{school_logo_src}" alt="School Logo" style="height: 40px; vertical-align: middle; margin-right: 10px;">'
        new_app_footer_html = APP_FOOTER_HTML_TEMPLATE.format(unboxed_path=unboxed_logo_src)

        # 1. Replace existing school logo img tag if present, otherwise insert it
        if 'alt="School Logo"' in content:
            # Regex to replace any existing school logo img tag with the updated relative path one
            content = re.sub(r'<img[^>]*alt="School Logo"[^>]*>', new_school_logo_tag, content)
            modified = True
        else:
            if '<a href' in content:
                content = content.replace(
                    '<a href="../../index.html" class="nav-brand">',
                    f'<a href="../../index.html" class="nav-brand">{new_school_logo_tag}'
                )
                content = content.replace(
                    '<a href="index.html" class="nav-brand">',
                    f'<a href="index.html" class="nav-brand">{new_school_logo_tag}'
                )
                modified = True

        # 2. Inject CSS rules into <style> if .site-footer isn't already there
        if '</style>' in content and '.site-footer' not in content:
            content = content.replace('</style>', f'{CSS_SNIPPET}\n    </style>')
            modified = True

        # 3. Replace existing footer if present, otherwise inject before </body>
        if 'class="site-footer"' in content:
            content = re.sub(r'<footer class="site-footer">.*?</footer>', new_app_footer_html, content, flags=re.DOTALL)
            modified = True
        elif '</body>' in content:
            content = content.replace('</body>', f'{new_app_footer_html}\n</body>')
            modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")
        else:
            print(f"No changes needed: {filepath}")

if __name__ == '__main__':
    update_html_files()