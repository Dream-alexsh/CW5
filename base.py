from typing import Dict

from unit import BaseUnit


class BaseSingleton(type):
    _instances: Dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1.5
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        # Старт игры
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        # Проверка хп игрока
        if self.player.hp > 0 and self.enemy.hp > 0:
            return None
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = f'Ничья'
        elif self.player.hp <= 0:
            self.battle_result = f'Вы проиграли'
        elif self.enemy.hp <= 0:
            self.battle_result = f'Вы выиграли'
        return self._end_game()

    def _stamina_regeneration(self):
        # Проверка выносливости
        if self.player.stamina + self.STAMINA_PER_ROUND > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina
        else:
            self.player.stamina += self.STAMINA_PER_ROUND

        if self.enemy.stamina + self.STAMINA_PER_ROUND > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina
        else:
            self.enemy.stamina += self.STAMINA_PER_ROUND

    def next_turn(self):
        # Следующий ход
        result = self._check_players_hp()
        if result is not None:
            return result
        if self.game_is_running:
            self._stamina_regeneration()
            return self.enemy.hit(self.player)

    def _end_game(self):
        # Конец игры
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):
        # Ход игрока
        result = self.player.hit(self.enemy)
        result_turn = self.next_turn()
        return f'{result}\n {result_turn}'

    def player_use_skill(self):
        # Использование скилла
        result = self.player.use_skill(self.enemy)
        result_turn = self.next_turn()
        return f'{result}\n {result_turn}'

