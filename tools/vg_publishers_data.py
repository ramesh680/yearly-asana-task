"""Major video game publishers. Source: Wikipedia (Video game publisher)."""
VGPUB_EDITION = "Major publishers"
VGPUB_SOURCE_URL = "https://en.wikipedia.org/wiki/Video_game_publisher"
W="https://en.wikipedia.org/wiki/"
def _t(rank,name,hq,website,wiki):
    return {"rank":rank,"publisher":name,"hq":hq,"website":website,"wikipedia":W+wiki}
VG_PUBLISHERS=[
 _t(1,"Nintendo","Kyoto, Japan","https://www.nintendo.com/","Nintendo"),
 _t(2,"Sony Interactive Entertainment","San Mateo, USA","https://www.playstation.com/","Sony_Interactive_Entertainment"),
 _t(3,"Xbox Game Studios","Redmond, USA","https://www.xbox.com/","Xbox_Game_Studios"),
 _t(4,"Electronic Arts","Redwood City, USA","https://www.ea.com/","Electronic_Arts"),
 _t(5,"Activision Blizzard","Santa Monica, USA","https://www.activisionblizzard.com/","Activision_Blizzard"),
 _t(6,"Ubisoft","Montreuil, France","https://www.ubisoft.com/","Ubisoft"),
 _t(7,"Take-Two Interactive","New York, USA","https://www.take2games.com/","Take-Two_Interactive"),
 _t(8,"Rockstar Games","New York, USA","https://www.rockstargames.com/","Rockstar_Games"),
 _t(9,"Tencent Games","Shenzhen, China","https://www.tencent.com/","Tencent_Games"),
 _t(10,"Square Enix","Tokyo, Japan","https://www.square-enix.com/","Square_Enix"),
 _t(11,"Capcom","Osaka, Japan","https://www.capcom.com/","Capcom"),
 _t(12,"Bandai Namco Entertainment","Tokyo, Japan","https://www.bandainamcoent.com/","Bandai_Namco_Entertainment"),
 _t(13,"Sega","Tokyo, Japan","https://www.sega.com/","Sega"),
 _t(14,"Konami","Tokyo, Japan","https://www.konami.com/","Konami"),
 _t(15,"Epic Games","Cary, USA","https://www.epicgames.com/","Epic_Games"),
 _t(16,"Valve","Bellevue, USA","https://www.valvesoftware.com/","Valve_Corporation"),
 _t(17,"Embracer Group","Karlstad, Sweden","https://embracer.com/","Embracer_Group"),
 _t(18,"Warner Bros. Games","Burbank, USA","https://www.wbgames.com/","Warner_Bros._Games"),
 _t(19,"NetEase Games","Hangzhou, China","https://www.neteasegames.com/","NetEase"),
 _t(20,"Riot Games","Los Angeles, USA","https://www.riotgames.com/","Riot_Games"),
 _t(21,"Bethesda Softworks","Rockville, USA","https://bethesda.net/","Bethesda_Softworks"),
 _t(22,"Krafton","Seoul, South Korea","https://www.krafton.com/","Krafton"),
 _t(23,"HoYoverse","Shanghai, China","https://www.hoyoverse.com/","MiHoYo"),
 _t(24,"CD Projekt","Warsaw, Poland","https://www.cdprojekt.com/","CD_Projekt"),
 _t(25,"Paradox Interactive","Stockholm, Sweden","https://www.paradoxinteractive.com/","Paradox_Interactive"),
 _t(26,"Devolver Digital","Austin, USA","https://www.devolverdigital.com/","Devolver_Digital"),
 _t(27,"Nexon","Tokyo, Japan","https://www.nexon.com/","Nexon"),
 _t(28,"Roblox Corporation","San Mateo, USA","https://www.roblox.com/","Roblox_Corporation"),
 _t(29,"Supercell","Helsinki, Finland","https://supercell.com/","Supercell"),
 _t(30,"Gearbox Publishing","Frisco, USA","https://www.gearboxpublishing.com/","Gearbox_Software"),
 _t(31,"2K","Novato, USA","https://2k.com/","2K_(company)"),
 _t(32,"Annapurna Interactive","Los Angeles, USA","https://annapurna.com/games","Annapurna_Interactive"),
 _t(33,"Focus Entertainment","Paris, France","https://www.focus-entmt.com/","Focus_Entertainment"),
 _t(34,"Sega of America","Irvine, USA","https://www.sega.com/","Sega_of_America"),
 _t(35,"miHoYo","Shanghai, China","https://www.mihoyo.com/","MiHoYo"),
]
