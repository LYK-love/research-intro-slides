# Design

This deck supports a short research introduction in a live conversation. Six slides cover background, interests, motivation, research questions, advisor fit, and strengths.

## Layout and typography

The Monochrome / Ivory Ledger direction uses cream paper (`#FAFADF`), dark ink (`#1A1A16`), thin rules, and generous whitespace. Jost supplies light headlines and body text; JetBrains Mono supplies structural labels. Both fonts are embedded in the HTML for offline use.

All content is authored at 1920 × 1080. A viewport wrapper scales the entire stage uniformly, preserving its layout on phones. Portrait displays have empty space above and below the slides.

## Behavior

`SlidePresentation` controls the active slide, URL fragment, navigation, and scaling. Hidden slides are inert and excluded from accessibility navigation. `InlineEditor` handles text-only edits, local storage, and downloading a portable HTML copy.

The page makes no runtime network requests. The paper link opens an external site only when followed. No analytics or backend is included.

## Maintenance

Edit slide content in `src/index.html`, keeping one idea per slide. Use the shared CSS classes and fixed canvas measurements. Long edits can exceed the intended layout: recheck all slides after changing content. Print CSS displays all slides in their final visual state, one slide per page; interactive animations do not appear in print.

The screenshot in `docs/preview.png` is an overview of the initial published version. Update it after material visual revisions.
