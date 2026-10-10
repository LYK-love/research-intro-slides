# Design

The deck supports a short research introduction during a live conversation. It uses a minimal Ivory Ledger style, with one main message per slide.

## Architecture

Human-editable slide fragments, a shared stylesheet, and two browser scripts are composed by `scripts/deck.py`. `src/deck.json` defines the title and ordered slide list. The document template in `src/index.html` defines the shell, with explicit placeholders for generated content. Page counts are derived from the manifest.

The preview server composes current sources on each page request. Save and refresh to see changes. The build command produces `dist/index.html` with embedded assets, preserving offline use and portable browser exports. There are no application dependencies, bundler, or framework; Python 3 is sufficient to preview and build. Node is used only for consistent source formatting.

## Layout and typography

The Ivory Ledger direction uses cream paper (`#FAFADF`), dark ink (`#1A1A16`), thin rules, and generous whitespace. Local Jost fonts supply headlines and body text; JetBrains Mono supplies labels.

Content is authored at 1920 × 1080. The viewport scales the whole stage uniformly, preserving the layout on phones. Print CSS displays each slide on a separate page.

## Behavior

`SlidePresentation` controls active slides, URL fragments, navigation, and scaling. Hidden slides are inert. `InlineEditor` handles text-only drafts, local storage, and portable HTML downloads. Draft keys include the source text version to avoid masking source edits during development.

No runtime network requests, backend, or analytics are required. The research link opens externally when followed. See [editing workflow](workflows.md) for maintenance instructions.
