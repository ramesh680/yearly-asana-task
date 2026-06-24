"""Serie A clubs (2025-26 season, 20). Source: legaseriea.it / Wikipedia."""
SERIEA_EDITION = "2025-26 season (20 clubs)"
SERIEA_SOURCE_URL = "https://en.wikipedia.org/wiki/2025%E2%80%9326_Serie_A"
W="https://en.wikipedia.org/wiki/"
def _t(rank,team,city,stadium,wiki):
    return {"rank":rank,"team":team,"city":city,"stadium":stadium,"website":"","wikipedia":W+wiki}
SERIEA_CLUBS=[
 _t(1,"Atalanta","Bergamo","Gewiss Stadium","Atalanta_BC"),
 _t(2,"Bologna","Bologna","Stadio Renato Dall'Ara","Bologna_FC_1909"),
 _t(3,"Cagliari","Cagliari","Unipol Domus","Cagliari_Calcio"),
 _t(4,"Como","Como","Stadio Giuseppe Sinigaglia","Como_1907"),
 _t(5,"Cremonese","Cremona","Stadio Giovanni Zini","U.S._Cremonese"),
 _t(6,"Fiorentina","Florence","Stadio Artemio Franchi","ACF_Fiorentina"),
 _t(7,"Genoa","Genoa","Stadio Luigi Ferraris","Genoa_CFC"),
 _t(8,"Inter Milan","Milan","San Siro","Inter_Milan"),
 _t(9,"Juventus","Turin","Allianz Stadium","Juventus_FC"),
 _t(10,"Lazio","Rome","Stadio Olimpico","S.S._Lazio"),
 _t(11,"Lecce","Lecce","Stadio Via del Mare","U.S._Lecce"),
 _t(12,"AC Milan","Milan","San Siro","AC_Milan"),
 _t(13,"Napoli","Naples","Stadio Diego Armando Maradona","SSC_Napoli"),
 _t(14,"Parma","Parma","Stadio Ennio Tardini","Parma_Calcio_1913"),
 _t(15,"Pisa","Pisa","Arena Garibaldi","Pisa_S.C."),
 _t(16,"Roma","Rome","Stadio Olimpico","AS_Roma"),
 _t(17,"Sassuolo","Reggio Emilia","Mapei Stadium","U.S._Sassuolo_Calcio"),
 _t(18,"Torino","Turin","Stadio Olimpico Grande Torino","Torino_FC"),
 _t(19,"Udinese","Udine","Bluenergy Stadium","Udinese_Calcio"),
 _t(20,"Hellas Verona","Verona","Stadio Marcantonio Bentegodi","Hellas_Verona_FC"),
]
