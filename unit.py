from __future__ import annotations
from abc import ABC, abstractmethod
from random import randint

from equipment import Weapon, Armor
from classes import UnitClass


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self._is_skill_used = False

    @property
    def health_points(self):
        # возвращаем аттрибут hp в красивом виде
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        # возвращаем аттрибут hp в красивом виде
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        # присваиваем нашему герою новое оружие
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        # одеваем новую броню
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        self.stamina -= self.weapon.stamina_per_hit * self.unit_class.stamina
        damage = self.weapon.damage * self.unit_class.attack

        # Проверяем, сможет ли противник заблокировать удар бронёй
        if target.stamina > target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage -= target.armor.defence * target.unit_class.armor

        return target.get_damage(damage)

    def get_damage(self, damage: int) -> int:
        # Расчитываем урон
        if damage > 0:
            self.hp -= damage
            return round(damage, 1)
        return 0

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        # Проверяем использование скилла
        if self._is_skill_used:
            return 'Навык уже использован.'
        self._is_skill_used = True
        return self.unit_class.skill.use(self, target)


class PlayerUnit(BaseUnit):
    # Просчитываем выносливость для удара игрока
    def hit(self, target: BaseUnit) -> str:
        if self.stamina * self.unit_class.stamina < self.weapon.stamina_per_hit:
            return f'{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости.'
        damage = self._count_damage(target)
        if damage > 0:
            return f'{self.name}, используя {self.weapon.name}, пробивает {target.armor.name} соперника и наносит {damage} урона.'
        return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."


class EnemyUnit(BaseUnit):
    # Просчитываем выносливость для удара противника и рандомно ставим использование скилла
    def hit(self, target: BaseUnit) -> str:
        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and randint(0, 100) < 10:
            return self.use_skill(target)

        if self.stamina * self.unit_class.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит Вам {damage} урона. "

        return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."


