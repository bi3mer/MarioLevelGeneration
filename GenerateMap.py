import random

def generate_map(
    grammar, seed, min_map_length, use_random_selection, start_index, 
    flag_index, end_index, random_selection_chance=0):

    random.seed(seed)
    grammar_size = len(random.sample(grammar.keys(), 1)[0].split(','))
    grammar_map = [start_index for i in range(6)]

    current_iteration = 0
    generate = True
    while generate:
        grammar_input = ','.join(grammar_map[-grammar_size:])
        grammar_values = grammar[grammar_input]
        weight_val = random.uniform(0, 1)
        current_weight = 0.0
        weight = 1.0 / float(len(grammar_values))
        
        for key in grammar_values:
            if use_random_selection:
                current_weight += weight
            else:
                if random_selection_chance > random.random():
                    current_weight += weight
                else:
                    current_weight += grammar_values[key]
            
            if current_weight > weight_val:
                if current_iteration < min_map_length and key == flag_index:
                    continue
                    
                grammar_map.append(key)
                if key == end_index:
                    generate = False
                    
                break
                
        current_iteration += 1

    return grammar_map
    
def convert_grammar_array_to_map(grammar_map, grammar_to_col):
    map_text = ''
    for g in grammar_map:
        map_text += grammar_to_col[g] + '\n'
    
    return map_text