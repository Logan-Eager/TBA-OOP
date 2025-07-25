# TEXT BASED ADVENTURE. OOP. PYTHON PROGRAM #
#
# MAP OF GAME
#              #   #   #  #   #    #  #
#              #   moldy skeleton     #
#   #   #   #   #   #   #   ~   #   #   #    #  #
#   dense shrubs  /  cross roads  /   old tree  #
#   #   #   #   #   #   /   #   #   #   #   #   #
                #    deep forest    #
                #  #   #   /   #  # #
                  #     start      #
                  #   #   #    #   #

# MODULE IMPORT
import random
import os
# START OF CLASSES AND INITIALISING


# defines level class
class Level:
    def __init__(self):
        # defining variables
        self.level_name = None
        self.level_description = None
        self.level_gates = None
        self.level_items = None
        self.level_enemies = None

    #  defines level setup function, defines instances of level class
    def setup(self, level_name, level_gates, level_description, level_items, level_enemies):
        self.level_name = level_name  # defines name string for level
        self.level_gates = level_gates  # defines list of gates for level
        self.level_description = level_description  # defines description string for level
        self.level_items = level_items  # defines list of items in level
        self.level_enemies = level_enemies  # defines list of enemies in level

    # defines enter function, gives player info of area
    def enter(self):
        print(self.level_description)

        # for loop to print gate in player location
        if len(self.level_gates) >= 1:
            print("There are gates to:")
            for ga in self.level_gates:
                ga.print_gate()

        # for loop to print items for use in a for loop
        if len(self.level_items) >= 1:
            print("There is", end=" ")
            for i in self.level_items:
                i.print_item()

        if self.level_enemies:
            print("There is", end=" ")
            self.level_enemies.print_enemy()

    # removes item from level (for use in take function)
    def remove_item(self, item):
        self.level_items.remove(item)

    # adds item to level (for use in drop function)
    def add_item(self, item):
        self.level_items.append(item)

    # removes enemy from level
    def remove_enemy(self):
        self.level_enemies = None

    def add_enemy(self, level):
        self.level_enemies = level

# defines gate class
class Gate:

    def __init__(self, gate_direction, gate_to, locked, key):
        self.gate_to = gate_to  # defines the level the gate leads to
        self.gate_direction = gate_direction  # defines the direction the gate points to
        self.locked = locked  # defines a boolean for if the gate is locked
        self.key = key  # defines a string for what key is needed for lock


    # defines unlock function for locked gates
    def unlock(self, gate_list):
        success = False
        for i in gate_list:
            if self.key == i.item_name:
                self.locked = False
                print("You turn the key and the %s gate is blown open by a gust of wind."
                % self.gate_direction)
                success = True
        if not success and self.locked:
            print("You do not have the key for this door.")

    # returns locked boolean
    def is_locked(self):
        return self.locked

    # returns direction of gate
    def is_gate(self, text):
        return self.gate_direction in text

    # prints direction of gate
    def print_gate(self):
        print("the %s." % self.gate_direction)


# defines player class
class Player:
    player_damage = 45

    def __init__(self, player_name, player_level):
        self.player_health = 100  # defines player health as 100
        self.player_name = player_name  # defines players name
        self.player_location = player_level  # defines where the player is located
        self.inventory = []  # defines the players inventory

    # changes player location
    def move(self, player_level):
        self.player_location = player_level

    # adds items to player inventory and removes from level
    def take(self, take_user_input):
        for i in self.player_location.level_items:
            if i.item_name in take_user_input:
                self.inventory.append(i)
                print("you take a %s" % i.item_name)
                self.player_location.remove_item(i)
            else:
                print("?")

    # removes item from inventory and adds to level
    def drop(self, drop_user_input):
        success = False
        for i in self.inventory:
            if i.item_name in drop_user_input:
                self.inventory.remove(i)
                self.player_location.add_item(i)
                print("You drop the %s" % i.item_name)
                success = True
        if not success:
            print("?")

    # prints inventory
    def print_inventory(self):
        print("Your inventory: ")
        for i in self.inventory:
            print("%s," % i.item_name)

    # attack function, randomly wins or loses battle and apply damage to losing side
    def attack(self, enemy):
        if self.player_location.level_enemies != None:
            if random.randint(0, 5) == 1:
                self.player_take_damage(enemy)

            else:
                if(enemy.enemy_take_damage(the_player)) == "Death":
                    clear_terminal()
                    print("The " + enemy.enemy_name + " has died")
                    self.player_location.level_enemies = None
                    if enemy.enemy_name == "skeleton":
                        print("You have obtained victory. Sit with your actions.")

                        while True:
                            input()
        else:
            print("?")

    def player_take_damage(self, enemy):
        player_damage_messages = ["shin", "eye", "brain", "scrotum"]
        self.player_health = self.player_health - enemy.enemy_damage
        print("The %s" % enemy.enemy_name, "charges forward and your %s is injured"
              % random.choice(player_damage_messages))


# defines item class
class Item:

    def __init__(self, item_name):
        self.item_name = item_name  # defines items name

    # function called for use in a for loop to print item
    def print_item(self):
        print("a %s." % self.item_name)


class Enemy:

    def __init__(self, enemy_name, enemy_health, enemy_damage, enemy_spawn):
        self.enemy_name = enemy_name
        self.enemy_health = enemy_health
        self.enemy_damage = enemy_damage
        self.enemy_spawn = enemy_spawn

    def randomise_spawn(self, enemy_locations):
        random_spawn = random.choice(enemy_locations)
        self.enemy_spawn = random_spawn
        random_spawn.add_enemy(self)

    def print_enemy(self):
        print("a %s." % self.enemy_name)

    def enemy_take_damage(self, player):
        enemy_damage_messages = ["face", "abdomen", "knee", "butt crack"]
        self.enemy_health = self.enemy_health - player.player_damage
        print("You swing your sword and hit the %s in the" % self.enemy_name, 
        random.choice(enemy_damage_messages))
        print(f"You did {player.player_damage}. The enemy has {self.enemy_health} health left.")

        if self.enemy_health <= 0:
            return "Death"

def clear_terminal():
    if os.name == "nt":
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print("\033[2J\033[H", end="")

# defines commands in list for player viewing
commands = ["go 'compass-direction'", "look", "take 'item'", "inventory", "unlock 'gate-direction'", "attack 'enemy'", "press up-arrowkey to repeat last command"]

# initialises levels
start_area = Level()
deep_forest_area = Level()
cross_road_area = Level()
moldy_skeleton_area = Level()
dense_shrubs_area = Level()
old_tree_area = Level()



# initialises items
player_sword = Item("sword")
rusted_key = Item("rusted key")

# initialises enemies
skeleton = Enemy("skeleton", 100, 25, moldy_skeleton_area)

wolf = Enemy("wolf", 50, 15, None)

# start area setup
gate1 = Gate("north", deep_forest_area, False, "")
start_area.setup("forest", [gate1], "You are in a dusk lit forest surrounded by trees. "
                                    "The only direction is deeper into the forest.", 
                                    [], None)

# the level setup function is given a name variable, a list of gates in the level,
#  a description string and items list
# gates are given four variables, direction, where the gate goes to, if the
# gate is locked and what the gates key is
# deep forest area setup
gate1 = Gate("south", start_area, False, "")
gate2 = Gate("north", cross_road_area, False, "")
deep_forest_area.setup("deep forest", [gate1, gate2],
"You are in a seemingly endless tunnel of dark oak trees.", [],
                       None)

# cross road area setup
gate1 = Gate("south", deep_forest_area, False, "")
gate2 = Gate("north", moldy_skeleton_area, True, "rusted key")
gate3 = Gate("west", dense_shrubs_area, False, "")
gate4 = Gate("east", old_tree_area, False, "")
cross_road_area.setup("cross road area", [gate2, gate4, gate1, gate3], "You are at a crossroads. "
"The path spirals into three directions."
" It is suddenly dark. ", [], None)

gate1 = Gate("east", cross_road_area, False, "")
dense_shrubs_area.setup("dense shrubs area", [gate1], "You are in an area with dense shrubbery."
                                                      " The only direction is back", [], None)

gate1 = Gate("west", cross_road_area, False, "")
old_tree_area.setup("old tree area", [gate1],
                    "You see a large old tree. Something is hanging off a branch", [rusted_key], None)

gate1 = Gate("south", cross_road_area, False, "")
moldy_skeleton_area.setup("moldy skeleton area", [gate1],
"You reach an ancient burial grounds with a monolithic crypt infront of you", [], skeleton)
# defines list of spawn areas, used for enemies
enemy_spawn_areas = [deep_forest_area, cross_road_area, dense_shrubs_area, old_tree_area]
wolf.randomise_spawn(enemy_spawn_areas)

# END OF CLASSES AND INITIALISING

# START OF FUNCTIONS AND MAIN GAME LOOPS


# defines function to loop player for incorrect answers
def incorrect_answer_loop(answers):
    while True:
        user_input_for_loop = str.lower(input(">"))

        if user_input_for_loop in answers:
            clear_terminal()
            return user_input_for_loop

        else:
            print("?")
            continue


# defines function for players sword creation
def sword_sequence(player):
    # print functions will not be commented because they are straight forward

    print("You are offered a sword.\n")

    print("What type of sword. \n Options: katana, claymore, dagger")

    # puts player in loop to collect sword type
    player_sword.sword_type = incorrect_answer_loop({"katana", "claymore", "dagger"})

    print("Your sword type is:", player_sword.sword_type, "\n")

    print("What colour sword.")

    # puts player in loop to collect sword colour
    player_sword.colour = str.lower(input(">"))
    clear_terminal()

    print("Your sword colour is:", player_sword.colour, "\n")

    print("What damage type.\n Options: holy, blood, fire")

    # puts player in loop to collect damage type
    player_sword.damage_type = incorrect_answer_loop({"holy", "blood", "fire"})

    print("Your swords damage type is:", player_sword.damage_type)

    print("Your sword is finished.\n")
    input("(press enter to continue)")
    clear_terminal()
    player.inventory.append(player_sword)




# asks name and stores in player instance
print("What is your name.")
user_input = input(">")
the_player = Player(user_input, start_area)
clear_terminal()

# begins sword sequence (off for debugging)
sword_sequence(the_player)

# gives player information and area setting
print("(Cry help for commands)")
print(the_player.player_location.level_description)

# starts game loop
while user_input != "exit":

    while the_player.player_health > 0:
        # asks user for input and stores as lower case
        user_input = str.lower(input(">"))
        clear_terminal()

        # looks for direction in input and if the direction is valid, moves player in that direction
        for d in the_player.player_location.level_gates:
            if d.is_gate(user_input):
                if d.locked:
                    if "unlock" in user_input:
                        break
                    print("The gate rattles and doesnt budge.")

                elif the_player.player_location.level_enemies is not None:
                    print("Your pride wont let you.")

                else:
                    the_player.move(d.gate_to)
                    print(the_player.player_location.level_description)
                    if the_player.player_location.level_enemies is not None:
                        print("Lingering in the darkness is a " + the_player.player_location.level_enemies.enemy_name)

        # tells player the commands when asked
        if "help" in user_input:
            print("the commands are:")
            for command in commands:
                print("--> " + command)


        # gives player location information
        elif "look" in user_input:
            the_player.player_location.enter()

        # takes items from level and gives to player
        elif "take" in user_input:
            the_player.take(user_input)

        # prints inventory to player
        elif "inventory" in user_input:
            the_player.print_inventory()

        elif "unlock" in user_input:
            for g in the_player.player_location.level_gates:
                g.unlock(the_player.inventory)

        elif "attack" in user_input:
            the_player.attack(the_player.player_location.level_enemies)

    print("\n##GAME OVER##\n  (you suck)")
    input("press enter to perish.")
    break
