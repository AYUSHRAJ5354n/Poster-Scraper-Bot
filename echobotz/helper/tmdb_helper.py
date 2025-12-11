import re
import requests
from config import Config
from .. import LOGGER

BASE_DIRECT = "https://api.themoviedb.org/3"
BASE_WORKER = "https://tmdbapi.the-zake.workers.dev/3" 

if Config.TMDB_ACCESS_TOKEN:
    BASE = BASE_DIRECT
    H = {
        "Authorization": f"Bearer {Config.TMDB_ACCESS_TOKEN}",
        "accept": "application/json"
    }
else:
    BASE = BASE_WORKER
    H = {
        "accept": "application/json"
    }

IMG = "https://image.tmdb.org/t/p/"

def _n(s):
    return re.sub(r"[^a-z0-9]+", "", str(s).lower())

def _s(q):
    LOGGER.info(f"TMDB SEARCH QUERY: {q}")

    t = q.strip()
    y = None
    m = re.search(r"(19|20)\d{2}$", t)
    if m:
        y = m.group(0)
        t = t[: -4].strip()
        LOGGER.info(f"YEAR DETECTED: {y}")

    p = {
        "query": t,
        "include_adult": "false",
        "language": "en-US",
        "page": 1,
    }

    r = requests.get(f"{BASE}/search/multi", headers=H, params=p).json()
    res = r.get("results") or []
    res = [x for x in res if x.get("media_type") in ("movie", "tv")]

    LOGGER.info(f"TMDB RESULTS FOUND (raw movie+tv): {len(res)}")

    if not res:
        LOGGER.warning("TMDB SEARCH RETURNED EMPTY")
        return None

    if y:
        flt = []
        for x in res:
            rd = x.get("release_date") or x.get("first_air_date") or ""
            yr = rd[:4] if rd else ""
            if yr == y:
                flt.append(x)
        if flt:
            res = flt
            LOGGER.info(f"YEAR FILTER APPLIED: {y}, RESULTS AFTER FILTER: {len(res)}")

    nq = _n(t)
    best = None
    best_score = -1

    for x in res:
        mt = x.get("media_type")
        title = (
            x.get("title")
            or x.get("name")
            or x.get("original_title")
            or x.get("original_name")
            or ""
        )
        nt = _n(title)

        rd = x.get("release_date") or x.get("first_air_date") or ""
        yr = rd[:4] if rd else ""
        vc = x.get("vote_count", 0) or 0
        pop = x.get("popularity", 0) or 0

        sc = 0

        if len(nq) <= 3:
            if nt == nq:
                sc += 1000
            elif nq in nt:
                sc += 500
        else:
            if nt == nq:
                sc += 4000
            elif nt.startswith(nq):
                sc += 2500
            elif nq in nt:
                sc += 1500

        if y and yr == y:
            sc += 5000

        sc += vc * 2
        sc += pop * 10

        if sc > best_score:
            best_score = sc
            best = (mt, x.get("id"), title, yr)

    LOGGER.info(f"TMDB SELECTED: {best} WITH SCORE: {best_score}")

    return best

def _pick_sets(items):
    en = []
    oth = []
    nul = []
    for x in items:
        lang = x.get("iso_639_1")
        if lang == "en":
            en.append(x)
        elif lang in (None, "", "xx"):
            nul.append(x)
        else:
            oth.append(x)
    for lst in (en, oth, nul):
        lst.sort(key=lambda z: z.get("vote_count", 0), reverse=True)
    use = en or oth or nul
    return use

def _i(kind, mid):
    if kind == "tv":
        url = f"{BASE}/tv/{mid}/images"
    else:
        url = f"{BASE}/movie/{mid}/images"

    LOGGER.info(f"TMDB IMAGE FETCH URL: {url}")

    r = requests.get(
        url,
        headers=H,
        params={
            "include_image_language": "en,null,hi,ta,te,ml,kn,bn,mr,gu,pa,ur,fr,es,de,it,ja,ko,zh",
        }
    ).json()

    d = {"posters": [], "backdrops": [], "logos": []}

    posters_raw = r.get("posters", []) or []
    backs_raw = r.get("backdrops", []) or []
    logos_raw = r.get("logos", []) or []

    LOGGER.info(
        f"TMDB IMAGES RAW → Posters: {len(posters_raw)}, "
        f"Backdrops: {len(backs_raw)}, Logos: {len(logos_raw)}"
    )

    use_p = _pick_sets(posters_raw)
    for x in use_p[:10]:
        d["posters"].append(IMG + "w500" + x["file_path"])

    backs_raw = [x for x in backs_raw if x.get("aspect_ratio", 0) >= 1.6]
    use_b = _pick_sets(backs_raw)
    for x in use_b[:10]:
        d["backdrops"].append(IMG + "original" + x["file_path"])

    use_l = _pick_sets(logos_raw)
    for x in use_l[:10]:
        d["logos"].append(IMG + "w500" + x["file_path"])

    LOGGER.info(
        f"TMDB IMAGES SELECTED → Posters: {len(d['posters'])}, "
        f"Backdrops: {len(d['backdrops'])}, Logos: {len(d['logos'])}"
    )

    return d
