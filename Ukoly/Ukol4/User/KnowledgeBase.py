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
        facts.append(Fact('yes', eval_function=self.yes))
        # Add numerical fact
        facts.append(Fact("money",eval_function=self.money, data=self.money))
        facts.append(Fact("free_place", eval_function=self.free_place, data=self.free_place))

        return facts

    def free_place(self):
        place = self.map_proxy.get_player_visible_tiles()
        free_place = 0
        edge = self.map_proxy.get_border_tiles()
        for i in place:
            if not self.map_proxy.is_position_occupied(i) and i not in edge:
                free_place += 1
        x = [0] * 3
        x[0] = self.free_place_low(free_place)
        x[1] = self.free_place_medium(free_place)
        x[2] = self.free_place_high(free_place)
        SUM = 0
        DIV = 0
        # hardcoded range of trapezoids
        # flat part left = 1
        for i in range(0, 3):
            SUM += i * x[0]
            DIV += x[0]
        # left part going down middle part rising
        for i in range(2, 4):
            SUM += i * max(x[0], x[1])
            DIV += max(x[0], x[1])
        # middle part = 1
        for i in range(4, 6):
            SUM += i * x[1]
            DIV += x[1]
        # middle going down
        # im yelling timber
        # right part rising
        for i in range(6, 8):
            SUM += i * max(x[1], x[2])
            DIV += max(x[1], x[2])
        # right part = 1
        for i in range(8, 10):
            SUM += i * x[2]
            DIV += x[1]

        result = SUM / DIV
        # tazisko
        if result <= 3:
            return "low"
        if result <= 7:
            return "medium"
        return "high"

    def free_place_low(self, free_place: int):
        if free_place <= 2:
            return 1
        if free_place >= 3:
            return 0
        return (free_place - 3) / (2 - 3)

    def free_place_medium(self, free_place: int):
        return max(0, min(
            (free_place - 2) / (4 - 2),
            1,
            (8 - free_place) / (8 - 6))
                   )

    def free_place_high(self, free_place: int):
        if free_place <= 6:
            return 0
        if free_place >= 8:
            return 1
        return (free_place - 6) / (8 - 6)


    def money(self):
        money = self.game_object_proxy.get_resources(self.player)
        x = [0] * 3
        x[0] = self.money_low(money)
        x[1] = self.money_medium(money)
        x[2] = self.money_high(money)
        SUM = 0
        DIV = 0
        #hardcoded range of trapezoids
        #flat part left = 1
        for i in range (0,36):
            SUM += i*x[0]
            DIV += x[0]
        #left part going down middle part rising
        for i in range (36,40):
            SUM += i*max(x[0],x[1])
            DIV += max(x[0],x[1])
        #middle part = 1
        for i in range(41,50):
            SUM += i*x[1]
            DIV += x[1]
        #middle going down
        #im yelling timber
        #right part rising
        for i in range (51,80):
            SUM += i*max(x[1],x[2])
            DIV += max(x[1],x[2])
        #right part = 1
        for i in range (81, 100):
            SUM += i*x[2]
            DIV += x[1]

        result = SUM/DIV
        #tazisko
        if result < 38:
            return "low"
        if result < 65:
            return "medium"
        return "high"

    def money_low (self, money:int):
        if money <= 36:
            return 1
        if money >= 40:
            return 0
        return (money - 40)/(36 - 40)

    def money_medium (self, money:int):
        return max(0, min(
                        (money - 36)/(40 -36),
                        1,
                        (100 - money)/(100 - 50))
                   )

    def money_high (self, money:int):
        if money <= 50:
            return 0
        if money >= 80:
            return 1
        return (money - 50)/(80 - 50)

    def yes(self):
        return True

    def no(self):
        return False

    def player_dont_have_base(self):
        if self.map_proxy.player_have_base(self.player):
            return False
        return True

    def free_tile(self, z):
        base = self.map_proxy.get_bases_positions().pop()
        sites = base.get_all_neighbours()
        frees = set()
        min = 0
        x = int(float(z))
        for pos in sites:
            if not self.map_proxy.is_position_occupied(pos):
                if min < x:
                    frees.add(pos)
                    min+=1
        if  x == min:
            return frees

#####
#####
#        base_q = self.map_proxy.get_bases_positions().pop().offset.q
    #        base_r = self.map_proxy.get_bases_positions().pop().offset.r
    #        pos = OffsetPosition
    #        if x == "1":
    #            pos = OffsetPosition(base_q - 1, base_r - 1)
    #        if x == "2":
    #            pos = OffsetPosition(base_q, base_r - 1)
    #        if x == "3":
    #            pos = OffsetPosition(base_q + 1, base_r - 1)
    #        if x == "4":
    #            pos = OffsetPosition(base_q + 1, base_r)
    #        if x == "5":
    #            pos = OffsetPosition(base_q, base_r + 1)
    #        if x == "6":
    #            pos = OffsetPosition(base_q - 1, base_r)
    #
    #        if x == "7":
    #            pos = OffsetPosition(base_q - 2, base_r - 1)
    #        if x == "8":
    #            pos = OffsetPosition(base_q + 2, base_r - 1)
    #        if x == "9":
    #            pos = OffsetPosition(base_q - 2, base_r + 1)
    #        if x == "10":
    #            pos = OffsetPosition(base_q + 2, base_r + 1)
    #
    #        if x == "11":
    #            pos = OffsetPosition(base_q, base_r + 2)
    #        if x == "12":
    #            pos = OffsetPosition(base_q, base_r - 2)
    #        if x == "13":
    #            pos = OffsetPosition(base_q + 2, base_r)
    #        if x == "14":
    #            pos = OffsetPosition(base_q - 2, base_r)
    #
    #        if x == "15":
    #            pos = OffsetPosition(base_q + 1, base_r + 2)
    #        if x == "16":
    #            pos = OffsetPosition(base_q + 1, base_r - 2)
    #        if x == "17":
    #            pos = OffsetPosition(base_q - 1, base_r + 2)
    #        if x == "18":
    #            pos = OffsetPosition(base_q - 1, base_r - 2)
    #        print("===================")
    #        print(pos)
    #        print(x)
    #        print(self.map_proxy.get_bases_positions().pop())
    #        print("===================")
    #        visible = self.map_proxy.get_player_visible_tiles()
    #        border = self.map_proxy.get_border_tiles()
    #        if not self.map_proxy.is_position_occupied(pos) and pos in visible\
    #                and pos not in border and self.map_proxy.is_position_on_map(pos):
    #            return pos
    #
####
#####
