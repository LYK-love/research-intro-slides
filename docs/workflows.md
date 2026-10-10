# Editing workflow

## Content and order

1. Run `npm run dev` (or `python3 scripts/deck.py dev`).
2. Open the preview URL.
3. Edit the relevant file in `src/slides/`. Save and refresh the browser.
4. Change the `slides` list in `src/deck.json` to reorder, add, or remove pages. Footers are numbered automatically.

Each slide is a regular HTML fragment, with readable indentation and semantic markup. Keep `class="slide"` on its section. Use `data-edit` on text that should support browser editing. Reuse the existing layout classes when adding a slide; custom slide layouts belong in `src/styles/deck.css`.

To add a page, copy a similar slide, give it a descriptive filename, update its content and `aria-label`, and list it in `deck.json`. No JavaScript changes are needed.

## Appearance and behavior

- Colors and fonts: `:root` and `@font-face` in `src/styles/deck.css`.
- Layout and animation: named sections in the same stylesheet, authored at 1920 × 1080.
- Navigation, viewport scaling, URL fragments: `src/scripts/presentation.js`.
- Browser draft editing and export: `src/scripts/editor.js`.
- Document shell and editing toolbar: `src/index.html` (a build template).
- Font assets: `src/assets/fonts/`.

## Browser drafts

E toggles text editing; Escape finishes it. Browser drafts are stored locally for the current URL and source text version. Changing source text starts a fresh draft, so stale browser edits do not hide code changes. Browser edits do not write source files: copy the desired text back into the corresponding slide file to retain it in Git. Save HTML downloads a portable copy for sharing.

## Share and verify

Run `npm run build`. Open or share `dist/index.html`, which embeds the styles, scripts, and fonts and works offline. It is generated output; edit files in `src/` instead.

Run `npm run format` before committing. Run the browser checks after content or layout changes, especially for text overflow. `docs/preview.png` shows the original design; refresh it after visual redesigns.
