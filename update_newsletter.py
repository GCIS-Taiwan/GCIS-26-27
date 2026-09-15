import os
import glob

# Configuration
SCHOOL_LOGO_HTML = '<img src="/assets/GCIS_Logo.svg" alt="School Logo" style="height: 40px; vertical-align: middle; margin-right: 10px;">'

APP_FOOTER_HTML = '''    <footer class="site-footer">
        <img src="/assets/unboxed_logo.svg" alt="Unboxed Logo">
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

def update_html_files():
    # Recursively find all .html files in the directory and subdirectories
    html_files = glob.glob('**/*.html', recursive=True)
    
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        modified = False

        # 1. Inject school logo into nav-brand if not already present
        if '<a href' in content and SCHOOL_LOGO_HTML not in content:
            content = content.replace(
                '<a href="../../index.html" class="nav-brand">',
                f'<a href="../../index.html" class="nav-brand">{SCHOOL_LOGO_HTML}'
            )
            content = content.replace(
                '<a href="index.html" class="nav-brand">',
                f'<a href="index.html" class="nav-brand">{SCHOOL_LOGO_HTML}'
            )
            modified = True

        # 2. Inject CSS rules into <style> if .site-footer isn't already there
        if '</style>' in content and '.site-footer' not in content:
            content = content.replace('</style>', f'{CSS_SNIPPET}\n    </style>')
            modified = True

        # 3. Inject site-footer before </body> if not already present
        if '</body>' in content and 'class="site-footer"' not in content:
            content = content.replace('</body>', f'{APP_FOOTER_HTML}\n</body>')
            modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")
        else:
            print(f"Skipped (already updated): {filepath}")

if __name__ == '__main__':
    update_html_files()