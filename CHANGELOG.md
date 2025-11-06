## Unreleased

## v0.8.0 (2025-10-26)

### Feat

- **cli**: add `--thumbnail` flag to download high-resolution video thumbnails
- **cli**: integrate thumbnail download workflow with existing Rich-based console output
- **deps**: include `requests` dependency for HTTP thumbnail retrieval

## v0.7.0 (2025-10-26)

### Feat

- **cli**: add authentication support for age-restricted and private videos via `--cookies` and `--cookies-from-browser`
- **cli**: support Chrome, Brave, Firefox, Edge, and Safari for browser-based cookies
- **tests**: mock `yt_dlp` to avoid network calls during CLI testing and ensure full offline coverage
- **docs**: update README with authentication usage and examples

## v0.6.1 (2025-10-25)

### Fix

- **playlist**: preserve playlist parameters in URL normalization and enable proper playlist detection and downloads

## v0.4.0 (2025-10-23)

### Feat

- **url**: normalize playlist URLs and improve universal YouTube URL handling

## v0.3.0 (2025-10-23)

### Feat

- **url**: add support for normalizing YouTube Shorts URLs

## v0.2.0 (2025-10-23)

### Feat

- **url**: add automatic YouTube URL normalization for shortlinks and parameters

## v0.1.0 (2025-10-23)

### Feat

- **cli**: implement initial YouTube video/audio downloader command