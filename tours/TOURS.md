# Tours: file format and how the viewer loads them

## Folder layout (in the repository, next to index.html)

```
tours/
  index.json                      list of tours shown in the picker  (your curator app regenerates this)
  tour.schema.json                JSON Schema, for validating in the curator app
  <tour-id>/
    tour.json                     the tour
    media/   *.jpg *.mp3          images and audio, referenced by relative path
    text/    *.txt                optional longer text, referenced with text_file
```

Paths inside `tour.json` are relative to the tour's own folder, so a tour folder can be moved or copied as a unit.

## URLs

| URL | What it does |
|---|---|
| `index.html` | Museum kiosk. Unchanged. |
| `index.html?mode=tour` | Web view: tour picker, then the guided tour. No idle reset or attract loop. |
| `index.html?tour=<id>` | Opens straight into one tour (good for QR codes at exhibits). |
| `index.html?tour=<id>&stop=3` | Opens at stop 3 (the viewer keeps `stop` updated as you move, so a link can be shared mid-tour). |
| `index.html?mode=curator` | Curator view, unchanged. |

## index.json

```json
{ "tours": [ { "id": "dunkeld-heritage-walk", "title": "...", "description": "...",
               "duration_min": 20, "stops": 3, "image": "dunkeld-heritage-walk/media/cover.jpg",
               "file": "dunkeld-heritage-walk/tour.json" } ] }
```
The browser cannot list a folder, so the viewer needs this manifest. The curator app should rewrite it whenever a tour is added, renamed or removed.

## tour.json

Tour level (only `title` and `stops` are required):

| Field | Meaning |
|---|---|
| `title`, `description`, `author`, `duration_min` | Shown on the intro card. |
| `here` | `{lon, lat, label}`: a pulsing blue "You're here" marker, and the walking direction to stop 1 is computed from it. |
| `overview` | Camera for the intro screen: `{lon, lat, zoom, pitch, bearing}`. Defaults to `here`, then stop 1. |
| `start_year` / `end_year` | Year shown on the intro / when the tour finishes. Default: the present. |
| `intro` or `intro_file`, `outro` | Text on the intro and finish cards. |
| `image`, `image_caption` | Image on the intro card. |

Each stop:

| Field | Meaning |
|---|---|
| `title`, `lon`, `lat` | Required. |
| `zoom` (17), `pitch` (55), `bearing` (current), `fly_ms` (3500) | Camera when arriving. |
| `year` | Timeline year when you arrive (e.g. 1300). Jumps by default; add `year_sweep_ms` to animate from the current year instead. |
| `year_steps` | Timed changes after arrival: `[{ "after_ms": 9000, "year": 2026, "mode": "sweep", "duration_ms": 5000 }]`. `mode` is `jump` (default) or `sweep`. This is the "flick into modern times" effect. |
| `season`, `night` | Optional scene settings for the stop. |
| `text` or `text_file`, `image`, `image_caption`, `audio` | Content. Every one is optional; a stop can be audio only, image only, etc. |
| `advance` | `manual` (default) or `auto`. Auto moves on when the audio ends, or after `dwell_ms` (default 15000) if there is no audio. |

The viewer adds numbered pins, a dashed line to the next stop, and "Next: <title>, 250 m north-east, about 3 min walk" automatically from the coordinates.

## Notes for the curator app

- Coordinates are WGS84 lon/lat. The mapped area is roughly 2 km around (-3.5806, 56.5627); stops outside it will show an empty map, and the viewer logs a console warning.
- Timeline range is the slider range (starts at 1200); years outside it are clamped.
- Keep images under ~300 KB and audio as mp3/m4a, since many visitors will be on mobile data.
- Browsers block audio autoplay until the visitor has tapped something. Tapping Begin / Next counts, so audio normally starts on its own, but if it does not, the visitor sees the play button.
- Tours are fetched with `cache: no-cache`, so edits show up on the next page load.
