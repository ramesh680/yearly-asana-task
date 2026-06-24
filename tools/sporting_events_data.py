"""Biggest sporting events, ranked by popularity. Sources: Bleacher Report /
Topend Sports 'biggest events' lists."""
EVENTS_EDITION = "Biggest global sporting events"
EVENTS_SOURCE_URL = "https://www.topendsports.com/world/lists/must-see-events/top100.htm"
W="https://en.wikipedia.org/wiki/"
def _t(rank,event,sport,website,wiki):
    return {"rank":rank,"event":event,"sport":sport,"website":website,"wikipedia":W+wiki}
SPORTING_EVENTS=[
 _t(1,"Summer Olympic Games","Multi-sport","https://www.olympics.com/","Summer_Olympic_Games"),
 _t(2,"FIFA World Cup","Football","https://www.fifa.com/en/tournaments/mens/worldcup","FIFA_World_Cup"),
 _t(3,"Super Bowl","American football","https://www.nfl.com/super-bowl/","Super_Bowl"),
 _t(4,"UEFA Champions League","Football","https://www.uefa.com/uefachampionsleague/","UEFA_Champions_League"),
 _t(5,"Winter Olympic Games","Multi-sport","https://www.olympics.com/","Winter_Olympic_Games"),
 _t(6,"ICC Cricket World Cup","Cricket","https://www.icc-cricket.com/","Cricket_World_Cup"),
 _t(7,"UEFA European Championship","Football","https://www.uefa.com/uefaeuro/","UEFA_European_Championship"),
 _t(8,"Rugby World Cup","Rugby union","https://www.rugbyworldcup.com/","Rugby_World_Cup"),
 _t(9,"Tour de France","Cycling","https://www.letour.fr/en/","Tour_de_France"),
 _t(10,"Wimbledon","Tennis","https://www.wimbledon.com/","The_Championships,_Wimbledon"),
 _t(11,"The Masters","Golf","https://www.masters.com/","Masters_Tournament"),
 _t(12,"Formula 1 Monaco Grand Prix","Motorsport","https://www.formula1.com/","Monaco_Grand_Prix"),
 _t(13,"Indianapolis 500","Motorsport","https://www.indianapolismotorspeedway.com/","Indianapolis_500"),
 _t(14,"Kentucky Derby","Horse racing","https://www.kentuckyderby.com/","Kentucky_Derby"),
 _t(15,"World Series","Baseball","https://www.mlb.com/world-series","World_Series"),
 _t(16,"NBA Finals","Basketball","https://www.nba.com/playoffs","NBA_Finals"),
 _t(17,"Stanley Cup Finals","Ice hockey","https://www.nhl.com/","Stanley_Cup_Finals"),
 _t(18,"Daytona 500","Motorsport","https://www.daytonainternationalspeedway.com/","Daytona_500"),
 _t(19,"The Open Championship","Golf","https://www.theopen.com/","The_Open_Championship"),
 _t(20,"US Open (tennis)","Tennis","https://www.usopen.org/","US_Open_(tennis)"),
 _t(21,"French Open","Tennis","https://www.rolandgarros.com/","French_Open"),
 _t(22,"Australian Open","Tennis","https://ausopen.com/","Australian_Open"),
 _t(23,"Commonwealth Games","Multi-sport","https://www.thecgf.com/","Commonwealth_Games"),
 _t(24,"ICC T20 World Cup","Cricket","https://www.icc-cricket.com/","ICC_Men's_T20_World_Cup"),
 _t(25,"Indian Premier League","Cricket","https://www.iplt20.com/","Indian_Premier_League"),
 _t(26,"Ryder Cup","Golf","https://www.rydercup.com/","Ryder_Cup"),
 _t(27,"FIFA Women's World Cup","Football","https://www.fifa.com/en/tournaments/womens/worldcup","FIFA_Women's_World_Cup"),
 _t(28,"NCAA March Madness","Basketball","https://www.ncaa.com/march-madness","NCAA_Division_I_men's_basketball_tournament"),
 _t(29,"College Football Playoff","American football","https://collegefootballplayoff.com/","College_Football_Playoff"),
 _t(30,"The Boat Race","Rowing","https://www.theboatrace.org/","The_Boat_Race"),
]
