"""Major video game consoles / platforms. Source: Wikipedia (Video game console)."""
VGPLAT_EDITION = "Major consoles & platforms"
VGPLAT_SOURCE_URL = "https://en.wikipedia.org/wiki/Video_game_console"
W="https://en.wikipedia.org/wiki/"
def _t(rank,name,maker,wiki):
    return {"rank":rank,"platform":name,"maker":maker,"website":"","wikipedia":W+wiki}
VG_PLATFORMS=[
 _t(1,"PlayStation 5","Sony","PlayStation_5"),
 _t(2,"Xbox Series X/S","Microsoft","Xbox_Series_X_and_Series_S"),
 _t(3,"Nintendo Switch 2","Nintendo","Nintendo_Switch_2"),
 _t(4,"Nintendo Switch","Nintendo","Nintendo_Switch"),
 _t(5,"PlayStation 4","Sony","PlayStation_4"),
 _t(6,"Xbox One","Microsoft","Xbox_One"),
 _t(7,"Steam Deck","Valve","Steam_Deck"),
 _t(8,"Wii","Nintendo","Wii"),
 _t(9,"Wii U","Nintendo","Wii_U"),
 _t(10,"Nintendo 3DS","Nintendo","Nintendo_3DS"),
 _t(11,"Nintendo DS","Nintendo","Nintendo_DS"),
 _t(12,"Game Boy","Nintendo","Game_Boy"),
 _t(13,"Nintendo Entertainment System","Nintendo","Nintendo_Entertainment_System"),
 _t(14,"Super Nintendo Entertainment System","Nintendo","Super_Nintendo_Entertainment_System"),
 _t(15,"Nintendo 64","Nintendo","Nintendo_64"),
 _t(16,"Nintendo GameCube","Nintendo","GameCube"),
 _t(17,"PlayStation (PS1)","Sony","PlayStation_(console)"),
 _t(18,"PlayStation 2","Sony","PlayStation_2"),
 _t(19,"PlayStation 3","Sony","PlayStation_3"),
 _t(20,"PlayStation Portable","Sony","PlayStation_Portable"),
 _t(21,"PlayStation Vita","Sony","PlayStation_Vita"),
 _t(22,"Xbox","Microsoft","Xbox_(console)"),
 _t(23,"Xbox 360","Microsoft","Xbox_360"),
 _t(24,"Sega Genesis","Sega","Sega_Genesis"),
 _t(25,"Sega Saturn","Sega","Sega_Saturn"),
 _t(26,"Sega Dreamcast","Sega","Dreamcast"),
 _t(27,"Atari 2600","Atari","Atari_2600"),
 _t(28,"TurboGrafx-16","NEC","TurboGrafx-16"),
 _t(29,"Neo Geo","SNK","Neo_Geo_(system)"),
 _t(30,"Steam (PC platform)","Valve","Steam_(service)"),
]
