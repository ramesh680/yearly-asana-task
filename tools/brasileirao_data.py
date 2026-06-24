"""Campeonato Brasileiro Série A clubs (2025 season, 20). Source: Wikipedia / CBF."""
BRASILEIRAO_EDITION = "2025 season (20 clubs)"
BRASILEIRAO_SOURCE_URL = "https://en.wikipedia.org/wiki/2025_Campeonato_Brasileiro_S%C3%A9rie_A"
W="https://en.wikipedia.org/wiki/"
def _t(rank,team,city,stadium,wiki):
    return {"rank":rank,"team":team,"city":city,"stadium":stadium,"website":"","wikipedia":W+wiki}
BRASILEIRAO_CLUBS=[
 _t(1,"Flamengo","Rio de Janeiro","Maracanã","Clube_de_Regatas_do_Flamengo"),
 _t(2,"Palmeiras","São Paulo","Allianz Parque","Sociedade_Esportiva_Palmeiras"),
 _t(3,"Botafogo","Rio de Janeiro","Estádio Nilton Santos","Botafogo_de_Futebol_e_Regatas"),
 _t(4,"Cruzeiro","Belo Horizonte","Mineirão","Cruzeiro_Esporte_Clube"),
 _t(5,"Fluminense","Rio de Janeiro","Maracanã","Fluminense_FC"),
 _t(6,"São Paulo","São Paulo","Morumbis","São_Paulo_FC"),
 _t(7,"Internacional","Porto Alegre","Beira-Rio","Sport_Club_Internacional"),
 _t(8,"Corinthians","São Paulo","Neo Química Arena","Sport_Club_Corinthians_Paulista"),
 _t(9,"Fortaleza","Fortaleza","Arena Castelão","Fortaleza_Esporte_Clube"),
 _t(10,"Bahia","Salvador","Arena Fonte Nova","Esporte_Clube_Bahia"),
 _t(11,"Atlético Mineiro","Belo Horizonte","Arena MRV","Clube_Atlético_Mineiro"),
 _t(12,"Grêmio","Porto Alegre","Arena do Grêmio","Grêmio_Foot-Ball_Porto_Alegrense"),
 _t(13,"Vasco da Gama","Rio de Janeiro","São Januário","CR_Vasco_da_Gama"),
 _t(14,"Red Bull Bragantino","Bragança Paulista","Estádio Nabi Abi Chedid","Red_Bull_Bragantino"),
 _t(15,"Vitória","Salvador","Barradão","Esporte_Clube_Vitória"),
 _t(16,"Juventude","Caxias do Sul","Alfredo Jaconi","Esporte_Clube_Juventude"),
 _t(17,"Santos","Santos","Vila Belmiro","Santos_FC"),
 _t(18,"Mirassol","Mirassol","Estádio José Maria de Campos Maia","Mirassol_Futebol_Clube"),
 _t(19,"Ceará","Fortaleza","Arena Castelão","Ceará_Sporting_Club"),
 _t(20,"Sport Recife","Recife","Ilha do Retiro","Sport_Club_do_Recife"),
]
