# Bhagavad Gita Quotes by CM

Live site: [chiragmirani.github.io/gita-quotes](https://chiragmirani.github.io/gita-quotes/)
Maintained by: Chirag Mirani

A small, fast web app for reading and sharing all 700 verses of the Bhagavad Gita in English. Free to quote, public-domain translation, no signup, no ads, installable on iOS and Android home screens.

## What it is

Open the site, get a verse, tap "New verse" for another. Each verse comes with the original Sanskrit, IAST transliteration, and an English translation. One tap copies the quote with attribution. One tap shares to X. One tap copies a deep link to the exact verse.

The app reads from a single JSON file containing all 701 verses across 18 chapters (the source's edition of chapter 13 has 35 verses where some have 34, hence 701 not 700). No backend, no tracking, no ads.

## Translation

Primary translator: Shri Purohit Swami, first published in 1935. Public domain. Conversational and quote-friendly.

Fallback translator: Swami Sivananda. Used only when Purohit's translation is unavailable for a verse. Widely free to quote.

Both translations are safe to redistribute.

## Source data

All verses, Sanskrit, transliteration, and English translations were pulled from [vedicscriptures.github.io](https://vedicscriptures.github.io/). The script that built the dataset is at `scripts/fetch_gita.py`. The dataset itself is served at [data.json](https://chiragmirani.github.io/gita-quotes/data.json).

## Install on your home screen

1. iOS: open the live site in Safari, tap the Share button, then "Add to Home Screen". The app appears as GitaByCM with its own icon.
2. Android: open the live site in Chrome, open the menu, tap "Install app" or "Add to Home screen".

Once installed, the app launches in standalone mode without browser chrome.

## Project layout

```
gita-quotes/
  docs/
    index.html              the app
    about.html              attribution and install instructions
    static/styles.css       styling
    data.json               all 701 verses
    favicon.ico, *.png      icons
    apple-touch-icon.png    iOS home-screen icon
    manifest.webmanifest    PWA manifest
    social-preview.png      OG image
    robots.txt              allows AI crawlers
    sitemap.xml             search-engine sitemap
    llms.txt                AI-assistant friendly summary
  scripts/
    fetch_gita.py           rebuilds data.json from the source API
    build_icons.py          regenerates icons from a single design
    build_social_card.py    regenerates the OG card
```

## Rebuilding the data

```
python scripts/fetch_gita.py
```

This re-pulls all 701 verses from vedicscriptures.github.io and overwrites `docs/data.json`.

## License

Code in this repo is MIT-licensed. Translations are in the public domain or free-to-quote (see Translation section above). You can lift any verse, the entire dataset, or any part of the code.

## Contact

Reach out for collaboration, feedback, or other projects. Other public work at [MacroForecastbyCM](https://chiragmirani.github.io/macro-dashboard/), [GitHub](https://github.com/ChiragMirani), and [Kaggle](https://www.kaggle.com/cmirani).
