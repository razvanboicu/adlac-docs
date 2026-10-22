#!/usr/bin/env python3
"""Apply ADLAC privacy links to an existing documentation checkout.
Preserves Turnstile site keys, JavaScript, all other form settings and content.
Place this file in the same directory as CNAME, index.html and adlac/.
Run: py apply_privacy_update.py
"""
from pathlib import Path
import os, re

root = Path(__file__).resolve().parent
if not (root/'adlac'/'support'/'index.html').exists() or not (root/'privacy'/'index.html').exists():
    raise SystemExit('Missing adlac/support/index.html or privacy/index.html. Extract the patch ZIP into the documentation root first.')

def relative(file, to):
    return os.path.relpath(to, start=file.parent).replace(os.sep, '/')

changed=0
for file in sorted(root.glob('adlac/**/index.html')) + [root/'index.html']:
    original=file.read_text(encoding='utf-8')
    text=original
    href=relative(file, root/'privacy'/'index.html')
    # Add a privacy link in all existing ADLAC navigation sidebars.
    if '<nav class="sidebar"' in text and '>Privacy policy</a>' not in text:
        text=re.sub(r'(?m)(<a href="[^"\n]*changelog/index\.html">Changelog</a>)',
                    lambda m: '<a href="'+href+'">Privacy policy</a>\n'+m.group(1),text,count=1)
    # Ensure the policy appears in every footer without removing existing text.
    if 'class="footer-inner"' in text and 'class="footer-privacy"' not in text:
        text=text.replace('</div>\n</footer>', '<a class="footer-privacy" href="'+href+'">Privacy policy</a>\n</div>\n</footer>',1)
    # Modify only copy surrounding the existing checkbox; leave input names and Turnstile unchanged.
    if file == root/'adlac'/'support'/'index.html':
        text=text.replace('I understand that the information I submit will be used to respond to this support request.',
           'I have read the <a href="'+href+'">Privacy Policy</a> and understand that my information will be used to handle this support request.')
        marker='<h2>Support request form</h2>'
        notice='<p class="small">We use the details you provide to handle your request and email you a ticket confirmation. Read our <a href="'+href+'">Privacy Policy</a> for information about storage, providers and your rights.</p>'
        if notice not in text and marker in text:
            text=text.replace(marker,marker+'\n'+notice,1)
    if file == root/'index.html' and 'class="top-actions"' in text and 'Privacy policy</a></div>' not in text:
        text=text.replace('</div></div></header>', '<a class="top-link" href="'+href+'">Privacy policy</a></div></div></header>',1)
    if text!=original:
        file.write_text(text, encoding='utf-8');changed+=1

css=root/'assets'/'docs.css'
css_text=css.read_text(encoding='utf-8')
addon="""

/* Privacy page and links */
.footer-privacy{color:inherit;text-decoration:underline;text-underline-offset:3px}
.policy-content h2{font-size:clamp(1.45rem,2.4vw,1.85rem);line-height:1.22;letter-spacing:-.025em}
.policy-content p,.policy-content li{max-width:76ch}
.policy-owner-note{background:#fff7e8;border:1px solid #f0d7ae;border-radius:14px;padding:16px 18px;margin:18px 0}
.policy-owner-note p{margin:6px 0 0}
.policy-owner-note mark{background:#fff1bf;padding:1px 4px;overflow-wrap:anywhere}
.policy-sidebar a[href^="#"]{font-size:.86rem}
.policy-content section{scroll-margin-top:100px}
.support-consent a{font-weight:700;text-underline-offset:2px}
"""
if '/* Privacy page and links */' not in css_text:
    css.write_text(css_text+'\n'+addon,encoding='utf-8');changed+=1

sitemap=root/'sitemap.xml'
if sitemap.exists():
    xml=sitemap.read_text(encoding='utf-8')
    url='https://docs.boicusolutions.com/privacy/'
    if url not in xml:
        xml=xml.replace('</urlset>',f'  <url><loc>{url}</loc></url>\n</urlset>')
        sitemap.write_text(xml,encoding='utf-8');changed+=1

search=root/'adlac'/'search-index.js'
if search.exists():
    js=search.read_text(encoding='utf-8')
    if '"title": "Privacy policy"' not in js:
        extra='{ "title": "Privacy policy", "summary": "How Boicu Solutions handles ADLAC support data and privacy requests.", "keywords": "privacy data GDPR personal data support", "href": "/privacy/" }'
        js=js.rstrip()
        if js.endswith('];'):
            js=js[:-2]+', '+extra+'];\n'
            search.write_text(js,encoding='utf-8');changed+=1

print(f'Privacy integration complete: {changed} files updated. Existing Turnstile site key was not changed.')
print('Review privacy/index.html for the legal identity/address placeholder before publishing.')
