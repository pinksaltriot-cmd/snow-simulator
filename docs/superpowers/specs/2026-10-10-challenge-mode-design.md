# Challenge Mode — "Storm Architect" (spec + plan)

**Date:** 2026-10-10 · **Status:** design approved; brief list pending approval

## Game

A 🏆 Challenge button in the header opens a level picker: 5 levels, each with one ❄️ Snow brief
(Detailed Input), one 🔥 Heat brief (Heat Index mode) and one ⛈️ Severe brief (Severe Storm mode).
Locked levels are greyed out. Opening a brief switches to its mode and applies the challenge limits.

A brief:
- **Targets:** 1–3, read from outputs the simulator already computes: RSI value/category, per-city
  impact tier, RHI category, per-city heat tier, per-city severe tier, and counts ("exactly two cities
  at Sweltering or above").
- **Budget:**
  - a city cap;
  - a **shared pool** split across those cities: ❄️ total snow inches, 🔥 total °F above 80 (from each
    city's temperature input), ⛈️ total gust + tornado mph.
  Every other input is free. The UI shows the pool remaining and blocks a run that overspends.
- **3 runs** per brief; the best run counts.

**Grading:** each target scores by its distance in steps on its own ladder: exact 100, 1 step 70,
2 steps 40, further 0. Overshoot and undershoot count alike. Count targets score by how far the count
is off, on the same 100/70/40/0 scale. The average of the targets gives the grade: A ≥ 90, B ≥ 80,
C ≥ 70, D ≥ 60, otherwise F. C or better passes; a level passes when all three briefs pass.

**Realism:** Levels 1–4 target only the realistic part of each ladder: impact tiers Calamitous and
below, RSI Cat 5 (Extreme) and below, heat tiers through Mass-Casualty Heat, severe tiers Incredible
Tornado and below. Level 5 may reach the historic-class and fictional tiers.

**Rank:** one step per level beaten: Apprentice → Drafter → Builder → Engineer → Architect. Beating
Level 5 earns the special top rank **Grand Architect of Storms**: a gold badge that stays in the
header outside Challenge Mode.

## Data

New `CHALLENGE` section. `SIM.CHALLENGE.BRIEFS` (or the file's equivalent namespace) is 15 objects:

```
{ id, level, mode:'snow'|'heat'|'severe', title, blurb:{en,yooper},
  budget:{maxCities, pool, poolKind}, targets:[{kind, value, op?, tierLadder?, label:{en,yooper}}],
  solution:[{city, ...inputs}] }
```

`solution` is used only by the self-test.

## State

- Entering a brief snapshots the current storm/mode inputs. Exiting restores them exactly.
- Progress is stored in `localStorage['snowsim.challenge.v1']`, with try/catch on every read and write;
  without storage the game still runs.
- Every string gets a Yoopanese label through the site's existing Yooper system.

## Self-test

The site's existing test harness, plus:
- Each brief's `solution` fits its budget (cities and pool) and grades A.
- An empty attempt and a naive attempt (whole pool in one city) grade below C.
- The full campaign plays through to Grand Architect of Storms.
- Snapshot and restore round-trip exactly.
- Every new string has a Yooper entry.
- All existing tests still pass.

## Release

Version **3.6.0**. Resync the hand-maintained line-count subheading. Push to main (Pages deploy).

## Build plan

1. Grader, budget enforcement and run counter, with unit tests.
2. UI: header button, picker, brief card, pool meter, report card, snapshot and restore.
3. Progress, rank, Grand Architect badge, Yooper strings, README/Yooper docs if present.
4. *(parallel)* Tune the 15 briefs from the approved list against the engine; record each `solution`.
5. Merge, full self-test, browser check in both languages, version bump, subheading resync, push.

## Draft brief list

Numbers are drafts and get tuned against the engine. If a brief is impossible, report it instead of
quietly changing its meaning.

| # | Lvl | Mode | Title | Budget | Targets |
|---|---|---|---|---|---|
| 1 | 1 | ❄️ | First Flakes | ≤3 cities, 12" | RSI Category 1 (Notable) |
| 2 | 1 | 🔥 | Warm Spell | 1 city, 20°F | city exactly **Hot** |
| 3 | 1 | ⛈️ | Thunder Rumble | ≤2 cities, 120 mph | worst city exactly **Strong Storm** |
| 4 | 2 | ❄️ | Lake-Effect Lock | ≤2 cities, 30" | worst city exactly **Major**; RSI no higher than Cat 1 |
| 5 | 2 | 🔥 | Muggy Corridor | ≤3 cities, 40°F | exactly 2 cities at **Muggy** or above; RHI Cat 1 |
| 6 | 2 | ⛈️ | Hail Alley | ≤3 cities, 220 mph | worst city exactly **Damaging Storm**; no city below **Severe Storm** |
| 7 | 3 | ❄️ | The Crippler | ≤4 cities, 60" | RSI Cat 3 (Major); worst city exactly **Crippling** |
| 8 | 3 | 🔥 | Heat Dome | ≤4 cities, 70°F | RHI Cat 3; worst city exactly **Oppressive** |
| 9 | 3 | ⛈️ | One Touchdown | ≤3 cities, 260 mph | exactly 1 city at **Tornado Touchdown**; others exactly **Severe Storm** |
| 10 | 4 | ❄️ | Wide but Shallow | ≤6 cities, 80" | RSI Cat 4 (Crippling); no city above **Major** |
| 11 | 4 | 🔥 | Spread the Swelter | ≤6 cities, 90°F | RHI Cat 4; no city above **Sweltering** |
| 12 | 4 | ⛈️ | Derecho Line | exactly 4 cities, 360 mph | all 4 exactly **Derecho-Class** |
| 13 | 5 | ❄️ | Historic | ≤5 cities, tight pool | worst city exactly **Historic**; RSI Cat 5 (Extreme) |
| 14 | 5 | 🔥 | Chicago '95 | ≤3 cities, tight pool | worst city exactly **1995 Chicago–Class**; exactly 1 city above Heat Emergency |
| 15 | 5 | ⛈️ | Atmospheric Tear | ≤4 cities, tight pool | one city exactly **Beyond EF5**; every other city **Derecho-Class** or above |
