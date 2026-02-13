from whacamole import SimpleMole, MoleState, SimpleHammer, WhacAMoleModel, WhacAMoleConfig
from random import Random

def test_whacamole():
	mole_counts = {SimpleMole: 6}
	turns = 5
	rng = Random(0)

	config = WhacAMoleConfig(mole_counts, turns, rng)
	hammer = SimpleHammer()

	model = WhacAMoleModel(config, hammer)

	assert model.is_game_over == False
	assert model.points == 0
	assert model.current_turn == 1

	model.start_turn()

	assert model.moles[0].state == MoleState.ACTIVE
	assert model.moles[1].state == MoleState.INACTIVE
	assert model.moles[3].state == MoleState.ACTIVE

	model.process_hit(0)

	assert model.moles[0].state == MoleState.HIT
	assert model.points == 1


