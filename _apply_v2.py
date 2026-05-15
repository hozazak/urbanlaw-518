#!/usr/bin/env python3
"""Apply P1+P2+P3 design upgrades to index-v2.html (one-shot)."""
import re
import sys

PATH = '/Users/youngbin/Downloads/urbanlaw-518/index-v2.html'

with open(PATH, 'r', encoding='utf-8') as f:
    html = f.read()

orig_len = len(html)
print(f'[in] {orig_len:,} chars')

# ============================================================
# CSS overrides — inject right before last </style>
# ============================================================
overrides = """
/* ============================================================
   v2 OVERRIDES — applied 2026-05-15
   P1-1: 표지 출판 메타포 확장 (FIG/foot stamp/watermark UL)
   P1-2: p3 win/fail 양음각 대비
   P1-3: p15-17 hero number
   P1-4: p19 4카드 → 시간순 흐름 (PHASE + 화살표)
   P2-5: p7 외곽 노드 페이드
   P2-6: dark slide UL watermark (light에도 옅게)
   P2-7: 격자 강도 강화
   P2-8: p13 luggage tag 깊이감
============================================================ */

/* P2-7: 격자 강도 강화 (0.035 → 0.055) */
section::after{
  background-image:
    linear-gradient(to right, rgba(15,38,71,0.055) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(15,38,71,0.055) 1px, transparent 1px) !important;
}
section.dark::after{
  background-image:
    linear-gradient(to right, rgba(255,255,255,0.06) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255,255,255,0.06) 1px, transparent 1px) !important;
}

/* P2-6: Watermark "UL" — slide 우상단 (cover 제외, 이미 있음) */
section:not(.cover)::before{
  content: 'UL';
  position: absolute;
  top: 38px;
  right: 110px;
  font-family: var(--mono);
  font-size: 22px;
  font-weight: 900;
  color: rgba(15,38,71,0.22);
  letter-spacing: 0.2em;
  line-height: 1;
  z-index: 3;
  pointer-events: none;
}
section.dark:not(.cover)::before{
  color: rgba(77,201,176,0.45);
}

/* P1-1: meta — FIG.NN + 페이지번호 */
.meta .fig-num{
  font-family: var(--mono);
  font-size: 20px;
  font-weight: 700;
  color: var(--ink-3);
  letter-spacing: 0.18em;
}
.meta .meta-sep{
  display: inline-block;
  margin: 0 10px;
  color: var(--ink-4);
  font-weight: 400;
}
section.dark .meta .fig-num{ color: rgba(255,255,255,0.58); }
section.dark .meta .meta-sep{ color: rgba(255,255,255,0.35); }

/* P1-1: foot stamp */
.foot .foot-stamp{
  font-family: var(--mono);
  font-size: 18px;
  font-weight: 800;
  color: var(--navy);
  letter-spacing: 0.18em;
  padding: 3px 10px;
  border: 1.5px solid var(--line);
  border-radius: 3px;
  margin-right: 4px;
}
.foot .foot-sep{
  margin: 0 14px;
  color: var(--ink-4);
}
.foot .foot-by{
  color: var(--ink-4);
}
section.dark .foot .foot-stamp{
  color: var(--paper);
  border-color: rgba(255,255,255,0.35);
}
section.dark .foot .foot-sep{ color: rgba(255,255,255,0.4); }
section.dark .foot .foot-by{ color: rgba(255,255,255,0.65); }

/* P1-2: p3 win/fail 양음각 대비 */
section[data-screen-label^="03 "] .res-col.win{
  background: linear-gradient(135deg, var(--teal-soft) 0%, rgba(215,235,232,0.45) 100%) !important;
  border: 1.5px solid var(--teal) !important;
  box-shadow: 0 12px 32px rgba(14,124,117,0.14), 0 4px 10px rgba(14,124,117,0.08) !important;
  transform: translateY(-6px);
}
section[data-screen-label^="03 "] .res-col.fail{
  background: var(--paper-3) !important;
  border: 1px solid var(--line-soft) !important;
  filter: saturate(0.55) brightness(0.97);
  box-shadow: inset 0 2px 8px rgba(15,38,71,0.10) !important;
}
section[data-screen-label^="03 "] .res-col.fail .verdict-icon,
section[data-screen-label^="03 "] .res-col.fail .stamp{
  opacity: 0.78;
}

/* P1-3: p15-17 hero number */
.case-hero{
  display: flex;
  align-items: center;
  gap: 36px;
  padding: 22px 38px 22px 34px;
  margin: 14px 0 22px;
  background: linear-gradient(90deg, var(--teal-soft) 0%, rgba(215,235,232,0.15) 70%, transparent 100%);
  border-left: 5px solid var(--teal);
  border-radius: 0 8px 8px 0;
}
.case-hero .hero-tag{
  font-family: var(--mono);
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 0.22em;
  color: var(--teal);
  text-transform: uppercase;
  white-space: nowrap;
  align-self: flex-start;
  padding-top: 18px;
}
.case-hero .hero-num{
  font-size: 88px;
  font-weight: 800;
  letter-spacing: -0.035em;
  color: var(--navy);
  line-height: 1;
  font-feature-settings: "tnum";
}
.case-hero .hero-num .hero-unit{
  font-size: 0.55em;
  font-weight: 700;
  color: var(--teal);
  margin-left: 4px;
  vertical-align: 14px;
}
.case-hero .hero-cap{
  font-size: 20px;
  color: var(--ink-2);
  font-weight: 500;
  flex: 1;
  line-height: 1.45;
  padding-bottom: 4px;
  align-self: flex-end;
  max-width: 580px;
}
.case-hero.case-hero-warn{
  background: linear-gradient(90deg, rgba(184,58,20,0.10) 0%, rgba(184,58,20,0.03) 70%, transparent 100%);
  border-left-color: var(--warn);
}
.case-hero.case-hero-warn .hero-tag,
.case-hero.case-hero-warn .hero-num{ color: var(--warn); }
.case-hero.case-hero-warn .hero-num .hero-unit{ color: var(--warn); }

/* P1-4: p19 4카드 → 시간순 흐름 */
section[data-screen-label^="19 "] .road-grid{
  gap: 48px !important;
  position: relative;
}
section[data-screen-label^="19 "] .road-card{
  position: relative;
}
section[data-screen-label^="19 "] .road-card::before{
  content: 'PHASE';
  display: block;
  font-family: var(--mono);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.22em;
  color: var(--teal);
  margin-bottom: 6px;
}
section[data-screen-label^="19 "] .road-card:not(:last-child)::after{
  content: '→';
  position: absolute;
  right: -34px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 30px;
  color: var(--teal);
  font-weight: 800;
  z-index: 3;
  line-height: 1;
}

/* P2-5: p7 외곽 노드 페이드 (옅은 가중치) */
section[data-screen-label^="07 "] g.node-edge:nth-of-type(n+4) circle{
  opacity: 0.88;
}
section[data-screen-label^="07 "] g.node-edge:nth-of-type(n+7) circle{
  opacity: 0.78;
}

/* P2-8: p13 luggage tag 깊이감 */
section[data-screen-label^="13 "] .ke-rtag{
  filter: drop-shadow(0 3px 5px rgba(15,38,71,0.10)) drop-shadow(0 14px 26px rgba(15,38,71,0.08));
}

/* head z-index — watermark 위로 */
.head{ position: relative; z-index: 2; }
"""

if '</style>' not in html:
    print('[!] no </style> tag found', file=sys.stderr)
    sys.exit(1)

# Inject before the FIRST </style> in head section
# Find the last </style> that comes before <body>
body_idx = html.find('<body>')
style_close_idx = html.rfind('</style>', 0, body_idx)
if style_close_idx == -1:
    print('[!] no </style> before <body>', file=sys.stderr)
    sys.exit(1)

html = html[:style_close_idx] + overrides + '\n' + html[style_close_idx:]
print(f'[ok] injected CSS overrides ({len(overrides):,} chars)')

# ============================================================
# P1-1: meta transformation
# ============================================================
def meta_replace(m):
    nn = m.group(1)
    return (
        f'<div class="meta">'
        f'<span class="fig-num">FIG.{nn}</span>'
        f'<span class="meta-sep">·</span>'
        f'<strong>{nn}</strong>/20'
        f'</div>'
    )

html, n_meta = re.subn(
    r'<div class="meta"><strong>(\d{2})</strong>\s*/\s*20</div>',
    meta_replace,
    html
)
print(f'[ok] meta transformed: {n_meta} slides')

# ============================================================
# P1-1: foot stamp transformation
# ============================================================
OLD_FOOT = '<div>도시조경본부 도시설계팀 / AI 실무 성과 보고 / 2026.05</div>'
NEW_FOOT = (
    '<div>'
    '<span class="foot-stamp">INTERNAL · URBANLAW VOL.01</span>'
    '<span class="foot-sep">·</span>'
    '<span class="foot-by">도시조경본부 도시설계팀 / 2026.05</span>'
    '</div>'
)
n_foot = html.count(OLD_FOOT)
html = html.replace(OLD_FOOT, NEW_FOOT)
print(f'[ok] foot transformed: {n_foot} slides')

# ============================================================
# P1-3: hero number insertion for p15/p16/p17
# ============================================================
heroes = [
    {  # p15 (1st occurrence)
        'tag': 'CASE 01 · 결론 수치',
        'num': '720',
        'unit': '%',
        'cap': '관광숙박 특례 상한 — 마포 조례 §51② 다목 (시도시계획위 심의)',
        'cls': '',
    },
    {  # p16 (2nd)
        'tag': 'CASE 02 · 결론 수치',
        'num': '250',
        'unit': '%',
        'cap': '한시 완화 상한 — 조례 §51②⑨ + 소규모주택정비법 §49 (2028.5.18까지)',
        'cls': '',
    },
    {  # p17 (3rd)
        'tag': 'CASE 03 · 결론',
        'num': '불가',
        'unit': '',
        'cap': '3중 정량 입증 — 개특법 §12 + 산지법 §12 + 서울 조례 §44·§48',
        'cls': 'case-hero-warn',
    },
]

count = {'i': 0}
def insert_hero(m):
    i = count['i']
    count['i'] += 1
    if i >= 3:
        return m.group(0)
    h = heroes[i]
    unit_html = f'<span class="hero-unit">{h["unit"]}</span>' if h['unit'] else ''
    hero_html = (
        f'<div class="case-hero {h["cls"]} anim d2">\n'
        f'      <div class="hero-tag">{h["tag"]}</div>\n'
        f'      <div class="hero-num">{h["num"]}{unit_html}</div>\n'
        f'      <div class="hero-cap">{h["cap"]}</div>\n'
        f'    </div>\n\n'
        f'    <div class="case-2col anim d3">'
    )
    return hero_html

html, n_hero = re.subn(
    r'<div class="case-2col anim d2">',
    insert_hero,
    html
)
print(f'[ok] hero inserted: {min(count["i"], 3)} / matched: {n_hero}')

# ============================================================
# Save
# ============================================================
new_len = len(html)
print(f'[out] {new_len:,} chars (delta: {new_len - orig_len:+,})')

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print('[done] saved to index-v2.html')
