# New Party Blower and Kite War Ladders Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the 327-tier snow-analog Party Blower and Kite War ladders with original 100- and 90-tier ladders built on fog and wind science, in English and Yoopanese.

**Architecture:** Each ladder is a literal array between existing `// PARTY_WAR_TIERS:BEGIN/END` and `// KITE_WAR_TIERS:BEGIN/END` markers in `index.html`. Lookups (`partyWarTierFor`, `kiteWarTierFor`), getters, cells and list renderers stay as they are. Thresholds are computed once from anchors by a scratch script and pasted in as literals. Descriptions are drafted band by band.

**Tech Stack:** single-file vanilla JS app (`snow-simulator/index.html`), browser selftest (`index.html?selftest=1`, console `SELFTEST n/n PASS`), served by the `snow-simulator` launch config on port 8080.

**Spec:** `snow-simulator/docs/superpowers/specs/2026-11-22-party-kite-ladders-design.md` (tier names, bands, anchors, voice — approved).

## Global Constraints

- Party: exactly 100 tiers, bands 40/35/25, band names `Clear Day | Fog Bank | Beyond the Weather`; tier 40 `max` = 86.5, tier 75 `max` = 4712, tier 100 `max` = Infinity, tier 1 `max` = 0.
- Kite: exactly 90 tiers, bands 39/30/21, band names `Calm Day | Gale | Beyond the Weather`; tier 39 `max` = 429.8, tier 69 `max` = 62660, tier 90 `max` = Infinity, tier 1 `max` = 0.
- Tier labels and order exactly as the spec's "Tier names" lists.
- Tier object: `{ band, max, css, label, icon, desc }`. No `bellows` / `launcher` fields.
- Description: 2–5 sentences, 30–110 words, at least 2 numerals. Water war voice (deadpan, many concrete numbers, slightly funny); The Next Rain is the calibration sample. Real deadly events (Great Smog of 1952, named hurricanes, derechos, tornadoes) are written as survival, never jokes. Last tier resets to the first.
- Yoopanese for every tier (`label` and `desc`), numbers unchanged; NWS product names stay English.
- Do not touch the water, cozy or snow ladders.

## Review Focus

- A score exactly on a threshold lands on the lower tier (`s <= max`) — tests check anchors at and just above band ends.
- Negative, NaN or missing scores land on tier 1 (existing lookup clamps; keep a test).
- Yooper mode must not change which tier is chosen (scoring is English) — keep the existing "tier is English in Yooper mode" test.
- A cached browser serves stale `index.html` / `yooper/*.js`: fetch with `{cache:'reload'}` before every selftest run.
- Old 327-tier labels must be gone from the Yooper files, or the "every tier has a Yooper entry" test passes vacuously on stale keys — test that no Yooper key is outside the English ladder.

---

### Task 1: Party Blower War — English ladder

**Files:**
- Modify: `snow-simulator/index.html` — Party header comment (above `const PARTY_WAR_BANDS`), the block between `// PARTY_WAR_TIERS:BEGIN` and `:END`, and the `// PB1` selftest block (replace it whole).

**Interfaces:**
- Consumes: `fogScore({vis, hours, type, start})`, `partyWarTierFor(score) -> {tier, index}`, `renderPartyWarList()`.
- Produces: `PARTY_WAR_TIERS` (100), unchanged `PARTY_WAR_BANDS`.

- [ ] **Step 1: Write the new PB1 test block** (replaces the old one; keep the Yooper sub-tests for Task 2):

```js
// PB1 Party Blower War: 100 original fog tiers
window.__snowTests.push((t) => {
  const P = PARTY_WAR_TIERS, at = s => partyWarTierFor(s).index + 1;
  const f = (vis, hours, type) => fogScore({ vis, hours, type: type || 'fog', start: 5 });
  t('party war has 100 tiers', P.length === 100);
  t('party band counts 40/35/25', [1,2,3].map(b => P.filter(x => x.band === b).length).join(',') === '40,35,25');
  t('party labels unique', new Set(P.map(x => x.label)).size === 100);
  t('party thresholds strictly increase', P.every((x, i) => i === 0 || x.max > P[i - 1].max));
  t('party tier 1 is 0, band ends 86.5 / 4712, last Infinity', P[0].max === 0 && P[39].max === 86.5 && P[74].max === 4712 && P[99].max === Infinity);
  t('party first and last labels', P[0].label === 'Everyone Can See Everyone' && P[99].label === 'The Next Clear Day');
  [[f(6,1,'haze'),3],[f(2,2,'mist'),9],[f(0.625,1),14],[f(0.5,2),21],[f(0.25,2),29],[f(0.25,6),30],[f(0.125,3),39],
   [f(0.25,12,'freezing'),45],[f(1/16,24),49],[f(0.25,480),59],[f(30/5280,120),61],[86.5,40],[86.51,41],[4712,75],[4712.01,76],[0,1],[-5,1]]
    .forEach(([s, n]) => t(`party anchor ${+s.toFixed(2)} -> #${n} ${P[n-1].label}`, at(s) === n));
  const bad = P.filter(x => { const w = x.desc.split(/\s+/).length, n = (x.desc.match(/\d[\d,.]*/g) || []).length,
    se = x.desc.split(/[.!?](?=\s|$)/).filter(z => z.trim()).length; return !x.icon || n < 2 || se < 2 || se > 5 || w < 30 || w > 110; });
  t('every party desc follows the format' + (bad.length ? ' (' + bad.slice(0,5).map(x => x.label).join(', ') + ')' : ''), bad.length === 0);
  t('party css runs pb0-pb15 by band', P.every(x => /^pb(\d|1[0-5])$/.test(x.css)) && P[0].css === 'pb0' && P[99].css === 'pb15');
  t('Party War list renders 100 rows under 3 bands', document.querySelectorAll('#partyWarList .war-row').length === 100
    && [...document.querySelectorAll('#partyWarList .cozy-band-head')].map(e => e.textContent).join('|') === 'Clear Day|Fog Bank|Beyond the Weather');
});
```

- [ ] **Step 2: Run selftest (cache-busted); expect the PB1 failures** (count 327, band counts, anchors).

- [ ] **Step 3: Compute the 100 thresholds** with a scratch script run in the page (it needs `fogScore`). Knots: tier 1 = 0, tier 40 = 86.5, tier 75 = 4712, tier 100 = Infinity, plus each anchor score from the test (score `s` → tier `n`): set `max[n] = s·1.04` and `max[n-1] = s/1.04`; when two anchors sit on adjacent tiers, set the shared boundary to the geometric mean of their scores. Fill the rest by log interpolation between knots (tier 2 starts from 0.01). Round to 3 significant figures (up for a tier's own anchor, so the anchor stays on it), keep strictly increasing, and keep band ends exact.

- [ ] **Step 4: Draft the 100 tiers** — label (spec order), band, icon (one emoji), desc (constraints above). Story beats by band are in the spec "Story and voice". css: band 1 → pb0–pb5, band 2 → pb6–pb11, band 3 → pb12–pb15, assigned evenly by position within the band (`lo + Math.floor((hi - lo + 1) * k / n)`).

- [ ] **Step 5: Paste the array between the markers** and rewrite the header comment: 100 tiers, driven by fogScore, bands with tier ranges and band-end scores, original fog-science ladder (no longer a snow analog).

- [ ] **Step 6: Run selftest; PB1 passes, nothing else fails** except the Yooper party tests (Task 2).

- [ ] **Step 7: Commit** `index.html` — "Party Blower War: new 100-tier fog ladder".

### Task 2: Party Blower War — Yoopanese

**Files:**
- Replace: `snow-simulator/yooper/party-war.js` (same wrapper: `window.YOOPER.PARTY_WAR_TIERS = Object.assign(..., { "<English label>": { label, desc } })`; header comment says 100 tiers).
- Modify: the PB1 block, adding the Yooper tests.

- [ ] **Step 1: Add tests to PB1:**

```js
  const Y = (window.YOOPER && window.YOOPER.PARTY_WAR_TIERS) || {};
  const nums = x => (x.match(/\d+(?:[.,]\d+)*/g) || []).join('|');
  const missing = P.filter(x => !(Y[x.label] && Y[x.label].label && Y[x.label].desc)).map(x => x.label);
  t('every party tier has a Yooper entry (' + missing.length + ' missing)', missing.length === 0);
  t('no stale Yooper party keys', Object.keys(Y).every(k => P.some(x => x.label === k)));
  t('Yooper party descs keep every number', P.every(x => !Y[x.label] || nums(Y[x.label].desc) === nums(x.desc)));
  t('party war tier is English in Yooper mode', YOOP.withLang('yooper', () => getPartyWar({ score: 50 })).label === getPartyWar({ score: 50 }).label);
```

- [ ] **Step 2: Run selftest; expect those to fail.**
- [ ] **Step 3: Write `yooper/party-war.js`** for all 100 tiers in the existing Yooper register (da/dat/eh, "yah", U.P. references where natural), numbers verbatim.
- [ ] **Step 4: Run selftest; all PB1 tests pass.**
- [ ] **Step 5: Commit** `yooper/party-war.js index.html` — "Party Blower War: Yoopanese".

### Task 3: Kite War — English ladder

**Files:**
- Modify: `snow-simulator/index.html` — Kite header comment, the block between `// KITE_WAR_TIERS:BEGIN` and `:END`, and the `// KW1` selftest block (replace whole).

**Interfaces:**
- Consumes: `windScore({sust, gust, hours, type})`, `kiteWarTierFor(score)`, `renderKiteWarList()`.
- Produces: `KITE_WAR_TIERS` (90), unchanged `KITE_WAR_BANDS`.

Per-tier top wind speed V (mph); `max[n] = windScore({sust: V, gust: 1.35·V, hours: 6, type: 'general'})`, rounded **up** to 4 significant figures (rounding down would push an anchor speed onto the next tier):

| Tiers | V |
|---|---|
| 1 | 0 (max exactly 0) |
| 2–11 | 1, 2, 3, 5, 6, 7, 9, 10, 11, 12 |
| 12–23 | 15, 16, 17, 18, 21, 22, 23, 24, 26, 28, 30, 31 |
| 24–38 | 35, 36.5, 38, 42, 44, 46, 50, 52, 54, 59, 61, 63, 68, 68.5, 69 |
| 39 | band end: max exactly 429.8 |
| 40–60 | 74, 85, 95, 105, 108, 112, 120, 125, 140, 150, 155, 160, 175, 185, 190, 215, 231, 253, 270, 301, 302 |
| 61–68 | 310, 318, 326, 334, 340, 346, 352, 357 |
| 69 | band end: max exactly 62660 |
| 70–89 | log-spaced from 62660 to 1e30 |
| 90 | Infinity |

- [ ] **Step 1: Write the new KW1 test block:**

```js
// KW1 Kite War: 90 original wind tiers
window.__snowTests.push((t) => {
  const K = KITE_WAR_TIERS, at = s => kiteWarTierFor(s).index + 1;
  const w = V => windScore({ sust: V, gust: 1.35 * V, hours: 6, type: 'general' });
  t('kite war has 90 tiers', K.length === 90);
  t('kite band counts 39/30/21', [1,2,3].map(b => K.filter(x => x.band === b).length).join(',') === '39,30,21');
  t('kite labels unique', new Set(K.map(x => x.label)).size === 90);
  t('kite thresholds strictly increase', K.every((x, i) => i === 0 || x.max > K[i - 1].max));
  t('kite tier 1 is 0, band ends 429.8 / 62660, last Infinity', K[0].max === 0 && K[38].max === 429.8 && K[68].max === 62660 && K[89].max === Infinity);
  t('kite first and last labels', K[0].label === 'Dead Calm' && K[89].label === 'The Next Breeze');
  [[w(3),4],[w(7),7],[w(10),9],[w(15),12],[w(21),16],[w(28),21],[w(35),24],[w(42),27],[w(50),30],[w(59),33],[w(68),36],
   [w(80),41],[w(140),48],[w(253),57],[w(302),60],[429.8,39],[429.81,40],[62660,69],[62660.1,70],[0,1],[-1,1]]
    .forEach(([s, n]) => t(`kite anchor ${+s.toFixed(2)} -> #${n} ${K[n-1].label}`, at(s) === n));
  let prev = -1, mono = true;
  for (let V = 0; V <= 1000; V += 0.5) { const i = at(w(V)); if (i < prev) mono = false; prev = i; }
  t('kite war never drops as the wind rises', mono);
  // same format check and css check as PB1, with kw0-kw15
  t('Kite War list renders 90 rows under 3 bands', document.querySelectorAll('#kiteWarList .war-row').length === 90
    && [...document.querySelectorAll('#kiteWarList .cozy-band-head')].map(e => e.textContent).join('|') === 'Calm Day|Gale|Beyond the Weather');
});
```

(The format and css tests are PB1's two tests with `K`, `kw`; copy them.)

- [ ] **Step 2: Run selftest; expect KW1 failures.**
- [ ] **Step 3: Compute the 90 thresholds** in the page from the V table.
- [ ] **Step 4: Draft the 90 tiers** — label (spec order), band, icon, desc. Descriptions of real tiers use the tier's real figures (Beaufort land descriptions; Saffir-Simpson and EF ranges; Iowa 2020 derecho 140 mph gust; Andrew 1992; Camille 1969; Allen 1980 190 mph; Patricia 2015 215 mph; Mount Washington 1934 231 mph; Barrow Island 1996 253 mph; Bridge Creek 1999 301 mph; El Reno 2013 302 mph, 2.6 miles wide). css: band 1 → kw0–kw5, band 2 → kw6–kw11, band 3 → kw12–kw15, as in Task 1.
- [ ] **Step 5: Paste the array** and rewrite the header comment (90 tiers, windScore, bands, top-speed placement, original wind-science ladder).
- [ ] **Step 6: Run selftest; KW1 passes**, except its Yooper tests.
- [ ] **Step 7: Commit** — "Kite War: new 90-tier wind ladder".

### Task 4: Kite War — Yoopanese

Same as Task 2 with `yooper/kite-war.js`, `window.YOOPER.KITE_WAR_TIERS`, `K`, `getKiteWar({ score: 50 })`. Commit — "Kite War: Yoopanese".

### Task 5: Release check and push

- [ ] **Step 1:** Run the full selftest (cache-busted); expect `SELFTEST n/n PASS`.
- [ ] **Step 2:** In the app, open Party Blower War Tiers and Kite War Tiers (English and Yoopanese) and run one fog city (Fresno, ¼ mi, 6 h) and one wind city (Denver, 35/50 mph, 6 h); confirm the war cells show new tiers.
- [ ] **Step 3:** Update the card counts' hint text if it names old tiers; resync the subheading line count to `wc -l < index.html`.
- [ ] **Step 4:** Commit and `git push origin main`.
- [ ] **Step 5:** Update memory `project_parallel_war_ladders.md` (party 100, kite 90, shipped commit).
