import sys
import requests
from bs4 import BeautifulSoup as Soup
from functools import partial
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
get = partial(requests.get, headers=headers, timeout=5)


def cookieandkate(sp, url):
    instructions = sp.find("div", {"class": "ERSInstructions"}).text
    return instructions

def allrecipes(sp, url):
    instructions = sp.find("ol", {"itemprop": "recipeInstructions"}).text
    return instructions

def smitten(sp, url):
    instruction = sp.find("div", {"class": "entry"}).text
    return instructions.split("Assembly")[1]

def tasty(sp, url):
    instructions = sp.find("span", {"itemprop": "instructions"}).text
    return instructions

def whatsgaby(sp, url):
    instructions = sp.find("ol", {"class": "instructions"}).text
    return instructions

def aspicy(sp, url):
    url = "http://www.aspicyperspective.com/" + url.split('/')[-1].split(".")[0] + "/2/"
    r = get(url)
    if r.status_code != 200:
        return None
    sp = Soup(r.text)
    try:
        instructions = sp.find("span", {"itemprop": "recipeInstructions"}).text
    except:
        return None
    return instructions

def bbc(sp, url):
    instructions = sp.find("ol", {"class": "recipe-method__list"}).text
    return instructions

def bbc2(sp, url):
    instructions = sp.find("div", {"class": "method"}).text
    return instructions

def biggirl(sp, url):
    instructions = sp.find("div", {"class": "ERSInstructions"}).text
    return instructions

def browney(sp, url):
    instructions = sp.find("div", {"class": "instructions"}).text
    return instructions

def bunycooks(sp, url):
    try:
        instructions = sp.find("span", {"itemprop": "recipeInstructions"}).text
    except AttributeError:
        url = url + '2/'
        r = get(url)
        sp = Soup(r.text)
        instructions = sp.find("span", {"itemprop": "recipeInstructions"}).text
    return instructions

def recipage(sp, url):
    return ''

def chow(sp, url):
    instructions = sp.find("div", {"itemprop": "recipeInstructions"}).text
    return instructions

def eatthelove(sp, url):
    instructions = sp.find("div", { "itemtype": "http://schema.org/Recipe"}).text
    return instructions.split("Directions")[1]

def elanas(sp, url):
    instructions = sp.find("div", {"class": "instructions"}).text
    return instructions

def epicurious(sp, url):
    instructions = sp.find("div", {"class": "instructions"}).text
    return instructions

def foodnet(sp, url):
    instructions = sp.find("ul", {"class": "recipe-directions-list"}).text
    return instructions

def jamie(sp, url):
    instructions = sp.find("div", {"itemprop": "recipeInstructions"}).text
    return instructions

def lovefood(sp, url):
    instructions = sp.find("ol", {"itemprop": "instructions"}).text
    return instructions

def serious(sp, url):
    instructions = sp.find("div", {"class": "recipe-procedures"}).text
    return instructions

def steamy(sp, url):
    instructions = sp.find("div", {"class": "directions"}).text
    return instructions

def little(sp, url):
    instructions = sp.find("span", {"itemprop": "recipeInstructions"}).text
    return instructions

def vintage(sp, url):
    instructions = sp.find("ol", {"id": "zlrecipe-instructions-list"}).text
    return instructions

def sonoma(sp, url):
    instructions = sp.find("div", {"class": "directions"}).text
    return instructions

def delish(sp, url):
    instructions = sp.find("div", {"class": "instructions"}).text
    return instructions

def naturallyella(sp, url):
    try:
        instructions = sp.find("div", {"class": "ERSInstructions"}).text
    except:
        return None
    return instructions

cookin = naturallyella

def pioneerwoman(sp, url):
    instructions = sp.find("span", {"itemprop": "recipeInstructions"}).text
    return instructions

def onehundredonecookbook(sp, url):
    instructions = sp.find("div", {"id": "recipe"}).text
    return instructions

def bonappetit(sp,url):
    instructions = sp.find("div", {"itemprop": "recipeInstructions"}).text
    return instructions

extractors = {
        'thepioneerwoman.com': pioneerwoman,
        '101cookbooks.com': onehundredonecookbook,
        'www.101cookbooks.com': onehundredonecookbook,
        'naturallyella.com': naturallyella,
        'delishhh.com': delish,
        'allrecipes.com': allrecipes,
        'cookieandkate.com': cookieandkate,
        'recipage.com':recipage,
        'smittenkitchen.com': smitten,
        'steamykitchen.com': steamy,
        'tastykitchen.com': tasty,
        'whatsgabycooking.com': whatsgaby,
        'www.aspicyperspective.com': aspicy,
        'www.bbc.co.uk': bbc,
        'www.bbcgoodfood.com': bbc2,
        'www.biggirlssmallkitchen.com': biggirl,
        'www.bonappetit.com': bonappetit,
        'www.browneyedbaker.com': browney,
        'www.bunkycooks.com': bunycooks,
        'www.chow.com': chow,
        'www.cookincanuck.com': cookin,
        'www.eatthelove.com': eatthelove,
        'www.elanaspantry.com': elanas,
        'www.epicurious.com': epicurious,
        'www.foodnetwork.com': foodnet,
        'www.jamieoliver.com': jamie,
        'www.lovefood.com': lovefood,
        'www.recipage.com': recipage,
        'www.seriouseats.com': serious,
        'www.steamykitchen.com': steamy,
        'www.thelittlekitchen.net': little,
        'www.thevintagemixer.com': vintage,
        'www.williams-sonoma.com': sonoma,
        }

