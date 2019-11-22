from typing import List
from OrodaelTurrim.Business.Interface.Player import PlayerTag
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameUncertaintyProxy
from ExpertSystem.Business.UserFramework import IKnowledgeBase
from ExpertSystem.Structure.RuleBase import Fact
from OrodaelTurrim.Structure.Enums import TerrainType, AttributeType, EffectType, GameRole
from OrodaelTurrim.Structure.Position import OffsetPosition, CubicPosition, AxialPosition


class KnowledgeBase(IKnowledgeBase):
    """
    Class for defining known facts based on Proxy information. You can transform here any information from
    proxy to better format of Facts. Important is method `create_knowledge_base()`. Return value of this method
    will be passed to `Inference.interfere`. It is recommended to use Fact class but you can use another type.

    |
    |
    | Class provides attributes:

    - **map_proxy [MapProxy]** - Proxy for access to map information
    - **game_object_proxy [GameObjectProxy]** - Proxy for access to all game object information
    - **uncertainty_proxy [UncertaintyProxy]** - Proxy for access to all uncertainty information in game
    - **player [PlayerTag]** - class that serve as instance of user player for identification in proxy methods

    """
    map_proxy: MapProxy
    game_object_proxy: GameObjectProxy
    game_uncertainty_proxy: GameUncertaintyProxy
    player: PlayerTag

    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy, player: PlayerTag):
        """
        You can add some code to __init__ function, but don't change the signature. You cannot initialize
        KnowledgeBase class manually so, it is make no sense to change signature.
        """
        super().__init__(map_proxy, game_object_proxy, game_uncertainty_proxy, player)



    def create_knowledge_base(self) -> List[Fact]:
        """
        Method for create user knowledge base. You can also have other class methods, but entry point must be this
        function. Don't change the signature of the method, you can change return value, but it is not recommended.

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!  TODO: Write implementation of your knowledge base definition HERE   !!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """

        facts = []

        # Add bool fact

        # Add fact with data holder
        # We can use there eval function same as data function
        # because if first_free_tile return None, bool value of None is False, otherwise bool value is True
        # You can use different functions for eval and data
        facts.append(Fact('player_dont_have_base', eval_function=self.player_dont_have_base))
        facts.append(Fact('free_tile', eval_function=self.free_tile, data=self.free_tile))
        facts.append(Fact('visible_free_tile', eval_function=self.visible_free_tile, data=self.visible_free_tile))
        facts.append(Fact('free_sides', eval_function=self.free_sides, data=self.free_sides))
        # facts.append(Fact('resources_archer6', eval_function=self.resources_archer6, data=self.free_first_ring))
        facts.append(Fact('resources_knight', eval_function=self.resources_knight))
        facts.append(Fact('has_guards', eval_function=self.has_guards))
        facts.append(Fact('resources_druid', eval_function=self.resources_druid))
        facts.append(Fact('resources_magician', eval_function=self.resources_magician))
        facts.append(Fact('resources_archer', eval_function=self.resources_archer))
        facts.append(Fact('king_low', eval_function=self.king_low))
        facts.append(Fact('found_good', eval_function=self.found_good, data=self.found_good))
        facts.append(
            Fact('free_place_from_base2', eval_function=self.free_place_from_base2, data=self.free_place_from_base2))
        facts.append(
            Fact('free_place_from_base3', eval_function=self.free_place_from_base3, data=self.free_place_from_base3))
        facts.append(Fact('resources_ent1', eval_function=self.resources_ent1))
        facts.append(Fact('enemy_of', eval_function=self.enemy_of))
        facts.append(Fact('near_minotaur', eval_function=self.near_minotaur, data=self.near_minotaur))
        facts.append(Fact('resources_archer5', eval_function=self.resources_archer5))
        facts.append(Fact('yes', eval_function=self.yes))
        facts.append(Fact('no', eval_function=self.no))
        # Add numerical fact
        facts.append(Fact("money", lambda: self.game_object_proxy.get_resources(self.player)))

        return facts

    def yes(self):
        return True
    def no(self):
        return False;

    def player_dont_have_base(self):
        if self.map_proxy.player_have_base(self.player):
            return False
        return True

    def found_good(self):
        inner = self.map_proxy.get_inner_tiles()
        border = self.map_proxy.get_border_tiles()
        ban = set()
        ban.update(border)
        for x in border:
            a = x.get_all_neighbours()
            for z in a:
                ban.add(z)
        for pos in inner:
            if self.map_proxy.get_terrain_type(pos).name == "FOREST" or self.map_proxy.get_terrain_type(
                    pos).name == "HILL" or self.map_proxy.get_terrain_type(pos).name == "VILLAGE" and pos not in ban:
                z = pos.get_all_neighbours()
                flag = True
                for a in z:
                    if a in border:
                        flag = False
                if flag:
                    return pos.offset

        return OffsetPosition(0, 0).offset




    def first_free_tile(self, terrain_type: str):
        """ Find random tile with given terrain type """
        tiles = self.map_proxy.get_inner_tiles()
        border_tiles = self.map_proxy.get_border_tiles()

        for position in tiles:
            terrain = self.map_proxy.get_terrain_type(position) == TerrainType.from_string(terrain_type)
            if terrain and position not in border_tiles:
                return position
        return None

    def visible_free_tile(self, terrain_type: str):
        """ Find random free tile with given terrain type """
        tiles = self.map_proxy.get_player_visible_tiles()
        border_tiles = self.map_proxy.get_border_tiles()

        for position in tiles:
            terrain = self.map_proxy.get_terrain_type(position) == TerrainType.from_string(terrain_type)
            occupied = self.map_proxy.is_position_occupied(position)
            if terrain and not occupied and position not in border_tiles:
                return position
        return None

    def resources_knight(self):
        if self.game_object_proxy.get_resources(self.player) >= 12:
            return True

    def resources_archer(self):
        if self.game_object_proxy.get_resources(self.player) >= 5:
            return True

    def has_guards(self):
        base = self.map_proxy.get_bases_positions().pop()
        if self.free_tile(1) and self.free_tile(2) and self.free_tile(3) and self.free_tile(4) \
            and self.free_tile(5) and self.free_tile(6):
                return True

    def near_minotaur(self):
        base = self.map_proxy.get_bases_positions().pop()
        positions = base.offset.get_all_neighbours()
        outer = set()
        for a in positions:
            outer.update(a.get_all_neighbours())
          #outer is near area
        spawn = self.game_uncertainty_proxy.spawn_information()[0]
        flag = False
        for pos in outer:
            flag = False
            for unit in spawn:
                if unit.game_object_type.name == "MINOTAUR":
                    flag = True
                    break

        if flag:
            return True
#
#            if self.game_object_proxy.get_object_type(pos).name == self.game_object_proxy.get_object_type(pos).MINOTAUR\
#                    or flag:
#                spawn_places = self.map_proxy.compute_visible_tiles(base, 2)
#                for spawn in spawn_places:
#                    if not self.map_proxy.is_position_occupied(spawn):
#                        return spawn

    def resources_druid(self):
        if self.game_object_proxy.get_resources(self.player) >= 25:
            return True

    def resources_magician(self):
        if self.game_object_proxy.get_resources(self.player) >= 30:
            return True

    def resources_ent1(self):
        if self.game_object_proxy.get_resources(self.player) >= 50:
            return True

    def resources_archer5(self):
        if self.game_object_proxy.get_resources(self.player) >= 25:
            return True

    def free_place_from_base2(self):
        home = self.map_proxy.get_bases_positions().pop()
        # visible tiles from base
        positions = self.map_proxy.compute_visible_tiles(home, 2)
        # border tiles
        ban = self.map_proxy.get_border_tiles()
        positions.difference_update(ban)
        emptyPos = set()
        for some in positions:
            # free positions
            if self.map_proxy.is_position_occupied(some) == False:
                emptyPos.add(some)
        return emptyPos

    def free_place_from_base3(self):
        home = self.map_proxy.get_bases_positions().pop()
        # visible tiles from base
        positions = self.map_proxy.compute_visible_tiles(home, 3)
        # border tiles
        ban = self.map_proxy.get_border_tiles()
        positions.difference_update(ban)
        emptyPos = set()
        for some in positions:
            # free positions
            if self.map_proxy.is_position_occupied(some) == False:
                emptyPos.add(some)
        return emptyPos

    def free_sides(self):
        free_pos = set()

        pos = OffsetPosition(-1, -5).offset
        if not self.map_proxy.is_position_occupied(pos):
            free_pos.add(pos)

        pos = OffsetPosition(-2, -5).offset
        if not self.map_proxy.is_position_occupied(pos):
            free_pos.add(pos)

        pos = OffsetPosition(-5, -3).offset
        if not self.map_proxy.is_position_occupied(pos):
            free_pos.add(pos)

        pos = OffsetPosition(-5, -2).offset
        if not self.map_proxy.is_position_occupied(pos):
            free_pos.add(pos)

        free_pos.intersection_update(self.map_proxy.get_player_visible_tiles())
        return free_pos

    def enemy_of(self, unit):
        for visible in self.map_proxy.get_player_visible_tiles():
            if self.game_object_proxy.get_role(visible).name == "MINOTAUR" and unit == "MAGICIAN" or unit == "DRUID":
                return True
            if self.game_object_proxy.get_role(visible).name == "DAEMON" and unit == "ENT":
                return True
            return False

    def free_tile(self, x):
        base_q = self.map_proxy.get_bases_positions().pop().offset.q
        base_r = self.map_proxy.get_bases_positions().pop().offset.r
        pos = OffsetPosition
        if x == "1":
            pos = OffsetPosition(base_q - 1, base_r - 1)
        if x == "2":
            pos = OffsetPosition(base_q, base_r - 1)
        if x == "3":
            pos = OffsetPosition(base_q + 1, base_r - 1)
        if x == "4":
            pos = OffsetPosition(base_q + 1, base_r)
        if x == "5":
            pos = OffsetPosition(base_q, base_r + 1)
        if x == "6":
            pos = OffsetPosition(base_q - 1, base_r)

        if x == "7":
            pos = OffsetPosition(base_q - 2, base_r - 1)
        if x == "8":
            pos = OffsetPosition(base_q + 2, base_r - 1)
        if x == "9":
            pos = OffsetPosition(base_q - 2, base_r + 1)
        if x == "10":
            pos = OffsetPosition(base_q + 2, base_r + 1)

        if x == "11":
            pos = OffsetPosition(base_q, base_r + 2)
        if x == "12":
            pos = OffsetPosition(base_q, base_r - 2)
        if x == "13":
            pos = OffsetPosition(base_q + 2, base_r)
        if x == "14":
            pos = OffsetPosition(base_q - 2, base_r)

        if x == "15":
            pos = OffsetPosition(base_q + 1, base_r + 2)
        if x == "16":
            pos = OffsetPosition(base_q + 1, base_r - 2)
        if x == "17":
            pos = OffsetPosition(base_q - 1, base_r + 2)
        if x == "18":
            pos = OffsetPosition(base_q - 1, base_r - 2)
        print("===================")
        print(pos)
        print(x)
        print(self.map_proxy.get_bases_positions().pop())
        print("===================")
        visible = self.map_proxy.get_player_visible_tiles()
        border = self.map_proxy.get_border_tiles()
        if not self.map_proxy.is_position_occupied(pos) and pos in visible\
                and pos not in border and self.map_proxy.is_position_on_map(pos):
            return pos

    def king_low(self):
        return True
