# Fog / Haze / Mist Mode + Party Blower War (v3.7.0) — spec + plan

**Date:** 2026-10-10 · **Status:** design approved; fog impact ladder approved 2026-10-10
**Next release:** Wind mode + Kite War = v3.8.0 (separate spec, after this ships).

## 1. Fog mode

A new `data-mode="fog"` button, built on the Heat Index mode pattern.

**Per-city inputs**
- City (the same city database the other modes use)
- Visibility: miles, accepting fractions like 1/4 and 1/16, or feet; down to 0
- Type: Mist / Haze / Fog / Freezing Fog. Freezing Fog is set automatically when temp ≤ 32°F and the type is Fog.
  Haze covers dry particulates (dust, smoke, smog).
- Duration (hours, up to multi-week)
- Start time (hour of day)
- Optional: temperature, dewpoint, wind speed

**Fog impact score.** One number per city, built from:
- visibility severity: steeply nonlinear, so dense fog at ¼ mi or below dominates;
- duration;
- type multiplier: Freezing Fog > Fog > Haze ≈ Mist;
- time of day: night and the morning commute weigh most;
- optional modifiers: wind shortens effective duration; a dewpoint at the temperature lengthens it.

The ladder's thresholds are calibrated to these anchors:

| Event | Lands on |
|---|---|
| 5 mi mist for 2 h at dawn | Mist |
| ½ mi fog, 4 h, morning | Fog / Thick Fog |
| ⅛ mi fog, 6 h, overnight | Dense Fog |
| 0 mi zero-zero, 8 h | Zero-Zero |
| ⅛ mi freezing fog, 12 h | Rime Fog |
| ¼ mi, 21 days, Central Valley | Week-Long Tule Fog or above |
| 1952 London (≤ 30 ft visibility, smog/haze, 5 days) | 1952 London–Class |

**Fog impact ladder:** 45 tiers (see the approved list below). Realistic through 1952 London–Class (tier 31).
Fiction starts at tier 32, matching the Heat ladder's realism rule.

**Alerts**
- Dense Fog Advisory: visibility ≤ ¼ mi over a wide area, the NWS criterion
- Freezing Fog Advisory
- Dense Smoke Advisory: haze from smoke
- Air Quality Alert: haze
- Special Weather Statement for patchy dense fog

**Impacts**
- Roads: slowdowns, chain-reaction pileup risk at ≤ ⅛ mi and highway speeds
- Airports: CAT I / II / III landing minimums by visibility (RVR 2400 / 1200 / below 600 ft), up to a ground stop
- Schools: 1–2 hour delays, up to closure for freezing fog or zero-zero
- Shipping and bridges

**Clearing timeline:** hour-by-hour visibility recovery.
- Daytime burn-off from sun and mixing: start around 2–3 h after sunrise, faster in summer.
- Night fog persists until morning.
- Wind ≥ 10 mph speeds clearing.
- Tule and inversion fogs can fail to burn off for days. Haze clears only with a wind shift or rain.

**Fill In The Gaps — Fog:** fills missing cities' values, using the Heat gap-fill pattern.

**Regional Fog Index (RFI):** uses the same regions and category structure as the RHI. Its category names are fog-themed.

## 2. Party Blower War Tiers

A new `data-mode="partywar"` button right after Cozy War Tiers. It works like the Snow, Water and Cozy war modes, and also adds
a Party Blower War column to Fog results.

- **323 tiers, parallel 1:1:** `PARTY_WAR_TIERS[i]` tells the same story as `SNOW_WAR_TIERS[i]`,
  `WATER_WAR_TIERS[i]` and `COZY_WAR_TIERS[i]`, told in fog and party blowers.
- **The Bellows** storyline carries `bellows:true` at exactly the indices where snow has the
  Spreader, water has `pump:true` and cozy has `fluffer:true`. The Bellows is a foot-pumped bellows feeding a manifold
  of party blowers; one stomp unrolls 6 at once with a honk you can hear through 50 ft of fog. It must
  be a real, buildable invention, never a fort plan. Its build stages mirror the Fluffer's (sketch → dimensions →
  argument over ratios → mock-up → …).
- **Driven by the fog impact score.** Thresholds use "match by era" like the Water War: the snow css
  bands map to party bands. Tier 1 is exactly 0 (a clear day). The survival floors sit at the same indices as the water ones.
- **Fog logic:** you can't see the other side, so the war is fought by sound. Bands are:
  Clear Day / Fog Bank / Beyond the Weather.
- **Voice:** the Water War's voice: the snow war's deadpan, with more concrete numbers and slightly funnier.
  Near deadly real conditions (Donora 1948, 1952 London) the tiers shift to survival, not jokes.
  Tiers are generic, with no named kids.
- Each tier has `band`, `max` (score threshold), `css` (`pb0`…), `icon`, `label` and `desc`, plus a full
  Yoopanese translation in the site's Yooper voice, kept in `yooper/party-war.js` like the other war files.
- A self-test checks:
  - exactly 323 tiers;
  - `bellows` indices === `fluffer` indices === `pump` indices;
  - thresholds strictly increase;
  - every tier has a Yooper entry.

## 3. Release

- Version **3.7.0**, in the title, h1 and the selftests that pin it.
- Resync the line-count subheading as the very last edit.
- The pinned impact fingerprint and every existing selftest must still pass; no existing result may move.
- Push to main (Pages).

## 4. Build plan

1. **Engine agent:** fog score, ladder, alerts, impacts, clearing timeline, gap fill, RFI, the Fog mode UI, the
   Party Blower War mode shell and lookup (`getPartyWar`), and selftests.
2. **Four tier-writer agents in parallel**, each writing a quarter of the 323 tiers (by index range, aligned
   to band boundaries) from the matching snow, water and cozy tiers, in English and Yoopanese, into separate
   scratch files.
3. **Coordinator:** merges the tiers, checks that the Bellows indices line up and that the voice is consistent, runs the full
   selftest, bumps the version, resyncs the line count, and pushes.

## 5. Fog impact ladder (draft for approval)

| # | Tier | Realm |
|---|---|---|
| 1 | Clear | real |
| 2 | Faint Haze | real |
| 3 | Light Haze | real |
| 4 | Patchy Mist | real |
| 5 | Mist | real |
| 6 | Thick Mist | real |
| 7 | Marine Layer | real |
| 8 | Patchy Fog | real |
| 9 | Shallow Ground Fog | real |
| 10 | Valley Fog | real |
| 11 | Fog | real |
| 12 | Thick Fog | real |
| 13 | Dense Fog | real (Dense Fog Advisory) |
| 14 | Pea Soup | real |
| 15 | Zero-Zero | real |
| 16 | Freezing Fog | real |
| 17 | Rime Fog | real |
| 18 | Ice Fog | real (Fairbanks −30s) |
| 19 | Pileup Fog | real |
| 20 | Airport Shutdown | real |
| 21 | Regional Ground Stop | real |
| 22 | Tule Fog | real |
| 23 | Lingering Tule Fog | real |
| 24 | Week-Long Tule Fog | real |
| 25 | Grand Banks–Class | real |
| 26 | Inversion Haze | real |
| 27 | Smoke Haze | real |
| 28 | 2023 Orange Sky–Class | real (June 2023 Northeast smoke) |
| 29 | Killer Smog | real |
| 30 | Donora 1948–Class | real |
| 31 | 1952 London–Class | real (ceiling of realism) |
| 32 | Fog Without End | fiction |
| 33 | The Brume | fiction |
| 34 | Fogbound Continent | fiction |
| 35 | The Long Grey | fiction |
| 36 | The Cloud Comes Down | fiction |
| 37 | Hemisphere Fog | fiction |
| 38 | The Grey Ocean | fiction |
| 39 | Planetary Murk | fiction |
| 40 | Venus-Class | fiction |
| 41 | Titan-Class | fiction |
| 42 | Nebular | fiction |
| 43 | The Unseen | fiction |
| 44 | The Last Light | fiction |
| 45 | Total Opacity | fiction |
