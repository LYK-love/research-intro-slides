# Research Introduction Slides
> You can use AI to translate or explain this document and the rest of the project's documentation in your preferred language.
>
> 你可以使用 AI 将本文档和本项目的其他文档翻译成你偏好的语言，或为你解读其中的内容。

A six-slide English introduction to Yukuan Lu's research in world models and vision, prepared for Fall 2027 PhD advisor conversations.

The presentation is a single offline-ready HTML file with embedded fonts, keyboard navigation, and inline text editing. Every slide uses a fixed 16:9 canvas that scales uniformly on desktop and mobile.

![Slide overview](docs/preview.png)

## Run locally

Open `src/index.html` in a browser, or serve it with Python 3:

```bash
python -m http.server 8000 --bind 127.0.0.1 --directory src
```

Then open [localhost:8000](http://localhost:8000). No application dependencies or build step are required.

## Present and edit

- Next/previous: arrow keys, Space, Page Up/Down, mouse wheel, or horizontal swipe.
- First/last: Home / End.
- Edit: press E or hover over the top-left corner; click text to change it.
- Finish editing: press Escape or click Done.
- Download an updated HTML file: Ctrl+S / Cmd+S or Save HTML.

Edits are saved in browser local storage for the current URL. To commit changes, download the edited HTML and replace `src/index.html`; browser edits do not modify the repository automatically.

Colors and font families are in `:root`; entrance animations use `.reveal`. See [design notes](docs/design.md).

## Test

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python -m unittest discover -s tests -v
```

GitHub Actions runs these checks on pushes and pull requests.

## Research reference

[Improving Weak World Models Behind Strong Agents in Atari Pong](https://arxiv.org/html/2607.15142v3)

## License and attribution

Project code is MIT licensed. The embedded Jost and JetBrains Mono fonts retain their SIL Open Font License; license texts are in `licenses/`. The presentation was created using [Frontend Slides](https://github.com/zarazhangrui/frontend-slides), with the Monochrome / Ivory Ledger design direction. See [third-party notices](docs/third-party.md).

This project was written collaboratively by humans and AI.
