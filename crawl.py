from bs4 import BeautifulSoup
from urlparse import urljoin
import urllib, re, requests, shutil, subprocess, os, time, json, sys

with open("ReleasedSwissVideoGames.html") as f:
    soup = BeautifulSoup(f)

def enc(l):
    return [x.encode('utf-8') for x in l]

def img_dims(src):
    name = "tmp/" + src.replace("/", "_").replace(":", "")
    if not os.path.exists(name):
        r2 = requests.get(src, timeout=8)
        if r2.status_code == 200:
            with open(name, 'wb') as f:
                f.write(r2.content)
    w, h = [int(x) for x in subprocess.check_output(["java", "-cp", ".", "ImgSize", name]).split(" ")]
    return (w, h)

def check_url(url):
    if not url.startswith("http"):
        return None
    try:
        r = requests.get(url, timeout=8)
    except:
        return None
    if 199 < r.status_code < 400:
        return BeautifulSoup(r.text)
    else:
        return None

def screenshot(soup):
    best_size = 200 * 100
    best_screen_url = None
    for img_tag in soup.find_all('img'):
        time.sleep(0.1)
        try:
            src = urljoin(url, img_tag["src"])
            w, h = img_dims(src)
            size = w * h
            aspect = w * 1.0 / h
            if aspect < 5.0 and aspect > 0.3 and size > best_size:
                best_screen_url = src
                best_size = size
        except:
            pass
    for a_tag in soup.find_all('a'):
        if "href" in a_tag.attrs and (a_tag["href"].endswith(".jpg") or a_tag["href"].endswith(".png")):
            time.sleep(0.1)
            try:
                src = urljoin(url, a_tag["href"])
                w, h = img_dims(src)
                size = w * h
                aspect = w * 1.0 / h
                if aspect < 5.0 and aspect > 0.3 and size > best_size:
                    best_screen_url = src
                    best_size = size
            except:
                pass
    if not best_screen_url:
        return None
    # Copy to media
    format = best_screen_url.split(".")[-1].lower()
    src = "tmp/" + best_screen_url.replace("/", "_").replace(":", "")
    dst = "img/media/" + re.sub("[^a-zA-Z0-9.]", "", best_screen_url)
    if not format in ["jpg", "png", "gif"]:
        format = "png"
        dst = dst + ".png"
    subprocess.check_output(["java", "-cp", ".", "Resize", src, "400", dst, format])
    return dst

def youtube(soup):
    for iframe_tag in soup.find_all('iframe'):
        if 'src' in iframe_tag.attrs and "youtube.com/embed/" in iframe_tag['src']:
            m = re.match(".*youtube.com/embed/([^/]+).*", iframe_tag['src'])
            if m:
                return "https://www.youtube.com/watch?v=" + m.group(1)

def steam(soup):
    for iframe_tag in soup.find_all('iframe'):
        if 'src' in iframe_tag.attrs and iframe_tag['src'].startswith("http://store.steampowered.com/widget/"):
            m = re.match("http://store.steampowered.com/widget/([^/]+)/", iframe_tag['src'])
            if m:
                return "http://store.steampowered.com/app/" + m.group(1) + "/"

def vimeo(soup):
    for iframe_tag in soup.find_all('iframe'):
        if 'src' in iframe_tag.attrs and "player.vimeo.com" in iframe_tag['src']:
            m = re.match(".*player.vimeo.com/video/([^/]+).*", iframe_tag['src'])
            if m:
                return "http://player.vimeo.com/video/" + m.group(1) + "/"

def apple(soup):
    for a_tag in soup.find_all('a'):
        if 'href' in a_tag.attrs and a_tag['href'].startswith("https://itunes.apple.com"):
            return a_tag['href']

def google(soup):
    for a_tag in soup.find_all('a'):
        if 'href' in a_tag.attrs and a_tag['href'].startswith("https://play.google.com"):
            return a_tag['href']

update_mask = None
if len(sys.argv) > 1:
    with open(sys.argv[1], "r") as f:
        update_mask = set(json.load(f))

json_l = []
try:
    with open("out.json", "r") as f:
        json_l = json.load(f)
except:
    pass

def put(json_l, o):
    for x in range(len(json_l)):
        if json_l[x]["name"] == o["name"]:
            json_l[x] = o
            return
    json_l.append(o)

for p in soup.find_all("p"):
    if p.a and "href" in p.a.attrs:
        name = p.a.text
        if update_mask and not name in update_mask:
            continue
        url = urllib.unquote(p.a["href"].replace("http://www.google.com/url?q=", "").replace("https://www.google.com/url?q=", "").split("&")[0])
        soup = check_url(url)
        print name
        if not soup:
            print "Skipped - cannot load website at " + url
        else:
            m = re.match(".*\\(([^,]+),? ?(([0-9]{4}))?\\).*", p.text)
            if not m:
                m = re.match(".*\\((.+)(, ?([0-9]{4}))\\).*", p.text)
            if not m:
                m = re.match(".*\\(([^,]+),? ?(([0-9]{4})).*", p.text)
            if not m:
                print "Skipped - cannot parse info: " + p.text
            else:
                developer = m.group(1)
                year = m.group(3)
                screen = screenshot(soup)
                yt = youtube(soup)
                vim = vimeo(soup)
                st = steam(soup)
                ap = apple(soup)
                goog = google(soup)
                o = {"name": name, "url": url, "developer": developer}
                if year:
                    o["year"] = year
                if screen:
                    o["screenshot"] = screen
                if yt:
                    o["youtube"] = yt
                if vim:
                    o["vimeo"] = vim
                if st:
                    o["steam"] = st
                if ap:
                    o["apple"] = ap
                if goog:
                    o["google"] = goog
                put(json_l, o)
                print name, url, developer, year or "", screen or "", yt or "", vim or "", st or "", ap or "", goog or ""
with open("out.json", "w") as f:
    json.dump(json_l, f)
