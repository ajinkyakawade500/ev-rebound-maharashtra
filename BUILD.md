# Build notes

The numerical analysis uses only the Python standard library and supports Python 3.10 or later.

Run commands from the repository root in this order:

```bash
python analysis/reproduce.py
python analysis/check_model.py
python -m pip install -r requirements-build.txt
python analysis/make_figures.py
python scripts/build_pdfs.py
```

The build scripts do not download sources, call external services or fit statistical models. Figures use Matplotlib. PDFs use ReportLab and read the Markdown files as their content source. Mathematical expressions are rendered locally with Matplotlib, so a LaTeX installation is not required.

DejaVu fonts are required for PDF typography. The builder checks a standard Linux font path and Matplotlib's bundled font directory. To use another installation, set the `EV_REBOUND_FONT_DIR` environment variable to the folder containing the DejaVu Sans, Serif and Mono TTF files. The required font filenames are listed in `scripts/build_pdfs.py`.

The Markdown-to-PDF builder intentionally supports only the headings, paragraphs, bullet lists, links, simple tables, image references, equations and page-break comments used in these editions. It is not a general Markdown converter.

To validate future changes, inspect the regenerated PDFs as rendered pages in addition to reading extracted text. Changes to scenario assumptions should also be reflected in the narrative, which is not automatically numerically templated. The script outputs remain the authoritative arithmetic for those assumptions.
