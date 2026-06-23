"""
Baked-in Top Motorsports reference data: the 10 most popular motorsport series
and events, with each one's discipline, official website, social handles
(X/Twitter, Instagram, YouTube) and Wikipedia page.

Ranking and selection follow SportsWave's "Top 10 Most Popular Motorsports",
cross-referenced with Wikipedia's list of motorsport championships. The official
sites are JavaScript-heavy, so this is a curated snapshot stored here and
refreshed periodically. Social accounts are official handles; blank where not
verifiable. Wikipedia links are direct article URLs.

Sources:
  https://www.sportswave.ca/the-top-10-most-popular-motorsports/
  https://en.wikipedia.org/wiki/List_of_motorsport_championships
"""

MOTORSPORT_EDITION = "Top 10 by popularity"
MOTORSPORT_SOURCE_URL = "https://www.sportswave.ca/the-top-10-most-popular-motorsports/"

TOP_MOTORSPORTS = [
    {"rank": 1, "series": "Formula 1", "category": "Open-wheel (circuit)", "website": "https://www.formula1.com/", "twitter": "https://x.com/F1", "instagram": "https://www.instagram.com/f1", "youtube": "https://www.youtube.com/@Formula1", "wikipedia": "https://en.wikipedia.org/wiki/Formula_One"},
    {"rank": 2, "series": "NASCAR", "category": "Stock car", "website": "https://www.nascar.com/", "twitter": "https://x.com/NASCAR", "instagram": "https://www.instagram.com/nascar", "youtube": "https://www.youtube.com/NASCAR", "wikipedia": "https://en.wikipedia.org/wiki/NASCAR"},
    {"rank": 3, "series": "MotoGP", "category": "Motorcycle road racing", "website": "https://www.motogp.com/", "twitter": "https://x.com/MotoGP", "instagram": "https://www.instagram.com/motogp", "youtube": "https://www.youtube.com/motogp", "wikipedia": "https://en.wikipedia.org/wiki/Grand_Prix_motorcycle_racing"},
    {"rank": 4, "series": "IndyCar", "category": "Open-wheel (circuit/oval)", "website": "https://www.indycar.com/", "twitter": "https://x.com/IndyCar", "instagram": "https://www.instagram.com/indycar", "youtube": "https://www.youtube.com/@indycar", "wikipedia": "https://en.wikipedia.org/wiki/IndyCar_Series"},
    {"rank": 5, "series": "24 Hours of Le Mans", "category": "Endurance (sports car)", "website": "https://www.24h-lemans.com/en", "twitter": "https://x.com/24hoursoflemans", "instagram": "https://www.instagram.com/24heuresdumans", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/24_Hours_of_Le_Mans"},
    {"rank": 6, "series": "World Rally Championship", "category": "Rally", "website": "https://www.wrc.com/", "twitter": "https://x.com/OfficialWRC", "instagram": "https://www.instagram.com/officialwrc", "youtube": "https://www.youtube.com/@wrc", "wikipedia": "https://en.wikipedia.org/wiki/World_Rally_Championship"},
    {"rank": 7, "series": "Dakar Rally", "category": "Rally raid (off-road)", "website": "https://www.dakar.com/", "twitter": "https://x.com/dakar", "instagram": "", "youtube": "https://www.youtube.com/@OfficialDakar", "wikipedia": "https://en.wikipedia.org/wiki/Dakar_Rally"},
    {"rank": 8, "series": "Formula E", "category": "Electric open-wheel", "website": "https://www.fiaformulae.com/", "twitter": "https://x.com/FIAFormulaE", "instagram": "https://www.instagram.com/fiaformulae", "youtube": "https://www.youtube.com/@FIAFormulaE", "wikipedia": "https://en.wikipedia.org/wiki/Formula_E"},
    {"rank": 9, "series": "Motocross (MXGP)", "category": "Off-road motorcycle", "website": "https://www.mxgp.com/", "twitter": "https://x.com/mxgp", "instagram": "https://www.instagram.com/mxgp", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Motocross_World_Championship"},
    {"rank": 10, "series": "Isle of Man TT", "category": "Motorcycle road race", "website": "https://www.iomttraces.com/", "twitter": "https://x.com/ttracesofficial", "instagram": "https://www.instagram.com/ttracesofficial", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Isle_of_Man_TT"},
]
