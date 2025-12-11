from requests import post

URL = "https://graphql.anilist.co"


def _req(q, vars=None):
    r = post(URL, json={"query": q, "variables": vars or {}}, timeout=10)
    r.raise_for_status()
    j = r.json()
    if "errors" in j:
        raise RuntimeError(j["errors"])
    return j["data"]


def _search(title, per_page: int = 8):
    q = """
    query ($search: String, $perPage: Int) {
      Page(perPage: $perPage) {
        media(search: $search, type: ANIME) {
          id
          idMal
          title {
            romaji
            english
            native
          }
          format
          episodes
          seasonYear
          status
        }
      }
    }
    """
    d = _req(q, {"search": title, "perPage": per_page})
    return d["Page"]["media"]


def _get(aid: int):
    q = """
    query ($id: Int) {
      Media(id: $id, type: ANIME) {
        id
        idMal
        title {
          romaji
          english
          native
        }
        synonyms
        format
        status
        season
        seasonYear
        episodes
        duration
        averageScore
        popularity
        favourites
        rankings {
          rank
          type
          allTime
          season
          year
        }
        genres
        tags {
          name
          rank
          isAdult
        }
        studios(isMain: true) {
          nodes {
            name
          }
        }
        description(asHtml: false)
        bannerImage
        coverImage {
          extraLarge
          large
          color
        }
        startDate { year month day }
        endDate { year month day }
        nextAiringEpisode {
          episode
          timeUntilAiring
        }
        externalLinks {
          site
          url
        }
        siteUrl
      }
    }
    """
    d = _req(q, {"id": aid})
    return d["Media"]
