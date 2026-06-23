"""
Baked-in Top Beauty Brands reference data: the 10 best-selling beauty brands on
Ulta.com in 2025 (by share of online sales), with each brand's category, the
Ulta.com online sales share, official website, social handles (Instagram,
X/Twitter) and Wikipedia page.

Ranking is the "Top 10 brands by online share of sales on ulta.com in 2025"
reported by WWD using Navigo Marketing data (excludes brick-and-mortar and Ulta
app sales). The shares are a snapshot; refresh periodically. Social accounts are
official brand handles; blank where not verifiable. Wikipedia links are direct
article URLs.

Sources:
  https://www.ulta.com/
  https://wwd.com/beauty-industry-news/beauty-features/ulta-beauty-top-brands-clinique-skin-care-1238468506/
"""

BEAUTY_EDITION = "Ulta.com 2025 online sales share"
BEAUTY_SOURCE_URL = "https://www.ulta.com/"

TOP_BEAUTY_BRANDS = [
    {"rank": 1, "brand": "Clinique", "category": "Skincare & makeup", "share": "3.3%", "website": "https://www.clinique.com/", "instagram": "https://www.instagram.com/clinique", "twitter": "https://x.com/clinique", "wikipedia": "https://en.wikipedia.org/wiki/Clinique"},
    {"rank": 2, "brand": "La Roche-Posay", "category": "Skincare (dermatological)", "share": "2.5%", "website": "https://www.laroche-posay.us/", "instagram": "https://www.instagram.com/larocheposayusa", "twitter": "https://x.com/LaRochePosayUSA", "wikipedia": "https://en.wikipedia.org/wiki/La_Roche-Posay"},
    {"rank": 3, "brand": "Ulta Beauty Collection", "category": "Retailer own-brand", "share": "2.4%", "website": "https://www.ulta.com/brand/ulta-beauty-collection", "instagram": "https://www.instagram.com/ultabeauty", "twitter": "https://x.com/ultabeauty", "wikipedia": "https://en.wikipedia.org/wiki/Ulta_Beauty"},
    {"rank": 4, "brand": "Redken", "category": "Haircare (professional)", "share": "2.0%", "website": "https://www.redken.com/", "instagram": "https://www.instagram.com/redken", "twitter": "https://x.com/Redken5thAve", "wikipedia": "https://en.wikipedia.org/wiki/Redken"},
    {"rank": 5, "brand": "Sol de Janeiro", "category": "Body & fragrance", "share": "1.5%", "website": "https://soldejaneiro.com/", "instagram": "https://www.instagram.com/soldejaneiro", "twitter": "", "wikipedia": "https://en.wikipedia.org/wiki/Sol_de_Janeiro"},
    {"rank": 6, "brand": "e.l.f. Cosmetics", "category": "Makeup (mass)", "share": "1.4%", "website": "https://www.elfcosmetics.com/", "instagram": "https://www.instagram.com/elfcosmetics", "twitter": "https://x.com/elfcosmetics", "wikipedia": "https://en.wikipedia.org/wiki/E.l.f."},
    {"rank": 7, "brand": "Tarte Cosmetics", "category": "Makeup", "share": "1.3%", "website": "https://tartecosmetics.com/", "instagram": "https://www.instagram.com/tartecosmetics", "twitter": "https://x.com/tartecosmetics", "wikipedia": ""},
    {"rank": 8, "brand": "OPI", "category": "Nail care", "share": "1.2%", "website": "https://www.opi.com/", "instagram": "https://www.instagram.com/opi", "twitter": "https://x.com/OPI_PRODUCTS", "wikipedia": "https://en.wikipedia.org/wiki/OPI_Products"},
    {"rank": 9, "brand": "NYX Professional Makeup", "category": "Makeup (mass)", "share": "1.2%", "website": "https://www.nyxcosmetics.com/", "instagram": "https://www.instagram.com/nyxcosmetics", "twitter": "https://x.com/nyxcosmetics", "wikipedia": "https://en.wikipedia.org/wiki/NYX_(company)"},
    {"rank": 10, "brand": "Tree Hut", "category": "Body care", "share": "1.1%", "website": "https://www.treehutshea.com/", "instagram": "https://www.instagram.com/treehut", "twitter": "", "wikipedia": "https://en.wikipedia.org/wiki/Tree_Hut"},
]
