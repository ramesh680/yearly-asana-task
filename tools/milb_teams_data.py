"""Minor League Baseball - Triple-A clubs (30): International League + Pacific
Coast League, with MLB parent club. Source: mlb.com/milb / Wikipedia."""
MILB_EDITION = "Triple-A clubs (30)"
MILB_SOURCE_URL = "https://www.mlb.com/milb"
W="https://en.wikipedia.org/wiki/"
def _t(rank,team,league,parent,city,wiki):
    return {"rank":rank,"team":team,"league":league,"parent":parent,"city":city,"website":"","wikipedia":W+wiki}
MILB_TEAMS=[
 _t(1,"Buffalo Bisons","International League","Toronto Blue Jays","Buffalo, NY","Buffalo_Bisons"),
 _t(2,"Charlotte Knights","International League","Chicago White Sox","Charlotte, NC","Charlotte_Knights"),
 _t(3,"Columbus Clippers","International League","Cleveland Guardians","Columbus, OH","Columbus_Clippers"),
 _t(4,"Durham Bulls","International League","Tampa Bay Rays","Durham, NC","Durham_Bulls"),
 _t(5,"Gwinnett Stripers","International League","Atlanta Braves","Lawrenceville, GA","Gwinnett_Stripers"),
 _t(6,"Indianapolis Indians","International League","Pittsburgh Pirates","Indianapolis, IN","Indianapolis_Indians"),
 _t(7,"Iowa Cubs","International League","Chicago Cubs","Des Moines, IA","Iowa_Cubs"),
 _t(8,"Jacksonville Jumbo Shrimp","International League","Miami Marlins","Jacksonville, FL","Jacksonville_Jumbo_Shrimp"),
 _t(9,"Lehigh Valley IronPigs","International League","Philadelphia Phillies","Allentown, PA","Lehigh_Valley_IronPigs"),
 _t(10,"Louisville Bats","International League","Cincinnati Reds","Louisville, KY","Louisville_Bats"),
 _t(11,"Memphis Redbirds","International League","St. Louis Cardinals","Memphis, TN","Memphis_Redbirds"),
 _t(12,"Nashville Sounds","International League","Milwaukee Brewers","Nashville, TN","Nashville_Sounds"),
 _t(13,"Norfolk Tides","International League","Baltimore Orioles","Norfolk, VA","Norfolk_Tides"),
 _t(14,"Omaha Storm Chasers","International League","Kansas City Royals","Omaha, NE","Omaha_Storm_Chasers"),
 _t(15,"Rochester Red Wings","International League","Washington Nationals","Rochester, NY","Rochester_Red_Wings"),
 _t(16,"Scranton/Wilkes-Barre RailRiders","International League","New York Yankees","Moosic, PA","Scranton/Wilkes-Barre_RailRiders"),
 _t(17,"St. Paul Saints","International League","Minnesota Twins","St. Paul, MN","St._Paul_Saints"),
 _t(18,"Syracuse Mets","International League","New York Mets","Syracuse, NY","Syracuse_Mets"),
 _t(19,"Toledo Mud Hens","International League","Detroit Tigers","Toledo, OH","Toledo_Mud_Hens"),
 _t(20,"Worcester Red Sox","International League","Boston Red Sox","Worcester, MA","Worcester_Red_Sox"),
 _t(21,"Albuquerque Isotopes","Pacific Coast League","Colorado Rockies","Albuquerque, NM","Albuquerque_Isotopes"),
 _t(22,"El Paso Chihuahuas","Pacific Coast League","San Diego Padres","El Paso, TX","El_Paso_Chihuahuas"),
 _t(23,"Las Vegas Aviators","Pacific Coast League","Athletics","Las Vegas, NV","Las_Vegas_Aviators"),
 _t(24,"Oklahoma City Comets","Pacific Coast League","Los Angeles Dodgers","Oklahoma City, OK","Oklahoma_City_Comets"),
 _t(25,"Reno Aces","Pacific Coast League","Arizona Diamondbacks","Reno, NV","Reno_Aces"),
 _t(26,"Round Rock Express","Pacific Coast League","Texas Rangers","Round Rock, TX","Round_Rock_Express"),
 _t(27,"Sacramento River Cats","Pacific Coast League","San Francisco Giants","West Sacramento, CA","Sacramento_River_Cats"),
 _t(28,"Salt Lake Bees","Pacific Coast League","Los Angeles Angels","South Jordan, UT","Salt_Lake_Bees"),
 _t(29,"Sugar Land Space Cowboys","Pacific Coast League","Houston Astros","Sugar Land, TX","Sugar_Land_Space_Cowboys"),
 _t(30,"Tacoma Rainiers","Pacific Coast League","Seattle Mariners","Tacoma, WA","Tacoma_Rainiers"),
]
