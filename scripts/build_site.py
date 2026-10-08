#!/usr/bin/env python3
"""Build crawlable static pages from the shared index.html content (stdlib only)."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import shutil
import xml.etree.ElementTree as ET
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '_site'
BASE = 'https://thu-sail-lab.github.io/home/'
# Content stays in index.html so the existing news/publication editors keep working.
PAGES = {
    'home': ('', 'SAIL Lab | Tsinghua University',
             "SAIL Lab in Tsinghua University's Department of Industrial Engineering researches time-series analysis, causal inference, and industrial superintelligence (SI)."),
    'research': ('research/', 'Research | SAIL Lab | Tsinghua University',
                 'Explore SAIL Lab research in time-series analysis, causal inference, anomaly detection, and industrial superintelligence (SI) at Tsinghua University.'),
    'publications': ('publications/', 'Publications | SAIL Lab | Tsinghua University',
                     'Publications by SAIL Lab researchers at Tsinghua University, with authors, venues, and available paper links.'),
    'awards': ('awards/', 'Awards | SAIL Lab | Tsinghua University',
               'Research awards and honors received by members of SAIL Lab in the Department of Industrial Engineering at Tsinghua University.'),
    'team': ('team/', 'Team | SAIL Lab | Tsinghua University',
             'Meet the faculty, research fellows, students, research assistants, and alumni of SAIL Lab at Tsinghua University.'),
    'partners': ('partners/', 'Partners | SAIL Lab | Tsinghua University',
                 'Industry partners and research collaborations of SAIL Lab in the Department of Industrial Engineering at Tsinghua University.'),
    'contact': ('contact/', 'Contact | SAIL Lab | Tsinghua University',
                'Contact SAIL Lab in the Department of Industrial Engineering, Shunde Building, Tsinghua University, Beijing.'),
    'opensource': ('opensource/', 'Open Source | SAIL Lab | Tsinghua University',
                   'Explore open-source research code and GitHub repositories from SAIL Lab at Tsinghua University.'),
    'chen-zhang': ('team/chen-zhang/', 'Chen Zhang (张晨) | SAIL Lab | Tsinghua University',
                   'Chen Zhang (张晨) is a tenured associate professor in Industrial Engineering at Tsinghua University and principal investigator of SAIL Lab.'),
}


def split_content(source):
    markers = list(re.finditer(r'<!-- (HOME|RESEARCH|PUBLICATIONS|AWARDS|TEAM|PARTNERS|CONTACT|OPEN SOURCE) PAGE -->', source))
    assert len(markers) == 8, 'Expected eight source sections'
    footer = source.index('<!-- Footer -->')
    sections = {}
    for i, match in enumerate(markers):
        key = match[1].lower().replace(' ', '')
        end = markers[i+1].start() if i+1 < len(markers) else footer
        sections[key] = source[match.end():end]
    principal = sections['team'].split('<!-- Principal Investigator -->')[1].split('<!-- Research Fellows -->')[0]
    # A self-link on the Team card becomes plain text on the dedicated profile.
    principal = principal.replace('<a href="team/chen-zhang/">Prof. Chen Zhang (张晨)</a>', 'Prof. Chen Zhang (张晨)')
    sections['chen-zhang'] = '''<div id="chen-zhang" class="page">
<section class="hero"><div class="hero-container"><h1>Chen Zhang (张晨)</h1>
<p class="hero-subtitle">Department of Industrial Engineering, Tsinghua University</p>
<p class="hero-affiliation" lang="zh-CN">清华大学工业工程系 · 张晨课题组</p></div></section>
<section class="section"><div class="container">''' + principal + '''
<p><a href="publications/">View publications</a> · <a href="team/">Meet the SAIL Lab team</a></p>
</div></section></div>'''
    return source[:markers[0].start()], sections, source[footer:]


def metadata(document, route, title, description):
    document = re.sub(r'<title>.*?</title>', '<title>'+escape(title)+'</title>', document, count=1)
    values = {'description': description, 'og:title': title, 'twitter:title': title,
              'og:description': description, 'twitter:description': description,
              'og:url': BASE+route, 'twitter:url': BASE+route}
    def meta(match):
        tag = match[0]
        name = re.search(r'(?:name|property)="([^"]+)"', tag)
        if name and name[1] in values:
            tag = re.sub(r'content="[^"]*"', 'content="'+escape(values[name[1]], quote=True)+'"', tag)
        return tag
    document = re.sub(r'<meta\b[^>]*>', meta, document)
    document = re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="'+BASE+route+'">', document)
    organization = {'@type': 'ResearchOrganization', '@id': BASE+'#lab',
                    'name': 'Superintelligence And Industrial Lab', 'alternateName': 'SAIL Lab', 'url': BASE,
                    'parentOrganization': {'@type': 'Organization', 'name': 'Department of Industrial Engineering, Tsinghua University'},
                    'sameAs': ['https://github.com/thu-sail-lab']}
    person = {'@type': 'Person', '@id': BASE+'team/chen-zhang/#person', 'name': 'Chen Zhang',
              'alternateName': '张晨', 'url': BASE+'team/chen-zhang/',
              'jobTitle': 'Tenured Associate Professor',
              'image': BASE+'images/team/chenzhang-2026.png',
              'worksFor': organization['parentOrganization'],
              'affiliation': {'@id': BASE+'#lab'},
              'sameAs': ['https://www.ie.tsinghua.edu.cn/info/1051/1048.htm',
                         'https://www.ie.tsinghua.edu.cn/eng/info/1051/1031.htm']}
    page = {'@type': 'ProfilePage' if route == 'team/chen-zhang/' else 'WebPage',
            '@id': BASE+route, 'url': BASE+route, 'name': title, 'description': description,
            'isPartOf': {'@id': BASE+'#website'},
            'about': {'@id': BASE+'#lab'}}
    if route == 'team/chen-zhang/':
        page['mainEntity'] = {'@id': person['@id']}
    graph = [organization, {'@type': 'WebSite', '@id': BASE+'#website', 'url': BASE,
                           'name': 'SAIL Lab · Tsinghua University', 'publisher': {'@id': BASE+'#lab'}}, page]
    if route in ('team/', 'team/chen-zhang/'):
        graph.append(person)
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('<', '\\u003c')
    return document.replace('</head>', '<script type="application/ld+json">'+data+'</script>\n</head>')


def render(header, section, footer, key):
    route, title, description = PAGES[key]
    section = re.sub(r'class="page(?: active)?"', 'class="page active"', section, count=1)
    document = header + '<main>\n' + section + '</main>\n' + footer
    # Relative URLs work on GitHub Pages under /home/ AND on a local preview server.
    prefix = '../' * route.count('/')
    def link(match):
        tag = match[0]
        page = re.search(r'data-page="([^"]+)"', tag)
        if page:
            classes = re.search(r'class="([^"]*)"', tag)
            active = page[1] == ('team' if key == 'chen-zhang' else key)
            if classes:
                names = [x for x in classes[1].split() if x != 'active']
                if active:
                    names.append('active')
                tag = tag[:classes.start(1)]+' '.join(names)+tag[classes.end(1):]
            elif active:
                tag = tag[:-1]+' class="active">'
            if active:
                tag = tag[:-1]+' aria-current="page">'
        def url(attr):
            value = attr[2]
            if value and not re.match(r'(?:[a-zA-Z][a-zA-Z0-9+.-]*:|/|#)', value):
                value = prefix+value
            return attr[1]+'="'+value+'"'
        return re.sub(r'\b(href|src|data-src)="([^"]*)"', url, tag)
    document = re.sub(r'<[a-zA-Z][^>]*>', link, document)
    return metadata(document, route, title, description)


class PageCheck(HTMLParser):
    """Validate the route/asset contract before publishing any pages."""
    def __init__(self):
        super().__init__()
        self.assets = []; self.links = []; self.pages = []; self.canonicals = []
        self.ids = []; self.divs = 0; self.h1s = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div': self.divs += 1
        if tag == 'h1': self.h1s += 1
        if 'id' in attrs: self.ids.append(attrs['id'])
        if 'page' in attrs.get('class', '').split(): self.pages.append(attrs)
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonicals.append(attrs['href'])
        for name in ('src', 'href'):
            url = attrs.get(name, '')
            if url and not re.match(r'(?:[a-zA-Z][a-zA-Z0-9+.-]*:|/|#)', url):
                self.links.append(url)
        if 'data-page' in attrs:
            assert attrs.get('href') and attrs['href'] != '#', 'Uncrawlable navigation'
    def handle_endtag(self, tag):
        if tag == 'div':
            self.divs -= 1
            assert self.divs >= 0, 'Unexpected closing div'


def validate():
    for key, (route, _, _) in PAGES.items():
        path = OUTPUT / route / 'index.html'
        document = path.read_text()
        parsed = PageCheck(); parsed.feed(document)
        assert parsed.divs == 0, (route, 'Unclosed div')
        assert len(parsed.pages) == 1 and 'active' in parsed.pages[0]['class'].split(), route
        assert parsed.h1s == 1, (route, 'Expected a single page heading')
        assert len(parsed.ids) == len(set(parsed.ids)), (route, 'Duplicate IDs')
        assert parsed.canonicals == [BASE+route], route
        assert 'thuie-isda.github.io' not in document, (route, 'Old site URL')
        for url in parsed.links:
            target = (path.parent / unquote(url.split('#')[0].split('?')[0])).resolve()
            assert target.is_relative_to(OUTPUT.resolve()), (route, url)
            assert target.exists(), (route, 'Missing local resource', url)
        for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>', document, re.S):
            json.loads(data)
    urls = ET.parse(OUTPUT/'sitemap.xml').findall('{*}url/{*}loc')
    assert {url.text for url in urls} == {BASE+page[0] for page in PAGES.values()}
    print('Validated 9 visible static pages, canonical URLs, structured data, sitemap, and local links/assets.')


def main():
    if OUTPUT.exists(): shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    for folder in ('images', 'logo'):
        shutil.copytree(ROOT/folder, OUTPUT/folder)
    # Keep Google's ownership-verification file in every deployment.
    for filename in ('styles.css', 'script.js', 'publications.json',
                     'google4a9f20f35c2b9b55.html'):
        shutil.copy2(ROOT/filename, OUTPUT/filename)
    header, sections, footer = split_content((ROOT/'index.html').read_text())
    for key, (route, _, _) in PAGES.items():
        target = OUTPUT/route/'index.html'; target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(header, sections[key], footer, key), encoding='utf-8')
    sitemap = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(
        '<url><loc>'+BASE+page[0]+'</loc></url>' for page in PAGES.values()) + '</urlset>\n'
    (OUTPUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+sitemap)
    (OUTPUT/'.nojekyll').touch()
    validate()

if __name__ == '__main__': main()
