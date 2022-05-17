from re import L


albums_by_artist = {"Tyler The Creator" : ["Flower Boy", "Igor", "Call Me When You Get Lost"], 
                    "Tame Impala": ["Innervisions"],
                    "SZA": ["CTRL"],
                    "Beyonce": ["B'Day", "Beyonce", "Lemonade"]}

hotness_by_artist = {"Tyler The Creator": 5,
                    "Tame Impala": 5,
                    "SZA": 7,
                    "Beyonce": 9}

def remove_flowers(item):
    if item.find("Flower") >= 0:
        i = item.find("Flower")
        new_item = item.replace(item[i : (i + len("Flower"))], "")
        return new_item
    else:
        return item

no_flowers = {}
l = []
for key, value in albums_by_artist.items():
    for v in value:
        new_v = remove_flowers(v)
        l.append(new_v)
    no_flowers[key] = l 
    l =[]
    
print(no_flowers)