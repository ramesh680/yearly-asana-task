"""
Baked-in Racquet Sports reference data: major racket/racquet sports with their
international governing body, governing-body website, social handles and
Wikipedia page, followed by other racket sports from Wikipedia's "List of racket
sports". Governing bodies/websites/socials are verified where a sport has one;
traditional or toy games with no governing body are left blank.

Sources:
  https://en.wikipedia.org/wiki/List_of_racket_sports
"""

RACQUET_EDITION = "Major sports + Wikipedia list"
RACQUET_SOURCE_URL = "https://en.wikipedia.org/wiki/List_of_racket_sports"

RACQUET_SPORTS = [
    {"rank": 1, "sport": "Tennis", "governing_body": "International Tennis Federation (ITF)", "website": "https://www.itftennis.com/", "twitter": "https://x.com/ITFTennis", "instagram": "https://www.instagram.com/itftennis", "wikipedia": "https://en.wikipedia.org/wiki/Tennis"},
    {"rank": 2, "sport": "Badminton", "governing_body": "Badminton World Federation (BWF)", "website": "https://bwfbadminton.com/", "twitter": "https://x.com/bwfmedia", "instagram": "https://www.instagram.com/bwf.official", "wikipedia": "https://en.wikipedia.org/wiki/Badminton"},
    {"rank": 3, "sport": "Table tennis", "governing_body": "International Table Tennis Federation (ITTF)", "website": "https://www.ittf.com/", "twitter": "https://x.com/ittfworld", "instagram": "https://www.instagram.com/ittfworld", "wikipedia": "https://en.wikipedia.org/wiki/Table_tennis"},
    {"rank": 4, "sport": "Squash", "governing_body": "World Squash Federation (WSF)", "website": "https://www.worldsquash.sport/", "twitter": "https://x.com/WorldSquash", "instagram": "https://www.instagram.com/worldsquashofficial", "wikipedia": "https://en.wikipedia.org/wiki/Squash_(sport)"},
    {"rank": 5, "sport": "Pickleball", "governing_body": "USA Pickleball / International Pickleball Federation", "website": "https://usapickleball.org/", "twitter": "https://x.com/USAPickleball", "instagram": "https://www.instagram.com/usapickleball", "wikipedia": "https://en.wikipedia.org/wiki/Pickleball"},
    {"rank": 6, "sport": "Padel", "governing_body": "International Padel Federation (FIP)", "website": "https://www.padelfip.com/", "twitter": "https://x.com/padelfip", "instagram": "https://www.instagram.com/padelfip", "wikipedia": "https://en.wikipedia.org/wiki/Padel_(sport)"},
    {"rank": 7, "sport": "Racquetball", "governing_body": "International Racquetball Federation (IRF)", "website": "https://www.internationalracquetball.com/", "twitter": "https://x.com/irfracquetball", "instagram": "https://www.instagram.com/international_racquetball", "wikipedia": "https://en.wikipedia.org/wiki/Racquetball"},
    {"rank": 8, "sport": "Platform tennis", "governing_body": "American Platform Tennis Association (APTA)", "website": "https://www.platformtennis.org/", "twitter": "", "instagram": "https://www.instagram.com/americanplatformtennis", "wikipedia": "https://en.wikipedia.org/wiki/Platform_tennis"},
    {"rank": 9, "sport": "Beach tennis", "governing_body": "International Tennis Federation (ITF)", "website": "https://www.itftennis.com/en/itf-tours/world-tennis-tour/beach-tennis/", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Beach_tennis"},
    {"rank": 10, "sport": "Paddle tennis", "governing_body": "International POP Tennis Association (POP Tennis)", "website": "", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Paddle_tennis"},
    {"rank": 11, "sport": "Basque pelota", "governing_body": "International Federation of Basque Pelota (FIPV)", "website": "https://www.fipv.net/en", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Basque_pelota"},
    {"rank": 12, "sport": "Chaza", "governing_body": "", "website": "", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Chaza"},
    {"rank": 13, "sport": "Downside ball game", "governing_body": "", "website": "", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Downside_ball_game"},
    {"rank": 14, "sport": "Four wall paddleball", "governing_body": "National Paddleball Association (NPA)", "website": "https://npa.paddleball.org/", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Four_wall_paddleball"},
    {"rank": 15, "sport": "Frescobol", "governing_body": "Confederação Brasileira de Frescobol (CBraF)", "website": "", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Frescobol"},
    {"rank": 16, "sport": "Hanetsuki", "governing_body": "", "website": "", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Hanetsuki"},
    {"rank": 17, "sport": "Jokari", "governing_body": "", "website": "", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Jokari"},
    {"rank": 18, "sport": "Jombola", "governing_body": "Jombola Association Malaysia (JAM)", "website": "https://www.jombola.org/", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Jombola"},
    {"rank": 19, "sport": "Matkot", "governing_body": "", "website": "", "twitter": "", "instagram": "https://www.instagram.com/matkotisrael", "wikipedia": "https://en.wikipedia.org/wiki/Matkot"},
    {"rank": 20, "sport": "Miniten", "governing_body": "", "website": "", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Miniten"},
    {"rank": 21, "sport": "One wall paddleball", "governing_body": "Paddleball Family Alliance (PFA)", "website": "https://paddleballfamily.com/", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/One_wall_paddleball"},
    {"rank": 22, "sport": "Paddle ball", "governing_body": "", "website": "", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Paddle_ball_(sport)"},
    {"rank": 23, "sport": "Paleta Frontón", "governing_body": "Federación Deportiva Peruana de Paleta Frontón", "website": "https://www.fedperufronton.com/", "twitter": "", "instagram": "https://www.instagram.com/fedperuanapaletafronton", "wikipedia": "https://en.wikipedia.org/wiki/Paleta_Frontón"},
    {"rank": 24, "sport": "Pang Pong", "governing_body": "", "website": "", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Pang_Pong"},
    {"rank": 25, "sport": "Pelota mixteca", "governing_body": "Federación Mexicana de Juegos y Deportes Autóctonos y Tradicionales", "website": "", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Pelota_mixteca"},
    {"rank": 26, "sport": "Road tennis", "governing_body": "Barbados Road Tennis Association (BRTA)", "website": "", "twitter": "", "instagram": "https://www.instagram.com/brta21", "wikipedia": "https://en.wikipedia.org/wiki/Road_tennis"},
    {"rank": 27, "sport": "Roliball", "governing_body": "Taiji Bailong Ball Federation (TBBA)", "website": "https://www.bailongball.com/", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Roliball"},
    {"rank": 28, "sport": "Sphairee", "governing_body": "", "website": "", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Sphairee"},
    {"rank": 29, "sport": "Stoolball", "governing_body": "Stoolball England", "website": "https://www.stoolball.org.uk/", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Stoolball"},
    {"rank": 30, "sport": "Table squash", "governing_body": "", "website": "", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Table_squash"},
    {"rank": 31, "sport": "Tamburello", "governing_body": "Federazione Italiana Palla Tamburello (FIPT)", "website": "https://www.federtamburello.it/", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Tamburello"},
    {"rank": 32, "sport": "Tambourelli", "governing_body": "Scottish Tambourelli", "website": "http://scottishtambourelli.blogspot.com/", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Tambourelli"},
    {"rank": 33, "sport": "Totem tennis", "governing_body": "", "website": "", "twitter": "", "instagram": "", "wikipedia": "https://en.wikipedia.org/wiki/Totem_tennis"},
]
