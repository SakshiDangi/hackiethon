# player coding
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import (
    HP,
    LEFTBORDER,
    RIGHTBORDER,
    LEFTSTART,
    RIGHTSTART,
    PARRYSTUN,
)
from Game.PlayerConfigs import Player_Controller
from random import choice

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = OnePunchSkill
SECONDARY_SKILL = JumpBoostSkill

# constants, for easier move return
# movements
JUMP = ("move", (0, 1))
FORWARD = ("move", (1, 0))
BACK = ("move", (-1, 0))
JUMP_FORWARD = ("move", (1, 1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

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
        self.last_jump = 5

    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary

    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(
        self,
        player: Player_Controller,
        enemy: Player_Controller,
        player_projectiles,
        enemy_projectiles,
    ):
        distance = get_distance(player, enemy)

        if get_stun_duration(enemy) > 0 and distance == 1:
            return full_assault(player, enemy, PRIMARY, SECONDARY)

        # for proj in enemy_projectiles:
        #     proj.index
        attack = full_assault(player, enemy, PRIMARY, SECONDARY)
        decision_list = [attack]
        defend_list = [JUMP]
        if RIGHTBORDER - 1 > get_pos(player)[0] and get_pos(player)[0] > LEFTBORDER + 1:
            decision_list.append(BACK)
            defend_list.append(BACK)
        if get_last_move(player) and get_last_move(player)[0] != BLOCK[0]:
            defend_list.append(BLOCK)

        if not primary_on_cooldown(player):
            defend_list.append(PRIMARY)
        if not heavy_on_cooldown(player):
            defend_list.append(HEAVY)

        if enemy._mid_startup and distance == 1:
            action = choice(defend_list)
            return choice(defend_list)

        action = choice(decision_list)
        if distance == 1:
            return action

        # if enemy._mid_startup:
        #     return choice(decision_list)

        return JUMP_FORWARD