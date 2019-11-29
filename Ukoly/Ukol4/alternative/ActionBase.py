from ExpertSystem.Business.UserFramework import IActionBase
from OrodaelTurrim.Business.Interface.Player import PlayerTag
from OrodaelTurrim.Business.Logger import Logger
from OrodaelTurrim.Business.Proxy import GameControlProxy
from OrodaelTurrim.Structure.Enums import GameObjectType
from OrodaelTurrim.Structure.Filter.AttackFilter import AttackStrongestFilter, AttackNearestFilter, \
    AttackMostVulnerableFilter, AttackNoResistantFilter
from OrodaelTurrim.Structure.Filter.Factory import FilterFactory
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.Position import OffsetPosition
from User.AttackFilter import DummyAttackFilter, EmptyAttackFilter


class ActionBase(IActionBase):
    """
    You can define here your custom actions. Methods must be public (not starting with __ or _) and must have unique
    names. Methods could have as many arguments as you want. Instance of this class will be available in
    Inference class.

    **This class provides:**

    * self.game_control_proxy [GameControlProxy] for doing actions in game
    * self.player [PlayerTag] instance of your player for identification yourself in proxy

    Usage of ActionBase is described in documentation.


    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!               TODO: Write implementation of your actions HERE                !!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    game_control_proxy: GameControlProxy
    player: PlayerTag
    #
    #
    #
    def build(self, unit, free_tile):
        print(unit)
        print("####BUILD")
        real = 0
        if unit == "KNIGHT":
            real = GameObjectType.KNIGHT
        if unit == "ARCHER":
            real = GameObjectType.ARCHER
        if unit == "MAGICIAN":
            real = GameObjectType.MAGICIAN

        for i in free_tile:
            self.game_control_proxy.spawn_unit(
                SpawnInformation(self.player,
                                 real,
                                 i,
                                 [], []))

    def build_base_1(self, x, y):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.BASE,
                             OffsetPosition(x,y),
                             [], []))
        #place ARCHER many
    def place(self, unit, fuzzy):
        places = self.map_proxy.get_player_visible_tiles()
        free_place = set()
        real = GameObjectType.KNIGHT
        if unit == "KNIGHT":
            real = GameObjectType.KNIGHT
        if unit == "ARCHER":
            real = GameObjectType.ARCHER
        if unit == "MAGICIAN":
            real = GameObjectType.MAGICIAN
        edge = self.map_proxy.get_border_tiles()
        for i in places:
            if not self.map_proxy.is_position_occupied(i) and i not in edge:
                free_place.add(i)
        if fuzzy == "low":
            for i in range (2):
                self.game_control_proxy.spawn_unit(
                    SpawnInformation(self.player,
                                     real,
                                     free_place.pop(),
                                     [], []))
        if fuzzy == "medium":
            for i in range (6):
                self.game_control_proxy.spawn_unit(
                    SpawnInformation(self.player,
                                     real,
                                     free_place.pop(),
                                     [], []))
        if fuzzy == "high":
            for i in range (10):
                self.game_control_proxy.spawn_unit(
                    SpawnInformation(self.player,
                                     real,
                                     free_place.pop(),
                                     [], []))