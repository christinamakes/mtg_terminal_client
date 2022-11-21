from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import pyfiglet
import requests
from clint.textui import puts, indent, colored


def main():
    """Main driver function"""
    hello_text = pyfiglet.figlet_format("Magic CLI", font="colossal", width=110)
    bye_text = pyfiglet.figlet_format("Goodbye", font="colossal", width=110)
    print(hello_text)
    print("** Welcome to the Magic the Gathering CLI Tool by CMoore")
    print("** Use this tool to find information about Magic the Gathering cards")
    print("** Use your arrow keys to get started\n")
    while True:
        action = actions()
        if action == "Search card by name":
            search_by_name()
        if action == None:
            break
    print(bye_text)
    quit()


def actions():
    """Default actions in main menu"""
    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Search card by name",
            "Find card set",
            "Show current most expensive cards",
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
    response = requests.get("https://api.scryfall.com/cards/named?fuzzy=" + c_name)
    result = response.json()
    rarity = result["rarity"]
    # print card info from request
    with indent(4, quote=(" |")):
        puts(colored.green(result["type_line"]))
        puts(colored.green(result["oracle_text"]))
        puts(colored.green(result["mana_cost"]))
        puts(colored.green(result["set_name"]))
        puts(colored.green(rarity.capitalize()))
        puts(colored.green(result["released_at"]))
    price = inquirer.confirm(
        message="Would you like to fetch the card price?", default=True
    ).execute()
    if price:
        prices = result["prices"]
        # Make sure price is listed and valid
        check_type = isinstance(prices["usd"], str)
        if check_type == True:
            with indent(4, quote=colored.cyan(" |")):
                puts(colored.green("$" + prices["usd"]))
        else:
            with indent(4, quote=colored.cyan(" |")):
                puts(colored.green("Price not listed"))


if __name__ == "__main__":
    main()
