"""Build stories/origin-story.js from Jill's doc "How the Snow War Started"
(one tab, exported as HTML: an "English" section, then a "Yoopanese" section).

    python3 stories/build_origin.py "How the Snow War Started.html"

The byline is dropped, the two language sections are split apart, and each gets its
own title. The Yoopanese section already uses the Yooper tier names, so it goes in as written.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TITLES = {'en': 'How the Snow War Started', 'yp': 'How Da Whole Ting Started'}

def tidy(h, lang):
    h = re.sub(r' id="([^"]+)"', lambda m: f' id="os-{lang}-{m.group(1)}"', h)
    h = h.replace('<table>', '<div class="os-table-wrap"><table>').replace('</table>', '</table></div>')
    assert '<script' not in h and 'data-atom' not in h and '<h2' not in h, lang
    return f'<div class="os-title">{TITLES[lang]}</div>\n' + h.strip() + '\n'

def main(src):
    h = Path(src).read_text()
    en_at = h.index('<h2 id="english">English</h2>')
    yp_at = h.index('<h2 id="yoopanese">Yoopanese</h2>')
    en = h[en_at + len('<h2 id="english">English</h2>'):yp_at]
    yp = h[yp_at + len('<h2 id="yoopanese">Yoopanese</h2>'):]
    head = ('/* The origin of the Snow War (Nov 16, 2026 – Nov 15, 2029), shown by the Origin Story mode.\n'
            ' * Built by stories/build_origin.py from Jill\'s doc "How the Snow War Started"\n'
            ' * (English and Yoopanese sections). An invented story, not a real event. */\n')
    out = ROOT / 'stories' / 'origin-story.js'
    out.write_text(head + 'window.ORIGIN_STORY = ' + json.dumps({'en': tidy(en, 'en'), 'yooper': tidy(yp, 'yp')}, ensure_ascii=False) + ';\n')
    print('wrote', out)

if __name__ == '__main__':
    main(sys.argv[1])
