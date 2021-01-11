import requests

import config as cfg


def send_request():
    r = requests.get(cfg.HOST + cfg.HEROES_ENDPOINT)
    return r.json()


def main():
    heroes = send_request()
    print("{0:<5} {1:<20}".format("ID", "HERO NAME"))

    for hero in heroes:
        print("{0:<5} {1:<20}".format(hero["id"], hero["localized_name"]))


if __name__ == "__main__":
    main()
