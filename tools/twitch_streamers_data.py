"""
Baked-in Top Twitch Streamers reference data: the top channels from
TwitchTracker's overall ranking, with each channel's 30-day average viewers,
all-time peak viewers, hours watched, Twitch channel link, social handles
(X/Twitter, YouTube) and Wikipedia page (where one exists).

TwitchTracker's "Overall Rank" blends average concurrent viewers, followers,
views and stream time over the trailing 30 days. The page is JavaScript-rendered
and the figures move daily, so this is a curated snapshot stored here and
refreshed periodically. Social accounts are official channels; blank where not
verifiable. Wikipedia links are direct article URLs.

Source: https://twitchtracker.com/channels/ranking
"""

TWITCH_EDITION = "30-day overall rank"
TWITCH_SOURCE_URL = "https://twitchtracker.com/channels/ranking"

TOP_TWITCH_STREAMERS = [
    {"position": 1, "channel": "Caedrel", "avg_viewers": 107082, "peak_viewers": 422292, "hours_watched": 7440422, "twitch": "https://www.twitch.tv/caedrel", "twitter": "https://x.com/Caedrel", "youtube": "https://www.youtube.com/caedrel", "wikipedia": "https://en.wikipedia.org/wiki/Caedrel"},
    {"position": 2, "channel": "LVNDMARK", "avg_viewers": 33201, "peak_viewers": 165048, "hours_watched": 9573493, "twitch": "https://www.twitch.tv/lvndmark", "twitter": "", "youtube": "", "wikipedia": ""},
    {"position": 3, "channel": "Pestily", "avg_viewers": 25597, "peak_viewers": 244422, "hours_watched": 8581828, "twitch": "https://www.twitch.tv/pestily", "twitter": "", "youtube": "https://www.youtube.com/c/pestily", "wikipedia": ""},
    {"position": 4, "channel": "加藤純一うん〇ちゃん", "avg_viewers": 34182, "peak_viewers": 292323, "hours_watched": 7490404, "twitch": "https://www.twitch.tv/kato_junichi0817", "twitter": "https://x.com/unkochan1234567", "youtube": "https://www.youtube.com/channel/UCZetZElUvdElPrcstRjl9DA", "wikipedia": "https://en.wikipedia.org/wiki/Junichi_Kato_(streamer)"},
    {"position": 5, "channel": "eliasn97", "avg_viewers": 32734, "peak_viewers": 207475, "hours_watched": 7351503, "twitch": "https://www.twitch.tv/eliasn97", "twitter": "", "youtube": "", "wikipedia": ""},
    {"position": 6, "channel": "zackrawrr", "avg_viewers": 38662, "peak_viewers": 309124, "hours_watched": 6779423, "twitch": "https://www.twitch.tv/zackrawrr", "twitter": "https://x.com/asmongold", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Asmongold"},
    {"position": 7, "channel": "BastiGHG", "avg_viewers": 23059, "peak_viewers": 81048, "hours_watched": 6993867, "twitch": "https://www.twitch.tv/bastighg", "twitter": "", "youtube": "https://www.youtube.com/channel/UCgZpwegd4AdDlZNrIamIgRw", "wikipedia": ""},
    {"position": 8, "channel": "Papaplatte", "avg_viewers": 30724, "peak_viewers": 120011, "hours_watched": 5996717, "twitch": "https://www.twitch.tv/papaplatte", "twitter": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Papaplatte"},
    {"position": 9, "channel": "caseoh_", "avg_viewers": 52284, "peak_viewers": 110574, "hours_watched": 4970454, "twitch": "https://www.twitch.tv/caseoh_", "twitter": "", "youtube": "https://www.youtube.com/channel/UC63anZxfVGHUEmfBAf5w7pw", "wikipedia": ""},
    {"position": 10, "channel": "shroud", "avg_viewers": 22160, "peak_viewers": 516289, "hours_watched": 6309992, "twitch": "https://www.twitch.tv/shroud", "twitter": "https://x.com/shroud", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Shroud_(gamer)"},
    {"position": 11, "channel": "TheBurntPeanut", "avg_viewers": 25255, "peak_viewers": 93043, "hours_watched": 5929120, "twitch": "https://www.twitch.tv/theburntpeanut", "twitter": "", "youtube": "https://www.youtube.com/@TheBurntPeanut", "wikipedia": ""},
    {"position": 12, "channel": "Jynxzi", "avg_viewers": 33053, "peak_viewers": 208375, "hours_watched": 5563945, "twitch": "https://www.twitch.tv/jynxzi", "twitter": "", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Jynxzi"},
    {"position": 13, "channel": "HasanAbi", "avg_viewers": 28766, "peak_viewers": 312431, "hours_watched": 5375477, "twitch": "https://www.twitch.tv/hasanabi", "twitter": "", "youtube": "https://www.youtube.com/channel/UCtoaZpBnrd0lhycxYJ4MNOQ", "wikipedia": "https://en.wikipedia.org/wiki/Hasan_Piker"},
    {"position": 14, "channel": "aminematue", "avg_viewers": 49943, "peak_viewers": 1155060, "hours_watched": 4301715, "twitch": "https://www.twitch.tv/aminematue", "twitter": "", "youtube": "https://www.youtube.com/channel/UCNigJTVnMU8F3n08pYz0UYw", "wikipedia": ""},
    {"position": 15, "channel": "k4sen", "avg_viewers": 23644, "peak_viewers": 148289, "hours_watched": 5096914, "twitch": "https://www.twitch.tv/k4sen", "twitter": "https://x.com/thek4sen", "youtube": "", "wikipedia": ""},
    {"position": 16, "channel": "Riot Games", "avg_viewers": 74195, "peak_viewers": 854781, "hours_watched": 2805805, "twitch": "https://www.twitch.tv/riotgames", "twitter": "https://x.com/riotgames", "youtube": "https://www.youtube.com/riotgames", "wikipedia": "https://en.wikipedia.org/wiki/Riot_Games"},
    {"position": 17, "channel": "ibai", "avg_viewers": 76251, "peak_viewers": 9189762, "hours_watched": 2493398, "twitch": "https://www.twitch.tv/ibai", "twitter": "https://x.com/IbaiLlanos", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/Ibai_Llanos"},
    {"position": 18, "channel": "summit1g", "avg_viewers": 13518, "peak_viewers": 310998, "hours_watched": 5011503, "twitch": "https://www.twitch.tv/summit1g", "twitter": "https://x.com/summit1g", "youtube": "https://www.youtube.com/summit1g", "wikipedia": "https://en.wikipedia.org/wiki/Summit1g"},
    {"position": 19, "channel": "fps_shaka", "avg_viewers": 17009, "peak_viewers": 125341, "hours_watched": 4584970, "twitch": "https://www.twitch.tv/fps_shaka", "twitter": "", "youtube": "", "wikipedia": ""},
    {"position": 20, "channel": "Rubius", "avg_viewers": 34709, "peak_viewers": 383747, "hours_watched": 3735235, "twitch": "https://www.twitch.tv/rubius", "twitter": "https://x.com/Rubiu5", "youtube": "https://www.youtube.com/user/elrubiusOMG", "wikipedia": "https://en.wikipedia.org/wiki/El_Rubius"},
    {"position": 21, "channel": "xQc", "avg_viewers": 19301, "peak_viewers": 278176, "hours_watched": 4201259, "twitch": "https://www.twitch.tv/xqc", "twitter": "https://x.com/xQc", "youtube": "https://www.youtube.com/channel/UCmDTrq0LNgPodDOFZiSbsww", "wikipedia": "https://en.wikipedia.org/wiki/XQc"},
    {"position": 22, "channel": "sasavot", "avg_viewers": 24685, "peak_viewers": 99873, "hours_watched": 3634011, "twitch": "https://www.twitch.tv/sasavot", "twitter": "", "youtube": "", "wikipedia": ""},
    {"position": 23, "channel": "auronplay", "avg_viewers": 41635, "peak_viewers": 602038, "hours_watched": 2872843, "twitch": "https://www.twitch.tv/auronplay", "twitter": "https://x.com/auronplay", "youtube": "", "wikipedia": "https://en.wikipedia.org/wiki/AuronPlay"},
    {"position": 24, "channel": "ohnePixel", "avg_viewers": 32463, "peak_viewers": 298362, "hours_watched": 2782580, "twitch": "https://www.twitch.tv/ohnepixel", "twitter": "https://x.com/ohnePixel", "youtube": "https://www.youtube.com/@ohnepixel", "wikipedia": "https://en.wikipedia.org/wiki/OhnePixel"},
    {"position": 25, "channel": "Tumblurr", "avg_viewers": 37904, "peak_viewers": 346842, "hours_watched": 2444148, "twitch": "https://www.twitch.tv/tumblurr", "twitter": "https://x.com/sdrogoblur", "youtube": "", "wikipedia": ""},
]
