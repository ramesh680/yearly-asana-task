"""MLB teams (30), by league and division. Source: mlb.com / Wikipedia."""
MLB_EDITION = "30 teams (by league & division)"
MLB_SOURCE_URL = "https://www.mlb.com/"
W="https://en.wikipedia.org/wiki/"
def _t(rank,team,league,div,city,stadium,slug,wiki):
    return {"rank":rank,"team":team,"league":league,"division":div,"city":city,"stadium":stadium,
            "website":"https://www.mlb.com/%s"%slug,"wikipedia":W+wiki}
MLB_TEAMS=[
 _t(1,"Baltimore Orioles","AL","East","Baltimore, MD","Oriole Park at Camden Yards","orioles","Baltimore_Orioles"),
 _t(2,"Boston Red Sox","AL","East","Boston, MA","Fenway Park","redsox","Boston_Red_Sox"),
 _t(3,"New York Yankees","AL","East","Bronx, NY","Yankee Stadium","yankees","New_York_Yankees"),
 _t(4,"Tampa Bay Rays","AL","East","St. Petersburg, FL","Tropicana Field","rays","Tampa_Bay_Rays"),
 _t(5,"Toronto Blue Jays","AL","East","Toronto, ON","Rogers Centre","bluejays","Toronto_Blue_Jays"),
 _t(6,"Chicago White Sox","AL","Central","Chicago, IL","Rate Field","whitesox","Chicago_White_Sox"),
 _t(7,"Cleveland Guardians","AL","Central","Cleveland, OH","Progressive Field","guardians","Cleveland_Guardians"),
 _t(8,"Detroit Tigers","AL","Central","Detroit, MI","Comerica Park","tigers","Detroit_Tigers"),
 _t(9,"Kansas City Royals","AL","Central","Kansas City, MO","Kauffman Stadium","royals","Kansas_City_Royals"),
 _t(10,"Minnesota Twins","AL","Central","Minneapolis, MN","Target Field","twins","Minnesota_Twins"),
 _t(11,"Houston Astros","AL","West","Houston, TX","Daikin Park","astros","Houston_Astros"),
 _t(12,"Los Angeles Angels","AL","West","Anaheim, CA","Angel Stadium","angels","Los_Angeles_Angels"),
 _t(13,"Athletics","AL","West","West Sacramento, CA","Sutter Health Park","athletics","Athletics_(MLB_team)"),
 _t(14,"Seattle Mariners","AL","West","Seattle, WA","T-Mobile Park","mariners","Seattle_Mariners"),
 _t(15,"Texas Rangers","AL","West","Arlington, TX","Globe Life Field","rangers","Texas_Rangers_(baseball)"),
 _t(16,"Atlanta Braves","NL","East","Cumberland, GA","Truist Park","braves","Atlanta_Braves"),
 _t(17,"Miami Marlins","NL","East","Miami, FL","loanDepot park","marlins","Miami_Marlins"),
 _t(18,"New York Mets","NL","East","Queens, NY","Citi Field","mets","New_York_Mets"),
 _t(19,"Philadelphia Phillies","NL","East","Philadelphia, PA","Citizens Bank Park","phillies","Philadelphia_Phillies"),
 _t(20,"Washington Nationals","NL","East","Washington, D.C.","Nationals Park","nationals","Washington_Nationals"),
 _t(21,"Chicago Cubs","NL","Central","Chicago, IL","Wrigley Field","cubs","Chicago_Cubs"),
 _t(22,"Cincinnati Reds","NL","Central","Cincinnati, OH","Great American Ball Park","reds","Cincinnati_Reds"),
 _t(23,"Milwaukee Brewers","NL","Central","Milwaukee, WI","American Family Field","brewers","Milwaukee_Brewers"),
 _t(24,"Pittsburgh Pirates","NL","Central","Pittsburgh, PA","PNC Park","pirates","Pittsburgh_Pirates"),
 _t(25,"St. Louis Cardinals","NL","Central","St. Louis, MO","Busch Stadium","cardinals","St._Louis_Cardinals"),
 _t(26,"Arizona Diamondbacks","NL","West","Phoenix, AZ","Chase Field","dbacks","Arizona_Diamondbacks"),
 _t(27,"Colorado Rockies","NL","West","Denver, CO","Coors Field","rockies","Colorado_Rockies"),
 _t(28,"Los Angeles Dodgers","NL","West","Los Angeles, CA","Dodger Stadium","dodgers","Los_Angeles_Dodgers"),
 _t(29,"San Diego Padres","NL","West","San Diego, CA","Petco Park","padres","San_Diego_Padres"),
 _t(30,"San Francisco Giants","NL","West","San Francisco, CA","Oracle Park","giants","San_Francisco_Giants"),
]
