#!/bin/bash
# Convert all product markdown files to PDF for Gumroad upload
# Requires: pandoc (brew install pandoc) OR use web converter
#
# Usage: bash convert_to_pdf.sh

DIR="$(cd "$(dirname "$0")" && pwd)"
OUTDIR="$DIR/pdf_output"
mkdir -p "$OUTDIR"

echo "Converting product files to PDF..."
echo "Output directory: $OUTDIR"
echo ""

# Check for pandoc
if command -v pandoc &> /dev/null; then
    for f in "$DIR"/*.md; do
        base=$(basename "$f" .md)
        # Skip README and LISTING_METADATA
        if [[ "$base" == "README" ]] || [[ "$base" == "LISTING_METADATA" ]]; then
            continue
        fi
        echo "Converting: $base.md -> $base.pdf"
        pandoc "$f" -o "$OUTDIR/$base.pdf" \
            --pdf-engine=xelatex \
            -V geometry:margin=1in \
            -V fontsize=11pt \
            -V mainfont="Helvetica" \
            --highlight-style=tango \
            2>/dev/null || \
        pandoc "$f" -o "$OUTDIR/$base.pdf" 2>/dev/null || \
        echo "  FAILED: $base.md (try installing: brew install pandoc basictex)"
    done
    echo ""
    echo "Done. PDFs in: $OUTDIR/"
    ls -la "$OUTDIR/"
else
    echo "pandoc not installed. Install with: brew install pandoc"
    echo ""
    echo "Alternative: use these web converters:"
    echo "  - https://markdowntopdf.com (free)"
    echo "  - https://www.markdowntopdf.com (free)"
    echo "  - VS Code: install 'Markdown PDF' extension, right-click > Export"
    echo ""
    echo "Files to convert:"
    for f in "$DIR"/*.md; do
        base=$(basename "$f" .md)
        if [[ "$base" != "README" ]] && [[ "$base" != "LISTING_METADATA" ]]; then
            echo "  $base.md"
        fi
    done
fi
