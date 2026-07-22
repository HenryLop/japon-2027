"""
Export key project docs to a printable PDF for offline use during the trip.

Requires: pip install markdown weasyprint
"""

import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Install markdown: pip install markdown")
    sys.exit(1)

try:
    from weasyprint import HTML
except ImportError:
    print("Install weasyprint: pip install weasyprint")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = Path(__file__).parent / "output"

FILES_TO_EXPORT = [
    PROJECT_ROOT / "2-Datos-del-Viaje" / "2.1-Datos-e-Items-Completos.md",
]

STYLE = """
body { font-family: 'Segoe UI', system-ui, sans-serif; max-width: 700px;
       margin: 40px auto; padding: 0 20px; color: #1a1a1a; font-size: 10pt; }
h1 { border-bottom: 2px solid #333; padding-bottom: 8px; font-size: 18pt; }
h2 { color: #2a5a2a; margin-top: 20px; font-size: 13pt; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9pt; }
th, td { border: 1px solid #ccc; padding: 4px 8px; text-align: left; }
th { background: #f0f0f0; }
a { color: #1a5a9a; }
.page-break { page-break-after: always; }
"""


def export():
    OUTPUT_DIR.mkdir(exist_ok=True)
    combined_html = f"<style>{STYLE}</style>"

    for i, filepath in enumerate(FILES_TO_EXPORT):
        if not filepath.exists():
            print(f"Skipping {filepath} (not found)")
            continue
        md_content = filepath.read_text(encoding="utf-8")
        html = markdown.markdown(md_content, extensions=["tables", "fenced_code"])
        combined_html += html
        if i < len(FILES_TO_EXPORT) - 1:
            combined_html += '<div class="page-break"></div>'

    output_path = OUTPUT_DIR / "japon-2027-guia.pdf"
    HTML(string=combined_html).write_pdf(str(output_path))
    print(f"Exported to {output_path}")


if __name__ == "__main__":
    export()
