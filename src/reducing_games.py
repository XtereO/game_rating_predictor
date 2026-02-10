import pandas as pd

def reduce_games(raw_games):
    reduced_games = pd.DataFrame(columns=["id", "slug", "playtime", "platforms", "stores", "tags", "genres", "rating"])
    for rg in raw_games:
        reduced_game = pd.DataFrame([{
            "id": rg["id"],
            "slug": rg["slug"],
            "playtime": rg["playtime"],
            "platforms": _join_by_slug(rg["platforms"], "platform"),
            "stores": _join_by_slug(rg["stores"], "store"),
            "tags": _join_by_slug(filter(lambda t: t["language"]=="eng", rg["tags"])), 
            "genres": _join_by_slug(rg["genres"]), 
            "rating": rg["rating"]
        }])
        reduced_games = pd.concat([reduced_games, reduced_game], ignore_index=True)

    return reduced_games

def _join_by_slug(arr, col=""):
    if(arr==None):
        return ""
    if(col==""):
        return ",".join(a["slug"] for a in arr)
    return ",".join(a[col]["slug"] for a in arr)