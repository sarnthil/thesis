import json

definition = """chinese+china,mexican,italian,indian+india,german,jewish,spanish,canadian+french can,japanease,asian,irish,caribbean,middle east,indonesian,vietnamese,polish,russian,british+english,hungarian+hungary,oriental,thai+thailand,greek,turkish,american+so. america+america+new orleans+new york,korean,european+west europe,african,morocan,swedish,hawaiian,israeli,filipino,french,french,australian,american+newyork+country wom+country"""

mapping = {}
for synonyms in definition.split(","):
    synonyms = synonyms.split("+")
    for syn in synonyms:
        mapping[syn] = synonyms[0]

with open("../stats/top_ingredients.txt") as f:
    top_ings = [line.strip() for line in f]

print("category",*top_ings, sep="\t")

with open("../NYC+categories.jsonl") as cf, open("../NYC+openrecipes_cleanv1.jsonl") as gf:
    for cline, gline in zip(cf, gf):
        recipe = json.loads(gline)
        categories = json.loads(cline)['categories']
        for cat in categories:
            if cat in mapping:
                category = mapping[cat]
                break
        else:
            continue
        ings = [x['name'] for x in recipe['ingredients']]
        print(category,*(int(x in ings) for x in top_ings), sep="\t")
