"""Ants Vs. SomeBees."""

import random

from sqlalchemy.sql.operators import truediv

from ucb import main, interact, trace
from collections import OrderedDict

################
# Core Classes #
################


class Place:
    """A Place holds insects and has an exit to another Place."""
    is_hive = False

    def __init__(self, name, exit=None):
        """Create a Place with the given NAME and EXIT.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name
        self.exit = exit
        self.bees = []        # A list of Bees
        self.ant = None       # An Ant
        self.entrance = None  # A Place
        # Phase 1: Add an entrance to the exit
        # BEGIN Problem 2
        if exit:
            exit.entrance = self
        # END Problem 2

    def add_insect(self, insect):
        """Asks the insect to add itself to this place. This method exists so
        that it can be overridden in subclasses.
        """
        insect.add_to(self)

    def remove_insect(self, insect):
        """Asks the insect to remove itself from this place. This method exists so
        that it can be overridden in subclasses.
        """
        insect.remove_from(self)

    def __str__(self):
        return self.name


class Insect:
    """An Insect, the base class of Ant and Bee, has health and a Place."""

    next_id = 0  # Every insect gets a unique id number
    damage = 0
    # ADD CLASS ATTRIBUTES HERE
    is_waterproof = False

    def __init__(self, health, place=None):
        """Create an Insect with a health amount and a starting PLACE."""
        self.health = health
        self.full_health = health
        self.place = place

        # assign a unique ID to every insect
        self.id = Insect.next_id
        Insect.next_id += 1

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the insect from its place if it
        has no health remaining. Decorated in gui.py for GUI support.

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_health(2)
        >>> test_insect.health
        3
        """
        self.health -= amount
        if self.health <= 0:
            self.zero_health_callback()

            if self.place is not None:
                self.place.remove_insect(self)

    def action(self, gamestate):
        """The action performed each turn."""

    def zero_health_callback(self):
        """
        Called when health reaches 0 or below.
        Decorated in gui.py to support GUI
        """

    def add_to(self, place):
        self.place = place

    def remove_from(self, place):
        self.place = None

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.health, self.place)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    implemented = False  # Only implemented Ant classes should be instantiated
    food_cost = 0
    is_container = False
    is_doubled = False
    blocks_path = True
    # ADD CLASS ATTRIBUTES HERE

    def __init__(self, health=1):
        super().__init__(health)

    def can_contain(self, other):
        return False

    def store_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def remove_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def add_to(self, place):
        if place.ant is None:
            place.ant = self
        else:
            # BEGIN Problem 8b
            if place.ant.can_contain(self):
                place.ant.store_ant(self)
                self.place = place
            elif self.can_contain(place.ant):
                self.store_ant(place.ant)
                self.place = place
                place.ant = self
            #如果不用elif，则是否执行else只与第二个有关，那么当第一种情况为True，仍有可能执行else,而不是预期的多选一情况
            else:
                assert place.ant is None, 'Too many ants in {0}'.format(place)
            # END Problem 8b
        Insect.add_to(self, place)

    def remove_from(self, place):
        if place.ant is self:
            place.ant = None
        elif place.ant is None:
            assert False, '{0} is not in {1}'.format(self, place)
        else:
            place.ant.remove_ant(self)
        Insect.remove_from(self, place)

    def double(self):
        """Double this ants's damage, if it has not already been doubled."""
        # BEGIN Problem 12
        if not self.is_doubled:
            self.damage = self.damage * 2
            self.is_doubled = True
        # END Problem 12


class HarvesterAnt(Ant):
    """HarvesterAnt produces 1 additional food per turn for the colony."""

    name = 'Harvester'
    implemented = True
    # OVERRIDE CLASS ATTRIBUTES HERE
    food_cost = 2
    health = 1

    def action(self, gamestate):
        """Produce 1 additional food for the colony.

        gamestate -- The GameState, used to access game state information.
        """
        # BEGIN Problem 1
        gamestate.food += 1
        # END Problem 1


class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = 'Thrower'
    implemented = True
    damage = 1
    # ADD/OVERRIDE CLASS ATTRIBUTES HERE
    food_cost = 3
    health = 1
    lower_bound = 0
    upper_bound = float('inf')

    def nearest_bee(self):
        """Return a random Bee from the nearest Place (excluding the Hive) that contains Bees and is reachable from
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).
        """
        # BEGIN Problem 3 and 4
        tmp = self.place
        count = 0
        while (not tmp.is_hive) and self.lower_bound > count:
        #需要从实例中获取bound
            tmp = tmp.entrance
            count += 1
        while (not tmp.is_hive) and count <= self.upper_bound:
            if tmp.bees :
                return random_bee(tmp.bees)
            tmp = tmp.entrance
            count += 1
        return None

        # END Problem 3 and 4

    def throw_at(self, target):
        """Throw a leaf at the target Bee, reducing its health."""
        if target is not None:
            target.reduce_health(self.damage)

    def action(self, gamestate):
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee())


def random_bee(bees):
    """Return a random bee from a list of bees, or return None if bees is empty."""
    assert isinstance(bees, list), \
        "random_bee's argument should be a list but was a %s" % type(bees).__name__
    if bees:
        return random.choice(bees)

##############
# Extensions #
##############


class ShortThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at most 3 places away."""

    name = 'Short'
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 4
    implemented = True   # Change to True to view in the GUI
    upper_bound = 3
    # END Problem 4


class LongThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at least 5 places away."""

    name = 'Long'
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 4
    implemented = True   # Change to True to view in the GUI
    lower_bound = 5
    # END Problem 4


class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires."""

    name = 'Fire'
    damage = 3
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 5
    implemented = True   # Change to True to view in the GUI
    # END Problem 5

    def __init__(self, health=3):
        """Create an Ant with a HEALTH quantity."""
        super().__init__(health)

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the FireAnt from its place if it
        has no health remaining.

        Make sure to reduce the health of each bee in the current place, and apply
        the additional damage if the fire ant dies.
        """
        # BEGIN Problem 5
        original_bees = self.place.bees[:]
        # To avoid mutating while iterating
        Ant.reduce_health(self,amount)

        for bee in original_bees:
            bee.reduce_health(amount)
        if not self.place :
            for bee in original_bees:
                if bee.place:
                    bee.reduce_health(self.damage)

        # END Problem 5

# BEGIN Problem 6
class WallAnt(Ant):
    """WallAnt has a large health value."""

    name = 'Wall'
    implemented = True
    food_cost = 4

    def __init__(self, health=4):
    #因为如果不重写，初始化时会把health设为1
        super().__init__(health)

# END Problem 6

# BEGIN Problem 7
class HungryAnt(Ant):
    """HungryAnt can eat bees."""

    name = 'Hungry'
    implemented = True
    food_cost = 4
    chew_cooldown = 3

    def __init__(self, health=1):
        super().__init__(health)
        self.cooldown = 0

    def action(self, gamestate):
        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            if self.place.bees:
                the_bee = random_bee(self.place.bees)
                the_bee.reduce_health(the_bee.health)
                self.cooldown = self.chew_cooldown
# END Problem 7


class ContainerAnt(Ant):
    """
    ContainerAnt can share a space with other ants by containing them.
    """
    is_container = True

    def __init__(self, health):
        super().__init__(health)
        self.ant_contained = None

    def can_contain(self, other):
        # BEGIN Problem 8a
        return not (self.ant_contained or other.is_container)
        # END Problem 8a

    def store_ant(self, ant):
        # BEGIN Problem 8a
        self.ant_contained = ant
        # END Problem 8a

    def remove_ant(self, ant):
        if self.ant_contained is not ant:
            assert False, "{} does not contain {}".format(self, ant)
        self.ant_contained = None

    def remove_from(self, place):
        # Special handling for container ants
        if place.ant is self:
            # Container was removed. Contained ant should remain in the game
            place.ant = place.ant.ant_contained
            Insect.remove_from(self, place)
        else:
            # default to normal behavior
            Ant.remove_from(self, place)

    def action(self, gamestate):
        # BEGIN Problem 8a
        if self.ant_contained:
            self.ant_contained.action(gamestate)
        # END Problem 8a


class ProtectorAnt(ContainerAnt):
    """ProtectorAnt provides protection to other Ants."""

    name = 'Protector'
    food_cost = 4
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 8c
    implemented = True   # Change to True to view in the GUI

    def __init__(self,health=2):
        super().__init__(health)
    # END Problem 8c

# BEGIN Problem 9
class TankAnt(ContainerAnt):
    """ProtectorAnt provides protection to other Ants."""

    name = 'Tank'
    food_cost = 6
    implemented = True   # Change to True to view in the GUI
    damage = 1

    def __init__(self,health=2):
        super().__init__(health)

    def action(self, gamestate):
        super().action(gamestate)
        original_bees = self.place.bees[:]
        for bee in original_bees:
            bee.reduce_health(self.damage)


# END Problem 9


class Water(Place):
    """Water is a place that can only hold waterproof insects."""

    def add_insect(self, insect):
        """Add an Insect to this place. If the insect is not waterproof, reduce
        its health to 0."""
        # BEGIN Problem 10
        super().add_insect(insect)
        if not insect.is_waterproof:
            insect.reduce_health(insect.health)
        # END Problem 10

# BEGIN Problem 11
class ScubaThrower(ThrowerAnt):
    """Scuba is a kind of waterproof Thrower with higher food cost"""
    food_cost = 6
    name = 'Scuba'
    implemented = True
    is_waterproof = True

# END Problem 11


class QueenAnt(ThrowerAnt):
    """QueenAnt boosts the damage of all ants behind her."""

    name = 'Queen'
    food_cost = 7
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 12
    implemented = True  # Change to True to view in the GUI
    # END Problem 12

    def action(self, gamestate):
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.
        """
        # BEGIN Problem 12
        super().action(gamestate)
        tmp = self.place.exit
        while tmp:
            if tmp.ant:
                tmp.ant.double()
                if tmp.ant.is_container and tmp.ant.ant_contained:
                    tmp.ant.ant_contained.double()
            tmp = tmp.exit
        # END Problem 12

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and if the QueenAnt has no health
        remaining, signal the end of the game.
        """
        # BEGIN Problem 12
        super().reduce_health(amount)
        # END Problem 12

    def zero_health_callback(self):
        ants_lose()

################
# Extra Challenge #
################

# class SlowThrower(ThrowerAnt):
#     """ThrowerAnt that causes Slow on Bees."""
#
#     name = 'Slow'
#     food_cost = 6
#     # BEGIN Problem EC 1
#     implemented = True   # Change to True to view in the GUI
#     slowing_times = 5
#     # END Problem EC 1
#     #
#     def throw_at(self, target):
#         # BEGIN Problem EC 1
#         # 只有当有目标时才执行
#         if target:
#             # 检查蜜蜂是否是第一次被减速
#             # 如果它没有 .original_action 属性，说明是第一次
#             # 否则后面的original_action就是new_slow_action了
#             if not hasattr(target, 'original_action'):
#                 # 1. 保存蜜蜂最原始的 action 方法
#                 target.original_action = target.action
#
#             # 2. 定义一个新的 action 方法来替换它
#             # 这个新方法将作为 target 的方法被调用，所以它的第一个参数
#             # 实际上是 target 自身 (通常我们叫它 self，但这里为了清晰可以换个名字)
#             def new_slow_action(gamestate):
#                 # 检查减速效果是否还在
#                 if target.slow_turns > 0:
#                     # a. 只有在偶数回合才允许行动
#                     if gamestate.time % 2 == 0:
#                         target.is_frozen = False
#                         target.original_action(gamestate)  # 调用保存好的原始 action
#                     # b. (在奇数回合，什么也不做，即被减速了)
#                     else:
#                         target.is_frozen = True
#                     # c. 无论是否行动，回合数都减 1
#                     target.slow_turns -= 1
#
#                 else:
#                     # 效果结束后，直接调用原始action
#                     target.original_action(gamestate)
#                     target.is_frozen = False
#
#             # 3. 在目标蜜蜂上设置初始减速回合数
#
#             target.slow_turns = self.slowing_times
#
#             # 4. 用我们新定义的函数替换掉蜜蜂的 action 方法
#             target.action = new_slow_action
#         # END Problem EC 1

# In ants.py

class SlowThrower(ThrowerAnt):
    """ThrowerAnt that causes Slow on Bees."""

    name = 'Slow'
    food_cost = 6
    # BEGIN Problem EC 1
    implemented = True
    slowing_times = 5
    # END Problem EC 1

    def throw_at(self, target):
        """Slow the TARGET Bee by calling its slow method."""
        # BEGIN Problem EC 1
        if target:
            target.slow(self.slowing_times)
        # END Problem EC 1

# class ScaryThrower(ThrowerAnt):
#     """ThrowerAnt that intimidates Bees, making them back away instead of advancing."""
#
#     name = 'Scary'
#     food_cost = 6
#     # BEGIN Problem EC 2
#     implemented = +True   # Change to True to view in the GUI
#     Scary_times = 2
#     # END Problem EC 2
#
#     def throw_at(self, target):
#         # BEGIN Problem EC 2
#         #如果多次使用original_function， 一旦被第一个施加效果的蚂蚁
#         # （在这里是 ScaryThrower）设置，就永远不会再被更新。
#         # 就会导致反复覆写的出错，所以应当在Bee类中管理状态
#         if target:
#             if not hasattr(target, 'original_action'):
#                 target.original_action = target.action
#
#             def new_back_away_action(gamestate):
#                 if target.back_turns > 0:
#                     if target.place.entrance.is_hive and not target.is_frozen:
#                     #为了各个class都能获取，还是把is_frozen写到attribute里面
#                         target.back_turns -= 1
#                     elif not target.is_frozen:
#                         #这里复用了action的代码，也可以创造一个倒着飞的蜜蜂子类
#                         destination = target.place.entrance
#                         if target.blocked():
#                             target.sting(target.place.ant)
#                         elif target.health > 0 and destination is not None:
#                             target.move_to(destination)
#                         target.back_turns -= 1
#                 else:
#                     target.original_action(gamestate)
#
#             if not target.is_scared:
#                 target.back_turns = self.Scary_times
#                 target.action = new_back_away_action
#                 target.is_scared = True
#
#
#         # END Problem EC 2

class ScaryThrower(ThrowerAnt):
    """ThrowerAnt that intimidates Bees, making them back away instead of advancing."""

    name = 'Scary'
    food_cost = 6
    # BEGIN Problem EC 2
    implemented = True
    scary_duration = 2
    # END Problem EC 2

    def throw_at(self, target):
        """Scare the TARGET Bee by calling its scare method."""
        # BEGIN Problem EC 2
        if target:
            target.scare(self.scary_duration)
        # END Problem EC 2

class NinjaAnt(Ant):
    """NinjaAnt does not block the path and damages all bees in its place."""

    name = 'Ninja'
    damage = 1
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem EC 3
    implemented = True   # Change to True to view in the GUI
    blocks_path = False
    # END Problem EC 3

    def action(self, gamestate):
        # BEGIN Problem EC 3
        original_bees = self.place.bees[:]
        for bee in original_bees:
            bee.reduce_health(self.damage)
        # END Problem EC 3


class LaserAnt(ThrowerAnt):
    """ThrowerAnt that damages all Insects standing in its path."""

    name = 'Laser'
    food_cost = 10
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem EC 4
    implemented = True   # Change to True to view in the GUI
    damage = 2
    # END Problem EC 4

    def __init__(self, health=1):
        super().__init__(health)
        self.insects_shot = 0

    def insects_in_front(self):
        # BEGIN Problem EC 4
        tmp = self.place
        insects = {}
        dist = 0
        while not tmp.is_hive:
            for bee in tmp.bees:
                insects[bee] = dist
            if tmp.ant:
                if tmp.ant.is_container :
                    insects[tmp.ant] = dist
                    if tmp.ant.ant_contained:
                        if tmp.ant.ant_contained is not self:
                            insects[tmp.ant.ant_contained] = dist
                else:
                    if tmp.ant is not self:
                        insects[tmp.ant] = dist
            tmp = tmp.entrance
            dist += 1
        return insects


        # END Problem EC 4

    def calculate_damage(self, distance):
        # BEGIN Problem EC 4
        spec_damage = self.damage - distance * 0.25 - self.insects_shot * 0.0625
        return 0 if 0 > spec_damage else spec_damage
        # END Problem EC 4

    def action(self, gamestate):
        insects_and_distances = self.insects_in_front()
        LaserAnt.play_sound_effect() # laser beam sound effect
        for insect, distance in insects_and_distances.items():
            damage = self.calculate_damage(distance)
            insect.reduce_health(damage)
            if damage:
                self.insects_shot += 1

    @classmethod
    def play_sound_effect(cls):
        """Play laser sound effect. Decorated in gui.py"""
        pass


########
# Bees #
########

class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants."""

    name = 'Bee'
    damage = 1
    is_waterproof = True
    was_ever_scared = False
    slow_turns = 0
    scared_turns = 0

    def sting(self, ant):
        """Attack an ANT, reducing its health by 1."""
        ant.reduce_health(self.damage)

    def move_to(self, place):
        """Move from the Bee's current Place to a new PLACE."""
        if self.place is not None:
            self.place.remove_insect(self)

        if place is not None:
            place.add_insect(self)

    def blocked(self):
        """Return True if this Bee cannot advance to the next Place."""
        # Special handling for NinjaAnt
        # BEGIN Problem EC 3
        if self.place.ant and self.place.ant.blocks_path:
            return True
        else:
            return False
        # END Problem EC 3

    def scare(self, duration):
        """
        Scare this Bee for a given DURATION.
        A Bee can only be scared once in its lifetime.
        """
        # BEGIN Problem EC 2
        if not self.was_ever_scared:
            self.scared_turns = duration
            self.was_ever_scared = True
        # END Problem EC 2

    def slow(self, duration):
        """
        Slow this Bee for a given DURATION.
        """
        # BEGIN Problem EC 1
        self.slow_turns = duration
        # END Problem EC 1

    def action(self, gamestate):
        """A Bee's action stings the Ant that blocks its exit if it is
        blocked, or moves to the exit of its current place otherwise.

        This action method has been modified to account for Slow and Scary effects.
        """
        # BEGIN EC MODIFICATIONS
        # Priority 1: Check if slowed and unable to act this turn.
        if self.slow_turns > 0 and gamestate.time % 2 != 0:
            self.slow_turns -= 1
            return  # Frozen for this turn, do nothing.

        # Priority 2: Check if scared. If so, move backwards.
        if self.scared_turns > 0:
            destination = self.place.entrance
            # Do not move back into the Hive.
            if self.blocked():
                self.sting(self.place.ant)
            elif self.health > 0  and not destination.is_hive:
                self.move_to(destination)
            self.scared_turns -= 1
        # Priority 3: Default action if not scared.
        else:
            destination = self.place.exit
            if self.blocked():
                self.sting(self.place.ant)
            elif self.health > 0 and destination is not None:
                self.move_to(destination)

        # If the Bee was able to act this turn (wasn't frozen), decrement slow_turns.
        if self.slow_turns > 0:
            self.slow_turns -= 1
        # END EC MODIFICATIONS

    def add_to(self, place):
        place.bees.append(self)
        super().add_to(place)

    def remove_from(self, place):
        place.bees.remove(self)
        super().remove_from(place)


class Wasp(Bee):
    """Class of Bee that has higher damage."""
    name = 'Wasp'
    damage = 2


class Boss(Wasp):
    """The leader of the bees. Damage to the boss by any attack is capped.
    """
    name = 'Boss'
    damage_cap = 8

    def reduce_health(self, amount):
        super().reduce_health(min(amount, self.damage_cap))

    @classmethod
    def play_sound_effect(cls):
        "Play sound effect when boss arrives! Decorated in gui.py"
        pass


class Hive(Place):
    """The Place from which the Bees launch their assault.

    assault_plan -- An AssaultPlan; when & where bees enter the colony.
    """
    is_hive = True

    def __init__(self, assault_plan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees():
            self.add_insect(bee)
        # The following attributes are always None for a Hive
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, gamestate):
        exits = [p for p in gamestate.places.values() if p.entrance is self]

        for bee in self.assault_plan.get(gamestate.time, []):
            if Boss in bee.__class__.__mro__:
                Boss.play_sound_effect()
                GameState.display_notification('Boss Bee is Here!')
            bee.move_to(random.choice(exits))
            gamestate.active_bees.append(bee)

###################
# Game Components #
###################

class GameState:
    """An ant collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    """

    def __init__(self, beehive, ant_types, create_places, dimensions, food=2):
        """Create an GameState for simulating a game.

        Arguments:
        beehive -- a Hive full of bees
        ant_types -- a list of ant classes
        create_places -- a function that creates the set of places
        dimensions -- a pair containing the dimensions of the game layout
        """
        self.time = 0
        self.food = food
        self.beehive = beehive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.dimensions = dimensions
        self.active_bees = []
        self.configure(beehive, create_places)

    def configure(self, beehive, create_places):
        """Configure the places in the colony."""
        self.base = AntHomeBase('Ant Home Base')
        self.places = OrderedDict()
        self.bee_entrances = []

        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = beehive
                self.bee_entrances.append(place)
        register_place(self.beehive, False)
        create_places(self.base, register_place,
                      self.dimensions[0], self.dimensions[1])

    def ants_take_actions(self): # Ask ants to take actions
        for ant in self.ants:
            if ant.health > 0:
                ant.action(self)

    def bees_take_actions(self, num_bees): # Ask bees to take actions
        for bee in self.active_bees[:]:
            if bee.health > 0:
                bee.action(self)
            if bee.health <= 0:
                num_bees -= 1
                self.active_bees.remove(bee)
        if num_bees == 0: # Check if player won
            GameState.play_win_sound()
            raise AntsWinException()
        return num_bees

    def simulate(self):
        """Simulate an attack on the ant colony. This is called by the GUI to play the game."""
        num_bees = len(self.bees)
        try:
            while True:
                self.beehive.strategy(self) # Bees invade from hive
                yield None # After yielding, players have time to place ants
                self.ants_take_actions()
                self.time += 1
                yield None # After yielding, wait for throw leaf animation to play, then ask bees to take action
                num_bees = self.bees_take_actions(num_bees)
        except AntsWinException:
            print('All bees are vanquished. You win!')
            yield True
        except AntsLoseException:
            print('The bees reached homebase or the queen ant queen has perished. Please try again :(')
            yield False

    def deploy_ant(self, place_name, ant_type_name):
        """Place an ant if enough food is available.

        This method is called by the current strategy to deploy ants.
        """
        ant_type = self.ant_types[ant_type_name]
        if ant_type.food_cost > self.food:
            message = f'Not enough food!'
            print(message)
            GameState.display_notification(message)
        else:
            ant = ant_type()
            self.places[place_name].add_insect(ant)
            self.food -= ant.food_cost
            return ant

    def remove_ant(self, place_name):
        """Remove an Ant from the game."""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    def display_notification(message):
        """Display a notification! Decorated in gui.py for GUI support"""
        pass

    @classmethod
    def play_win_sound(cls):
        """Play the sound effect when ants win! Decorated in gui.py"""
        pass

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status


class AntHomeBase(Place):
    """AntHomeBase at the end of the tunnel, where the queen normally resides."""

    def add_insect(self, insect):
        """Add an Insect to this Place.

        Can't actually add Ants to a AntHomeBase. However, if a Bee attempts to
        enter the AntHomeBase, a AntsLoseException is raised, signaling the end
        of a game.
        """
        assert isinstance(insect, Bee), 'Cannot add {0} to AntHomeBase'
        raise AntsLoseException()


def ants_win():
    """Signal that Ants win."""
    raise AntsWinException()


def ants_lose():
    """Signal that Ants lose."""
    raise AntsLoseException()


def ant_types():
    """Return a list of all implemented Ant classes."""
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]


def bee_types():
    """Return a list of all implemented Bee classes."""
    all_bee_types = []
    new_types = [Bee]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_bee_types.extend(new_types)
    return all_bee_types


class GameOverException(Exception):
    """Base game over Exception."""
    pass


class AntsWinException(GameOverException):
    """Exception to signal that the ants win."""
    pass


class AntsLoseException(GameOverException):
    """Exception to signal that the ants lose."""
    pass


###########
# Layouts #
###########


def wet_layout(queen, register_place, tunnels=3, length=9, moat_frequency=3):
    """Register a mix of wet and and dry places."""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)


def dry_layout(queen, register_place, tunnels=3, length=9):
    """Register dry tunnels."""
    wet_layout(queen, register_place, tunnels, length, 0)


#################
# Assault Plans #
#################

class AssaultPlan(dict):
    """The Bees' plan of attack for the colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """
    def add_wave(self, bee_type, bee_health, time, count):
        """Add a wave at time with count Bees that have the specified health."""
        bees = [bee_type(bee_health) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    def all_bees(self):
        """Place all Bees in the beehive and return the list of Bees."""
        return [bee for wave in self.values() for bee in wave]