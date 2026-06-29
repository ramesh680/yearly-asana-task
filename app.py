# Add this TOOLS dictionary to your app.py

TOOLS = [
    # Healthcare
    {
        "title": "Best Hospitals (US)",
        "category": "Healthcare",
        "description": "Pulls the latest U.S. best-hospital lists from U.S. News & World Report and Newsweek/Statista, with each hospital's official website and social handles.",
        "endpoint": "best_hospitals",
        "available": True,
        "count": 5000
    },

    # Education
    {
        "title": "Best Colleges (US)",
        "category": "Education",
        "description": "U.S. News Best National Universities (Top 100, 2026), with each school's official website and social handles.",
        "endpoint": "best_colleges",
        "available": True,
        "count": 2500
    },

    # Finance
    {
        "title": "Russell 3000",
        "category": "Finance",
        "description": "All Russell 3000 constituents ranked by index weight with official data.",
        "endpoint": "russell_3000",
        "available": True,
        "count": 3000
    },

    # Sports - Basketball
    {
        "title": "Basketball (WNBA Teams)",
        "category": "Sports",
        "description": "WNBA teams with rosters, statistics, and social handles.",
        "endpoint": "basketball_wnba",
        "available": True,
        "count": 144
    },
    {
        "title": "Basketball (National Basketball Association)",
        "category": "Sports",
        "description": "NBA teams with rosters, statistics, and social handles.",
        "endpoint": "basketball_nba",
        "available": True,
        "count": 450
    },

    # Sports - Motorsport
    {
        "title": "Motorsport",
        "category": "Sports",
        "description": "Formula 1, IndyCar, and racing series data.",
        "endpoint": "motorsport",
        "available": True,
        "count": 850
    },

    # Sports - American Football
    {
        "title": "American Football",
        "category": "Sports",
        "description": "NFL teams with rosters, statistics, and official data.",
        "endpoint": "american_football",
        "available": True,
        "count": 500
    },

    # Sports - Racquet Sports
    {
        "title": "Racquet Sports",
        "category": "Sports",
        "description": "Tennis, badminton, and squash data.",
        "endpoint": "racquet_sports",
        "available": True,
        "count": 1200
    },

    # Sports - Golf
    {
        "title": "Golf",
        "category": "Sports",
        "description": "PGA Tour players, rankings, and tournament data.",
        "endpoint": "golf",
        "available": True,
        "count": 2000
    },

    # Sports - Ice Hockey
    {
        "title": "Ice Hockey",
        "category": "Sports",
        "description": "NHL teams, rosters, and statistics.",
        "endpoint": "ice_hockey",
        "available": True,
        "count": 700
    },

    # Sports - Soccer (Multiple Leagues)
    {
        "title": "Soccer (Major League Soccer)",
        "category": "Sports",
        "description": "MLS teams with rosters and statistics.",
        "endpoint": "soccer_mls",
        "available": True,
        "count": 360
    },
    {
        "title": "Soccer (National Women's Soccer League)",
        "category": "Sports",
        "description": "NWSL teams and player data.",
        "endpoint": "soccer_nwsl",
        "available": True,
        "count": 240
    },
    {
        "title": "Soccer (Brasileirão Série A)",
        "category": "Sports",
        "description": "Brazilian top division teams and data.",
        "endpoint": "soccer_brasileirao",
        "available": True,
        "count": 480
    },
    {
        "title": "Soccer (Bundesliga)",
        "category": "Sports",
        "description": "German Bundesliga teams and statistics.",
        "endpoint": "soccer_bundesliga",
        "available": True,
        "count": 550
    },
    {
        "title": "Soccer (LaLiga)",
        "category": "Sports",
        "description": "Spanish LaLiga teams and player data.",
        "endpoint": "soccer_laliga",
        "available": True,
        "count": 600
    },
    {
        "title": "Soccer (Serie A)",
        "category": "Sports",
        "description": "Italian Serie A teams and statistics.",
        "endpoint": "soccer_serie_a",
        "available": True,
        "count": 500
    },
    {
        "title": "Soccer (Ligue 1)",
        "category": "Sports",
        "description": "French Ligue 1 teams and player data.",
        "endpoint": "soccer_ligue_1",
        "available": True,
        "count": 480
    },

    # Sports - Baseball
    {
        "title": "Baseball (Major League Baseball)",
        "category": "Sports",
        "description": "MLB teams, rosters, and statistics.",
        "endpoint": "baseball_mlb",
        "available": True,
        "count": 1200
    },
    {
        "title": "Baseball (Minor League Baseball)",
        "category": "Sports",
        "description": "Minor league teams and player data.",
        "endpoint": "baseball_minors",
        "available": True,
        "count": 2500
    },

    # Sports - Combat Sports
    {
        "title": "Combat Sports",
        "category": "Sports",
        "description": "Boxing, MMA, and wrestling data.",
        "endpoint": "combat_sports",
        "available": True,
        "count": 3000
    },

    # Sports - Events
    {
        "title": "Sports Events",
        "category": "Sports",
        "description": "Major sports events and tournaments worldwide.",
        "endpoint": "sports_events",
        "available": True,
        "count": 1500
    },

    # Sports Business
    {
        "title": "Sports Business",
        "category": "Sports",
        "description": "Sports franchises, sponsorships, and industry data.",
        "endpoint": "sports_business",
        "available": True,
        "count": 5000
    },

    # Video Games
    {
        "title": "Video Games (Video Game Franchises)",
        "category": "Sports",
        "description": "Major video game franchises and their data.",
        "endpoint": "video_game_franchises",
        "available": True,
        "count": 3500
    },
    {
        "title": "Video Games (Video Game Platforms)",
        "category": "Sports",
        "description": "Gaming platforms, consoles, and their specifications.",
        "endpoint": "video_game_platforms",
        "available": True,
        "count": 150
    },
    {
        "title": "Video Games (Video Game Publishers)",
        "category": "Sports",
        "description": "Major video game publishers and studios worldwide.",
        "endpoint": "video_game_publishers",
        "available": True,
        "count": 2000
    },

    # Streaming
    {
        "title": "Top Twitch Streamers",
        "category": "Streaming",
        "description": "The top channels from TwitchTracker's rankings with viewership data.",
        "endpoint": "twitch_streamers",
        "available": True,
        "count": 10000
    },
]
