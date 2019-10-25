from typing import List, Set

from OrodaelTurrim.Business.Logger import Logger
from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameUncertaintyProxy
from ExpertSystem.Business.UserFramework import IKnowledgeBase
from ExpertSystem.Structure.RuleBase import Fact
from OrodaelTurrim.Structure.Enums import GameObjectType
from OrodaelTurrim.Structure.Position import CubicPosition


class KnowledgeBase(IKnowledgeBase):
    """
    Class for defining known facts based on Proxy information. You can transform here any information from
    proxy to better format of Facts. Important is method `create_knowledge_base()`. Return value of this method
    will be passed to `Interference.interfere`. It is recommended to use Fact class but you can use another type.

    |
    |
    | Class provides attributes:

    - **map_proxy [MapProxy]** - Proxy for access to map information
    - **game_object_proxy [GameObjectProxy]** - Proxy for access to all game object information
    - **uncertainty_proxy [UncertaintyProxy]** - Proxy for access to all uncertainty information in game
    - **player [IPlayer]** - instance of user player for identification in proxy methods

    """
    map_proxy: MapProxy
    game_object_proxy: GameObjectProxy
    game_uncertainty_proxy: GameUncertaintyProxy
    player: IPlayer


    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy, player: IPlayer):
        """
        You can add some code to __init__ function, but don't change the signature. You cannot initialize
        KnowledgeBase class manually so, it is make no sense to change signature.
        """
        super().__init__(map_proxy, game_object_proxy, game_uncertainty_proxy, player)

    def has_guards(self) -> bool:
        Logger.log('has_guards')
        base_position = CubicPosition(0, 0, 0)
        flag = True
        for z in base_position.get_all_neighbours():
            if self.game_object_proxy.get_object_type(z) != GameObjectType.ARCHER:
                flag = False
                Logger.log('Not all guards')
        return flag

    def cross_free(self) -> bool:
        flag = True
        if self.map_proxy.is_position_occupied(CubicPosition(0, 2, -2)):
            flag = False
        if self.map_proxy.is_position_occupied(CubicPosition(0, -2, 2)):
            flag = False
        if self.map_proxy.is_position_occupied(CubicPosition(-2, 1, 1)):
            flag = False
        if self.map_proxy.is_position_occupied(CubicPosition(2, -1, -1)):
            flag = False
        return flag

    def create_knowledge_base(self) -> List[Fact]:
        """
        Method for create user knowledge base. You can also have other class methods, but entry point must be this
        function. Don't change the signature of the method, you can change return value, but it is not recommended.

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!  TODO: Write implementation of your knowledge base definition HERE   !!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """

        facts = []

        # Add numerical fact
        user_resources = self.game_object_proxy.get_resources(self.player)
        facts.append(Fact("money", lambda: user_resources))

        #place base
        if not self.map_proxy.player_have_base(self.player):
            facts.append(Fact('player_dont_have_base'))
        else:
            facts.append(Fact('player_have_base'))

        #inner guards for long range
        if self.game_object_proxy.get_resources(self.player) >= 60:
            facts.append(Fact('can_buy_guard'))

        #placing druids in corners
        if self.game_object_proxy.get_resources(self.player) >= 100 and self.has_guards():
            facts.append(Fact('has_guards'))
            facts.append(Fact('has_resources_druid'))

        #place knights for defense line
        if self.game_object_proxy.get_resources(self.player) >= 120:
            facts.append(Fact('can_buy_extended_guard'))
        #resources for ENT
        if self.game_object_proxy.get_resources(self.player) >= 200:
            facts.append(Fact('has_resources_ent'))
        #position for ENT
        if self.cross_free():
            facts.append(Fact('cross_not_occupied'))
        return facts
