Film sources for student project pages. Each film is a canvas animation with a deterministic `render(t)`.

Render: put the fonts next to the HTML (`npm pack @fontsource/cormorant-garamond @fontsource/ibm-plex-mono`, unpack into `fontsource-cormorant-garamond/` and `fontsource-ibm-plex-mono/`), copy the HTML to `film.html`, run `python3 render.py` (Playwright + ffmpeg). Output: 1920x1080, 30 fps, H.264, plus `poster.jpg`.
