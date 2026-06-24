"""NHL teams (32), by conference and division. Source: nhl.com / Wikipedia."""
NHL_EDITION = "32 teams (by conference & division)"
NHL_SOURCE_URL = "https://www.nhl.com/"
W="https://en.wikipedia.org/wiki/"
def _t(rank,team,conf,div,city,arena,slug,wiki):
    return {"rank":rank,"team":team,"conference":conf,"division":div,"city":city,"arena":arena,
            "website":"https://www.nhl.com/%s"%slug,"wikipedia":W+wiki}
NHL_TEAMS=[
 _t(1,"Boston Bruins","Eastern","Atlantic","Boston, MA","TD Garden","bruins","Boston_Bruins"),
 _t(2,"Buffalo Sabres","Eastern","Atlantic","Buffalo, NY","KeyBank Center","sabres","Buffalo_Sabres"),
 _t(3,"Detroit Red Wings","Eastern","Atlantic","Detroit, MI","Little Caesars Arena","redwings","Detroit_Red_Wings"),
 _t(4,"Florida Panthers","Eastern","Atlantic","Sunrise, FL","Amerant Bank Arena","panthers","Florida_Panthers"),
 _t(5,"Montreal Canadiens","Eastern","Atlantic","Montreal, QC","Bell Centre","canadiens","Montreal_Canadiens"),
 _t(6,"Ottawa Senators","Eastern","Atlantic","Ottawa, ON","Canadian Tire Centre","senators","Ottawa_Senators"),
 _t(7,"Tampa Bay Lightning","Eastern","Atlantic","Tampa, FL","Amalie Arena","lightning","Tampa_Bay_Lightning"),
 _t(8,"Toronto Maple Leafs","Eastern","Atlantic","Toronto, ON","Scotiabank Arena","mapleleafs","Toronto_Maple_Leafs"),
 _t(9,"Carolina Hurricanes","Eastern","Metropolitan","Raleigh, NC","Lenovo Center","hurricanes","Carolina_Hurricanes"),
 _t(10,"Columbus Blue Jackets","Eastern","Metropolitan","Columbus, OH","Nationwide Arena","bluejackets","Columbus_Blue_Jackets"),
 _t(11,"New Jersey Devils","Eastern","Metropolitan","Newark, NJ","Prudential Center","devils","New_Jersey_Devils"),
 _t(12,"New York Islanders","Eastern","Metropolitan","Elmont, NY","UBS Arena","islanders","New_York_Islanders"),
 _t(13,"New York Rangers","Eastern","Metropolitan","New York, NY","Madison Square Garden","rangers","New_York_Rangers"),
 _t(14,"Philadelphia Flyers","Eastern","Metropolitan","Philadelphia, PA","Wells Fargo Center","flyers","Philadelphia_Flyers"),
 _t(15,"Pittsburgh Penguins","Eastern","Metropolitan","Pittsburgh, PA","PPG Paints Arena","penguins","Pittsburgh_Penguins"),
 _t(16,"Washington Capitals","Eastern","Metropolitan","Washington, D.C.","Capital One Arena","capitals","Washington_Capitals"),
 _t(17,"Chicago Blackhawks","Western","Central","Chicago, IL","United Center","blackhawks","Chicago_Blackhawks"),
 _t(18,"Colorado Avalanche","Western","Central","Denver, CO","Ball Arena","avalanche","Colorado_Avalanche"),
 _t(19,"Dallas Stars","Western","Central","Dallas, TX","American Airlines Center","stars","Dallas_Stars"),
 _t(20,"Minnesota Wild","Western","Central","Saint Paul, MN","Grand Casino Arena","wild","Minnesota_Wild"),
 _t(21,"Nashville Predators","Western","Central","Nashville, TN","Bridgestone Arena","predators","Nashville_Predators"),
 _t(22,"St. Louis Blues","Western","Central","St. Louis, MO","Enterprise Center","blues","St._Louis_Blues"),
 _t(23,"Utah Mammoth","Western","Central","Salt Lake City, UT","Delta Center","utah","Utah_Mammoth"),
 _t(24,"Winnipeg Jets","Western","Central","Winnipeg, MB","Canada Life Centre","jets","Winnipeg_Jets"),
 _t(25,"Anaheim Ducks","Western","Pacific","Anaheim, CA","Honda Center","ducks","Anaheim_Ducks"),
 _t(26,"Calgary Flames","Western","Pacific","Calgary, AB","Scotiabank Saddledome","flames","Calgary_Flames"),
 _t(27,"Edmonton Oilers","Western","Pacific","Edmonton, AB","Rogers Place","oilers","Edmonton_Oilers"),
 _t(28,"Los Angeles Kings","Western","Pacific","Los Angeles, CA","Crypto.com Arena","kings","Los_Angeles_Kings"),
 _t(29,"San Jose Sharks","Western","Pacific","San Jose, CA","SAP Center","sharks","San_Jose_Sharks"),
 _t(30,"Seattle Kraken","Western","Pacific","Seattle, WA","Climate Pledge Arena","kraken","Seattle_Kraken"),
 _t(31,"Vancouver Canucks","Western","Pacific","Vancouver, BC","Rogers Arena","canucks","Vancouver_Canucks"),
 _t(32,"Vegas Golden Knights","Western","Pacific","Paradise, NV","T-Mobile Arena","goldenknights","Vegas_Golden_Knights"),
]
