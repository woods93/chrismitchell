#!/usr/bin/env python3
"""Builds index.html for the Chris Mitchell site. Run: python3 build.py"""
import os, html, json

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---- Settings -------------------------------------------------------------
NAME = "Chris Mitchell"
EMAIL_USER, EMAIL_DOMAIN = "", ""   # fill in when Chris gives a public booking email; leave blank to hide
WEB3FORMS_KEY = ""                  # paste the Web3Forms access key here when it exists
SHOP_URL = ""                       # Fourthwall shop address; blank shows "coming soon"
HERO_IMAGE = "assets/images/hero.jpg"       # used only if the file exists
SING_COVER = "assets/images/sing-cover.jpg" # used only if the file exists
AUDIO = []   # e.g. [("All The Things You Are", "assets/audio/all-the-things-you-are.mp3")]
LINKS = []   # [("Spotify", url), ("Apple Music", url), ("YouTube", url)] once Chris confirms official links
VIDEOS = []  # [(youtube_id, "Title", "Note")]

SING_TRACKS = [
    "I Will Love Again", "All The Things You Are", "Love Somebody", "Unconcerned",
    "Gravity", "What True Love Is Like", "Sing", "Best of Intentions",
    "With A Little Help From My Friends", "People Get Ready (feat. Darci Monet)",
    "In Your Eyes", "Grace", "What True Love Is Like (Deep Dream Mix)",
]

BANDS = [
    ("The Collection", "Chris’s own band. Funky, theatrical, and loud, with a nonstop dance groove. Late-1990s Nashville party-scene favorites who opened for The Ohio Players, Parliament Funkadelic, and KC &amp; The Sunshine Band."),
    ("Trial By Fire", "A tribute to the music of Journey."),
    ("Ned Zeppelin", "Led Zeppelin, Nashville style."),
    ("The Long Players", "Classic albums, played live."),
    ("The Black Jacket Symphony", "Rock fans know the show: great records performed live, front to back."),
]

def e(s): return html.escape(s, quote=True)
def exists(rel): return os.path.exists(os.path.join(ROOT, rel))

def lite(vid, title):
    return f'''<button class="yt" type="button" data-id="{vid}" aria-label="Play video: {e(title)}">
  <img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360">
  <span class="play" aria-hidden="true"></span>
</button>'''

hero_media = (f'<img class="portrait" src="{HERO_IMAGE}" alt="Chris Mitchell" width="800" height="1000">'
              if exists(HERO_IMAGE) else '')
hero_cls = "hero has-photo" if hero_media else "hero"
cover = (f'<img class="cover" src="{SING_COVER}" alt="Sing album cover" width="400" height="400">'
         if exists(SING_COVER) else '')
tracks_html = "".join(f'<li><span>{e(t)}</span></li>' for t in SING_TRACKS)
bands_html = "".join(f'<article class="fam-card"><h3>{n}</h3><p>{d}</p></article>' for n, d in BANDS)
links_html = ("".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a>' for n, u in LINKS))
links_block = f'<p class="stream">{links_html}</p>' if links_html else ''

videos_block = ""
if VIDEOS:
    cards = "".join(f'<figure class="video">{lite(v[0], v[1])}<figcaption><strong>{e(v[1])}</strong><span>{e(v[2])}</span></figcaption></figure>' for v in VIDEOS)
    videos_block = f'<h3>Watch</h3><div class="videos">{cards}</div>'
audio_block = ""
if AUDIO:
    items = "".join(f'<li><span>{e(t)}</span><audio controls preload="none" src="{e(p)}"></audio></li>' for t, p in AUDIO)
    audio_block = f'<h3>Listen</h3><ul class="audio">{items}</ul>'

def _family_cards():
    with open(os.path.join(ROOT, "family.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    out = []
    for f in data:
        if f["id"] == "chris-mitchell":
            continue
        pic = ('<a class="fam-pic" href="%s" rel="noopener"><img src="%s" alt="%s" loading="lazy" '
               'referrerpolicy="no-referrer" onerror="this.parentNode.remove()"></a>'
               % (e(f["url"]), e(f["image"]), e(f["name"]))) if f.get("image") else ""
        out.append('<article class="fam-card">%s<h3><a href="%s" rel="noopener">%s</a></h3><p>%s</p></article>'
                   % (pic, e(f["url"]), e(f["name"]), e(f.get("blurb", ""))))
    return "".join(out)

family_html = _family_cards()
shop_html = (f'<p>Official Chris Mitchell merch.</p><p><a class="btn" href="{SHOP_URL}" target="_blank" rel="noopener">Visit the shop</a></p>'
             if SHOP_URL else '<p>Merch is on its way. Check back soon.</p>')
key_attr = e(WEB3FORMS_KEY)
mail_line = (f'For booking, vocals, studio time, and everything else, write to <a class="mail" data-u="{EMAIL_USER}" data-d="{EMAIL_DOMAIN}" href="#contact">email</a>, or use the form.'
             if EMAIL_USER else 'For booking, vocals, studio time, and everything else, use the form.')

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chris Mitchell — Nashville Vocalist, Bandleader &amp; Producer</title>
<meta name="description" content="Chris Mitchell is a Nashville vocalist, bandleader, and producer. Funk, soul, rock, and pop: The Collection, Nickelbug Records, and the album Sing.">
<meta property="og:title" content="Chris Mitchell">
<meta property="og:description" content="Nashville vocalist, bandleader, and producer. Hear the music, meet the bands, get in touch.">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600&family=Playfair+Display:wght@700;900&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css?v=cm1">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a class="brand" href="#top">Chris Mitchell</a>
  <nav aria-label="Main"><ul>
    <li><a href="#bio">Bio</a></li>
    <li><a href="#music">Music</a></li>
    <li><a href="#bands">Bands</a></li>
    <li><a href="#studio">Studio</a></li>
    <li><a href="#shop">Shop</a></li>
    <li><a href="#family">Family</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul></nav>
</header>
<main id="main">

<section id="top" class="{hero_cls}">
  <div class="hero-text">
    <p class="kicker">Vocalist · Bandleader · Producer · Nashville</p>
    <h1>Chris<br>Mitchell</h1>
    <p class="lede">Making the world a better place one song at a time.</p>
    <p><a class="btn" href="#music">Hear the music</a> <a class="btn ghost" href="#contact">Get in touch</a></p>
  </div>
  {hero_media}
</section>

<section id="bio">
  <h2>Bio</h2>
  <div class="prose">
    <p>Chris Mitchell loves to sing and is almost always doing it. Spend a few minutes with him and you will be serenaded with verses, choruses, and instrumental breaks, real and imagined.</p>
    <p>An Akron, Ohio native, he started on violin and in school singing in the early grades, wrote his first song in sixth grade, and went on to years of voice lessons, twelve bands, an orchestra, and two music schools before landing in Nashville.</p>
    <p>In the late 1990s his band The Collection became a fixture of the city’s party scene, a spectacle of hot pants, feather boas, choir robes, and a nonstop funky groove. In 2005 he began “Chris Mitchell Presents,” a monthly event that helped launch several Nashville artists.</p>
    <p>His album <em>Sing</em> (2010) came out on his own Nickelbug Records. Today he sings with The Collection and a lineup of Nashville tribute bands, produces and records at Nickelbug Music, and coaches vocalists.</p>
  </div>
</section>

<section id="music">
  <h2>Music</h2>
  <div class="album">
    {cover}
    <div>
      <h3><em>Sing</em> <span class="year">2010</span></h3>
      <p class="small">Nickelbug Records · R&amp;B, pop, and rock</p>
      <ol class="tracks">{tracks_html}</ol>
      {links_block}
    </div>
  </div>
  <h3><em>Chris Mitchell</em> <span class="year">1999</span></h3>
  <p>The self-titled CD from Chris Mitchell &amp; The Collection, produced by Chris Mitchell and Josh Harris. Listen.com called the group an eight-piece dance-pop act with confident R&amp;B vocals.</p>
  {audio_block}
  {videos_block}
</section>

<section id="bands">
  <h2>Bands &amp; Shows</h2>
  <p class="lede">Where to catch him on stage.</p>
  <div class="fam-grid">{bands_html}</div>
  <p class="small">Show dates will be posted here.</p>
</section>

<section id="studio">
  <h2>Studio</h2>
  <div class="prose">
    <p><strong>Nickelbug Music</strong> in Nashville is Chris’s recording studio and the home of Nickelbug Records. He produces, records, mixes, and masters, and has worked on projects including Wellsprings Ltd.’s <em>Hell Of A Ride</em> and a live Roger Cook recording. He also does live sound and coaches singers.</p>
  </div>
</section>

<section id="shop">
  <h2>Shop</h2>
  {shop_html}
</section>

<section id="family">
  <h2>Family</h2>
  <p class="lede">Artists, makers, poets, and saints.</p>
  <div class="fam-grid">{family_html}</div>
</section>

<section id="contact">
  <h2>Contact</h2>
  <p>{mail_line}</p>
  <form id="contact-form" class="form" action="https://api.web3forms.com/submit" method="POST" data-key="{key_attr}">
    <input type="hidden" name="access_key" value="{key_attr}">
    <input type="hidden" name="subject" value="New message from the Chris Mitchell website">
    <input type="hidden" name="from_name" value="Chris Mitchell website">
    <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off">
    <label>Name <input name="name" required autocomplete="name"></label>
    <label>Email <input type="email" name="email" required autocomplete="email"></label>
    <label>Message <textarea name="message" rows="5" required></textarea></label>
    <button class="btn" type="submit">Send</button>
    <p class="form-status" role="status"></p>
  </form>
</section>

</main>
<footer class="foot">© <span id="yr">2026</span> Chris Mitchell</footer>
<script src="js/site.js"></script>
</body>
</html>
'''

with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(PAGE)
print("wrote index.html", len(PAGE), "bytes")
