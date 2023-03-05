"""
    Program: Role Playing Game
    Author: sina vahabi
    Copyright: 2023/02
"""


from GameClasses.game import Person, bcolors
from GameClasses.magic import Spell
from GameClasses.inventory import Item
import datetime
import random
import json
import sys
import os


index = 0
magic_choice = 0
current_date = datetime.datetime.now()
final_date = str(current_date)

# Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")


# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]


# Instantiate People
player1 = Person("Sina :", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Luci :", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Jerry:", 3089, 174, 288, 34, player_spells, player_items)

enemy1 = Person("M.M  ", 1250, 130, 560, 325, [], [])
enemy2 = Person("Tom  ", 18200, 701, 525, 25, [], [])
enemy3 = Person("Robot", 1250, 130, 560, 325, [], [])


players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print(bcolors.BOLD + bcolors.OKGREEN + "\"YOU CAN TYPE '0' TO QUIT BATTLE.\"" + bcolors.ENDC)
    print("======================")

    print("NAME                 HP                                     MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()

        while True:
            try:
                choice = int(input("    Choose action: "))
                if choice > 3:
                    print(bcolors.FAIL + '    Please just choose between 1, 2 or 3!' + bcolors.ENDC)
                    continue
                if choice < 0:
                    print(bcolors.FAIL + '    Please just choose between 1, 2 or 3!' + bcolors.ENDC)
                    continue
                if choice == 0:
                    print('GOODBYE.')
                    running = False
                index = int(choice) - 1
            except:
                print(bcolors.FAIL + '    You can only choose integer numbers!' + bcolors.ENDC)
                continue
            break

        if not running:
            sys.exit()

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            while True:
                try:
                    magic_choice = int(input("    Choose magic: "))
                    if magic_choice > 6:
                        print(bcolors.FAIL + '    Please just choose between 1 till 6!' + bcolors.ENDC)
                        continue
                    if magic_choice < 0:
                        print(bcolors.FAIL + '    Please just choose between 1 till 6!' + bcolors.ENDC)
                        continue
                    if magic_choice == 0:
                        print('GOODBYE.')
                        running = False

                    magic_choice = magic_choice - 1
                except:
                    print(bcolors.FAIL + '    You can only choose integer numbers!' + bcolors.ENDC)
                    continue
                break

            if not running:
                sys.exit()

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":

                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            while True:
                try:
                    item_choice = int(input("    Choose item: "))
                    if item_choice > 6:
                        print(bcolors.FAIL + '    Please just choose between 1 till 6!' + bcolors.ENDC)
                        continue
                    if item_choice < 0:
                        print(bcolors.FAIL + '    Please just choose between 1 till 6!' + bcolors.ENDC)
                        continue
                    if item_choice == 0:
                        print('GOODBYE.')
                        running = False
                    item_choice = item_choice - 1
                except:
                    print((bcolors.FAIL + '    You can only choose integer numbers!' + bcolors.ENDC))
                    continue
                break

            if not running:
                sys.exit()

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    # Check if battle is over.
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if Player won.
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        # Saving progress via jason.
        if os.path.isfile('./game.json') and os.stat('./game.json').st_size != 0:
            saved_file = open('./game.json', 'r+')
            data = json.loads(saved_file.read())
            data['exp'] += 25
            if 70 <= data['exp'] <= 100:
                data['level'] += data['level']
                print(bcolors.BOLD + bcolors.OKGREEN + 'CONGRATULATIONS, Your level has been upgraded to' +
                      str(data['level']) + bcolors.ENDC)
            print('YOUR CURRENT EXP IS:', data['exp'])
            if 150 <= data['exp'] <= 250:
                data['level'] += data['level']
                print(bcolors.BOLD + bcolors.OKGREEN + 'CONGRATULATIONS, Your level has been upgraded to' +
                      str(data['level']) + bcolors.ENDC)
            print('YOUR CURRENT EXP IS:', data['exp'])
            if 350 <= data['exp'] <= 500:
                data['level'] += data['level']
                print(bcolors.BOLD + bcolors.OKGREEN + 'CONGRATULATIONS, Your level has been upgraded to' +
                      str(data['level']) + bcolors.ENDC)
            print('YOUR CURRENT EXP IS:', data['exp'])
        else:
            saved_file = open('./game.json', 'w+')
            data = {'exp': 25, 'level': 0, 'win': 0, 'lose': 0, 'date': final_date[:16]}
            print('YOU HAVE EARNED', data['exp'])
        running = False
    # Check if Enemy won.
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        # Saving progress via jason.
        if os.path.isfile('./game.json') and os.stat('./game.json').st_size != 0:
            saved_file = open('./game.json', 'r+')
            data = json.loads(saved_file.read())
            data['exp'] += 10
            if 70 <= data['exp'] <= 100:
                data['level'] += data['level']
                print(bcolors.BOLD + bcolors.OKGREEN + 'CONGRATULATIONS, Your level has been upgraded to' +
                      str(data['level']) + bcolors.ENDC)
            print('YOUR CURRENT EXP IS:', data['exp'])
            if 150 <= data['exp'] <= 250:
                data['level'] += data['level']
                print(bcolors.BOLD + bcolors.OKGREEN + 'CONGRATULATIONS, Your level has been upgraded to' +
                      str(data['level']) + bcolors.ENDC)
            print('YOUR CURRENT EXP IS:', data['exp'])
            if 350 <= data['exp'] <= 500:
                data['level'] += data['level']
                print(bcolors.BOLD + bcolors.OKGREEN + 'CONGRATULATIONS, Your level has been upgraded to' +
                      str(data['level']) + bcolors.ENDC)
            print('YOUR CURRENT EXP IS:', data['exp'])
        else:
            saved_file = open('./game.json', 'w+')
            data = {'exp': 25, 'level': 0, 'win': 0, 'lose': 0, 'date': final_date[:16]}
            print('YOU HAVE EARNED', data['exp'])
        running = False

    print("\n")
    # Enemy attack phase.
    for enemy in enemies:
        # Chose attack.
        target = random.randrange(0, 3)
        enemy_dmg = enemy.generate_damage()

        players[target].take_damage(enemy_dmg)
        print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for", enemy_dmg)

        if players[target].get_hp() == 0:
            print(players[target].name.replace(" ", "") + " has died.")
            del players[target]
