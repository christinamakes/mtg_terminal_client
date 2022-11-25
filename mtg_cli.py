from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import pyfiglet
import requests
from clint.textui import puts, indent, colored
from time import sleep
from random import random
from clint.textui import progress


def main():
    """Main driver function"""
    hello_text = pyfiglet.figlet_format("Magic CLI", font="colossal", width=110)
    bye_text = pyfiglet.figlet_format("Goodbye", font="colossal", width=110)
    print(hello_text)
    print("** Welcome to the Magic the Gathering CLI Tool by CMoore")
    print("** Use this tool to find information about Magic the Gathering cards")
    print("** Use your arrow keys to get started")
    while True:
        print("\n")
        action = actions()
        if action == "Search card by name":
            search_by_name()
        if action == "Explore Magic the Gathering":
            explore_MTG()
        if action == None:
            break
    print(bye_text)
    quit()


def mill():
    """mill progress bar"""
    with indent(2, quote=(" |")):
        puts(colored.blue("Fetching..."))
        for i in progress.mill(range(10)):
            sleep(random() * 0.2)


def actions():
    """Default actions in main menu"""
    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Search card by name",
            "Explore Magic the Gathering",
            "Generate random card name",
            Choice(value=None, name="Exit"),
        ],
        default="Search by card name",
    ).execute()
    return action


def search_by_name():
    """Search card by name with Scryfall API fuzzy name search"""
    c_name = inquirer.text(
        message="Enter card name:",
    ).execute()

    mill()

    response = requests.get("https://api.scryfall.com/cards/named?fuzzy=" + c_name)
    result = response.json()

    if result["object"] == "error":
        with indent(4, quote=(" |")):
            puts(colored.green("Card not found, please try another."))
    else:
        rarity = result["rarity"]
        # print card info from request
        with indent(2, quote=(" |")):
            puts(colored.green(result["name"]))
        with indent(4, quote=(" |")):
            puts(colored.green(result["type_line"]))
            puts(colored.green(result["oracle_text"]))
            puts(colored.green(result["mana_cost"]))
            puts(colored.green(result["set_name"]))
            puts(colored.green(rarity.capitalize()))
            puts(colored.green(result["released_at"]))
        price = inquirer.confirm(message="Fetch card price?", default=True).execute()
        if price:
            prices = result["prices"]
            # Make sure price is listed and valid
            check_type = isinstance(prices["usd"], str)
            if check_type == True:
                with indent(4, quote=(" |")):
                    puts(colored.green("$" + prices["usd"]))
            else:
                with indent(4, quote=(" |")):
                    puts(colored.green("Price not listed"))


def explore_MTG():
    action = inquirer.select(
        message="Choose category",
        choices=[
            "Land types",
            "Creature types",
            "Mana symbols",
            "Other symbols",
            "Unfinity symbols",
        ],
        default="Land types",
    ).execute()

    if action == "Land types":
        land()
    if action == "Creature types":
        creatures()
    if action == "Mana symbols":
        symbols(action)
    if action == "Other symbols":
        symbols(action)
    if action == "Unfinity symbols":
        symbols(action)


def land():
    """Search land types"""
    mill()

    response = requests.get("https://api.scryfall.com/catalog/land-types")
    result = response.json()

    for i in result["data"]:
        with indent(4, quote=(" |")):
            puts(colored.green(i))
    return


def creatures():
    """Search creature types"""

    mill()

    response = requests.get("https://api.scryfall.com/catalog/creature-types")
    result = response.json()

    items = result["total_values"]
    start = 0
    end = 13
    while end <= items:
        for i in range(start, end):
            if i != items:
                with indent(4, quote=(" |")):
                    puts(colored.green(result["data"][i]))
            else:
                break
        if end + 13 == items:
            break
        else:
            next_page = inquirer.confirm(message="Load more?", default=True).execute()
            if next_page == True:
                start += 13
                end += 13
            else:
                break
    return


def symbols(action):
    """Search MTG symbols"""

    mill()

    response = requests.get("https://api.scryfall.com/symbology")
    result = response.json()

    if action == "Mana symbols":
        for i in result["data"]:
            if i["represents_mana"] == True and i["funny"] == False:
                with indent(4, quote=(" |")):
                    symbol = i["symbol"]
                    english = i["english"]
                    puts(colored.green("%s - %s" % (symbol, english)))

    if action == "Other symbols":
        for i in result["data"]:
            if i["represents_mana"] == False and i["funny"] == False:
                with indent(4, quote=(" |")):
                    symbol = i["symbol"]
                    english = i["english"]
                    puts(colored.green("%s - %s" % (symbol, english)))

    if action == "Unfinity symbols":
        for i in result["data"]:
            if i["funny"] == True:
                with indent(4, quote=(" |")):
                    symbol = i["symbol"]
                    english = i["english"]
                    puts(colored.green("%s - %s" % (symbol, english)))
    return


if __name__ == "__main__":
    main()
