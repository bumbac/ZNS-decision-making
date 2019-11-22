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

    def build_base(self, x, y):
        # Custom log messages
        n = FilterFactory().attack_filter(AttackNearestFilter)
        Logger.log('Building base')
        base_pos = OffsetPosition(x, y).offset
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.BASE,
                             base_pos,
                             [n], []))
        base_pos = OffsetPosition(-5, -5).offset
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.MAGICIAN,
                             base_pos,
                             [n], []))
        base_pos = OffsetPosition(-4, -5).offset
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.MAGICIAN,
                             base_pos,
                             [n], []))
        base_pos = OffsetPosition(-5, -4).offset
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.MAGICIAN,
                             base_pos,
                             [n], []))
        base_pos = OffsetPosition(-4, -3).offset
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.ARCHER,
                             base_pos,
                             [n], []))
        base_pos = OffsetPosition(-3, -5).offset
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.ARCHER,
                             base_pos,
                             [n], []))

    def build_base_good(self, found_good):
        # Custom log messages
        n = FilterFactory().attack_filter(AttackNearestFilter)
        Logger.log('Building base')
        base_pos = found_good
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.BASE,
                             base_pos,
                             [n], []))

    def restore_guard(self, unit, free_tile):
        nearest_filter = FilterFactory().attack_filter(AttackNearestFilter)
        resist_filter = FilterFactory().attack_filter(AttackNoResistantFilter)
        guard = GameObjectType.KNIGHT
        if unit == "KNIGHT":
            guard = GameObjectType.KNIGHT
        if unit == "ARCHER":
            guard = GameObjectType.ARCHER
        if unit == "DRUID":
            guard = GameObjectType.DRUID
        if unit == "MAGICIAN":
            guard = GameObjectType.MAGICIAN
        if unit == "ENT":
            guard = GameObjectType.ENT
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             guard,
                             free_tile,
                             [nearest_filter, resist_filter], []))
        print("Restore guard ", unit)

    def place_magician_base(self, free_place_from_base2):
        nearest_filter = FilterFactory().attack_filter(AttackNearestFilter)
        vulnerable_filter = FilterFactory().attack_filter(AttackMostVulnerableFilter)
        resist_filter = FilterFactory().attack_filter(AttackNoResistantFilter)
        dummy_filter = FilterFactory().attack_filter(DummyAttackFilter)
        pos = free_place_from_base2.pop()
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.MAGICIAN,
                             pos,
                             [nearest_filter, resist_filter, vulnerable_filter], []))

    def place_archer(self,free_tile):
        pos = free_tile
        vulnerable_filter = FilterFactory().attack_filter(AttackMostVulnerableFilter)
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.ARCHER,
                             pos,
                             [vulnerable_filter], []))

    def place_magician(self, free_sides):
        nearest_filter = FilterFactory().attack_filter(AttackNearestFilter)
        vulnerable_filter = FilterFactory().attack_filter(AttackMostVulnerableFilter)
        resist_filter = FilterFactory().attack_filter(AttackNoResistantFilter)
        pos = free_sides.pop()
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.MAGICIAN,
                             pos,
                             [nearest_filter, resist_filter], []))

    def place_druid(self, free_place_from_base2):
        nearest_filter = FilterFactory().attack_filter(AttackNearestFilter)
        vulnerable_filter = FilterFactory().attack_filter(AttackMostVulnerableFilter)
        resist_filter = FilterFactory().attack_filter(AttackNoResistantFilter)
        pos = free_place_from_base2.pop()
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.DRUID,
                             pos,
                             [nearest_filter, resist_filter, vulnerable_filter], []))

    def place_druid_minotaur(self, near_minotaur):
        nearest_filter = FilterFactory().attack_filter(AttackNearestFilter)
        vulnerable_filter = FilterFactory().attack_filter(AttackMostVulnerableFilter)
        resist_filter = FilterFactory().attack_filter(AttackNoResistantFilter)
        pos = near_minotaur
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.DRUID,
                             pos,
                             [nearest_filter, resist_filter, vulnerable_filter], []))
    def pl(self):
        print("FUUUCK")
        pos = OffsetPosition(-3, -4).offset
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.ENT,
                             pos,
                             [], []))
        pos = OffsetPosition(-4, -3).offset
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.ENT,
                             pos,
                             [], []))

    def pp(self):
        print("MEEE")
        pos = OffsetPosition(-5, -4).offset
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.ARCHER,
                             pos,
                             [], []))


