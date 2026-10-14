# MoreMe Design System

Source: colors and fonts ported from a Kombai-generated redesign of the login page (see git history, "Restyle login page with colors/fonts from a Kombai redesign"). Confirmed working in both light rendering contexts; not tested against a dark-mode media query since the app doesn't currently define one.

## Current scope

Applied only to the auth pages (`tasks/templates/tasks/login.html`, `tasks/templates/tasks/signup.html`), scoped under a `.auth-page` wrapper class. The rest of the app (task lists, forms, navbar chrome) intentionally still uses the original plain palette — this was a deliberate scoping choice, not an oversight. Don't assume these tokens apply site-wide unless asked to extend them.

## Palette

| Token           | Hex       | Role                                  |
| --------------- | --------- | ------------------------------------- |
| `--custard`     | `#FAF1A4` | Page/section background               |
| `--ink`         | `#660721` | Primary text                          |
| `--brick`       | `#BD4850` | Primary action color (buttons, links) |
| `--brick-hover` | `#A83B44` | Hover state for brick elements        |
| `--rule`        | `#A78A54` | Borders/dividers                      |
| `--field`       | `#FFF7CE` | Input background                      |
| `--field-focus` | `#F8E998` | Input background on focus             |

Status-row pastel colors (used site-wide on the task list, unrelated to the auth palette above): pending = pastel red `#ffcdd2`, in progress = pastel orange `#ffe0b2`, completed = pastel green `#c8e6c9`.

## Typography

- **Display/headings:** Urbanist, weights 600/700/800, uppercase, tight letter-spacing (`-0.03em` to `-0.065em` depending on size)
- **Body/UI:** Fira Sans, weights 400/500/600/700
- Both loaded via Google Fonts CDN (`fonts.googleapis.com`), not self-hosted.

## Known gotcha when editing these templates

This project's Django templates get auto-reformatted by an editor hook after every write. That reformatter will sometimes split a Django template tag's `{% ... %}` across a line break — and Django 3.2's template parser silently mis-parses that (an `{% if %}` or `{% include %}` tag with its closing `%}` on its own line gets dropped entirely, with no error, just broken behavior). This already broke an `{% include %}`-based attempt to share the auth-page CSS between login and signup. Workaround: keep each `{% %}` tag's full open/close on one logical unit, and after any edit to a template, re-fetch the rendered page (not just a template-parse check) to confirm nothing silently vanished.
