# Front Mode — spec (draft)

**Date:** 2026-11-22 · **Status:** design approved; front impact ladder approved 2026-11-22. Jill's decisions: no Fill In The Gaps, no regional index, no war tiers.
**Pattern:** built on the Fog / Wind mode pattern (specs 2026-10-10-fog-mode-design.md, 2026-10-12-wind-mode-design.md).

## Why

Four Tulsa test runs, all fronts, all through Detailed Input (2026-11-22):

| # | Event | Simulator result | What it missed |
|---|---|---|---|
| 1 | Nov 20: dry Arctic front, 60 → 32°F in 4.5 h | Very Light, wind chill 20°F | The 28°F crash and its speed. "Temp before the front" only feeds flash freeze, which needs wet roads |
| 2 | Oct 1: 78°F, sunny, humid → 55°F, cloudy, dry in 6 h | None, no alerts | Drop, humidity swing, sky swing, timing; 55°F is ~24°F below the Oct 1 normal high |
| 3 | Mar 10: occluded front pins temps at 33°F, 0.75″ slush over 8 h | Moderate, Winter Weather Advisory, 2-hour delays | No front type; can't say the temp is held at 33°F; storm type "Flurry Dud, also resembles Polar Vortex Outbreak"; impact likely too high for wet slush on warm March ground |
| 4 | May 2: run 2 reversed, 55°F cloudy dry → 78°F sunny humid in 6 h | None, no alerts | A rise is accepted silently and ignored; the humidity surge (the severe-weather setup) isn't scored |

**Shared gap:** the simulator scores one moment. A front is a change between two air masses over time, and the change is what makes it an event.

## 1. Front mode

A new `data-mode="front"` button, placed after Wind.

**Per-city inputs**
- City (the shared city database)
- Front type:
  - Cold front
  - Arctic front (a cold front with an arctic air mass behind it)
  - Backdoor cold front (arrives from the NE/E)
  - Warm front
  - Occluded front (cold-type / warm-type, optional)
  - Stationary front
  - Dryline
- **Before** the front: temperature (required), humidity or dewpoint, sky
- **After** the front: temperature (required), humidity or dewpoint, sky
- Transition time (hours): how long the change takes. For an occluded or stationary front this is how long the front **holds** conditions steady instead.
- Start date and time
- Optional overrides, before and after: wind speed, gust, direction, pressure. Left blank, they're estimated (§2).
- Optional: 850mb temp, and precipitation phases (the Detailed Input phase builder). When phases are entered they replace the precipitation estimate in §4.

**Derived values** (shown in the result)
- Temperature change (°F) and rate (°F/hr)
- Dewpoint change
- Departure from normal before and after, using the city's climatology for the date. The simulator already has climatology for the warming outlook.
- Whether the change crosses 32°F

## 2. Wind, pressure and direction (every front type)

Every result shows a wind and pressure panel, before / at passage / after:
- **Wind direction:** before and after, as compass points and degrees, plus the shift at passage
- **Wind speed and gust:** before, peak at passage, after
- **Pressure (mb):** before, the minimum at passage, after, and the change, shown rising or falling

When the overrides are blank, typical values by front type:

| Front | Before → after direction | Wind | Pressure |
|---|---|---|---|
| Cold | S/SW → NW | gust spike at passage, breezy behind | falls ahead, minimum at passage, sharp rise behind |
| Arctic | S/SW → N | strongest post-frontal gusts | the biggest rise; 1035+ mb highs behind |
| Backdoor cold | S/SW → NE/E | gusty and short-lived | modest rise |
| Warm | E/SE → S/SW | gradually stronger | steady slow fall, then levels off |
| Occluded | SE/E → W/NW (veering through S) | strong around the low | lowest at passage; the low is nearby |
| Stationary | light, variable across the boundary | weak | flat for the duration |
| Dryline | S/SE → W/SW | gusty, dry westerlies | small fall |

Speeds scale with the temperature contrast and the transition rate: a sharper front blows harder.

## 3. Severe weather (when the front can set it off)

For any front type that can fire storms, the result shows a **"Severe Storm mode entry"** card. Its fields match Severe Storm mode's inputs one-to-one, so they can be copied straight in:

| Severe Storm mode field | From the front |
|---|---|
| City | same city |
| Storm arrives | the time of passage, from the start time plus the transition |
| Temp before (°F) | the before-storm temperature (warm-sector air) |
| Dewpoint | the warm-sector dewpoint |
| Peak gust (mph) | estimated (below) |
| Hail (in) | estimated |
| Rain (in) … over (min) | estimated |
| Tornado (mph) | estimated, or blank when tornadoes are unlikely |
| Pressure from (mb) … down to (mb) … in (min) | from the §2 pressure trace |

**When it shows:** the warm-sector dewpoint is ~55°F or higher and the warm-sector temperature ~65°F or higher. The front type also matters: warm fronts and drylines most often; cold, Arctic and occluded fronts when the warm air ahead qualifies; stationary fronts with training storms. Below the threshold the card reads "No severe weather expected" and gives the reason (too dry or too cool).

**How the estimates scale:** with the dewpoint (moisture), the temperature contrast (lift), the season (spring peak) and the front type:
- **Dryline and warm front:** discrete supercells, so hail and tornadoes are favored.
- **Cold front:** a squall line, so damaging wind is favored, with smaller hail and brief tornadoes.
- **Stationary front:** training storms, so heavy rain over a long period is favored.

Each estimate also names the storm mode, such as "discrete supercells", "squall line" or "training storms", so the Severe Storm mode run can be told what it represents.

Run 4 (May 2, warm front, 55 → 78°F, humid) is the anchor case for this card.

## 4. Snow and winter precipitation (when the after side is cold enough)

When the after-front air is near or below freezing and there's moisture, the result shows a **"Detailed Input entry"** card. It's in the same shape as the phase builder: phases in order, each with a type, an amount and hours, plus the storm temp, so it can be copied into Detailed Input.

**Type by temperature and the layer aloft.** This follows the snow-type rule (default Snowball; Oklahoma mid-20s is never Powder). Every winter type in Detailed Input can come out of a front:

| Surface temp | Aloft (850mb / warm layer) | Type |
|---|---|---|
| 33–36°F | no warm layer; flakes melt near the ground | Rain-Snow Mix |
| 33–35°F | warm layer aloft, shallow cold layer near the ground | Rain-Sleet Mix |
| 33–34°F | marginal warm layer (850mb near 0°C), changing over | Rain-Sleet-Snow Mix |
| ≥ 33°F | heavy, wet snow outrunning the melt | Slush |
| 32–33°F | no warm layer | Slush |
| ≤ 32°F | weak warm layer (850mb 0 to +1°C), partial melting | Sleet-Snow Mix |
| ≤ 32°F | warm layer aloft, deep cold layer below | Sleet |
| ≤ 32°F | warm layer aloft, shallow cold layer below | Ice / Freezing Rain |
| 20–31°F | all cold | Snowball Snow |
| < 20°F | all cold, dry, high-ratio air mass | Powder |
| 15–32°F | only a shallow moist layer, weak lift: low stratus, no deep cloud | Snow Grains |

**Phase order by front type.** Every type runs as its own phase, in order:
- **Cold / Arctic:** Rain → Rain-Sleet Mix → Rain-Sleet-Snow Mix → Sleet-Snow Mix → Snowball (or Powder when it's cold enough) as the cold air deepens. Then Snow Grains in the shallow stratus that often lingers behind an Arctic front.
- **Warm front in winter:** the reverse, the classic Plains ice setup. Snowball → Sleet-Snow Mix → Sleet → Ice / Freezing Rain → Rain-Sleet Mix → Rain as warm air overruns the cold.
- **Backdoor cold:** a shallow cold wedge, so drizzle-to-Snow Grains and Freezing Rain are favored over deep snow.
- **Occluded:** a steady single type, held for the duration. Rain-Snow Mix or Slush when it sits near freezing, as in run 3.
- **Stationary:** the type depends on which side the city is on, and can flip back and forth if the front wobbles.

A fast front can skip phases: a sharp Arctic front often goes straight from Rain to Snowball with a brief Rain-Snow Mix between.

**Thundersnow.** The card adds a Thundersnow phase, the Detailed Input type of that name, when a cold side gets convective lift:
- **Arctic and strong cold fronts:** a sharp front (a fast temperature fall) with moisture ahead and a very cold 850mb behind (≤ −8°C). This is the snow-side cousin of a squall line, a burst of heavy snow with lightning right at passage.
- **Occluded fronts:** a deep low (falling pressure, ≤ ~1000 mb) wrapping moisture back into the cold air. This is the comma head and TROWAL band.
- **Warm fronts in winter:** elevated storms riding up over the cold air at the surface, with thunder over Snowball or Sleet.
- **What the phase carries:** it runs short, usually 1–3 h inside the longer snow, and sets the Detailed Input peak rate at 2–3″/hr. Its snow type follows the temperature table above.
- **When it's left out:** the air is cold but stable, with weak lift or a slow transition. The card says why.

**Amount:** scales with the before-side moisture (dewpoint), the transition time and the front type. A dry front, like run 1, gives "No precipitation expected" and the reason.

Run 3 (Mar 10, occluded, 33°F, 0.75″ slush over 8 h) is the anchor case for this card.

## 5. Front impact score

One number per city, built from:
- **magnitude:** the temperature change, nonlinear, so 30°F+ swings dominate;
- **rate:** °F/hr, weighted strongly. A 28°F drop in 4.5 h (6.2°F/hr) has to outscore the same drop over 24 h;
- **departure from normal:** the after-front temp against the date's normal. 55°F on Oct 1 counts as a shock; 55°F in January doesn't;
- **freezing crossing:** a bonus when the change goes through 32°F. This hands off to the existing flash-freeze logic when the roads are wet;
- **humidity swing:** a dewpoint jump or crash;
- **wind and pressure:** post-frontal gusts, the size of the wind shift, and the pressure change;
- **type multiplier:** Arctic > cold > backdoor > dryline > warm. Occluded and stationary fronts score on **duration held** instead of rate.

The score rates the front itself. Severe weather and snow are rated in their own modes once their cards are entered there, so they don't count twice.

**Calibration anchors** (realistic up to the historic records, following the impact-tier realism rule)

| Event | Lands on |
|---|---|
| Typical fall front, 8°F drop over 12 h | low tier, noticeable |
| Run 2: Oct 1, 78 → 55°F in 6 h | first-fall-front tier, moderate |
| Run 4: May 2 warm front, 55 → 78°F in 6 h, humid | moderate |
| Run 1: Nov 20, 60 → 32°F in 4.5 h, gusty | strong Arctic front |
| Great Blue Norther, Nov 11, 1911 (Oklahoma City 83 → 17°F in a day) | historic-class tier |
| Browning, MT, Jan 23–24, 1916 (44 → −56°F, 100°F in 24 h) | top realistic tier |

**Front impact ladder:** 45 tiers (§5a). Realistic through Browning 1916–Class (tier 27). Fiction starts at tier 28, following the realism rule of the other ladders.

## 5a. Front impact ladder (draft for approval)

Rises and drops share one ladder: a warm front lands wherever its score puts it. Chinook and downslope rises (Spearfish 1943, Loma 1972) belong to Wind mode, not here, because they aren't fronts.

| # | Tier | Basis |
|---|---|---|
| 1 | No Front | nothing crosses |
| 2 | Wind Shift | the wind turns; the temperature barely moves |
| 3 | Weak Front | a few degrees, a few clouds |
| 4 | Noticeable Front | ~8°F over 12 h |
| 5 | Sweater Front | ~10–12°F; the afternoon feels different |
| 6 | Jacket Front | ~15°F; people go back inside for a coat |
| 7 | Clean Sweep | the humidity drops out and the sky scrubs clean |
| 8 | Sharp Front | ~15–20°F in a few hours |
| 9 | First Fall Front | run 2: Oct 1, 78 → 55°F in 6 h, ~24°F below normal |
| 10 | Warm Surge | run 4: May 2, 55 → 78°F in 6 h, dewpoints climbing |
| 11 | Strong Front | ~25°F in 6 h with gusts |
| 12 | Temperature Cliff | ~25°F+ in 3 h or less |
| 13 | Blue Norther | the classic Plains norther: blue-black sky to the north, a sudden cold wind |
| 14 | Arctic Front | run 1: Nov 20, 60 → 32°F in 4.5 h, gusty |
| 15 | Hard Arctic Front | ~35°F drop into the 20s |
| 16 | Flash-Freeze Front | crossing 32°F fast onto wet ground |
| 17 | Arctic Plunge | ~40°F drop into the teens |
| 18 | Arctic Outbreak | ~40°F+, multi-state, single digits behind |
| 19 | Cross-Polar Flow | air straight from Siberia over the pole; subzero behind |
| 20 | Armistice Day 1940–Class | Nov 11, 1940: 60s to single digits across the Upper Midwest |
| 21 | Groundhog Day 2011–Class | Feb 1, 2011: the Tulsa blizzard front, with thundersnow; Nowata −31°F days later |
| 22 | Christmas 1983–Class | Dec 1983: the Arctic outbreak that froze the Plains to the Gulf |
| 23 | Uri 2021–Class | Feb 2021: the Arctic front behind the Texas grid failure |
| 24 | Elliott 2022–Class | Dec 22, 2022: Denver fell ~37°F in an hour |
| 25 | Great Arctic Outbreak 1899–Class | Feb 1899: subzero to the Gulf Coast, ice floes in the Mississippi at New Orleans |
| 26 | Great Blue Norther 1911–Class | Nov 11, 1911: Oklahoma City 83 → 17°F in a day |
| 27 | Browning 1916–Class | Jan 23–24, 1916: 44 → −56°F, 100°F in 24 h (ceiling of realism) |
| 28 | The Hundred-and-Twenty | a 120°F swing in a day |
| 29 | Continental Front | one front, coast to coast, at once |
| 30 | Front Without End | the passage never finishes |
| 31 | The Wall | a vertical cliff of air, warm on one side and arctic a step away |
| 32 | Hemisphere Front | the whole Northern Hemisphere changes air mass |
| 33 | Equator Freeze | the Arctic air reaches the equator |
| 34 | Planetary Front | the whole planet swaps air masses |
| 35 | Cryogenian Front | the front that starts a Snowball Earth |
| 36 | Mars-Class | a Martian sunset swing, ~180°F |
| 37 | Moon-Class | the lunar terminator, ~500°F between sun and shadow |
| 38 | Mercury-Class | the Mercury terminator, ~1,000°F |
| 39 | Terminator Line | the permanent day/night edge of a tidally locked world |
| 40 | Stellar Front | the edge of a star's corona |
| 41 | Supernova Front | the shock wave of an exploding star |
| 42 | Absolute Zero Front | the after-temp reaches −459.67°F |
| 43 | Heat Death Front | the last temperature difference left in the universe |
| 44 | The Last Front | nothing left to cross |
| 45 | Perfect Equilibrium | the scale wraps back to No Front: every air mass the same, everywhere |

## 6. Alerts

The NWS has no "front" alert, so this mode issues the existing products the front sets off:
- **Freeze / Hard Freeze Warning, Frost Advisory:** from the after-front temp and humidity, gated by the existing growing-season logic and `getFrost`
- **Flash freeze:** the existing logic, when the change crosses 32°F onto wet surfaces
- **Wind Advisory / High Wind Warning:** wind-mode criteria on the post-frontal gusts
- **Red Flag Warning / Fire Weather Watch:** dry post-frontal air plus wind, using the wind mode's rule (humidity ≤ 15%, gusts ≥ 25)
- **Dense Fog Advisory:** warm and stationary fronts with saturated air, through the fog mode's logic
- **Special Weather Statement** for a rapid temperature drop (≥ 20°F in ≤ 6 h) with no other product

Severe and winter alerts come from Severe Storm mode and Detailed Input once their cards are run there.

## 7. Impacts and timeline

**Impacts**
- **People caught outside:** dressed for the before temp, standing in the after temp. This is the signature front impact
- **Pipes and plants:** a first hard freeze arriving fast, with nothing covered
- **Roads:** only with a freezing crossing on wet surfaces, or post-frontal crosswinds
- **Schools:** recess and outdoor activities called in; bus stops at the after temp
- **Fire:** dry, gusty post-frontal air

**Front timeline:** an hour-by-hour trace over the transition time. It shows the temperature, the dewpoint, the wind (speed and direction arrow) and the pressure.
- **Cold and Arctic:** the temperature falls fastest in the first hour after passage, with the wind shift, the gust spike and the pressure jump at passage, then levels off.
- **Warm:** a slower, steadier rise; the dewpoint leads the temperature.
- **Dryline:** a sharp dewpoint crash at passage, while the temperature often *rises*.
- **Occluded / stationary:** a flat line held for the duration.

## 8. Fixes surfaced by the runs (separate from the mode)

- Run 3: 0.75″ of slush at 33°F in March came out Moderate with a Winter Weather Advisory and region-wide 2-hour delays. Check the slush impact and advisory threshold at ≥ 33°F on warm-season ground. NWS Tulsa's advisory starts around 1″ of snow.
- Run 3: the storm type was "Flurry Dud, also resembles Polar Vortex Outbreak, Southern Snowpocalypse". The resemblance matcher ignores temperature.
- "Temp before the front" in Detailed Input accepts a rise (run 4) without a note. Say that it only affects flash freeze.

## 9. Decisions

1. **Ladder:** the 45-tier list in §5a, approved 2026-11-22.
2. **Yoopanese:** every new string ships in English and Yoopanese, as with the other modes.
