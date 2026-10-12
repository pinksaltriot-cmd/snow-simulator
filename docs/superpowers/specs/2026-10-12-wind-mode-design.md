# Wind Mode + Kite War (v3.8.0) — spec + plan

**Date:** 2026-10-12 · **Status:** design approved (1a 2b 3a 4a); wind impact ladder pending approval
**Pattern:** a copy of the Fog mode + Party Blower War build (v3.7.0, spec 2026-10-10-fog-mode-design.md).

## 1. Wind mode

A new `data-mode="wind"` button, built on the Fog/Heat mode pattern.

**Per-city inputs**
- City
- Sustained wind (mph, required) and peak gust (mph)
- Direction
- Duration (hours)
- Type:
  - General / synoptic
  - Downslope (Chinook / Santa Ana / foehn)
  - Thunderstorm / derecho
  - Coastal gale / bomb cyclone
  - Mountain-top
- Optional: relative humidity (fire weather), temperature

**Wind impact score.** One number per city, built from:
- sustained wind and gust, steeply nonlinear, since damage rises roughly with the cube of speed;
- duration;
- type multiplier: a derecho is short but intense; downslope winds are gusty;
- optional: humidity, for fire-weather emphasis.

The ladder's thresholds are calibrated to these anchors:

| Event | Lands on |
|---|---|
| 5 mph afternoon breeze | Light Breeze |
| 15 mph, gusts 22, all day | Moderate Breeze |
| 35 mph, gusts 50, 12 h | Gale / Strong Gale |
| 60 mph, gusts 80, 6 h downslope | Chinook / Downslope Windstorm |
| 2020 Iowa derecho (sustained ~100, gust 140, ~14 h line) | 2020 Iowa Derecho–Class |
| 1934 Mount Washington (231 mph gust) | Mount Washington 1934–Class |
| 1996 Barrow Island (253 mph gust) | Barrow Island 1996–Class |

**Wind impact ladder:** 45 tiers (list below), Beaufort-based at the bottom. Realistic through Barrow Island
1996–Class (tier 25). Fiction starts at tier 26, following the Heat and Fog ladders' realism rule.

**Alerts:** NWS criteria.
- Wind Advisory: sustained 31–39 mph or gusts 46–57.
- High Wind Watch / Warning: sustained ≥ 40 or gusts ≥ 58.
- Extreme Wind Warning: sustained ≥ 115.
- Lake Wind Advisory.
- Red Flag Warning when humidity ≤ 15% and gusts ≥ 25.

**Impacts**
- Power: outages, scaling from scattered to widespread to grid down
- Trees: branches, then uprooting, then forest blowdown
- High-profile vehicles: restrictions, then rollovers
- Aviation: crosswind limits, then ground stop
- Structures: shingles → roofs → walls
- Schools
- Coastal / lake: waves and seiche

**Wind-down timeline:** hour-by-hour decay.
- Synoptic gales fade over hours.
- Thunderstorm and derecho gusts end within the hour.
- Downslope events pulse overnight.

**Fill In The Gaps — Wind**, and a **Regional Wind Index (RWI)** using the RHI/RFI regions, with wind-themed category names.

## 2. Kite War Tiers

A new `data-mode="kitewar"` button right after Party Blower War Tiers. It works like the other war modes, and also adds a Kite War
column to Wind results.

- **323 tiers, parallel 1:1:** `KITE_WAR_TIERS[i]` tells the same story as the snow, water, cozy and party
  tiers at index i, told in wind and kites.
- **The Launcher** storyline carries `launcher:true` at exactly the indices of `fluffer:true` / `pump:true` /
  `bellows:true`. The Launcher is a slingshot frame that throws a kite straight into the wind, so it is airborne with
  no running start: two uprights, surgical-tubing bands, a cradle that releases the kite at the top of the throw.
  It must be a real, buildable invention with concrete dimensions. Its build stages mirror the other inventions
  (sketch with an arrow labeled "kite goes up here" → dimensions → ratio argument → mock-up → …).
- **Driven by the wind impact score.** Thresholds are era-mapped like the Party and Water wars. Tier 1 is exactly 0
  (dead calm). Survival floors sit at the same indices as the water and party floors. Kite logic shapes the story:
  - still air means no war at all;
  - flying is best in breezes;
  - past gale force kites can't be flown, so the upper real tiers are about survival (Iowa 2020, Mount Washington), and then legend and myth.
- Bands Calm Day / Gale / Beyond the Weather, at the cozy and party band indices (1–129, 130–237, 238–323).
  The css is `kw0`…`kw15`, mirroring the snow css.
- **Voice:** the Water War voice: the snow war's deadpan, with more concrete numbers and slightly funnier. The survival tiers
  turn serious.
  - Tiers are generic, with no names.
  - Hand-written Yoopanese in `yooper/kite-war.js`; no scripted dialect pass.
- **Self-tests:**
  - exactly 323 tiers;
  - `launcher` === `bellows` === `fluffer` === `pump` indices;
  - thresholds strictly increase;
  - css matches the snow band;
  - every tier has a Yooper entry.

## 3. Release

- Version **3.8.0**.
- Resync the line-count subheading as the last edit.
- Every existing selftest and the impact fingerprint must still pass.
- Push to main.

## 4. Build plan

What we learned from v3.7.0 is built in from the start:
- 8 tier writers from the start;
- a shared canon note;
- hand-written Yooper;
- one engine agent that builds everything in-page.

1. **Engine agent:**
   - the wind score, ladder, alerts, impacts, wind-down timeline, gap fill, RWI, and the Wind mode UI;
   - the Kite War mode, `getKiteWar`, the thresholds, and a merge.py that globs `kitewar/part*.json`;
   - self-tests.
2. **Eight tier writers in parallel**, using the v3.7.0 ranges: 1–46, 47–91, 92–134, 135–176, 177–211, 212–246, 247–285,
   286–323. Each reads the snow, water, cozy and party tiers at the same index.
3. **Coordinator:**
   - writes the Launcher canon up front;
   - runs the combined validation and a handoff voice check;
   - bumps the version, resyncs the line count, and pushes.

## 5. Wind impact ladder (draft for approval)

| # | Tier | Realm |
|---|---|---|
| 1 | Calm | Beaufort 0 |
| 2 | Light Air | Beaufort 1 |
| 3 | Light Breeze | Beaufort 2 |
| 4 | Gentle Breeze | Beaufort 3 |
| 5 | Moderate Breeze | Beaufort 4 |
| 6 | Fresh Breeze | Beaufort 5 |
| 7 | Strong Breeze | Beaufort 6 |
| 8 | Near Gale | Beaufort 7 |
| 9 | Gale | Beaufort 8 |
| 10 | Strong Gale | Beaufort 9 |
| 11 | Storm | Beaufort 10 |
| 12 | Violent Storm | Beaufort 11 |
| 13 | Hurricane Force | Beaufort 12 |
| 14 | Tree-Toppler | real |
| 15 | Grid-Down Wind | real |
| 16 | Chinook | real |
| 17 | Santa Ana | real |
| 18 | Downslope Windstorm | real |
| 19 | Derecho | real |
| 20 | Bomb Cyclone Gale | real |
| 21 | 1962 Columbus Day–Class | real |
| 22 | Black Sunday 1935–Class | real |
| 23 | 2020 Iowa Derecho–Class | real |
| 24 | Mount Washington 1934–Class | real |
| 25 | Barrow Island 1996–Class | real (ceiling of realism) |
| 26 | Jet Stream Descends | fiction |
| 27 | Wind Without End | fiction |
| 28 | The Long Gale | fiction |
| 29 | Continental Gale | fiction |
| 30 | The Great Blow | fiction |
| 31 | Hemisphere Gale | fiction |
| 32 | Planetary Gale | fiction |
| 33 | Jupiter-Class | fiction |
| 34 | Saturn-Class | fiction |
| 35 | Neptune-Class | fiction |
| 36 | Supersonic Wind | fiction |
| 37 | Hot-Jupiter–Class | fiction |
| 38 | Solar Wind | fiction |
| 39 | Stellar Gale | fiction |
| 40 | Supernova Shockwave | fiction |
| 41 | Galactic Wind | fiction |
| 42 | Quasar Outflow | fiction |
| 43 | The Wind Between | fiction |
| 44 | The Last Gust | fiction |
| 45 | Total Stillness | fiction (the scale wraps back to calm, beyond everything) |
