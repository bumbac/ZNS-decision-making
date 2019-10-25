from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Business.Proxy import GameControlProxy, MapProxy
from ExpertSystem.Business.UserFramework import IActionBase
from OrodaelTurrim.Business.Logger import Logger
from OrodaelTurrim.Structure.Enums import GameObjectType
from OrodaelTurrim.Structure.Filter.AttackFilter import AttackStrongestFilter
from OrodaelTurrim.Structure.Filter.Factory import FilterFactory
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.Position import OffsetPosition, CubicPosition
from User.AttackFilter import DummyAttackFilter, EmptyAttackFilter


class ActionBase(IActionBase):
    """
    You can define here your custom actions. Methods must be public (not starting with __ or _) and must have unique
    names. Methods could have as many arguments as you want. Instance of this class will be available in
    Interference class.


    **This class provides:**

    * self.game_control_proxy [GameControlProxy] for doing actions in game
    * self.map_proxy [MapProxy] for finding places on map
    * self.player [IPlayer] instance of your player for identification yourself in proxy

    MapProxy should be used there only for finding right place on the map. For example functions like:
    * spawn_knight_on_nearest_mountain(x,y)
    * spawn_unit_near_to_base(amount_of_units, unit_type)
    * spawn_unit_far_in_direction(direction)
    * etc...

    It is forbidden, to create whole login in those functions. Whole behaviour logic must be editable without,
    touching code in ActionBase (login must mainly depend on rules). So it's forbidden to use functions like:
    * prepare_defence()
    * spawn_ideal_amount_of_units_at_ideal_places()
    * defend_my_base()
    * etc...

    You can use () operator on ActionBase instance to call your function by `str` name or `Expression` class.
    Expression class will also pass arguments from self to your method. () operator using only args so be careful about
    order and number of arguments.

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!               TODO: Write implementation of your actions HERE                !!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    game_control_proxy: GameControlProxy
    map_proxy: MapProxy
    player: IPlayer


    def build_base(self, position_q: int, position_r: int):
        # Custom log messages
        Logger.log('Building base')

        # Create instance of custom filter
        empty_filter = FilterFactory().attack_filter(EmptyAttackFilter)
        dummy_filter = FilterFactory().attack_filter(DummyAttackFilter, 'Base attacking')

        # Create instance of default filter
        strongest_filter = FilterFactory().attack_filter(AttackStrongestFilter)

        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.BASE,
                             OffsetPosition(int(position_q), int(position_r)),
                             [empty_filter, dummy_filter, strongest_filter], []))

    def place_base(self):
        Logger.log('Place on 0 0 0')
        base_position = CubicPosition(0, 0, 0)
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.BASE,
                             base_position,
                             [], []))
        self.place_guard(1)

    def place_guard(self, z: int):
        Logger.log('Placing guards')
        troop = GameObjectType.ARCHER
        if z == 1:
            troop = GameObjectType.ARCHER
        if z == 2:
            troop = GameObjectType.KNIGHT
        if z == 3:
            troop = GameObjectType.DRUID
        x = CubicPosition(-1, 1, 0)
        self.game_control_proxy.spawn_unit(
                SpawnInformation(self.player,
                                 troop,
                                 x,
                                 [], []))
        x = CubicPosition(-1, 0, 1)
        self.game_control_proxy.spawn_unit(
                SpawnInformation(self.player,
                                 troop,
                                 x,
                                 [], []))
        x = CubicPosition(0, -1, 1)
        self.game_control_proxy.spawn_unit(
                SpawnInformation(self.player,
                                 troop,
                                 x,
                                 [], []))
        x = CubicPosition(0, 1, -1)
        self.game_control_proxy.spawn_unit(
                SpawnInformation(self.player,
                                 troop,
                                 x,
                                 [], []))
        x = CubicPosition(1, -1, 0)
        self.game_control_proxy.spawn_unit(
                SpawnInformation(self.player,
                                 troop,
                                 x,
                                 [], []))
        x = CubicPosition(1, 0, -1)
        self.game_control_proxy.spawn_unit(
                SpawnInformation(self.player,
                                 troop,
                                 x,
                                 [], []))

    def place_extended(self):
        Logger.log('Placing extended soldiers')
        base_position = CubicPosition(0, 0, 0)
        for z in base_position.get_all_neighbours():
            for x in z.get_all_neighbours():
                if self.map_proxy.is_position_occupied(x):
                    continue
                self.game_control_proxy.spawn_unit(
                    SpawnInformation(self.player,
                                     GameObjectType.KNIGHT,
                                     x,
                                     [], []))

    def place_druid_square(self):
        Logger.log('Placing druid in corner')
        x = CubicPosition(-2, 2, 0)
        troop = GameObjectType.DRUID
        if not self.map_proxy.is_position_occupied(x):
            self.game_control_proxy.spawn_unit(
                SpawnInformation(self.player,
                                 troop,
                                 x,
                                 [], []))
        x = CubicPosition(-2, 0, 2)
        if not self.map_proxy.is_position_occupied( x):
            self.game_control_proxy.spawn_unit(
                SpawnInformation(self.player,
                                 troop,
                                 x,
                                 [], []))
        x = CubicPosition(2, 0, -2)
        if not self.map_proxy.is_position_occupied(x):
            self.game_control_proxy.spawn_unit(
                SpawnInformation(self.player,
                                 troop,
                                 x,
                                 [], []))
        x = CubicPosition(2, -2, 0)
        if not self.map_proxy.is_position_occupied(x):
            self.game_control_proxy.spawn_unit(
                SpawnInformation(self.player,
                                 troop,
                                 x,
                                 [], []))

    def place_cross_ent(self):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.ENT,
                             CubicPosition(0, 2, -2),
                             [],[]))
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.ENT,
                             CubicPosition(0, -2, 2),
                             [], []))
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.ENT,
                             CubicPosition(-2, 1, 1),
                             [], []))
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.ENT,
                             CubicPosition(2, -1, -1),
                             [], []))