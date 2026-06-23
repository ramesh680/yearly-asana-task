"""
Baked-in Saudi Pro League reference data: the 18 clubs of the 2025/26 Saudi Pro
League (Roshn Saudi League) season, ordered by final league position, with each
club's home city, stadium, points, official website, social handles
(X/Twitter, Instagram, Facebook, YouTube) and Wikipedia page.

Versioned yearly snapshot. The official Saudi Pro League site
(https://www.spl.com.sa/en) is JavaScript-rendered, so the club list and final
standings are stored here and refreshed each season. Social accounts are
official club handles; blank where not verifiable. Wikipedia links are direct
article URLs.

Source: https://www.spl.com.sa/en
"""

SPL_EDITION = "2025/26"
SPL_SOURCE_URL = "https://www.spl.com.sa/en"

SAUDI_PRO_LEAGUE_CLUBS = [
    {"position": 1, "club": "Al-Nassr", "city": "Riyadh", "stadium": "Al-Awwal Park", "points": 86, "website": "https://www.alnassr.sa/", "twitter": "https://x.com/AlNassrFC", "instagram": "https://www.instagram.com/alnassr", "facebook": "https://www.facebook.com/AlNassrFC", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al-Nassr_FC"},
    {"position": 2, "club": "Al-Hilal", "city": "Riyadh", "stadium": "Kingdom Arena", "points": 84, "website": "https://www.alhilal.com/", "twitter": "https://x.com/Alhilal_FC", "instagram": "https://www.instagram.com/alhilal", "facebook": "https://www.facebook.com/AlhilalFC", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al_Hilal_SFC"},
    {"position": 3, "club": "Al-Ahli", "city": "Jeddah", "stadium": "King Abdullah Sports City Stadium", "points": 81, "website": "https://www.alahlifc.sa/", "twitter": "https://x.com/ALAHLI_FCEN", "instagram": "https://www.instagram.com/alahliclub.sa", "facebook": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al-Ahli_Saudi_FC"},
    {"position": 4, "club": "Al-Qadsiah", "city": "Khobar", "stadium": "Prince Mohammed bin Fahd Stadium", "points": 77, "website": "https://alqadsiah.com/", "twitter": "https://x.com/AlQadsiahEN", "instagram": "https://www.instagram.com/fcqadsiah", "facebook": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al_Qadsiah_FC"},
    {"position": 5, "club": "Al-Ittihad", "city": "Jeddah", "stadium": "King Abdullah Sports City Stadium", "points": 55, "website": "https://ittihadclub.sa/", "twitter": "https://x.com/ittihad_en", "instagram": "https://www.instagram.com/ittihadclub.sa", "facebook": "https://www.facebook.com/ittihadclub.sa", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al-Ittihad_Club_(Jeddah)"},
    {"position": 6, "club": "Al-Taawoun", "city": "Buraidah", "stadium": "King Abdullah Sports City (Buraidah)", "points": 53, "website": "", "twitter": "https://x.com/AltaawounFC", "instagram": "https://www.instagram.com/altaawounfc", "facebook": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al_Taawoun_FC"},
    {"position": 7, "club": "Al-Ettifaq", "city": "Dammam", "stadium": "EGO Stadium", "points": 50, "website": "https://www.ettifaq.com/", "twitter": "https://x.com/ettifaq", "instagram": "https://www.instagram.com/ettifaq", "facebook": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al-Ettifaq_Club"},
    {"position": 8, "club": "Neom", "city": "Tabuk", "stadium": "King Khalid Sport City Stadium", "points": 45, "website": "https://www.neom.com/en-us/neom-sports-club", "twitter": "", "instagram": "https://www.instagram.com/neomsportsclub", "facebook": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Neom_SC"},
    {"position": 9, "club": "Al-Hazem", "city": "Ar Rass", "stadium": "Al-Hazem Club Stadium", "points": 42, "website": "https://www.alhazemfc.net/", "twitter": "https://x.com/AlhazemFC_EN", "instagram": "https://www.instagram.com/alhazem_fc", "facebook": "https://www.facebook.com/alhazemfc", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al-Hazem_FC"},
    {"position": 10, "club": "Al-Fayha", "city": "Al-Majma'ah", "stadium": "Al-Majma'ah Sports City Stadium", "points": 38, "website": "", "twitter": "https://x.com/AlfayhaSC_en", "instagram": "https://www.instagram.com/alfayhasc", "facebook": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al-Fayha_Club"},
    {"position": 11, "club": "Al-Fateh", "city": "Al-Mubarraz", "stadium": "Maydan Tamweel Aloula", "points": 37, "website": "https://fatehclub.com/", "twitter": "https://x.com/EnFatehclub", "instagram": "https://www.instagram.com/fatehclub", "facebook": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al_Fateh_SC"},
    {"position": 12, "club": "Al-Khaleej", "city": "Saihat", "stadium": "Prince Mohammed bin Fahd Stadium", "points": 37, "website": "", "twitter": "", "instagram": "", "facebook": "https://www.facebook.com/khaleejclub", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al-Khaleej_FC"},
    {"position": 13, "club": "Al-Shabab", "city": "Riyadh", "stadium": "SHG Arena", "points": 35, "website": "https://www.alshabab-sc.sa/", "twitter": "https://x.com/AlShabab_EN", "instagram": "https://www.instagram.com/alshababsaudifc", "facebook": "https://www.facebook.com/AlshababSaudiFC", "youtube": "https://www.youtube.com/c/Shababfc", "wikipedia": "https://en.wikipedia.org/wiki/Al-Shabab_FC_(Riyadh)"},
    {"position": 14, "club": "Al-Kholood", "city": "Ar Rass", "stadium": "Al-Hazem Club Stadium", "points": 33, "website": "https://www.alkholoodclub.com/", "twitter": "https://x.com/AlKholoodFC_EN", "instagram": "https://www.instagram.com/alkholoodclub", "facebook": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al-Kholood_Club"},
    {"position": 15, "club": "Al-Riyadh", "city": "Riyadh", "stadium": "SHG Arena", "points": 30, "website": "https://riyadhclub.sa/", "twitter": "https://x.com/Alriyadh_EN", "instagram": "https://www.instagram.com/alriyadh_fc", "facebook": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al-Riyadh_SC"},
    {"position": 16, "club": "Damac", "city": "Khamis Mushait", "stadium": "Damac Club Stadium", "points": 29, "website": "https://damac.sa/", "twitter": "https://x.com/DAMAC_CLUB", "instagram": "https://www.instagram.com/damac_club", "facebook": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Damac_Club"},
    {"position": 17, "club": "Al-Okhdood", "city": "Najran", "stadium": "Prince Hathloul bin Abdulaziz Sports City Stadium", "points": 20, "website": "https://alakhdoud.com/", "twitter": "https://x.com/alakhdoud", "instagram": "https://www.instagram.com/alakhdoud", "facebook": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al-Okhdood_Club"},
    {"position": 18, "club": "Al-Najma", "city": "Unaizah", "stadium": "King Abdullah Sports City (Buraidah)", "points": 16, "website": "", "twitter": "https://x.com/alnajmah_EN", "instagram": "https://www.instagram.com/alnajma_club", "facebook": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Al-Najma_SC_(Saudi_Arabia)"},
]
