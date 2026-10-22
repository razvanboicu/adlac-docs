#!/usr/bin/env python3
"""Apply ADLAC expanded documentation to an existing static GitHub Pages checkout.
No external dependencies. Safe to rerun; preserves page bodies and other integrations.
"""
from pathlib import Path
import json, re, shutil, sys, html

PACKAGE = Path(__file__).resolve().parent
if len(sys.argv) != 2:
    sys.exit('Usage: py apply_adlac_expansion.py PATH_TO_DOCS_REPOSITORY')
ROOT = Path(sys.argv[1]).expanduser().resolve()
if not (ROOT/'adlac'/'sections-reference'/'index.html').exists() or not (ROOT/'assets'/'docs.js').exists():
    sys.exit(f'Error: {ROOT} does not appear to be the ADLAC documentation repository root.')
META = json.loads((PACKAGE/'manifest.json').read_text(encoding='utf-8'))

basic_nav = [
('Start', [('Overview','/adlac/index.html'),('Getting started','/adlac/getting-started/index.html'),('Theme settings','/adlac/theme-settings/index.html')]),
('Store structure',[('Header & navigation','/adlac/header-navigation/index.html'),('Footer & localization','/adlac/footer-localization/index.html'),('Product page','/adlac/products/index.html'),('Quick Buy','/adlac/quick-buy/index.html'),('Collections','/adlac/collections/index.html'),('Search & filtering','/adlac/search-filtering/index.html'),('Cart & checkout','/adlac/cart-checkout/index.html')]),
('Content',[('Homepage & sections','/adlac/homepage-sections/index.html'),('Section reference','/adlac/sections-reference/index.html'),('Blog & pages','/adlac/blog-pages/index.html')]),
]
extra_nav = [
('Integrations',[('Product specifications','/adlac/product-specifications/index.html'),('Reviews & app blocks','/adlac/reviews-apps/index.html'),('Markets & languages','/adlac/markets-localization/index.html')]),
('Help',[('FAQ','/adlac/faq/index.html'),('Troubleshooting','/adlac/troubleshooting/index.html'),('Support','/adlac/support/index.html'),('Privacy policy','/privacy/index.html'),('Changelog','/adlac/changelog/index.html')])]

def build_nav(current):
    out=[]
    def link(title,href):
        active=' aria-current="page"' if current==href else ''
        return f'<a href="{href}"{active}>{html.escape(title)}</a>'
    for group,items in basic_nav:
        out.append(f'<div class="sidebar-title">{html.escape(group)}</div>')
        out.extend(link(t,h) for t,h in items)
    out.append('<div class="sidebar-title">Section guides</div>')
    for group, items in META['section_groups']:
        opened=' open' if any(current == item['url'] for item in items) else ''
        out.append(f'<details class="doc-nav-group"{opened}><summary>{html.escape(group)} <span class="nav-count">{len(items)}</span></summary>')
        out.extend(link(item['title'],item['url']) for item in items)
        out.append('</details>')
    feats=[x for x in META['entries'] if x['href'].startswith('guides/')]
    opened=' open' if any(current=='/adlac/'+item['href'] for item in feats) else ''
    out.append('<div class="sidebar-title">Feature guides</div>')
    out.append(f'<details class="doc-nav-group"{opened}><summary>Feature walkthroughs <span class="nav-count">{len(feats)}</span></summary>')
    out.extend(link(item['title'],'/adlac/'+item['href']) for item in feats)
    out.append('</details>')
    for group,items in extra_nav:
        out.append(f'<div class="sidebar-title">{html.escape(group)}</div>')
        out.extend(link(t,h) for t,h in items)
    return '\n'.join(out)

# Add new pages only if missing; overwrite only generated feature-guide pages on rerun.
new=0
for p in (PACKAGE/'new_pages').rglob('index.html'):
    rel=p.relative_to(PACKAGE/'new_pages')
    dest=ROOT/rel
    if dest.exists() and 'ADLAC expanded docs generated' not in dest.read_text(encoding='utf-8'):
        print(f'Skipping manually edited new page: {rel}')
        continue
    dest.parent.mkdir(parents=True,exist_ok=True)
    contents=p.read_text(encoding='utf-8')
    dest.write_text('<!-- ADLAC expanded docs generated: section and feature guides -->\n'+contents,encoding='utf-8')
    new+=1

# Update only existing ADLAC page navigation, not content, support JS, Turnstile key, or privacy page.
nav_pattern=re.compile(r'(<nav\b[^>]*\bdata-sidebar\b[^>]*>)(.*?)(</nav>)',re.S)
changed=0
for p in (ROOT/'adlac').rglob('index.html'):
    rel=p.relative_to(ROOT)
    current='/'+rel.as_posix()
    data=p.read_text(encoding='utf-8')
    def repl(m):return m.group(1)+'\n'+build_nav(current)+'\n'+m.group(3)
    result,count=nav_pattern.subn(repl,data,count=1)
    if count!=1:
        print('Warning: no navigation found in',rel)
        continue
    if result!=data:
        p.write_text(result,encoding='utf-8');changed+=1

# A clickable catalog on the reference page (the full source reference remains unmodified).
ref_path=ROOT/'adlac'/'sections-reference'/'index.html'
raw=ref_path.read_text(encoding='utf-8')
start='<!-- ADLAC EXPANDED SECTION CATALOG START -->'
end='<!-- ADLAC EXPANDED SECTION CATALOG END -->'
if start in raw and end in raw:
    raw=re.sub(re.escape(start)+r'.*?'+re.escape(end),'',raw,flags=re.S)
items=''.join(f'<li><a href="{x["url"]}">{html.escape(x["title"])}</a></li>' for g,ls in META['section_groups'] for x in ls)
catalog=f'''{start}\n<div class="callout"><strong>Individual section guides</strong>Open a dedicated page for any ADLAC section. Each page lists the available controls, defaults and blocks.</div>\n<div class="section-guide-catalog"><ul>{items}</ul></div>\n{end}\n'''
raw,count=re.subn(r'(?=<section class="ref-section" id=)',lambda m:catalog,raw,count=1)
if count:ref_path.write_text(raw,encoding='utf-8')
else:print('Warning: Could not insert section guide catalog')

# Merge into existing search list and keep any manual/custom index entries.
idx_path=ROOT/'adlac'/'search-index.js'
idx_raw=idx_path.read_text(encoding='utf-8')
match=re.search(r'window\.ADLAC_SEARCH_INDEX\s*=\s*(\[.*\])\s*;',idx_raw,re.S)
if not match:sys.exit('Error: search-index.js structure is unexpected; navigation was updated, but search index needs manual review.')
items=json.loads(match.group(1));existing={x.get('href') for x in items}
for e in META['entries']:
    if e['href'] not in existing:
        items.append(e);existing.add(e['href'])
    else:
        for i,item in enumerate(items):
            if item.get('href')==e['href']:
                items[i]=e;break
idx_path.write_text('window.ADLAC_SEARCH_INDEX = '+json.dumps(items,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')

# Preserve all other JS functionality: fix old relative result URLs, include summaries and rank title matches.
js=ROOT/'assets'/'docs.js'
jstxt=js.read_text(encoding='utf-8')
if 'const href = x.href.startsWith' not in jstxt:
    old='''matches.map(x => `<a href="${x.href}"><strong>${x.title}</strong><br><span class="small">${x.summary}</span></a>`).join('')'''
    fixed='''matches.map(x => {\n            const href = x.href.startsWith('/') ? x.href : `/adlac/${x.href.replace(/^(\\.\\/)+/, '')}`;\n            return `<a href="${href}"><strong>${x.title}</strong><br><span class="small">${x.summary}</span></a>`;\n          }).join('')'''
    if old in jstxt:jstxt=jstxt.replace(old,fixed)
    else:print('Warning: Could not patch old-style search link handling; review docs.js')
old_filter=".filter(item => (item.title + ' ' + item.keywords).toLowerCase().includes(q))"
new_filter=".filter(item => (item.title + ' ' + item.summary + ' ' + item.keywords).toLowerCase().includes(q))"
jstxt=jstxt.replace(old_filter,new_filter)
# Place exact/starts-with title matches before broad keyword matches.
needle=".filter(item => (item.title + ' ' + item.summary + ' ' + item.keywords).toLowerCase().includes(q))\n        .slice(0, 8)"
replacement=".filter(item => (item.title + ' ' + item.summary + ' ' + item.keywords).toLowerCase().includes(q))\n        .sort((a, b) => Number(b.title.toLowerCase().includes(q)) - Number(a.title.toLowerCase().includes(q)))\n        .slice(0, 8)"
jstxt=jstxt.replace(needle,replacement)
js.write_text(jstxt,encoding='utf-8')

css=ROOT/'assets'/'docs.css'
csstxt=css.read_text(encoding='utf-8')
if 'ADLAC EXPANDED NAV CSS' not in csstxt:
    csstxt+='''\n/* ADLAC EXPANDED NAV CSS */\n.sidebar .doc-nav-group{margin:4px 0 6px;padding:0 0 1px}\n.sidebar .doc-nav-group summary{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 10px;border-radius:10px;cursor:pointer;font-size:.9rem;font-weight:700;color:var(--text);list-style:none}\n.sidebar .doc-nav-group summary::-webkit-details-marker{display:none}\n.sidebar .doc-nav-group summary::before{content:'▸';font-size:.8rem;color:var(--muted);margin-right:4px}\n.sidebar .doc-nav-group[open] summary::before{content:'▾'}\n.sidebar .doc-nav-group summary:hover{background:var(--surface)}\n.sidebar .doc-nav-group a{font-size:.84rem;margin-left:12px;padding:6px 9px}\n.sidebar .nav-count{font-size:.75rem;color:var(--muted);font-weight:500;margin-left:auto}\n.section-guide-catalog ul{columns:2;column-gap:22px;margin:8px 0 24px}\n.section-guide-catalog li{break-inside:avoid;margin:4px 0}\n.section-guide-catalog a{text-decoration:underline;text-underline-offset:3px}\n.search-results{top:calc(100% + 8px);max-height:min(60vh,420px);overflow-y:auto}\n@media(max-width:680px){.section-guide-catalog ul{columns:1}}\n'''
    css.write_text(csstxt,encoding='utf-8')

# Add exactly one entry for each new page to sitemap.
smap=ROOT/'sitemap.xml'
site=smap.read_text(encoding='utf-8')
for e in META['entries']:
    url='https://docs.boicusolutions.com/adlac/'+e['href']
    if url not in site:site=site.replace('</urlset>',f'  <url><loc>{url}</loc></url>\n</urlset>')
smap.write_text(site,encoding='utf-8')
print(f'Done. Created/updated {new} generated pages; refreshed navigation in {changed} ADLAC pages; search has {len(items)} entries.')
print('Support form, Turnstile Site Key and privacy page were not changed.')
