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
    IMAGE = "Rock"
    SOLID = True

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    NAME = 'key'

    def interact(self, player):
        player.inventory.append(self.NAME)
        GAME_BOARD.draw_msg("You just acquired the KEY! You have %d items!" %(len(player.inventory)))
        print player.inventory

class DoorClosed(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True

    def interact(self, player):
        if 'key' in player.inventory and self.IMAGE == 'DoorClosed':
            self.change_image('DoorOpen')
            #self.SOLID = False 
            GAME_BOARD.draw_msg("HELLYA, DOOR IS OPEN!!!") 
        elif self.IMAGE == 'DoorOpen':
            self.SOLID = False
        else:
            GAME_BOARD.draw_msg("GO GET THE KEY!!!!!!!")

class Gem(GameElement):
    #IMAGE = "BlueGem"
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

class BlueGem(Gem):
    IMAGE = "BlueGem"


class Chest_Closed(GameElement):
    IMAGE = "Chest"
    SOLID = True


    def interact(self, player):
        if 'key' in player.inventory and self.IMAGE == 'Chest':
            self.change_image('Star')
            #self.SOLID = False 
            GAME_BOARD.draw_msg("Get the Star and finish the game!!!") 
        elif self.IMAGE == 'Star':
            self.SOLID = False
        else:
            GAME_BOARD.draw_msg("You don't have enough gems!!")

class EnemyBug(GameElement):
    IMAGE = 'EnemyBug'
    direction = 1

    def update(self, dt):

        next_x = self.x + self.direction

        if next_x < 0 or next_x >= self.board.width:
            self.direction *= -1
            next_x = self.x

        self.board.del_el(self.x, self.y)
        self.board.set_el(next_x, self.y, self)

class Character(GameElement):
    IMAGE = "Princess"

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

                if existing_el and existing_el.SOLID:
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
        (5, 7)
    ]
    walls = []
    for pos in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0], pos[1], wall)
        walls.append(wall)

    
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



