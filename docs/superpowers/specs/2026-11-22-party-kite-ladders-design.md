# New Party Blower War and Kite War Ladders — design

**Date:** 2026-11-22 · **Status:** design approved in conversation (sections 1–3); tier names awaiting Jill's review
**Replaces:** the 327-tier Party Blower and Kite ladders, which retold the snow war tier for tier (v3.7.0 / v3.8.0, parallel rebuild 66d65c9 and later). Those stay in git.

## Decisions (Jill, 2026-11-22)

- The Water War and Cozy War went back to their original 222- and 150-tier ladders (ffc9b59). The war ladders no longer parallel each other.
- Party and Kite get **new, original ladders**, not analogs of the snow war.
- **Sizes:** Party Blower War **100** tiers. Kite War **90** tiers ("a little shorter than party").
- **Story:** each ladder is built on its own weather science: party on real fog and visibility classes, kite on real wind scales (Beaufort, hurricane and tornado classes, record winds). Gear grows naturally with the weather; there is no single invention storyline (the Bellows and Launcher flags go away).
- **Kept:** the driving scores (`fogScore` for party, `windScore` for kite), the band names, and the water war voice.
- **Not kept:** party and kite no longer pair with each other; they are independent ladders of different lengths.

## Shape and thresholds

Both ladders keep today's band boundary scores, so a run lands in the same band it does now (on a new tier). Tier 1 is exactly 0 on both. Thresholds are literal numbers in the source so they can be hand-edited; they are set from the anchors below and interpolated on a log scale between anchors.

### Party Blower War — 100 tiers

| Band | Tiers | Score range | Weather |
|---|---|---|---|
| 1 Clear Day | #1–40 | 0 – 86.5 | clear, haze, mist, patchy fog, fog, Dense Fog Advisory |
| 2 Fog Bank | #41–75 | to 4,712 | all-day and freezing fog, valley/tule fog, sea fog, record fogs; realism edge at #61, fiction after |
| 3 Beyond the Weather | #76–100 | past 4,712 | fiction |

Fog score anchors (fogScore, fog type unless noted, starting 5 am):

| Conditions | Score | Lands on |
|---|---|---|
| clear | 0 | #1 Everyone Can See Everyone |
| haze, 6 mi, 1 h | 0.6 | Haze on the Horizon (#3) |
| mist, 2 mi, 2 h | 5.2 | First Mist / Damp Paper Tongue (#8–9) |
| fog, ⅝ mi, 1 h | 13.7 | Patchy Fog (#14) |
| fog, ½ mi, 2 h | 25.6 | Fog Rolls In (#21) |
| fog, ¼ mi, 2–6 h | 43–68 | Quarter-Mile Fog / Dense Fog Advisory (#29–30) |
| fog, ⅛ mi, 3 h | 79 | One-Eighth Mile (#39) |
| freezing fog, ¼ mi, 12 h | 168 | Freezing Fog (#45) |
| tule fog, 1/16 mi, 24 h | 237 | Tule Fog (#49) |
| Grand Banks, ¼ mi for 20 days | 552 | Grand Banks (#59) |
| London 1952, ~30 ft for 5 days | 727 | The Great Smog of 1952 (#61, realism edge) |

### Kite War — 90 tiers

| Band | Tiers | Score range | Weather |
|---|---|---|---|
| 1 Calm Day | #1–39 | 0 – 429.8 | Beaufort 0–11, about three tiers per force |
| 2 Gale | #40–69 | to 62,660 | hurricane force, hurricane categories, derechos, record gusts, EF3–EF5 tornadoes; realism edge at #60, fiction after |
| 3 Beyond the Weather | #70–90 | past 62,660 | fiction |

Kite thresholds come from windScore at the tier's sustained-wind anchor (general type, gust 1.35× sustained, 6 hours):

| Sustained mph | Score | Lands on |
|---|---|---|
| 0 | 0 | #1 Dead Calm |
| 3 | 0.03 | Light Air (#4) |
| 7 | 0.42 | Light Breeze (#7) |
| 10 | 1.3 | Gentle Breeze (#9) |
| 15 | 4.3 | Moderate Breeze (#12) |
| 21 | 11.8 | Fresh Breeze (#16) |
| 28 | 28.4 | Power Kites Only (#21) |
| 35 | 55 | Near Gale (#24) |
| 42 | 96 | Gale (#27) |
| 50 | 162 | Strong Gale (#30) |
| 59 | 265 | Storm (#33) |
| 68 | 405 | Violent Storm (#36) |
| 80 | 659 | Category 1 (#41) |
| 150 (Barrow Island 1996, 253 gust) | 5,429 | Barrow Island 1996 (#57) |
| 300 | 34,726 | El Reno 2013 (#60, realism edge) |

## Story and voice

- **Party:** fought by sound because nobody can see the other side. The fog decides what's possible. In clear air everyone can see everyone, so there's barely a war. In mist the blowers come out. In dense fog the war goes acoustic: honk codes, call-and-response, roped lanes, echo maps. Record fogs bring standing fog societies, and the fiction band carries fog off the planet, where sound eventually has nothing to travel through.
- **Kite:** fought on the line. The wind decides what flies and what breaks. Dead calm means no war at all. The golden age is 8–25 mph, the real kite-flying window, with fighter kites and line-cutting. Above about 25 mph only power kites fly; past about 40 nothing does, and the war turns to holding ground, anchoring, and saving the kites. The fiction band climbs from supersonic wind to planetary and stellar winds.
- **Voice:** the water war register: plain, deadpan declarative sentences, lots of concrete numbers, slightly funnier than the snow war. Calibration sample: The Next Rain.
- **Real disasters** (the Great Smog of 1952; the named hurricanes, derechos and tornadoes) turn from play to survival, as the water war does near deadly heat. No jokes about deaths; the war stops and people shelter.
- **Endings:** each ladder's last tier resets to its first, as The Next Rain does: The Next Clear Day returns to Everyone Can See Everyone; The Next Breeze returns to Dead Calm.

## Format

Each tier: `{ band, max, css, label, icon, desc }`, where `max` is the upper score threshold, and the last tier's `max` is Infinity.

- **Description:** 2–5 sentences, 30–110 words, at least 2 numbers.
- **CSS:** the existing classes, mapped by band.
- **Yoopanese:** every tier gets a label and description in yooper/party-war.js and yooper/kite-war.js. NWS product names stay in English.

## Tier names

### Party Blower War (100)

**1. Clear Day (40)**
Everyone Can See Everyone · Blower in the Junk Drawer · Haze on the Horizon · One Practice Honk · Distant Ridge Goes Soft · Birthday Leftovers · Streetlight Halos · First Mist · Damp Paper Tongue · Honk Across the Yard · Mist on the Windshield · Echo Test · Fogged Glasses · Patchy Fog · Lost Frisbee · Two-Honk Hello · Shallow Fog · Fog Around the Ankles · Call and Response · Hiding in Plain Mist · Fog Rolls In · Half-Mile Front · Porch Light Beacons · Honk Codes · Roll Call by Sound · Limp Blower Doctrine · Curler on Duty · Fog Lights On · Quarter-Mile Fog · Dense Fog Advisory · Rope Line · Blind Ambush · Bag of Fifty · Duct-Tape Megaphone · Echo Mapping · Cul-de-Sac Fog Front · Party Store Run in the Fog · The Unseen Picnic · One-Eighth Mile · Sound Supremacy

**2. Fog Bank (35)**
Fog Bank · All-Day Fog · School Buses Crawl · Foghorn Envy · Freezing Fog · Rime on the Tongues · Honk Relay · Valley Fog · Tule Fog · Second Day of Fog · Pileup Warning · The Long Gray · Neighborhood Echo Grid · Sea Fog · Harbor Horns · Lighthouse Rivalry · Advection Fog · Point Reyes · Grand Banks · The Pea-Souper · The Great Smog of 1952 · Month of Fog · Five-Foot World · Fog Calendar · The Fog Census · Rope City · Honk Courts · Season Without Sun · Arm's-Length Republic · Bell Towers Rebuilt · The Two-Foot Line · Fog Year · Nose Fog · The Honk Library · One-Foot Fog

**3. Beyond the Weather (25)**
Fog Decade · Fog in the Mail · Continental Fog · The Last Clear Photograph · Fog Thick as Milk · Swimming Through Air · Sound Becomes the Sky · Planetary Fog · Fog Seen from the Moon · The Moon Goes Gray · Fog Between Planets · Titan Accord · Venus Overcast · Nebula Fog · Fog of Ten Thousand Suns · The Galactic Gray · Intergalactic Honk · Dark-Matter Mist · Fog Older Than Light · The Cosmic Haze · Silence Outruns Sound · The Last Honk · Fog Without Air · The Great Gray · The Next Clear Day

### Kite War (90)

**1. Calm Day (39)**
Dead Calm · Kite Leaning on the Garage · Smoke Drifts · Light Air · Running Launch · Leaves Rustle · Light Breeze · First Lift · Gentle Breeze · Diamond Kites Aloft · String Tangle Truce · Moderate Breeze · Box Kite Weather · The Golden Afternoon · Line Cutters · Fresh Breeze · Fighter Kite Season · Tail Discipline · Reel Wars · Strong Breeze · Power Kites Only · Lifted Off the Lawn · Spar Snaps · Near Gale · Grounded Fleet · Walking Against It · Gale · Twigs Break · Kite Shed Lockdown · Strong Gale · Shingles Lift · Anchor Crews · Storm · Trees Down · Reels in the Basement · Violent Storm · Line Inventory · The Waiting Room · Force Eleven Holdout

**2. Gale (30)**
Hurricane Force · Category 1 · Kites in the Bathtub · Category 2 · Derecho · 2020 Iowa Derecho · Category 3 · Taped Windows · Category 4 · EF3 Tornado · Andrew 1992 · Category 5 · Camille 1969 · EF4 Tornado · Allen 1980 · Patricia 2015 · Mount Washington 1934 · Barrow Island 1996 · EF5 Tornado · Bridge Creek 1999 · El Reno 2013 · First Unrecorded Wind · Ground-Level Jet Stream · The Flat Country · Kites Become Anchors · The Bunker Reel · Topsoil Leaves · Hills Sanded Down · The Last Standing Pole · No Line Holds

**3. Beyond the Weather (21)**
Supersonic Wind · Sonic Boom Weather · Saturn Weather · Neptune Class · Kite at Mach Two · Hot Jupiter Winds · WASP-127b · Escape Breeze · Solar Wind · Solar Sail Kites · Coronal Mass Ejection · Pulsar Wind · Supernova Front · Galactic Wind · Quasar Outflow · Relativistic Jet · The Wind Between Galaxies · Dark Energy Draft · The Last Gust · Heat Death Calm · The Next Breeze

## Implementation

- Replace the blocks between `PARTY_WAR_TIERS:BEGIN/END` and `KITE_WAR_TIERS:BEGIN/END`, plus their header comments. The lookup functions (`partyWarTierFor`, `kiteWarTierFor`) and list renderers stay; check them for any dependence on the 327 length, the `bellows` and `launcher` flags, or the snow war's css bands.
- Replace yooper/party-war.js and yooper/kite-war.js.
- Descriptions are drafted band by band against this spec and the voice sample, then checked against the format rules.

## Testing

Selftest blocks for party and kite are rewritten:
- counts (100 and 90) and band counts (40/35/25, 39/30/21);
- unique labels, strictly increasing thresholds, tier 1 = 0, last = Infinity;
- every anchor in the two tables above lands on its named tier;
- monotonic: the tier never drops as fog or wind worsens;
- format rules per description;
- every tier has a Yooper entry, and Yooper mode keeps numbers intact;
- the list renders 100 / 90 rows under the three band headings.

Then run the full selftest, resync the line count, commit, and push to main (Jill: "commit and push when done").
