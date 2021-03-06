import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
class Rock(GameElement):
    # Rocks are solid by default and have the image of rock
    IMAGE = "Rock"
    SOLID = True

class Tree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

class Wall(GameElement):
    # Walls are solid by defailt and have the image of a low wal
    IMAGE = "Wall"
    SOLID = True

class Key(GameElement):
    # keys have the key image and a the name of key and are not solid.
    # interact method allows keys to be picked up by player
    IMAGE = "Key"
    SOLID = False
    NAME = 'key'

    def interact(self, player):
        #adds the name of the key to the player's inventory
        player.inventory.append(self.NAME)
        GAME_BOARD.draw_msg("You just acquired the KEY! You have %d items!" %(len(player.inventory)))
        print player.inventory

class DoorClosed(GameElement):
    #doors have the image of a closed door and is solid by default.
    #after player gets the key the door finds the key, changes the image, and becomes not solid
    IMAGE = "DoorClosed"
    SOLID = True
    message = False

    def interact(self, player):
        if 'key' in player.inventory and self.IMAGE == 'DoorClosed':
            self.change_image('DoorOpen')
            GAME_BOARD.draw_msg("HELLYA, DOOR IS OPEN!!!")
            self.message = True 
            #print message
        elif self.IMAGE == 'DoorOpen':
            self.SOLID = False
        else:
            self.message = True
            #print message
            GAME_BOARD.draw_msg("GO GET THE KEY!!!!!!!")

class Gem(GameElement):
    #gems are not solid and are added to player inventory 
    #gems can be in 3 colors: blue, green, orange, and the gem color is determined
    #by the choose color method
    IMAGE = ''
    SOLID = False
    NAME = "gem"

    def choose_color(self, color):
        if color == "Orange":
            self.IMAGE = "OrangeGem"
        elif color == "Blue":
            self.IMAGE = 'BlueGem'
        elif color == 'Green':
            self.IMAGE = 'GreenGem'

    def interact(self, player):
        player.inventory.append(self.NAME)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" %(len(player.inventory)))
        print player.inventory

# this is another way to choose color, maybe we can refactor to include subclasses later
# class BlueGem(Gem):
#     IMAGE = "BlueGem"


class Chest_Closed(GameElement):
    #the closed chest works just like the door. When it opens, it reveals the star
    #which ends the game.
    IMAGE = "Chest"
    SOLID = True
    message = False

    def interact(self, player):
        self.message = True
        if 'gem' in player.inventory and self.IMAGE == 'Chest':
            self.change_image('Star') 
            GAME_BOARD.draw_msg("Get the Star and finish the game!!!") 
        elif self.IMAGE == 'Star':
            self.SOLID = False
            GAME_BOARD.draw_msg("Hooray! You WON!!!!!")
        else:
            GAME_BOARD.draw_msg("You don't have enough gems!!")

class EnemyBug(GameElement):
    # enemybug is a non player character which crawls across the middle of the board.
    IMAGE = 'EnemyBug'
    direction = 1
    message = False

    def update(self, dt):

        next_x = self.x + self.direction

        if next_x < 0 or next_x >= self.board.width:
            self.direction *= -1
            #next_x = self.x
        else:
            existing_el = self.board.get_el(next_x, self.y)
            #print self.x, self.y
            if existing_el:
                print existing_el
                self.interact(existing_el)
            if not existing_el or existing_el.SOLID == False:
                self.board.del_el(self.x, self.y)
                self.board.set_el(next_x, self.y, self)

    def interact(self, player):

        if 'gem' in player.inventory:
            self.message = True
            player.inventory.remove('gem')
            GAME_BOARD.draw_msg('The bug stole your gem! Sux for you.')
            self.direction *= -1
            #debugging code:
            print player.inventory
        else:
            GAME_BOARD.draw_msg('The bug ate you! GAME OVER!')
            self.message = True
            

class Character(GameElement):
    IMAGE = "Princess"
    SOLID = False 

    def next_pos(self, direction):
        if direction == 'up':
            return (self.x, self.y-1)
        elif direction == 'down':
            return (self.x, self.y+1)
        elif direction == 'left':
            return (self.x -1, self.y)
        elif direction == 'right':
            return (self.x +1, self.y)
        return None

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def keyboard_handler(self, symbol, modifier):
        direction = None
        if symbol == key.UP:
            #self.board.draw_msg('%s says: "You pressed up!"' % self.IMAGE)
            direction ='up'
        elif symbol == key.DOWN:
            #self.board.draw_msg('%s says: "You pressed down!"' % self.IMAGE)
            direction ='down'
        elif symbol == key.LEFT:
            #self.board.draw_msg('%s says: "You pressed left!"' % self.IMAGE)
            direction ='left'
        elif symbol == key.RIGHT:
            #self.board.draw_msg('%s says: "You pressed right!"' % self.IMAGE)
            direction ='right'
        elif symbol == key.SPACE:
            self.board.erase_msg()

        self.board.draw_msg('%s moves %s' % (self.IMAGE, direction)) 
        
        if direction:

 
            next_location = self.next_pos(direction)
            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]  

                if next_x < 0 or next_x >= GAME_WIDTH:
                    
                    next_x = next_x % GAME_WIDTH
                    #self.board.set_el(next_x, next_y, self)
                elif next_y < 0 or next_y >= GAME_HEIGHT:
                    next_y = next_y % GAME_HEIGHT
                    #self.board.set_el(next_x, next_y, self)

                existing_el = self.board.get_el(next_x, next_y)

                if existing_el:
                    existing_el.interact(self)

                #debugging code:

                # if existing_el.message:
                #     print existing_el.message

                if existing_el and existing_el.SOLID:
                    if hasattr(existing_el, "message"):
                        if existing_el.message == True:
                            pass
                    else:
                        self.board.draw_msg("There's something in my way!")
         

                elif existing_el is None or not existing_el.SOLID:
                    self.board.del_el(self.x, self.y)
                    self.board.set_el(next_x, next_y, self)

                #

                
               

            # if next_location:
            #     next_x = next_location[0]
            #     next_y = next_location[1]
            #     self.board.del_el(self.x, self.y)
            #     self.board.set_el(next_x, next_y, self)




####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    
    # Initialize and Register a whole bunch of rocks
    rock_positions = [
        (2,1),
        (1,2),
        (3,2),
        (0,6),
        (6,0),
        (2,3)
    ]

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False

    wall_positions = [
        (7, 5),
        (6, 5),
        (5, 5),
        (5, 7),
        (4, 2),
        (5, 2),
        (6, 2)
    ]
    walls = []
    for pos in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0], pos[1], wall)
        walls.append(wall)

    tree_positions = [
        (2,6),
        (2,5),
        (3,5),
        (3,6)

    ]

    trees = []
    for pos in tree_positions:
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        rocks.append(tree)


    
    doorclosed = DoorClosed()
    GAME_BOARD.register(doorclosed)
    GAME_BOARD.set_el(5,6, doorclosed)

    chestclosed = Chest_Closed()
    GAME_BOARD.register(chestclosed)
    GAME_BOARD.set_el(7,7, chestclosed)

    enemybug = EnemyBug()
    GAME_BOARD.register(enemybug)
    GAME_BOARD.set_el(0,4, enemybug)


    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(2, 2, player)
    print player

    GAME_BOARD.draw_msg("This game is wicked awesome. Because we're Bostonites")

    gem_positions = {
        (1,6): "Orange" ,
        (3,7): "Green",
        (3,1): "Blue",
        (7,3): "Orange"
    }

    gems = []
    for pos in gem_positions.keys():
        gem = Gem()
        gem.choose_color(gem_positions[pos])
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0], pos[1], gem)
        gems.append(gem)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(0,0, key)



