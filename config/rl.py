# Every variable has a default and a hard coded value. If you do not want to use
# the hard code value then just set it to None and these default values that have
# been hard coded below
assessment_iterations = 100
grammar_name = None
max_iterations = 100000
grammar_size = None
minimum_maps = 1
seed = 0
min_map_length = 50
max_map_length = 200
random_selection_chance = 0.15

# One of these need to be set but None is a valid option for rewards you do not
# want set. All of these values should either be None or between 0 and 1
target_coin_reward = None
target_enemies = 0.7
target_linearity = 0.2
target_rewards = None

# The following sets defaults and does basic error checking in the configuration
# file when it is imported
if grammar_size == None:
    grammar_size = 4
    print(f'Defaulted grammar_size to {grammar_size}.')
elif not isinstance(grammar_size, int):
    raise Exception('Grammar size must be of type int.')
elif grammar_size <= 0 or grammar_size > 7:
    raise Exception('Grammar size must be greater than 0 and less than 7.')

if grammar_name == None:
    grammar_name = 'DEFAULT_GRAMMAR_NAME.json'
    print(f'Defaulted grammar_name to {grammar_name}.')
elif not isinstance(grammar_name, str):
    raise Exception('grammar_name must be of type string.')
elif len(grammar_name) == 0:
    raise Exception('grammar_name cannot be an empty string')
elif grammar_name.endswith('.json') == False:
    grammar_name += '.json'
    print(f'modifed grammar_name to include ".json": {grammar_name}')

if max_iterations == None:
    max_iterations = 5000
    print(f'defaulted max_iterations to {max_iterations}.')
elif not isinstance(max_iterations, int):
    raise Exception('max_iterations must be of type integer.')
elif max_iterations <= 0:
    raise Exception('max iterations must be greater than 0.')

if seed == None:
    from datetime import datetime
    seed = datetime.now()
    print(f'defaulted seed to {seed}.')
elif not isinstance(seed, int):
    raise Exception('seed must be of type int.')

if minimum_maps == None:
    minimum_maps = 10
elif not isinstance(minimum_maps, int):
    raise Exception('minimum_maps must be of type integer.')
elif minimum_maps <= 0:
    raise Exception('minimum_mpas must be greater than 0.')

if assessment_iterations == None:
    assessment_iterations = 100
elif not isinstance(assessment_iterations, int):
    raise Exception('assessment_iterations must be of type integer.')
elif assessment_iterations <= 0:
    raise Exception('assessment_iterations must be greater than 0.')

if min_map_length == None:
    min_map_length = 50
elif not isinstance(min_map_length, int):
    raise Exception('min_map_length must be of type integer.')
elif min_map_length <= 0:
    raise Exception('min_map_length must be greater than 0.')

if max_map_length == None:
    max_map_length = 200
elif not isinstance(max_map_length, int):
    raise Exception('max_map_length must be of type integer.')
elif max_map_length <= 0:
    raise Exception('max_map_length must be greater than 0.')

if min_map_length > max_map_length:
    raise Exception('min_map_length must be less than or equal to max_map_length.')

if random_selection_chance == None:
    max_map_length = 0.2
elif not isinstance(max_map_length, int):
    raise Exception('random_selection_chance must be of type integer.')
elif random_selection_chance < 0 or random_selection_chance > 1:
    raise Exception('random_selection_chance must be greater than 0 and less than 1.')
    
# Now we check the rewards to make sure the user has input proper values and has
# atleast one that is not None
valid_target_configuration = False

if target_coin_reward != None:
    if not isinstance(target_coin_reward, float) and not isinstance(target_coin_reward, int):
        raise Exception('target_coin_reward must be of either type float or int.')

    if target_coin_reward < 0 or target_coin_reward > 1:
        raise Exception('target coin_reward must be greater than or equal to 0 or less than or equal to 1')

    valid_target_configuration = True

if target_enemies != None:
    if not isinstance(target_enemies, float) and not isinstance(target_enemies, int):
        raise Exception('target_enemies must be of either type float or int.')

    if target_enemies < 0 or target_enemies > 1:
        raise Exception('target_enemies must be greater than or equal to 0 or less than or equal to 1')

    valid_target_configuration = True

if target_linearity != None:
    if not isinstance(target_linearity, float) and not isinstance(target_linearity, int):
        raise Exception('target_linearity must be of either type float or int.')

    if target_linearity < 0 or target_linearity > 1:
        raise Exception('target_linearity must be greater than or equal to 0 or less than or equal to 1')

    valid_target_configuration = True

if target_rewards != None:
    if not isinstance(target_rewards, float) and not isinstance(target_rewards, int):
        raise Exception('target_rewards must be of either type float or int.')

    if target_rewards < 0 or target_rewards > 1:
        raise Exception('target_rewards must be greater than or equal to 0 or less than or equal to 1')

    valid_target_configuration = True

if not valid_target_configuration:
    raise Exception('Atleast one target heuristic must be set.')