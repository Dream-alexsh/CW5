from flask import Flask, render_template, request, redirect, url_for

from base import Arena
from classes import unit_classes
from equipment import Equipment
from unit import BaseUnit, PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()
equipment = Equipment()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    if request.method == 'GET':
        result = {"header": "Выбор героя для игрока",  # для названия страниц
                  "classes": unit_classes,  # для названия классов
                  "weapons": equipment.get_weapons_names(),  # для названия оружия
                  "armors": equipment.get_armors_names() # для названия брони
        }
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        user_name = request.form['name']
        armor = request.form['armor']
        weapon = request.form['weapon']
        unit_class = request.form['unit_class']

        player = PlayerUnit(name=user_name, unit_class=unit_classes.get(unit_class))

        player.equip_armor(equipment.get_armor(armor))
        player.equip_weapon(equipment.get_weapon(weapon))
        heroes['player'] = player
        return redirect(url_for('choose_enemy'))

@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == 'GET':
        result = {"header": "Выбор героя для противника",  # для названия страниц
                  "classes": unit_classes,  # для названия классов
                  "weapons": equipment.get_weapons_names(),  # для названия оружия
                  "armors": equipment.get_armors_names()  # для названия брони
                  }
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        user_name = request.form['name']
        armor = request.form['armor']
        weapon = request.form['weapon']
        unit_class = request.form['unit_class']

        enemy = EnemyUnit(name=user_name, unit_class=unit_classes.get(unit_class))

        enemy.equip_armor(equipment.get_armor(armor))
        enemy.equip_weapon(equipment.get_weapon(weapon))
        heroes['enemy'] = enemy
        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run()
