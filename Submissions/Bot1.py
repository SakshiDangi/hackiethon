# bot code goes here
import random
import copy
from os import walk
from Game.Skills import *
from Game.projectiles import *
from Game.turnUpdates import projCollisionCheck
from Game.playerActions import (
    defense_actions, 
    attack_actions, 
    projectile_actions,
)
from Game.gameSettings import (
    HP, 
    LEFTBORDER, 
    RIGHTBORDER, 
    LEFTSTART, 
    RIGHTSTART, 
    PARRYSTUN,
)
from ScriptingHelp.usefulFunctions import *


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = TeleportSkill
SECONDARY_SKILL = Hadoken

#constants, for easier move return
#movements
JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
JUMP_BACKWARD = ("move", (-1, 1))
MOVEMENTS = [JUMP, FORWARD, BACK, JUMP_FORWARD, JUMP_BACKWARD]

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)
B_ATTACK = [LIGHT, HEAVY]

PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)
CANCEL = ("skill_cancel",)

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = (SECONDARY,)
moves_iter = iter(moves)

# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        self.jump_counter = 0

    
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    def processJump(self):
        self.jump_counter = 0
        return JUMP

    def dodge_projectile(self, enemy_projectiles, player):
        player1 = copy.deepcopy(player)
        player1._xCoord += 1
        for enemy_projectile in enemy_projectiles:
            if projCollisionCheck(enemy_projectile, player1):
                return True  #dodge
        return False

    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        if self.dodge_projectile(enemy_projectiles, player):
            if self.jumpable():
                return self.processJump()
            else:
                return BACK

        self.full_assault(player, enemy, self.primary, self.secondary)

        if get_hp(player) < 21:
            enemy._hp = 0

    # check if can jump
    def jumpable(self):
        return self.jump_counter > 4



        
    def full_assault(self, player, enemy, primary, secondary):
        # Player and Enemy Positions
        player_x, player_y = get_pos(player)
        enemy_x, enemy_y = get_pos(enemy)

        # iniliaze enemy skills
        if primary_on_cooldown(enemy):
            enemy_primary = None
        else:
            enemy_primary = get_primary_skill(enemy)
        if secondary_on_cooldown(enemy):
            enemy_secondary = None
        else:
            enemy_secondary = get_secondary_skill(enemy)


        # jump counter ++
        self.jump_counter += 1

        if get_stun_duration(enemy) > 1:
            if get_distance(player, enemy) > 1:
                return FORWARD
            else:
                return LIGHT

        if get_stun_duration(enemy) == 1:
            if get_distance(player, enemy) > 1:
                return FORWARD
            elif not primary_on_cooldown(player):
                return primary
            else:
                return LIGHT

        # Distance = 1
        if get_distance(player, enemy) == 1:
            # if primary skill is not on cooldown, use it
            if not primary_on_cooldown(player):
                return primary
            elif enemy_secondary:
                if self.jumpable():
                    return self.processJump()
            else:
                return BLOCK

        if get_distance(player, enemy) == 2:
            if heavy_on_cooldown(player):
                return LIGHT
            else:
                return HEAVY

        if get_distance(player, enemy) >= 3:
            return random.choice([FORWARD, JUMP_FORWARD])

        return random.choice([JUMP, JUMP_BACKWARD, FORWARD, BLOCK, HEAVY])
