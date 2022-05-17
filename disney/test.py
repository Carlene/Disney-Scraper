albums_by_artist = {"Tyler The Creator" : ["Flower Boy", "Igor", "Call Me When You Get Lost"], 
                    "Tame Impala": ["Innervisions"],
                    "SZA": ["CTRL"],
                    "Beyonce": ["B'Day", "Beyonce", "Lemonade"]}

hotness_by_artist = {"Tyler The Creator": 5,
                    "Tame Impala": 5,
                    "SZA": 7,
                    "Beyonce": 9}

combined = {}
for artist in albums_by_artist:
    if artist in hotness_by_artist:
        combined[artist] = albums_by_artist[artist]
        combined[artist].append(hotness_by_artist[artist])
print(combined)