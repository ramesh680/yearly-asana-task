"""
Baked-in WNBA reference data: the 13 Women's National Basketball Association
teams of the 2025 season, ordered by final regular-season standing, with each
team's home city, arena, win-loss record, official website, social handles
(X/Twitter, Instagram, Facebook) and Wikipedia page.

Versioned yearly snapshot. The official WNBA site (wnba.com) is
JavaScript-rendered, so the team list and final standings are stored here and
refreshed each season. Las Vegas Aces won the 2025 WNBA Finals (third title);
the order below reflects the regular-season standings. Social accounts are
official team handles; blank where not verifiable. Wikipedia links are direct
article URLs.

Source: https://www.wnba.com/standings
"""

WNBA_EDITION = "2025 season"
WNBA_SOURCE_URL = "https://www.wnba.com/standings"

WNBA_TEAMS = [
    {"position": 1, "team": "Minnesota Lynx", "city": "Minneapolis, MN", "arena": "Target Center", "wins": 34, "losses": 10, "website": "https://lynx.wnba.com/", "twitter": "https://x.com/minnesotalynx", "instagram": "https://www.instagram.com/minnesotalynx", "facebook": "https://www.facebook.com/minnesotalynx", "wikipedia": "https://en.wikipedia.org/wiki/Minnesota_Lynx"},
    {"position": 2, "team": "Las Vegas Aces", "city": "Las Vegas, NV", "arena": "Michelob Ultra Arena", "wins": 30, "losses": 14, "website": "https://aces.wnba.com/", "twitter": "https://x.com/LVAces", "instagram": "https://www.instagram.com/lvaces", "facebook": "https://www.facebook.com/LVACES", "wikipedia": "https://en.wikipedia.org/wiki/Las_Vegas_Aces"},
    {"position": 3, "team": "Atlanta Dream", "city": "College Park, GA", "arena": "Gateway Center Arena", "wins": 30, "losses": 14, "website": "https://dream.wnba.com/", "twitter": "https://x.com/AtlantaDream", "instagram": "https://www.instagram.com/atlantadream", "facebook": "https://www.facebook.com/AtlantaDream", "wikipedia": "https://en.wikipedia.org/wiki/Atlanta_Dream"},
    {"position": 4, "team": "Phoenix Mercury", "city": "Phoenix, AZ", "arena": "PHX Arena", "wins": 27, "losses": 17, "website": "https://mercury.wnba.com/", "twitter": "https://x.com/PhoenixMercury", "instagram": "https://www.instagram.com/phoenixmercury", "facebook": "https://www.facebook.com/phoenixmercury", "wikipedia": "https://en.wikipedia.org/wiki/Phoenix_Mercury"},
    {"position": 5, "team": "New York Liberty", "city": "Brooklyn, NY", "arena": "Barclays Center", "wins": 27, "losses": 17, "website": "https://liberty.wnba.com/", "twitter": "https://x.com/nyliberty", "instagram": "https://www.instagram.com/nyliberty", "facebook": "", "wikipedia": "https://en.wikipedia.org/wiki/New_York_Liberty"},
    {"position": 6, "team": "Indiana Fever", "city": "Indianapolis, IN", "arena": "Gainbridge Fieldhouse", "wins": 24, "losses": 20, "website": "https://fever.wnba.com/", "twitter": "https://x.com/IndianaFever", "instagram": "https://www.instagram.com/indianafever", "facebook": "", "wikipedia": "https://en.wikipedia.org/wiki/Indiana_Fever"},
    {"position": 7, "team": "Seattle Storm", "city": "Seattle, WA", "arena": "Climate Pledge Arena", "wins": 23, "losses": 21, "website": "https://storm.wnba.com/", "twitter": "https://x.com/seattlestorm", "instagram": "https://www.instagram.com/seattlestorm", "facebook": "", "wikipedia": "https://en.wikipedia.org/wiki/Seattle_Storm"},
    {"position": 8, "team": "Golden State Valkyries", "city": "San Francisco, CA", "arena": "Chase Center", "wins": 23, "losses": 21, "website": "https://valkyries.wnba.com/", "twitter": "https://x.com/valkyries", "instagram": "https://www.instagram.com/valkyries", "facebook": "", "wikipedia": "https://en.wikipedia.org/wiki/Golden_State_Valkyries"},
    {"position": 9, "team": "Los Angeles Sparks", "city": "Los Angeles, CA", "arena": "Crypto.com Arena", "wins": 21, "losses": 23, "website": "https://sparks.wnba.com/", "twitter": "https://x.com/LASparks", "instagram": "https://www.instagram.com/la_sparks", "facebook": "", "wikipedia": "https://en.wikipedia.org/wiki/Los_Angeles_Sparks"},
    {"position": 10, "team": "Washington Mystics", "city": "Washington, D.C.", "arena": "CareFirst Arena", "wins": 16, "losses": 28, "website": "https://mystics.wnba.com/", "twitter": "https://x.com/WashMystics", "instagram": "https://www.instagram.com/washmystics", "facebook": "", "wikipedia": "https://en.wikipedia.org/wiki/Washington_Mystics"},
    {"position": 11, "team": "Connecticut Sun", "city": "Uncasville, CT", "arena": "Mohegan Sun Arena", "wins": 11, "losses": 33, "website": "https://sun.wnba.com/", "twitter": "https://x.com/ConnecticutSun", "instagram": "https://www.instagram.com/connecticutsun", "facebook": "", "wikipedia": "https://en.wikipedia.org/wiki/Connecticut_Sun"},
    {"position": 12, "team": "Chicago Sky", "city": "Chicago, IL", "arena": "Wintrust Arena", "wins": 10, "losses": 34, "website": "https://sky.wnba.com/", "twitter": "https://x.com/chicagosky", "instagram": "https://www.instagram.com/chicagosky", "facebook": "https://www.facebook.com/chicagosky", "wikipedia": "https://en.wikipedia.org/wiki/Chicago_Sky"},
    {"position": 13, "team": "Dallas Wings", "city": "Arlington, TX", "arena": "College Park Center", "wins": 10, "losses": 34, "website": "https://wings.wnba.com/", "twitter": "https://x.com/DWingsHoops", "instagram": "https://www.instagram.com/dallaswingsbasketball", "facebook": "", "wikipedia": "https://en.wikipedia.org/wiki/Dallas_Wings"},
]
