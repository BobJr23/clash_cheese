import requests

api_key = "key here"

headers = {
    "Accept": "application/json",
    "authorization": f"Bearer {api_key}",
}


def get_players(tag, player_name):
    members = []

    for x in tag:
        r = requests.get(
            f"https://proxy.royaleapi.dev/v1/clans/%23{x[1:]}/members",
            headers,
        ).json()
        for x in r["items"]:
            members.append(x)

    players = []
    if player_name != "all":
        lst = filter(lambda x: x["name"].lower().startswith(player_name[0]), members)
    else:
        lst = members
    for i, x in enumerate(lst):
        players.append(x["tag"])
        print(i, x["name"])
    name = input("Which one? ('n' if not present)\n> ")
    if "n" in name:
        return None
    else:
        return players[int(name)]


def get_clan(name, trophy):
    r = requests.get(
        f"https://proxy.royaleapi.dev/v1/clans?name={name}&limit=20",
        headers,
    ).json()
    lst = list(filter(lambda x: x["requiredTrophies"] <= trophy, r["items"]))
    tags = []
    print("Multi-select clan by separating numbers")
    for i, x in enumerate(lst):
        tags.append(x["tag"])
        print(
            i,
            x["tag"],
            x["name"],
            str(x["requiredTrophies"]),
        )
    numbers = input("Which clans?").split()

    clan = [tags[x] for x in map(lambda x: int(x), numbers)]

    return clan


def get_deck(tag):
    r = requests.get(
        f"https://proxy.royaleapi.dev/v1/players/%23{tag}/battlelog",
        headers,
    ).json()
    r2 = requests.get(
        f"https://proxy.royaleapi.dev/v1/players/%23{tag}",
        headers,
    ).json()

    deck2 = [x["name"] for x in r2["currentDeck"]]

    # l = r[0]["team"][0]["cards"]
    # print(r[0]["gameMode"]["name"] + "\n")
    # lst = [x["name"] for x in l]
    # print(lst)
    return deck2


def live(deck):
    order = ["unknown" for x in range(8)]
    while True:
        for i, x in enumerate(deck):
            print(i + 1, x)
        played = deck[int(input("Which card\n> ")) - 1]
        if played in order:
            order.remove(played)
            print("ye")
        else:
            order.remove("unknown")

        order.append(played)
        print(order[:4])


clan_tags = get_clan(
    input("What clan name?\n> "), int(input("What is the maximum trophy count?\n> "))
)
player_tag = None

while not player_tag:
    player_tag = get_players(
        clan_tags,
        input(
            "What is the player's first letter? ('all' to see full member list)\n> "
        ).lower(),
    )

player_tag = player_tag[1:]
print(player_tag)
deck = get_deck(player_tag)
live(deck)


# type
# battleTime
# isLadderTournament
# arena
# gameMode
# deckSelection
# team
# opponent
# isHostedMatch
