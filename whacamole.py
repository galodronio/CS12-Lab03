# pyright: strict

from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum, auto
from random import Random, choice, randint
from typing import Protocol


class MoleState(StrEnum):
    INACTIVE = 'inactive'
    ACTIVE = 'active'
    HIT = 'hit'


class Mole(Protocol):
    def __init__(self):
        self.spawn()

    @property
    def base_hit_points(self) -> int:
        return 0

    @property
    def base_turns_active(self) -> int:
        return 0

    @property
    def points(self) -> int:
        return 0

    @property
    def state(self) -> MoleState:
        return self._state

    def spawn(self) -> None:
        self._state = MoleState.INACTIVE
        self._active_turns = self.base_turns_active
        self._hit_points = self.base_hit_points

    def pop_up(self) -> None:
        self._state = MoleState.ACTIVE

    def hide(self) -> None:
        self._state = MoleState.INACTIVE

    def receive_hit(self, damage) -> int:
        self._state = MoleState.HIT
        self._hit_points -= damage
        if self._hit_points <= 0: return self.points
        else: return 0

    def update_next_turn_state(self) -> None:
        if self.state == MoleState.HIT:
            if self._hit_points <= 0:
                self.spawn()

        elif self.state == MoleState.ACTIVE:
            self._active_turns -= 1
            if self._active_turns <= 0:
                self.spawn()


class SimpleMole():
    def __init__(self):
        self.spawn()

    @property
    def base_hit_points(self) -> int:
        return 1

    @property
    def base_turns_active(self) -> int:
        return 2

    @property
    def points(self) -> int:
        return 1

    @property
    def state(self) -> MoleState:
        return self._state

    def spawn(self) -> None:
        self._state = MoleState.INACTIVE
        self._active_turns = self.base_turns_active
        self._hit_points = self.base_hit_points

    def pop_up(self) -> None:
        self._state = MoleState.ACTIVE

    def hide(self) -> None:
        self._state = MoleState.INACTIVE

    def receive_hit(self, damage) -> int:
        self._state = MoleState.HIT
        self._hit_points -= damage
        if self._hit_points <= 0: return self.points
        else: return 0

    def update_next_turn_state(self) -> None:
        if self.state == MoleState.HIT:
            if self._hit_points <= 0:
                self.spawn()

        elif self.state == MoleState.ACTIVE:
            self._active_turns -= 1
            if self._active_turns <= 0:
                self.spawn()


class WhacAMoleHammer(Protocol):
    def __init__(self):
        self.power = power
        self.width = width


class SimpleHammer():
    def __init__(self):
        self.power = 1
        self.width = 1


class WhacAMoleConfig:
    def __init__(self, mole_counts: dict[Mole, int], turns: int, rng: Random):
        self.mole_counts = mole_counts
        self.turns = turns
        self.rng = rng


class WhacAMoleModel:
    def __init__(self, _config: WhacAMoleConfig, _hammer: WhacAMoleHammer):
        self._config = _config
        self._hammer = _hammer
        self._turn = 1
        self._moles = [m() for m in _config.mole_counts for n in range(_config.mole_counts[m])]
        self._total_points = 0
        self._is_game_over = False

    @property
    def moles(self) -> list[Mole]:
        return self._moles

    @property
    def current_turn(self) -> int:
        return self._turn 

    @property
    def points(self) -> int:
        return self._total_points 

    @property
    def is_game_over(self) -> int:
        return self._is_game_over

    def process_hit(self, idx: int) -> None:
        if self._moles[idx].state == MoleState.ACTIVE:
            self._total_points += self._moles[idx].receive_hit(self._hammer.power)

    def start_turn(self) -> None:
        inactive_moles = [x for x in self._moles if x.state == MoleState.INACTIVE]
        inactive_mole_count = len(inactive_moles)

        if self._turn == 1:
            self._config.rng.choice(inactive_moles).pop_up()
            inactive_mole_count -= 1

        for n in range(inactive_mole_count//2):
            if self._config.rng.choice((True, False)): break
            self._config.rng.choice(inactive_moles).pop_up()

    def finish_turn(self):
        for m in self._moles:
            m.update_next_turn_state()

        self._turn += 1
        if self._turn >= self._config.turns: self._is_game_over = True



class WhacAMoleView:
    def ask_for_hole_to_hit(self):
        return int(input('Enter the hole you want to whack'
                         ' (0-indexed): '))

    def display_turn(self, model: WhacAMoleModel):
        print(f'Turn {model.current_turn}')
        print(f'Points: {model.points}')
        print(' '.join([self._display_mole(mole) for mole in model.moles]))
        # print(' '.join([str(i) for i in range(len(model.moles))]))

    def _display_mole(self, mole: Mole) -> str:
        match mole.state:
            case MoleState.INACTIVE:
                return '_'
            case MoleState.HIT:
                return 'x'
            case MoleState.ACTIVE:
                return '🟤'
            case _:
                raise ValueError


class WhacAMoleController:
    def __init__(self, model: WhacAMoleModel, view: WhacAMoleView):
        self._model = model
        self._view = view

    def start(self):
        model = self._model
        view = self._view

        while not model.is_game_over:
            model.start_turn()
            view.display_turn(model)
            idx = view.ask_for_hole_to_hit()
            model.process_hit(idx)
            view.display_turn(model)
            model.finish_turn()