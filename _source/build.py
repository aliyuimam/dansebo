#!/usr/bin/env python3
"""Builds the DanSebo website.
   dist/   -> preview build (CSS/JS inlined, map shown as a card because maps can't embed in the preview)
   deploy/ -> production build (shared site.css / site.js, live Google Map embed)
"""
import json, os, shutil, sys, html
ROOT = os.path.dirname(os.path.abspath(__file__))
# Set your domain here (e.g. 'https://www.dansebo.com') to add sitemap, canonical and social-share tags.
SITE_URL = os.environ.get('SITE_URL', '').rstrip('/')
SRC = os.path.join(ROOT, 'src')
CSS = open(os.path.join(SRC, 'site.css')).read()
JS = open(os.path.join(SRC, 'site.js')).read()
E = html.escape

SITE = 'DanSebo Global Services'
PHONE = '+234 907 826 5699'; PHONE2 = '+234 706 838 3802'
EMAIL = 'danseboglobalservices@gmail.com'
ADDR = 'Suite 52, Alhalal Plaza, Opp. Hamdala Hotel, Waff Road, Kaduna, Nigeria'
WA = 'https://wa.me/2349078265699'
MAPQ = 'Alhalal+Plaza+Waff+Road+Kaduna'
MAP_LINK = f'https://www.google.com/maps/search/?api=1&query={MAPQ}'
MAP_DIR = f'https://www.google.com/maps/dir/?api=1&destination={MAPQ}'
MAP_EMBED = f'https://www.google.com/maps?q={MAPQ}&output=embed'

ICONS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="i-x" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
<symbol id="i-ext" viewBox="0 0 24 24"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="i-zoom" viewBox="0 0 24 24"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="i-wa" viewBox="0 0 24 24"><path fill="currentColor" d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5 5.1-1.34A9.9 9.9 0 1 0 12.04 2Zm0 18.1a8.2 8.2 0 0 1-4.2-1.15l-.3-.18-3.03.8.81-2.95-.2-.31a8.23 8.23 0 1 1 6.92 3.79Zm4.5-6.15c-.25-.12-1.46-.72-1.69-.8-.23-.08-.39-.12-.55.12-.17.25-.64.8-.78.97-.14.16-.29.18-.53.06a6.74 6.74 0 0 1-3.37-2.94c-.25-.44.25-.41.72-1.36.08-.16.04-.3-.02-.43-.06-.12-.55-1.33-.76-1.82-.2-.48-.4-.41-.55-.42h-.47a.9.9 0 0 0-.66.31 2.76 2.76 0 0 0-.86 2.05 4.8 4.8 0 0 0 1 2.55 11 11 0 0 0 4.2 3.7c1.56.68 2.17.73 2.95.62.48-.07 1.46-.6 1.67-1.18.2-.58.2-1.07.14-1.18-.06-.1-.22-.16-.47-.28Z"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M6.6 3h2.6l1.5 4.2-1.9 1.4a12 12 0 0 0 6.6 6.6l1.4-1.9 4.2 1.5v2.6A2.6 2.6 0 0 1 18.4 20 15.4 15.4 0 0 1 4 5.6 2.6 2.6 0 0 1 6.6 3Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3.5 6.5 12 13l8.5-6.5" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="9.5" r="2.6" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
<symbol id="i-pinfill" viewBox="0 0 24 24"><path d="M12 22s-7.5-6.6-7.5-12.3a7.5 7.5 0 0 1 15 0C19.5 15.4 12 22 12 22Z" fill="currentColor"/><circle cx="12" cy="9.7" r="2.8" fill="#fff"/></symbol>
<symbol id="s-print" viewBox="0 0 24 24"><rect x="3" y="9" width="18" height="8" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M7 9V3h10v6M7 14h10v7H7z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
<symbol id="s-brand" viewBox="0 0 24 24"><path d="M12 2.5 21.5 12 12 21.5 2.5 12z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M12 7.5 16.5 12 12 16.5 7.5 12z" fill="currentColor"/></symbol>
<symbol id="s-ict" viewBox="0 0 24 24"><path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="s-train" viewBox="0 0 24 24"><path d="M2 9l10-5 10 5-10 5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
<symbol id="s-mentor" viewBox="0 0 24 24"><circle cx="8" cy="7" r="3" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17" cy="9" r="2.3" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M2.5 20c.6-3.6 2.8-5.5 5.5-5.5s4.9 1.9 5.5 5.5M14 15c.8-.5 1.8-.8 3-.8 2.2 0 3.8 1.5 4.5 4.3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
<symbol id="s-gift" viewBox="0 0 24 24"><rect x="3" y="8" width="18" height="5" rx="1" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M5 13v8h14v-8M12 8v13M12 8c-1-3-5-4-5-1.5S11 8 12 8Zm0 0c1-3 5-4 5-1.5S13 8 12 8Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
<symbol id="s-layers" viewBox="0 0 24 24"><path d="m12 3 9 5-9 5-9-5z M3 13l9 5 9-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
<symbol id="s-eye" viewBox="0 0 24 24"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
<symbol id="s-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3.5 2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
<symbol id="s-tag" viewBox="0 0 24 24"><path d="M3 12V4h8l10 10-8 8z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="7.5" cy="8.5" r="1.6" fill="currentColor"/></symbol>
<symbol id="s-team" viewBox="0 0 24 24"><circle cx="12" cy="8" r="3.2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M5 20c.7-3.8 3.4-6 7-6s6.3 2.2 7 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
<symbol id="s-support" viewBox="0 0 24 24"><path d="M4 13v-1a8 8 0 0 1 16 0v1" fill="none" stroke="currentColor" stroke-width="1.8"/><rect x="3" y="13" width="4" height="6" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.8"/><rect x="17" y="13" width="4" height="6" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
<symbol id="s-monitor" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="12" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8 20h8M12 16v4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
<symbol id="s-chart" viewBox="0 0 24 24"><path d="M3 20h18M6 20v-6M11 20V9M16 20v-9M21 20V5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
<symbol id="s-pen" viewBox="0 0 24 24"><path d="M4 20l1.5-5L15 5.5a2.1 2.1 0 0 1 3 3L8.5 18z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M13.5 7l3 3" stroke="currentColor" stroke-width="1.8"/></symbol>
<symbol id="s-kids" viewBox="0 0 24 24"><circle cx="12" cy="6" r="2.6" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M5 10l7 2 7-2M12 12v4l-3 5M12 16l3 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="s-globe" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
<symbol id="s-seal" viewBox="0 0 24 24"><circle cx="12" cy="9" r="6" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m8.5 14-1.5 7 5-2.5 5 2.5-1.5-7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="m9.5 9 1.8 1.8L14.8 7.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="s-target" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="1.6" fill="currentColor"/></symbol>
<symbol id="s-heart" viewBox="0 0 24 24"><path d="M12 20s-8-4.7-8-10.5A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 8 2.5C20 15.3 12 20 12 20Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
<symbol id="so-ig" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.3" cy="6.7" r="1.2" fill="currentColor"/></symbol>
<symbol id="so-tt" viewBox="0 0 24 24"><path d="M14 3v11.5a3.5 3.5 0 1 1-3.5-3.5M14 3c.4 2.6 2.2 4.4 5 4.6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
<symbol id="so-fb" viewBox="0 0 24 24"><path d="M14 21v-8h3l.5-3.5H14V7.6c0-1 .3-1.7 1.8-1.7h1.8V2.8A24 24 0 0 0 15 2.7c-2.6 0-4.4 1.6-4.4 4.5v2.3H7.7V13h2.9v8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></symbol>
</svg>'''

def ic(name, cls='ic'):
    return f'<span class="{cls}"><svg aria-hidden="true"><use href="#{name}"/></svg></span>'
def arrow(): return '<svg aria-hidden="true"><use href="#i-arrow"/></svg>'

NAV = [('index.html','Home'),('about.html','About'),('services.html','Services'),('training.html','Training'),('gallery.html','Gallery'),('contact.html','Contact')]

def header(active):
    links = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==active else ""}>{t}</a>' for h,t in NAV)
    return f'''<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="{SITE}, home">
      <img class="on-light" src="assets/logo.png" alt="DanSebo Global Services Ltd" width="937" height="232">
      <img class="on-dark" src="assets/logo-white.png" alt="DanSebo Global Services Ltd" width="937" height="232">
    </a>
    <button class="menu-btn" id="menuBtn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
    <nav class="nav" id="nav" aria-label="Main">{links}<a class="btn" href="contact.html#quote">Get a quote</a></nav>
  </div>
</header>'''

FOOTER = f'''<footer>
  <div class="wrap">
    <div class="f-grid">
      <div class="f-brand">
        <img src="assets/logo-white.png" alt="DanSebo Global Services Ltd" width="937" height="232" loading="lazy">
        <p>Printing, branding, ICT and training for businesses, institutions and individuals. Your Vision, Our Expertise.</p>
        <div class="socials">
          <a href="https://www.instagram.com/dansebo.ng/" target="_blank" rel="noopener" aria-label="Instagram"><svg aria-hidden="true"><use href="#so-ig"/></svg></a>
          <a href="https://www.tiktok.com/@dansebo.ng" target="_blank" rel="noopener" aria-label="TikTok"><svg aria-hidden="true"><use href="#so-tt"/></svg></a>
          <a href="https://www.facebook.com/p/Dan-Sebo-Global-Services-LTD-100091279508615/" target="_blank" rel="noopener" aria-label="Facebook"><svg aria-hidden="true"><use href="#so-fb"/></svg></a>
          <a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp"><svg aria-hidden="true"><use href="#i-wa"/></svg></a>
        </div>
      </div>
      <div><h4>Company</h4><ul><li><a href="about.html">About us</a></li><li><a href="about.html#ceo">Our CEO</a></li><li><a href="about.html#certificates">Certificates</a></li><li><a href="gallery.html">Gallery</a></li></ul></div>
      <div><h4>What we do</h4><ul><li><a href="services.html#printing">Printing &amp; Production</a></li><li><a href="services.html#branding">Branding &amp; Design</a></li><li><a href="services.html#ict">ICT &amp; Digital</a></li><li><a href="training.html">Training programmes</a></li></ul></div>
      <div><h4>Contact</h4><ul><li>{PHONE}</li><li>{EMAIL}</li><li>{ADDR}</li></ul></div>
    </div>
    <div class="f-bottom"><span>© <span id="yr">2026</span> DanSebo Global Services Ltd. RC 8413837.</span><span>Your Vision, Our Expertise.</span></div>
  </div>
</footer>
<a class="float-wa" href="{WA}" target="_blank" rel="noopener" aria-label="Chat with DanSebo on WhatsApp"><svg aria-hidden="true"><use href="#i-wa"/></svg></a>'''

def page_head(crumb, title, sub):
    return f'''<section class="page-head"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>{crumb}</span></nav>
  <h1>{title}</h1><p>{sub}</p>
</div></section>'''

CTA = f'''<section class="section tight"><div class="wrap"><div class="cta">
  <div><h2>Have a project in mind?</h2><p>Tell us what you need and we'll send a design plan and a clear price.</p></div>
  <div class="actions"><a class="btn btn-white" href="contact.html#quote">Request a quote {arrow()}</a><a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="#i-wa"/></svg>WhatsApp us</a></div>
</div></div></section>'''

STATS = [('9','Years of experience'),('500','Happy clients'),('1000','Projects completed'),('5','Team members')]
def stats(flat=False):
    cells=''.join(f'<div class="stat"><strong>{"{:,}".format(int(n))}<sup>+</sup></strong><span>{l}</span></div>' for n,l in STATS)
    return f'''<section class="stats{" flat" if flat else ""}" aria-label="Our achievements"><div class="wrap"><div class="stats-card">
  <div class="stats-intro"><b>Our achievements</b><span>Building trust through delivered results and client satisfaction.</span></div>{cells}
</div></div></section>'''

SERVICES = [
 ('printing','s-print','Printing &amp; Production',['Posters, flyers and banners','Business cards, jotters and paper bags','IV cards, ID cards and stickers']),
 ('branding','s-brand','Branding &amp; Creative Design',['Logo design and brand identity','Company profile and social media design','Marketing materials']),
 ('ict','s-ict','ICT &amp; Digital Solutions',['Website design and development','Social media management','IT support and computer services']),
 ('training','s-train','Training &amp; Mentorship',['Computer and digital skills training','Mentorship and career guidance','Entrepreneurship programmes']),
]
def svc_cards():
    out=[]
    for i,(id_,icn,t,items) in enumerate(SERVICES):
        lis=''.join(f'<li>{x}</li>' for x in items)
        href='training.html' if id_=='training' else f'services.html#{id_}'
        out.append(f'<article class="svc"><span class="num">0{i+1}</span>{ic(icn)}<h3>{t}</h3><ul class="ticks">{lis}</ul><span class="more">and lots more</span><a class="link" href="{href}">Learn more {arrow()}</a></article>')
    return '<div class="svc-grid">'+''.join(out)+'</div>'

WHY = [
 ('s-layers','Everything under one roof','Design, printing, branding and digital work handled by one team, so nothing gets lost between suppliers.'),
 ('s-eye','You approve before we produce','Every job starts with a proof. Nothing is printed until you are happy with it.'),
 ('s-clock','Delivered on time','We agree a timeline at the start and keep you updated until the job is done.'),
 ('s-tag','Clear, fair pricing','A written quote before work begins, with no surprises when you collect.'),
 ('s-team','Experienced team','Over nine years of designing, printing and training for clients of every size.'),
 ('s-support','Support after delivery','Reprints, file updates and advice whenever you need them.'),
]
def why_block():
    items=''.join(f'<div class="why-item">{ic(i)}<div><h3>{t}</h3><p>{d}</p></div></div>' for i,t,d in WHY)
    return f'''<div class="why">
  <div class="why-media"><img src="assets/tall-reception.jpg" alt="DanSebo reception with a lit display of branded products" width="960" height="1280" loading="lazy" style="object-position:center 35%"><div class="why-badge"><strong>9+</strong><span>Years of<br>experience</span></div></div>
  <div><div class="eyebrow">Why choose us</div><h2 style="font-size:clamp(2rem,3.8vw,2.9rem);font-weight:800;margin-top:14px">A partner that takes your brand as seriously as you do.</h2>
  <div class="why-list">{items}</div></div>
</div>'''

EXPERTISE = [
 ('s-print','Printing &amp; Production','Commercial and large-format printing, finished and packed in-house.'),
 ('s-brand','Branding &amp; Creative Design','Identities, campaigns and marketing materials that look consistent everywhere.'),
 ('s-monitor','ICT &amp; Digital Solutions','Websites, social media management and practical technology support.'),
 ('s-train','Education &amp; Training','Hands-on computer and digital skills courses, in class and online.'),
 ('s-mentor','Mentorship','Guidance for young people building careers and confidence.'),
 ('s-gift','Corporate Gifts &amp; Merchandise','Branded mugs, caps, shirts, pens, bags and souvenirs for events and teams.'),
]
def expertise():
    return '<div class="exp-grid">'+''.join(f'<div class="exp">{ic(i)}<h3>{t}</h3><p>{d}</p></div>' for i,t,d in EXPERTISE)+'</div>'

PARTNERS = [
 ('NTIC','Education partner','https://ntic.edu.ng/','<img src="assets/partner-ntic.png" alt="NTIC logo" width="240" height="378" loading="lazy">'),
 ('Galaxy UniPrep','Education partner','https://galaxy.com.ng/','<span class="word">Galaxy <span>UniPrep</span></span>'),
 ('Vento Furniture','Business partner','https://ventofurniture.com/','<img src="assets/partner-vento.svg" alt="Vento Furniture logo" width="294" height="78" loading="lazy">'),
]
def partners():
    return '<div class="partners">'+''.join(f'''<a class="partner" href="{u}" target="_blank" rel="noopener"><div class="logo">{logo}</div><div class="pmeta"><div><b>{n}</b><small>{r}</small></div><span class="ext"><svg aria-hidden="true"><use href="#i-ext"/></svg></span></div></a>''' for n,r,u,logo in PARTNERS)+'</div>'

CEO_NAME='Ahmad Ismail Waziri'
CEO_ROLE='Founder &amp; Chief Executive Officer'
CEO_BIO=[
 f'{CEO_NAME} is an entrepreneur, educator and technology-driven business leader passionate about building sustainable businesses and creating opportunities for young people.',
 'As Founder and CEO of DanSebo Global Services Ltd, he leads the company with a clear vision to build a trusted brand across Printing, ICT, Education and Mentorship Services.',
 'His approach combines creativity, technology, education and entrepreneurship to deliver practical solutions while empowering individuals and businesses to grow.',
 'Driven by the belief in <b>Your Vision, Our Expertise</b>, he continues to build DanSebo as more than a business: a platform for opportunity, innovation and lasting impact.',
]
def ceo(full):
    bio=CEO_BIO if full else CEO_BIO[:2]
    paras=''.join(f'<p>{p}</p>' for p in bio)
    act = '' if full else f'<div class="actions"><a class="btn btn-primary" href="about.html#ceo">Read full profile {arrow()}</a></div>'
    return f'''<div class="ceo">
  <div class="ceo-card"><div class="photo"><img src="assets/ceo.jpg" alt="{CEO_NAME}, Founder and CEO of DanSebo Global Services" width="743" height="900" loading="lazy"></div>
    <div class="ceo-name"><b>{CEO_NAME}</b><span>{CEO_ROLE}</span></div></div>
  <div class="ceo-text"><div class="eyebrow">Meet our CEO</div><h2>Building a platform for opportunity.</h2>
    <p class="ceo-quote">“Your Vision, Our Expertise is more than a slogan. It is how we serve every client and every student.”</p>
    <div class="bio">{paras}</div>
    <div class="sig"><span class="bar"></span><div><b>{CEO_NAME}</b><br><span>Founder &amp; CEO, DanSebo Global Services Ltd</span></div></div>{act}
  </div>
</div>'''

GALLERY = [
 ('hero-hub.jpg','Tech Hub','The Tech Hub wall and branded seating','workspace',True,(1080,607)),
 ('hero-reception.jpg','Reception &amp; lounge','Reception lounge with wall lights','workspace',True,(1080,607)),
 ('products.jpg','Branded merchandise','Notebooks, bags, caps, pens and mugs produced by DanSebo','work',False,(520,415)),
 ('hero-office.jpg','Management office','Management office with the Nigerian flag and globe','workspace',True,(1080,607)),
 ('hero-creative.jpg','Creative room','Entrance to the Creative Room','workspace',True,(1080,607)),
 ('banner.jpg','Roll-up banner','A DanSebo roll-up banner: We Design, We Brand, We Print, We Train','work',False,(724,1400)),
 ('tall-reception.jpg','Reception &amp; showroom','Reception desk and display cabinet of branded products','workspace',False,(960,1280)),
 ('tall-hub.jpg','Production area','Production printer beside the Tech Hub wall','workspace',False,(960,1107)),
 ('tall-lecture.jpg','Training room','Training room with screen and flip chart','training',False,(960,1027)),
 ('tall-creative.jpg','Creative room door','Shelving and the Creative Room door','workspace',False,(959,1400)),
 ('tall-ceo.jpg',"CEO's office",'CEO office with certificates on the wall','workspace',False,(960,1227)),
]
def gallery_slider(auto=True):
    items=[]
    for i,(f,cap,alt,tag,cover,(w,h)) in enumerate(GALLERY):
        a='src' if i<2 else 'data-src'
        items.append(f'<figure class="gs-item{" cover" if cover else ""}{" on" if i==0 else ""}" data-cap="{cap}"><img class="blur" {a}="assets/{f}" alt="" aria-hidden="true"><img class="main" src="assets/{f}" alt="{E(alt)}" width="{w}" height="{h}"{"" if i==0 else " loading=\"lazy\""}></figure>')
    return f'''<div class="gs" data-auto="{1 if auto else 0}">
  <div class="gs-stage" tabindex="0" role="region" aria-roledescription="carousel" aria-label="Photo gallery">
    {''.join(items)}
    <button class="gs-zoom" type="button"><svg aria-hidden="true"><use href="#i-zoom"/></svg>View full size</button>
    <div class="gs-bar"><div class="gs-cap" aria-live="polite"><b></b><span></span></div><div class="gs-btns"><button class="g-prev flip" type="button" aria-label="Previous photo">{arrow()}</button><button class="g-next" type="button" aria-label="Next photo">{arrow()}</button></div></div>
  </div>
  <div class="gs-thumbs" aria-label="Choose a photo"></div>
</div>'''

COURSES = {
 'formFee': 5000,
 'courses': [
  {'id':'basic-computer','icon':'s-monitor','title':'Basic Computer Training','duration':'8 weeks','fee':80000,'level':'Beginner','mode':'Physical or virtual',
   'summary':'Build real confidence with computers for school, work and business, starting from the very basics.',
   'forWhom':'Complete beginners, students, job seekers and office staff.',
   'outcome':'You will use a computer confidently and produce everyday documents, spreadsheets and presentations on your own.',
   'modules':['Computer fundamentals and Windows','Files, folders and storage','Microsoft Word','Microsoft Excel','Microsoft PowerPoint','Internet, email and online safety','Typing speed and accuracy','Printing, scanning and everyday tasks']},
  {'id':'web-basic','icon':'s-ict','title':'Basic Web Design & Development','duration':'8 weeks','fee':150000,'level':'Beginner','mode':'Physical or virtual',
   'summary':'Learn how websites are built and publish your first responsive site.',
   'forWhom':'Beginners, small business owners and anyone curious about building for the web.',
   'outcome':'You will build and publish a responsive multi-page website.',
   'modules':['How the web works','HTML page structure','CSS styling and layout','Responsive design for phones','Introduction to JavaScript','Domains, hosting and publishing','Project: your own website']},
  {'id':'web-full','icon':'s-ict','title':'Full Web Design & Development','duration':'12 weeks','fee':250000,'level':'Intermediate','mode':'Physical or virtual',
   'summary':'Go from layouts to working web applications, front end and back end.',
   'forWhom':'Learners with basic computer skills who want a career-ready web skill set.',
   'outcome':'You will build, version and deploy a complete web application for your portfolio.',
   'modules':['HTML, CSS and responsive layouts','JavaScript and the DOM','Modern front-end tools','Git and GitHub','Back-end basics and databases','Forms, APIs and integrations','Deployment and hosting','Capstone project']},
  {'id':'data','icon':'s-chart','title':'Data Analysis & Visualization','duration':'12 weeks','fee':200000,'level':'Beginner to intermediate','mode':'Physical or virtual',
   'summary':'Turn raw data into clear insight with spreadsheets, dashboards and SQL.',
   'forWhom':'Graduates, professionals and business owners who work with numbers.',
   'outcome':'You will clean data, analyse it and present findings in a dashboard.',
   'modules':['Data fundamentals','Excel for analysis: formulas and pivot tables','Cleaning and preparing data','Principles of good charts','Dashboards with Power BI','Introduction to SQL','Reporting and data storytelling','Capstone project']},
  {'id':'online','icon':'s-globe','title':'Online Computer Courses','duration':'8 weeks','fee':120000,'level':'All levels','mode':'Virtual',
   'summary':'Core computer and office skills taught live online, so you can learn from anywhere.',
   'forWhom':'Learners outside Kaduna and busy professionals who need flexible timing.',
   'outcome':'You will work confidently with office tools and online collaboration apps.',
   'modules':['Computer basics','Microsoft Office essentials','Google Workspace','Online meetings and collaboration','Research, email and productivity','Digital safety']},
  {'id':'kids','icon':'s-kids','title':'Kids Computer Courses','duration':'8 weeks','fee':80000,'level':'Children','mode':'Physical or virtual',
   'summary':'A friendly introduction to computers and creative technology for children.',
   'forWhom':'Children who are new to computers or ready for their first coding steps.',
   'outcome':'Your child will use a computer safely and create simple projects and games.',
   'modules':['Using a computer safely','Mouse and typing skills','Drawing and creative tools','Introduction to Word and PowerPoint','Fun coding with Scratch','Internet safety for kids']},
  {'id':'graphic','icon':'s-pen','title':'Graphic Design','duration':'8 weeks','fee':150000,'level':'Beginner','mode':'Physical or virtual',
   'summary':'Design logos, flyers and social media graphics the way professionals do.',
   'forWhom':'Aspiring designers, content creators and business owners.',
   'outcome':'You will produce print-ready and social-ready designs and a starter portfolio.',
   'modules':['Design principles','Colour and typography','Photoshop and CorelDRAW basics','Canva for quick design','Logo and brand identity','Flyers, posters and social media graphics','Preparing print-ready files','Portfolio project']},
 ]}

def course_cards():
    out=[]
    for c in COURSES['courses']:
        out.append(f'''<button class="course" type="button" data-course="{c['id']}" aria-haspopup="dialog">
  <div class="course-top">{ic(c['icon'])}<span class="chip grey">{c['level']}</span></div>
  <h3>{E(c['title'])}</h3><p>{c['summary']}</p>
  <div class="meta"><span class="chip">{c['duration']}</span><span class="chip">{c['mode']}</span></div>
  <span class="link">View details {arrow()}</span>
</button>''')
    out.append(f'''<a class="course alt" href="contact.html#training" style="text-decoration:none">
  <div class="course-top">{ic('s-mentor')}</div>
  <h3>Mentorship &amp; Entrepreneurship</h3><p>Custom mentorship, career guidance and business programmes for individuals, schools and organisations.</p>
  <span class="link" style="margin-top:auto">Talk to us {arrow()}</span>
</a>''')
    return '<div class="course-grid">'+''.join(out)+'</div>'

COURSE_DIALOG = f'''<dialog class="course-dlg" id="courseDlg" aria-labelledby="dTitle">
  <div class="dlg">
    <div class="dlg-main">
      <button class="dlg-close" type="button" aria-label="Close"><svg aria-hidden="true"><use href="#i-x"/></svg></button>
      <span class="chip" id="dLevel"></span>
      <h2 id="dTitle"></h2>
      <p class="summary" id="dSummary"></p>
      <div class="facts"><div><small>Duration</small><b id="dDur"></b></div><div><small>Mode</small><b id="dMode"></b></div><div><small>Award</small><b id="dCert"></b></div></div>
      <h4>What you will learn</h4>
      <ol class="modules" id="dModules"></ol>
      <h4>Who it is for</h4><p id="dFor" style="color:var(--muted)"></p>
      <h4>Outcome</h4><p id="dOutcome" style="color:var(--muted)"></p>
    </div>
    <div class="dlg-side">
      <div class="price-box">
        <div class="price-row main"><span>Course fee</span><b id="dFee"></b></div>
        <div class="price-row"><span>Application form (one-time)</span><b id="dForm"></b></div>
        <div class="price-row"><span>Total</span><b id="dTotal"></b></div>
      </div>
      <ul class="incl"><li><svg aria-hidden="true"><use href="#i-check"/></svg>Notepad and pen</li><li><svg aria-hidden="true"><use href="#i-check"/></svg>Student ID card and shirt</li><li><svg aria-hidden="true"><use href="#i-check"/></svg>Course manual</li><li><svg aria-hidden="true"><use href="#i-check"/></svg>Recognised certificate</li></ul>
      <form class="enrol" id="enrolForm" novalidate>
        <h3>Enrol in this course</h3>
        <div class="field"><label for="ename">Full name <span class="req">*</span></label><input id="ename" name="ename" autocomplete="name" required></div>
        <div class="field"><label for="eemail">Email <span class="req">*</span></label><input id="eemail" name="eemail" type="email" autocomplete="email" required></div>
        <div class="field"><label for="ephone">Phone <span class="req">*</span></label><input id="ephone" name="ephone" type="tel" autocomplete="tel" required></div>
        <div class="field"><label id="modeLbl">Preferred class</label><div class="seg" role="radiogroup" aria-labelledby="modeLbl"><label><input type="radio" name="mode" value="Physical" id="m-phys" checked><span>Physical</span></label><label><input type="radio" name="mode" value="Virtual" id="m-virt"><span>Virtual</span></label></div></div>
        <button class="btn btn-primary" type="submit">Proceed to payment {arrow()}</button>
        <p class="pay-note">Fees may change. Confirm the current fee before paying.</p>
        <div class="pay-msg" id="payMsg" role="status" hidden></div>
      </form>
    </div>
  </div>
</dialog>'''

# ---------------- Pages ----------------
HERO_SLIDES=[('hero-hub.jpg','Tech Hub'),('hero-reception.jpg','Reception &amp; lounge'),('hero-creative.jpg','Creative room'),('hero-office.jpg','Management office')]
def home():
    slides=''.join(f'<div class="hero-slide{" on" if i==0 else ""}" data-cap="{c}"><img src="assets/{f}" alt=""{"" if i==0 else " loading=\"lazy\""}></div>' for i,(f,c) in enumerate(HERO_SLIDES))
    return f'''<main>
<section class="hero" aria-label="Welcome">
  <div class="hero-slides" aria-hidden="true">{slides}</div>
  <div class="wrap"><div class="hero-copy">
    <div class="eyebrow">Printing · Branding · ICT · Training</div>
    <h1>Your Vision,<br><em>Our Expertise.</em></h1>
    <p class="lead">DanSebo Global Services helps businesses, institutions and individuals build brands people trust, and gives people the digital skills to grow.</p>
    <div class="actions"><a class="btn btn-white" href="contact.html#quote">Get a quote {arrow()}</a><a class="btn btn-ghost" href="services.html">Explore services</a></div>
  </div></div>
  <div class="hero-ctrl"><div class="wrap">
    <div class="hero-cap"><b>01 / 04</b><span>Tech Hub</span></div>
    <div class="hero-bars" aria-label="Slides"></div>
    <div class="hero-arrows"><button class="h-prev flip" type="button" aria-label="Previous slide">{arrow()}</button><button class="h-next" type="button" aria-label="Next slide">{arrow()}</button></div>
  </div></div>
</section>
{stats()}
<section class="section"><div class="wrap">
  <div class="head"><div><div class="eyebrow">Our services</div><h2>Everything your brand needs, under one roof.</h2></div><p>From a single business card to a full brand rollout, we design, produce and deliver with care.</p></div>
  {svc_cards()}
</div></section>
<section class="section soft"><div class="wrap">{why_block()}</div></section>
<section class="section"><div class="wrap">
  <div class="head"><div><div class="eyebrow">Training</div><h2>Learn skills. Build confidence. Create opportunities.</h2></div><p>Practical, instructor-led courses in computing, web development, data and design. In class or online.</p></div>
  <div class="split" style="align-items:stretch">
    <div class="split-media"><img src="assets/tall-lecture.jpg" alt="DanSebo training room with projector screen and flip chart" width="960" height="1027" loading="lazy" style="height:100%"></div>
    <div style="display:flex;flex-direction:column;justify-content:center">
      <ul class="ticks" style="grid-template-columns:1fr;gap:14px;font-size:1.02rem">{''.join(f'<li><b style="color:var(--ink)">{E(c["title"])}</b>&nbsp;· {c["duration"]}</li>' for c in COURSES['courses'][:5])}</ul>
      <div class="actions" style="margin-top:30px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-primary" href="training.html">See all courses {arrow()}</a></div>
    </div>
  </div>
</div></section>
<section class="section soft" id="ceo"><div class="wrap">{ceo(False)}</div></section>
<section class="section"><div class="wrap">
  <div class="head"><div><div class="eyebrow">Inside DanSebo</div><h2>A workspace built for creating and learning.</h2></div><p>Reception and showroom, a lecture room, a creative room and our production area.</p></div>
  {gallery_slider()}
</div></section>
<section class="section soft"><div class="wrap">
  <div class="head"><div><div class="eyebrow">Our partners</div><h2>Trusted by organisations we work alongside.</h2></div><p>We are proud to collaborate with these institutions and businesses.</p></div>
  {partners()}
</div></section>
{cert_strip()}
{CTA}
</main>'''

CERTS = [
 ('cert-cac.jpg','Certificate of Incorporation','Corporate Affairs Commission (CAC)','RC 8413837 · 15 April 2025',(844,1080)),
 ('cert-tin.jpg','Taxpayer Identification Number','Joint Tax Board · FIRS','Issued 17 April 2025',(1080,754)),
 ('cert-scuml.jpg','SCUML Certificate of Registration','Special Control Unit against Money Laundering','RN SC 191801275 · 30 May 2025',(1080,749)),
 ('cert-nassi.jpg','NASSI Certificate of Registration','Nigerian Association of Small Scale Industrialists','NASSI-KDN-61148',(1070,757)),
]
def cert_cards():
    return ''.join(f'''<button class="cert" type="button" data-lb="certs" data-cap="{t}" data-src="assets/{f}"><div class="doc"><img src="assets/{f}" alt="{t}, {iss}" width="{w}" height="{h}" loading="lazy"></div><div class="txt"><b>{t}</b><span>{iss}</span><small>{meta}</small></div></button>''' for f,t,iss,meta,(w,h) in CERTS)
def cert_strip():
    items=''.join(f'<a href="about.html#certificates"><img src="assets/{f}" alt="" loading="lazy"><span><b>{t}</b><small>{iss}</small></span></a>' for f,t,iss,meta,_ in CERTS)
    return f'''<section class="section tight"><div class="wrap">
  <div class="head"><div><div class="eyebrow">Registered &amp; certified</div><h2>A company you can verify.</h2></div><p>Incorporated with CAC and registered with the Joint Tax Board, SCUML and NASSI.</p></div>
  <div class="cert-strip">{items}</div>
</div></section>'''

def about():
    return f'''<main>
{page_head('About','About DanSebo','A registered Nigerian company working across printing, branding, ICT, education and mentorship.')}
<section class="section"><div class="wrap split">
  <div class="split-media"><img src="assets/hero-hub.jpg" alt="The DanSebo Tech Hub" width="1080" height="607"></div>
  <div><div class="eyebrow">Who we are</div><h2>More than a print shop.</h2>
    <div class="body"><p>DanSebo Global Services Ltd (RC 8413837) brings design, branding, printing, digital solutions and training together under one roof.</p><p>For over nine years we have helped businesses, schools, organisations and individuals present themselves professionally, and helped young people gain skills that create real opportunity.</p></div>
    <div class="values"><span class="chip">We Design</span><span class="chip">We Brand</span><span class="chip">We Print</span><span class="chip">We Train</span></div>
  </div>
</div></section>
{stats(flat=True)}
<section class="section soft" style="margin-top:72px"><div class="wrap">
  <div class="head single"><div><div class="eyebrow">Purpose</div><h2>What drives us.</h2></div></div>
  <div class="mv">
    <div>{ic('s-target')}<h3>Our mission</h3><p>To deliver creative, reliable and affordable printing, branding and digital solutions, while equipping people with practical skills to succeed.</p></div>
    <div>{ic('s-eye')}<h3>Our vision</h3><p>To be a trusted brand known across Africa and beyond for quality, innovation and lasting impact.</p></div>
    <div>{ic('s-heart')}<h3>Our values</h3><p>The standards behind every job and every class.</p><div class="values"><span class="chip">Quality</span><span class="chip">Integrity</span><span class="chip">Creativity</span><span class="chip">Impact</span></div></div>
  </div>
</div></section>
<section class="section"><div class="wrap">
  <div class="head"><div><div class="eyebrow">Areas of expertise</div><h2>Where we do our best work.</h2></div><p>Six connected disciplines, delivered by one team.</p></div>
  {expertise()}
</div></section>
<section class="section soft" id="ceo"><div class="wrap">{ceo(True)}</div></section>
<section class="section" id="certificates"><div class="wrap">
  <div class="head"><div><div class="eyebrow">Certificates</div><h2>Registered and accountable.</h2></div><p>DanSebo Global Services Ltd is incorporated with the Corporate Affairs Commission and registered with the relevant national bodies.</p></div>
  <div class="certs">
    {cert_cards()}
  </div>
  <p class="fine" style="margin-top:18px;color:var(--muted);font-size:.88rem">Select a certificate to view it full size.</p>
</div></section>
<section class="section soft"><div class="wrap">
  <div class="head"><div><div class="eyebrow">Our partners</div><h2>Organisations we work alongside.</h2></div><p>Select a partner to visit their website.</p></div>
  {partners()}
</div></section>
{CTA}
</main>'''

SVC_DETAIL=[
 ('printing','Printing &amp; Production','Quality prints, finished in-house.','From everyday business stationery to large-format display, we handle the design, print and finishing.',
   ['Posters, flyers and banners','Business cards and jotters','Paper bags and packaging','IV cards and invitations','ID cards and lanyards','Stickers and SAV','Notebooks and calendars','Mugs, caps and T-shirts'],'products.jpg',True),
 ('branding','Branding &amp; Creative Design','A brand that looks the same everywhere.','We create identities and marketing materials that make your business easy to recognise and easy to trust.',
   ['Logo design','Brand identity guides','Company profile design','Social media design','Marketing materials','Signage and display','Packaging design','Event branding'],'banner.jpg',False),
 ('ict','ICT &amp; Digital Solutions','Technology that works for your business.','Practical digital services that help you reach customers online and keep your work running smoothly.',
   ['Website design and development','Social media management','Digital marketing support','IT support and maintenance','Computer services','Email and online setup'],'hero-office.jpg',False),
 ('training','Training &amp; Mentorship','Skills that open doors.','Hands-on courses and mentorship for children, students, professionals and entrepreneurs, in class or online.',
   ['Computer training','Web development','Data analysis','Graphic design','Mentorship programmes','Entrepreneurship training'],'tall-lecture.jpg',False),
]
def services():
    blocks=[]
    for i,(id_,t,h,body,items,img,contain) in enumerate(SVC_DETAIL):
        lis=''.join(f'<li>{x}</li>' for x in items)
        cta = f'<a class="btn btn-primary" href="training.html">View courses {arrow()}</a>' if id_=='training' else f'<a class="btn btn-primary" href="contact.html#{id_}">Request a quote {arrow()}</a>'
        style=' style="object-position:center 20%"' if img=='banner.jpg' else ''
        blocks.append(f'''<div class="split svc-detail{" rev" if i%2 else ""}" id="{id_}">
  <div class="split-media{" contain" if contain else ""}"><img src="assets/{img}" alt="{t.replace('&amp;','and')} at DanSebo" loading="lazy"{style}></div>
  <div><div class="eyebrow">0{i+1} · {t}</div><h2>{h}</h2><div class="body"><p>{body}</p></div><ul class="ticks">{lis}</ul><p style="color:var(--muted);margin-top:14px;font-style:italic">and lots more</p><div class="actions">{cta}</div></div>
</div>''')
    return f'''<main>
{page_head('Services','Our services','Printing, branding, digital solutions and training, delivered by one team from brief to finished work.')}
<section class="section"><div class="wrap">{''.join(blocks)}</div></section>
<section class="section soft"><div class="wrap">
  <div class="head"><div><div class="eyebrow">How it works</div><h2>Simple from request to delivery.</h2></div><p>The same four steps for every job, so you always know what happens next.</p></div>
  <ol class="steps"><li><h3>Send your brief</h3><p>Tell us what you need, the quantity and your deadline.</p></li><li><h3>We design</h3><p>Our team creates or refines the artwork around your brand.</p></li><li><h3>You approve</h3><p>You review a proof. Nothing is produced until you approve it.</p></li><li><h3>We deliver</h3><p>Collect from our office or have it delivered to you.</p></li></ol>
</div></section>
{CTA}
</main>'''

def training():
    return f'''<main>
{page_head('Training','Training programmes','Practical, instructor-led courses for children, students, professionals and entrepreneurs. Choose a course to see what you will learn and the fees.')}
<section class="section"><div class="wrap">
  <div class="head"><div><div class="eyebrow">Courses</div><h2>Find the right course.</h2></div><p>All courses run as physical classes in our training room or as live virtual classes.</p></div>
  {course_cards()}
</div></section>
<section class="section soft"><div class="wrap split">
  <div class="split-media"><img src="assets/tall-lecture.jpg" alt="DanSebo training room" width="960" height="1027" loading="lazy"></div>
  <div><div class="eyebrow">Every student receives</div><h2>Everything you need to start learning.</h2>
  <ul class="ticks" style="grid-template-columns:1fr 1fr"><li>Notepad and pen</li><li>Student ID card</li><li>Branded shirt</li><li>Course manual</li><li>Recognised certificate</li><li>Flexible timing</li></ul>
  <div class="body"><p>A one-time application form of ₦5,000 applies to every course.</p></div></div>
</div></section>
<section class="section"><div class="wrap">
  <div class="head single"><div><div class="eyebrow">Questions</div><h2>Frequently asked questions.</h2></div></div>
  <div class="faq">
    <details><summary>Can I take a course online?</summary><p>Yes. Every course is available as a live virtual class, and the Online Computer Courses programme is designed to be taken entirely online.</p></details>
    <details><summary>Will I receive a certificate?</summary><p>Yes. Every student who completes a course receives a recognised certificate.</p></details>
    <details><summary>Is there a registration fee?</summary><p>Yes. A one-time application form of ₦5,000 applies when you register for any course.</p></details>
    <details><summary>Do you teach children?</summary><p>Yes. Our Kids Computer Courses introduce children to computers, creativity tools and simple coding.</p></details>
    <details><summary>Can you train our staff or students as a group?</summary><p>Yes. We run custom training, mentorship and entrepreneurship programmes for schools and organisations. <a class="link" href="contact.html#training">Contact us</a> to plan one.</p></details>
  </div>
</div></section>
{CTA}
{COURSE_DIALOG}
<script>window.DS_COURSES={json.dumps(COURSES)};</script>
</main>'''

def gallery():
    cells=''.join(f'<button type="button" data-tag="{tag}" data-cap="{cap}"><img src="assets/{f}" alt="{E(alt)}" width="{w}" height="{h}" loading="lazy"><span>{cap}</span></button>' for f,cap,alt,tag,cover,(w,h) in GALLERY)
    return f'''<main>
{page_head('Gallery','Gallery','A look inside our workspace and some of the work we produce.')}
<section class="section"><div class="wrap">{gallery_slider(auto=False)}</div></section>
<section class="section soft"><div class="wrap">
  <div class="head single"><div><div class="eyebrow">All photos</div><h2>Browse by category.</h2></div></div>
  <div class="filters" role="group" aria-label="Filter photos"><button type="button" data-f="all" aria-pressed="true">All</button><button type="button" data-f="workspace" aria-pressed="false">Workspace</button><button type="button" data-f="training" aria-pressed="false">Training</button><button type="button" data-f="work" aria-pressed="false">Our work</button></div>
  <div class="masonry">{cells}</div>
</div></section>
{CTA}
</main>'''

def contact(variant):
    if variant=='deploy':
        mapinner=f'<iframe src="{MAP_EMBED}" title="Map showing DanSebo at Alhalal Plaza, Waff Road, Kaduna" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>'
    else:
        mapinner='<div class="map-art" aria-hidden="true"></div><div class="map-pin" aria-hidden="true"><svg><use href="#i-pinfill"/></svg></div>'
    return f'''<main>
{page_head('Contact','Contact us','Send us a message from anywhere, or visit our head office in Kaduna.')}
<section class="section" id="quote"><div class="wrap contact">
  <div>
    <div class="eyebrow">Get in touch</div>
    <h2 style="font-size:clamp(1.9rem,3.6vw,2.6rem);font-weight:800;margin:14px 0 28px">Let's work together.</h2>
    <div class="cinfo">
      <div>{ic('i-wa')}<p><small>Phone &amp; WhatsApp</small><span>{PHONE}</span></p></div>
      <div>{ic('i-phone')}<p><small>Alternative line</small><span>{PHONE2}</span></p></div>
      <div>{ic('i-mail')}<p><small>Email</small><span>{EMAIL}</span></p></div>
      <div>{ic('i-pin')}<p><small>Head office</small><span>{ADDR}</span></p></div>
    </div>
  </div>
  <form class="cform" id="contactForm" novalidate>
    <h2>Send us a message</h2>
    <p>Ask a question, request a quote or propose a partnership.</p>
    <div class="row2"><div class="field"><label for="cname">Name <span class="req">*</span></label><input id="cname" name="cname" autocomplete="name"></div><div class="field"><label for="corg">Organisation</label><input id="corg" name="corg" autocomplete="organization"></div></div>
    <div class="row2"><div class="field"><label for="cemail">Email</label><input id="cemail" name="cemail" type="email" autocomplete="email"></div><div class="field"><label for="cphone">Phone</label><input id="cphone" name="cphone" type="tel" autocomplete="tel"></div></div>
    <div class="field"><label for="csubject">Subject</label><select id="csubject" name="csubject"><option>General enquiry</option><option>Request a quote</option><option>Printing &amp; Production</option><option>Branding &amp; Creative Design</option><option>ICT &amp; Digital Solutions</option><option>Training &amp; Mentorship</option><option>Partnership</option></select></div>
    <div class="field"><label for="cmsg">Message <span class="req">*</span></label><textarea id="cmsg" name="cmsg" placeholder="Tell us what you need, quantities and your deadline"></textarea></div>
    <div class="btns"><a class="btn btn-primary" id="cfWa" href="{WA}" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="#i-wa"/></svg>Send via WhatsApp</a></div>
    <div class="form-ok" id="cfOk" role="status" hidden>WhatsApp has opened with your message. Press send there to reach us.</div>
  </form>
</div></section>
<section class="section tight soft"><div class="wrap">
  <div class="head single"><div><div class="eyebrow">Find us</div><h2>Visit our head office.</h2></div></div>
  <div class="map">{mapinner}
    <div class="map-card"><b>DanSebo Global Services Ltd</b><span>{ADDR}</span><div class="btns"><a class="btn btn-primary" href="{MAP_DIR}" target="_blank" rel="noopener">Get directions</a><a class="btn btn-line" href="{MAP_LINK}" target="_blank" rel="noopener">Open in Google Maps</a></div></div>
  </div>
</div></section>
</main>'''

PAGES = [
 ('index.html','DanSebo Global Services','Printing, branding, ICT and training. Your Vision, Our Expertise.',home,True),
 ('about.html','About · DanSebo Global Services','About DanSebo Global Services Ltd, our CEO, certificates and partners.',about,False),
 ('services.html','Services · DanSebo Global Services','Printing, branding, ICT and training services from DanSebo.',services,False),
 ('training.html','Training · DanSebo Global Services','Computer, web, data and design courses from DanSebo.',training,False),
 ('gallery.html','Gallery · DanSebo Global Services','Photos of the DanSebo workspace and our work.',gallery,False),
 ('contact.html','Contact · DanSebo Global Services','Contact DanSebo Global Services Ltd.',contact,False),
]
FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">'
BASE=':root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'

ICON_LINKS='<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">\n<link rel="icon" type="image/png" sizes="48x48" href="assets/favicon-48.png">\n<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">\n<meta name="theme-color" content="#3F3F98">'
SLUG={'index.html':'/','about.html':'/about','services.html':'/services','training.html':'/training','gallery.html':'/gallery','contact.html':'/contact'}

def vercelize(doc):
    """Clean URLs and root-relative asset paths for Vercel."""
    for fn,slug in SLUG.items():
        doc=doc.replace(f'href="{fn}#',f'href="{slug if slug!="/" else "/"}#').replace(f'href="{fn}"',f'href="{slug}"')
    doc=doc.replace('src="assets/','src="/assets/').replace('href="assets/','href="/assets/').replace('data-src="assets/','data-src="/assets/')
    doc=doc.replace('href="site.css"','href="/site.css"').replace('src="site.js"','src="/site.js"')
    return doc

def seo(fn,title,desc):
    if not SITE_URL: return ''
    url=SITE_URL+(SLUG[fn] if SLUG[fn]!='/' else '/')
    return (f'<link rel="canonical" href="{url}">\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="DanSebo Global Services">\n'
            f'<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{SITE_URL}/assets/hero-hub.jpg">\n<meta name="twitter:card" content="summary_large_image">')

def full_doc(title,meta,styles,bodycls,content):
    return f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n{meta}\n<style>{BASE}</style>\n{styles}\n</head>\n<body{bodycls}>\n{content}\n</body>\n</html>'

NOT_FOUND=f'''<main>
<section class="page-head" style="min-height:60vh;display:flex;align-items:center"><div class="wrap">
  <div class="eyebrow">Error 404</div>
  <h1>We couldn\'t find that page.</h1>
  <p>The link may be old or mistyped. Try one of these instead.</p>
  <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:28px"><a class="btn btn-primary" href="index.html">Go to the home page</a><a class="btn btn-line" href="services.html">Our services</a><a class="btn btn-line" href="contact.html">Contact us</a></div>
</div></section>
</main>'''

def build(variant):
    out=os.path.join(ROOT, 'dist' if variant=='preview' else 'deploy')
    shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    shutil.copytree(os.path.join(ROOT,'assets'), os.path.join(out,'assets'))
    if variant=='deploy':
        open(os.path.join(out,'site.css'),'w').write(CSS); open(os.path.join(out,'site.js'),'w').write(JS)
    pages=list(PAGES)+([('404.html','Page not found · DanSebo Global Services','This page could not be found.',lambda:NOT_FOUND,False)] if variant=='deploy' else [])
    for fn,title,desc,fnc,hero in pages:
        body = fnc(variant) if fnc is contact else fnc()
        bodycls = '' if hero else ' class="no-hero"'
        if variant=='deploy':
            styles='<link rel="stylesheet" href="site.css">'; script='<script src="site.js" defer></script>'
            meta=f'<title>{title}</title>\n<meta name="description" content="{desc}">\n{ICON_LINKS}\n{seo(fn,title,desc) if fn in SLUG else ""}\n{FONTS}'
            if fn=='404.html': meta+='\n<meta name="robots" content="noindex">'
        else:
            styles=f'<style>{CSS}</style>'; script=f'<script>{JS}</script>'
            meta=f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n<meta name="description" content="{desc}">\n{ICON_LINKS}\n{FONTS}'
        content=f'{ICONS}\n{header(fn)}\n{body}\n{FOOTER}\n{script}'
        if variant=='preview' and fn=='index.html':
            doc=f'{meta}\n{styles}\n{content}'
        else:
            doc=full_doc(title,meta,styles,bodycls,content)
        if variant=='deploy': doc=vercelize(doc)
        open(os.path.join(out,fn),'w').write(doc)
    if variant=='deploy':
        vercel={"cleanUrls":True,"trailingSlash":False,
          "headers":[
            {"source":"/assets/(.*)","headers":[{"key":"Cache-Control","value":"public, max-age=31536000, immutable"}]},
            {"source":"/(site.css|site.js)","headers":[{"key":"Cache-Control","value":"public, max-age=3600, must-revalidate"}]},
            {"source":"/(.*)","headers":[{"key":"X-Content-Type-Options","value":"nosniff"},{"key":"Referrer-Policy","value":"strict-origin-when-cross-origin"},{"key":"X-Frame-Options","value":"SAMEORIGIN"}]}]}
        open(os.path.join(out,'vercel.json'),'w').write(json.dumps(vercel,indent=2)+'\n')
        robots='User-agent: *\nAllow: /\n'+(f'\nSitemap: {SITE_URL}/sitemap.xml\n' if SITE_URL else '')
        open(os.path.join(out,'robots.txt'),'w').write(robots)
        if SITE_URL:
            urls=''.join(f'  <url><loc>{SITE_URL}{slug if slug!="/" else "/"}</loc></url>\n' for slug in SLUG.values())
            open(os.path.join(out,'sitemap.xml'),'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    print(variant,'->',out, sorted(os.listdir(out)))

if __name__=='__main__':
    for v in (sys.argv[1:] or ['preview','deploy']): build(v)
