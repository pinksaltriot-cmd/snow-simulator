"""Build stories/kessler-court.js from the two tabs of Jill's doc
"The Snow War: How It Started" (exported as HTML).

    python3 stories/build_kessler.py EN.html YOOPANESE.html

The English tab goes in as written (the byline is dropped, the "not in the simulator"
note is updated, the link to the Yoopanese tab becomes a pointer to the page's toggle).
The Yoopanese tab gets every Snow War tier name swapped for its Yooper label from
yooper/snow-war-*.js, and the per-tier North/South times copied from the English climb,
said the Yooper way.
"""
import html, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def ladder():
    js = r'''
global.window = {};
const fs = require("fs");
for (const f of ["snow-war-a", "snow-war-b", "snow-war-forts"]) eval(fs.readFileSync("yooper/" + f + ".js", "utf8"));
const s = fs.readFileSync("index.html", "utf8");
const a = s.indexOf("const SNOW_WAR_TIERS = ["), b = s.indexOf("\n];", a);
const T = eval(s.slice(a + "const SNOW_WAR_TIERS = ".length, b + 2));
const Y = window.YOOPER.SNOW_WAR_TIERS;
console.log(JSON.stringify(T.map((t, i) => [i + 1, t.label, (Y[t.label] || {}).label || t.label])));
'''
    return json.loads(subprocess.check_output(['node', '-e', js], cwd=ROOT))

def common(h, lang):
    h = re.sub(r'<p><time[^>]*>.*?</time>.*?</p>\n?', '', h, count=1)
    h = re.sub(r'<h1 id="[^"]*">(.*?)</h1>', r'<div class="ks-title">\1</div>', h, count=1)
    h = h.replace('<mark>', '').replace('</mark>', '').replace('<em></em>', '')
    h = re.sub(r'</em><em>', '', h)
    h = re.sub(r' id="([^"]+)"', lambda m: f' id="ks-{lang}-{m.group(1)}"', h)
    h = h.replace('<table>', '<div class="ks-table-wrap"><table>').replace('</table>', '</table></div>')
    assert '<script' not in h and 'data-atom' not in h
    return h

def clean_en(h):
    h = re.sub(r'<p><em>An invented origin.*?</p>', '<p><em>An invented origin for the Snow War ladder, not a real event. Tier names and numbers come from the current 327-tier ladder.</em></p>', h, count=1, flags=re.S)
    h = re.sub(r'<h2 id="yoopanese">Yoopanese</h2>\s*<p>The whole story.*?</p>', '<p class="ks-note">The whole story, same facts and numbers, said the way a Yooper would: press 🗣️ Yoopanese at the top of the page.</p>', h, flags=re.S)
    return common(h, 'en')

ART = r"(?:da|Da|a|A|its|Its|dere|Dere)"

def yooper_names(h, tiers):
    """Swap every English tier label in the visible text for its Yooper label."""
    pairs = sorted([(en, yp) for _, en, yp in tiers if en != yp], key=lambda p: -len(p[0]))
    alt = '|'.join(re.escape(html.escape(en, quote=True).replace('&#x27;', '&#39;')) for en, _ in pairs)
    to_yp = {html.escape(en, quote=True).replace('&#x27;', '&#39;'): html.escape(yp, quote=False).replace("'", '&#39;') for en, yp in pairs}
    word = re.compile(r'(?<![A-Za-z])(' + ART + r' )?(' + alt + r')(?![A-Za-z]|&#39;)')
    def sub_text(text, before):
        def one(m):
            art, en = m.group(1) or '', m.group(2)
            yp = to_yp[en]
            if art and yp.startswith('Da '):
                yp = yp[3:]
            # "Da" opens a sentence or a heading; mid-sentence it is "da".
            prior = (before + text[:m.start()]).rstrip()
            if not art and yp.startswith('Da ') and prior and re.search(r"[a-z,;']$", prior):
                yp = 'da ' + yp[3:]
            return art + yp
        return word.sub(one, text)
    parts = re.split(r'(<[^>]+>)', h)
    out, quote, prev = [], 0, ''
    block = re.compile(r'<(?:/?(?:p|li|ul|ol|h\d|div|td|th|tr|table|blockquote)\b)')
    for p in parts:
        if p.startswith('<'):
            if p.startswith('<blockquote'): quote += 1
            if p.startswith('</blockquote'): quote -= 1
            if block.match(p): prev = ''
            out.append(p)
        else:
            out.append(p if quote else sub_text(p, prev))
            prev += html.unescape(p)
    return ''.join(out)

def times_from_en(en_html):
    """Each climb bullet's time lines, keyed by the first tier number in its lead."""
    out = {}
    for li in re.finditer(r'<li><p><strong>([^<]*?)\((\d{3})[^<]*</strong>.*?</p>(<ul>.*?</ul>)</li>', en_html, re.S):
        sub = li.group(3)
        lines = re.findall(r'<li><p>(.*?)</p></li>', sub, re.S) or re.findall(r'<li>(.*?)</li>', sub, re.S)
        if any('North' in l and 'South' in l for l in lines):
            out[int(li.group(2))] = [html.unescape(re.sub(r'<[^>]+>', '', l)) for l in lines]
    return out

def yooper_time(line, yp_of):
    m = re.match(r'North: (.+?) · South: (.+)$', line)
    if m:
        return f'Da North got dere {m.group(1)} · da South got dere {m.group(2)}'
    m = re.match(r'(.+?) \((\d{3})\): North (.+?) · South (.+)$', line)
    assert m, line
    return f'{yp_of[int(m.group(2))]} ({m.group(2)}): da North {m.group(3)} · da South {m.group(4)}'

def add_times(h, times, yp_of):
    seen = {}
    def one(m):
        n = int(m.group(2))
        seen[n] = seen.get(n, 0) + 1
        if n not in times: return m.group(0)
        if n == 111 and seen[n] == 1: return m.group(0)   # "Igloo, started": the time sits under "finished"
        items = ''.join(f'<li><p>{html.escape(yooper_time(l, yp_of), quote=False)}</p></li>' for l in times[n])
        return m.group(1) + f'<ul>{items}</ul></li>'
    return re.sub(r'(<li><p><strong>[^<]*?\((\d{3})[^<]*</strong>.*?</p>)</li>', one, h, flags=re.S)

def main(en_path, yp_path):
    tiers = ladder()
    yp_of = {n: yp for n, _, yp in tiers}
    en = clean_en(Path(en_path).read_text())
    yp = Path(yp_path).read_text()
    yp = re.sub(r"<p><em>A made-up origin.*?</p>", "<p><em>A made-up origin for da Snow War ladder, an&#39; it ain&#39;t a real event. Tier names an&#39; numbers come from da current 327-tier ladder.</em></p>", yp, count=1, flags=re.S)
    times = times_from_en(Path(en_path).read_text())
    assert sum(len(v) for v in times.values()) >= 70, len(times)
    yp = add_times(yp, times, yp_of)        # match on the English lead before the names change
    yp = yooper_names(yp, tiers)
    yp = common(yp, 'yp')
    head = ('/* The Kessler Court origin of the Snow War, shown by the Kessler Court Story mode.\n'
            ' * Built by stories/build_kessler.py from Jill\'s doc "The Snow War: How It Started"\n'
            ' * (English tab and Yoopanese tab). An invented story, not a real event. */\n')
    (ROOT / 'stories' / 'kessler-court.js').write_text(head + 'window.KESSLER_STORY = ' + json.dumps({'en': en, 'yooper': yp}, ensure_ascii=False) + ';\n')

if __name__ == '__main__':
    main(*sys.argv[1:3])
