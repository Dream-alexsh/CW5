import marshmallow
import marshmallow_dataclass

from dataclasses import dataclass
from typing import List, Optional
from random import uniform
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float


    # Рандомное число между мин. и макс. для оружия
    @property
    def damage(self):
        return uniform(self.min_damage, self.max_damage)


@dataclass
class EquipmentData:
    # содержит 2 списка - с оружием и с броней
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Optional[Weapon]:
        # Получаем название оружия
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon
        return None

    def get_armor(self, armor_name: str) -> Optional[Armor]:
        # Получаем название брони
        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor
        return None

    def get_weapons_names(self) -> List[Weapon]:
        # возвращаем список с оружием
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> List[Armor]:
        # возвращаем список с броней
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # Берем данные из json файла и десериализуем их

        equipment_file = open("./data/equipment.json", encoding='utf-8')
        data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
