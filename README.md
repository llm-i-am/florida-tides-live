# Florida Tidecast · V2

A mobile-first Florida coastal tide explorer designed primarily for iPhone Safari. Choose a place or shoreline point to compare NOAA astronomical tide predictions with an **experimental live-gauge-adjusted estimate**.

> **Important:** The experimental estimate is not an official NOAA product, is not calibrated or independently accuracy-validated for arbitrary beaches, and is **not for navigation, flooding, swimming safety, or deciding if a location is safe to access**. Reported heights reference the selected NOAA station's local MLLW datum, **not** the exact beach's surveyed datum or water depth.

## Open and deploy

- The site lives in [`index.html`](./index.html) on the default `main` branch.
- In GitHub: **Settings → Pages → Build and deployment → Deploy from a branch → main → / (root) → Save**.
- Once published, the expected GitHub Pages address is **https://llm-i-am.github.io/florida-tides-live/**. That URL will not work until Pages is enabled and deployment succeeds.
- The first page load requires network access to NOAA services; the map and search also depend on third-party services. There is no account, backend, API key, build tool, or installation step.
- The prior generated iteration is preserved at [`archive/v1-index.html`](./archive/v1-index.html).

## V2 highlights

- **iPhone-first UI:** responsive translucent-glass styling, light/dark color schemes, readable touch-sized controls, safe-area padding, reduced-motion support, mobile-friendly date inputs, and a clear tide reading immediately on screen.
- **Choose a Florida coastal location:** quick picks, address/place search, optional device geolocation, numeric latitude/longitude, and a map with an explicit **Use this spot** confirmation action.
- **Station discovery:** downloads NOAA metadata for prediction stations and water-level gauges, caches catalogs, selects a geographically nearby and coarse-region-compatible prediction station, and shows the underlying NOAA station ID and distance.
- **Predicted vs. observed:** compares a live gauge reading with NOAA's astronomical prediction **at that same station and timestamp**. The difference is in **feet**, not a percentage (percentages around zero tide height are unstable).
- **Experimental transfer estimate:** combines eligible residuals with freshness, distance, and coarse-basin weighting; ignores old/bad readings; trims large disagreement where three or more gauges are available; limits geographic transfer strength; and decays a current correction over upcoming hours.
- **Transparent sources:** reports the baseline station, contributing gauges and their weights, and displays official NOAA predictions separately from app-generated estimates.
- **Graceful degradation:** if NOAA live observations are missing, it displays the NOAA astronomical baseline rather than inventing a current measurement.

## Estimation method

For each eligible live gauge at time `t`, calculate:

```text
residual_g(t) = observed_water_level_g(t) - NOAA_prediction_g(t)
```

All inputs use feet relative to each gauge's own MLLW datum, and each pair is computed at the **same gauge**, avoiding direct subtraction of absolute heights at unrelated stations.

The app computes a weighted mean residual, with `weight = coarse_region_compatibility × exp(−distance_km / 55) × exp(−reading_age_minutes / 90)`. With at least three valid gauges it can exclude a single large residual disagreement. It then applies a **heuristic, not validated** transfer-strength factor and decays the correction into the future with a 9-hour e-folding time. It does **not** forecast wind setup, storms, surge, or local hydraulic effects.

The NOAA astronomical baseline is selected from a nearby tide-prediction site; graphical heights between NOAA high and low extrema are visual interpolations, not separately computed NOAA harmonic predictions.

## Current limitations and caution

- **This is not true hydrodynamic triangulation.** Coarse geographic regions are proxies only; they do not model channels, inlets, waterway connectivity, bathymetry, or varying local tidal phase.
- The model cannot claim a calibrated uncertainty range or improved accuracy at Cypress Point Park or any other specific shoreline without historical holdout validation.
- The shoreline's actual water depth, current, beach accessibility, and flood risk cannot be inferred from this graph.
- Some places fall outside the currently supported NOAA station-search range, especially when metadata services are unavailable.
- The current UI uses **America/New_York (Eastern Time)** for date/time display, including locations in Florida's **Central Time** panhandle. Central Time support needs to be addressed before relying on displayed clock times there.
- Live-observation corrections are time-limited heuristics. For longer-range planning, trust an official local NOAA prediction or purpose-built hydrodynamic forecast instead.
- Place search uses OpenStreetMap Nominatim; map rendering uses Leaflet and OpenStreetMap tiles. Availability and acceptable use depend on those public services' policies.

## Data sources

- [NOAA CO-OPS Data API](https://api.tidesandcurrents.noaa.gov/api/prod/)
- [NOAA CO-OPS Metadata API](https://api.tidesandcurrents.noaa.gov/mdapi/prod/)
- [NOAA tide predictions](https://tidesandcurrents.noaa.gov/)
- [Leaflet](https://leafletjs.com/)
- [OpenStreetMap](https://www.openstreetmap.org/) and [Nominatim](https://nominatim.org/)

This website is an independent project and is not an official NOAA publication.

## Development history

- **V1:** Location-aware NOAA predictions plus an experimental live adjustment. [Archived here](./archive/v1-index.html).
- **V2:** iPhone-first redesign, safer mobile map selection, improved source labeling, more conservative residual handling, and responsive chart enhancements.

GitHub Pages hosts only the static files; no secrets or personal information should be added to this public repository.
