"""Professional golf tours. Source: golftours.com / Wikipedia (Professional golf tours)."""
GOLF_EDITION = "Major professional tours"
GOLF_SOURCE_URL = "https://en.wikipedia.org/wiki/Professional_golf_tours"
W="https://en.wikipedia.org/wiki/"
def _t(rank,tour,region,website,wiki):
    return {"rank":rank,"tour":tour,"region":region,"website":website,"wikipedia":W+wiki}
GOLF_TOURS=[
 _t(1,"PGA Tour","United States / Global","https://www.pgatour.com/","PGA_Tour"),
 _t(2,"LPGA Tour","United States / Global (women)","https://www.lpga.com/","LPGA"),
 _t(3,"DP World Tour","Europe / Global","https://www.europeantour.com/","European_Tour"),
 _t(4,"LIV Golf","Global","https://www.livgolf.com/","LIV_Golf"),
 _t(5,"PGA Tour Champions","United States (50+)","https://www.pgatour.com/champions","PGA_Tour_Champions"),
 _t(6,"Korn Ferry Tour","United States (developmental)","https://www.pgatour.com/korn-ferry-tour","Korn_Ferry_Tour"),
 _t(7,"Ladies European Tour","Europe (women)","https://ladieseuropeantour.com/","Ladies_European_Tour"),
 _t(8,"Japan Golf Tour","Japan","https://www.jgto.org/","Japan_Golf_Tour"),
 _t(9,"LPGA of Japan Tour","Japan (women)","https://www.lpga.or.jp/","LPGA_of_Japan_Tour"),
 _t(10,"Asian Tour","Asia","https://www.asiantour.com/","Asian_Tour"),
 _t(11,"Sunshine Tour","Southern Africa","https://sunshinetour.com/","Sunshine_Tour"),
 _t(12,"PGA Tour of Australasia","Australasia","https://pga.org.au/","PGA_Tour_of_Australasia"),
 _t(13,"Challenge Tour","Europe (developmental)","https://www.europeantour.com/challenge-tour/","Challenge_Tour"),
 _t(14,"Epson Tour","United States (women, developmental)","https://www.epsontour.com/","Epson_Tour"),
 _t(15,"PGA Tour Americas","Americas (developmental)","https://www.pgatour.com/pgatouramericas","PGA_Tour_Americas"),
 _t(16,"Legends Tour","Europe (seniors)","https://www.legendstour.com/","Legends_Tour_(European_Seniors)"),
]
