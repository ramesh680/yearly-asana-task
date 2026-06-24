"""Bundesliga clubs (2025-26 season, 18). Source: bundesliga.com / Wikipedia."""
BUNDESLIGA_EDITION = "2025-26 season (18 clubs)"
BUNDESLIGA_SOURCE_URL = "https://en.wikipedia.org/wiki/2025%E2%80%9326_Bundesliga"
W="https://en.wikipedia.org/wiki/"
def _t(rank,team,city,stadium,wiki):
    return {"rank":rank,"team":team,"city":city,"stadium":stadium,"website":"","wikipedia":W+wiki}
BUNDESLIGA_CLUBS=[
 _t(1,"Bayern Munich","Munich","Allianz Arena","FC_Bayern_Munich"),
 _t(2,"Bayer Leverkusen","Leverkusen","BayArena","Bayer_04_Leverkusen"),
 _t(3,"VfB Stuttgart","Stuttgart","MHPArena","VfB_Stuttgart"),
 _t(4,"RB Leipzig","Leipzig","Red Bull Arena","RB_Leipzig"),
 _t(5,"Borussia Dortmund","Dortmund","Signal Iduna Park","Borussia_Dortmund"),
 _t(6,"Eintracht Frankfurt","Frankfurt","Deutsche Bank Park","Eintracht_Frankfurt"),
 _t(7,"SC Freiburg","Freiburg","Europa-Park Stadion","SC_Freiburg"),
 _t(8,"FC Augsburg","Augsburg","WWK Arena","FC_Augsburg"),
 _t(9,"Werder Bremen","Bremen","Weserstadion","SV_Werder_Bremen"),
 _t(10,"VfL Wolfsburg","Wolfsburg","Volkswagen Arena","VfL_Wolfsburg"),
 _t(11,"Union Berlin","Berlin","Stadion An der Alten Försterei","1._FC_Union_Berlin"),
 _t(12,"Borussia Mönchengladbach","Mönchengladbach","Borussia-Park","Borussia_Mönchengladbach"),
 _t(13,"Mainz 05","Mainz","Mewa Arena","1._FSV_Mainz_05"),
 _t(14,"1. FC Heidenheim","Heidenheim","Voith-Arena","1._FC_Heidenheim"),
 _t(15,"FC St. Pauli","Hamburg","Millerntor-Stadion","FC_St._Pauli"),
 _t(16,"TSG Hoffenheim","Sinsheim","PreZero Arena","TSG_1899_Hoffenheim"),
 _t(17,"1. FC Köln","Cologne","RheinEnergieStadion","1._FC_Köln"),
 _t(18,"Hamburger SV","Hamburg","Volksparkstadion","Hamburger_SV"),
]
