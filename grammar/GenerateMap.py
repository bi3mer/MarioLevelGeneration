import random

END_GRAMMAR   = '36'
FLAG_GRAMMAR  = '35'
START_GRAMMAR = '0'

# @note: could be improved to reduce duplicate code 
def generate_map_weighted(grammar, seed, min_map_length):
    random.seed(seed)
    grammar_size = len(random.sample(grammar.keys(), 1)[0].split(','))
    grammar_map = [START_GRAMMAR for i in range(6)]

    current_iteration = 0
    generate = True
    while generate:
        grammar_input = ','.join(grammar_map[-grammar_size:])
        grammar_values = grammar[grammar_input]
        weight_val = random.uniform(0, 1)
        current_weight = 0.0
        
        for key in grammar_values:
            current_weight += grammar_values[key]
            
            if current_weight > weight_val:
                if current_iteration < min_map_length and key == FLAG_GRAMMAR:
                    continue
                    
                grammar_map.append(key)
                if key == END_GRAMMAR:
                    generate = False
                    
                break
                
        current_iteration += 1

    return grammar_map

def generate_map_unweighted(grammar, seed, min_map_length):
    random.seed(seed)
    grammar_size = len(random.sample(grammar.keys(), 1)[0].split(','))
    grammar_map = [START_GRAMMAR for i in range(6)]

    current_iteration = 0
    generate = True
    while generate:
        grammar_input = ','.join(grammar_map[-grammar_size:])
        grammar_values = grammar[grammar_input]
        weight_val = random.uniform(0, 1)
        current_weight = 0.0
        weight = 1.0 / float(len(grammar_values))
        
        for key in grammar_values:
            current_weight += weight
            
            if current_weight > weight_val:
                if current_iteration < min_map_length and key == FLAG_GRAMMAR:
                    continue
                    
                grammar_map.append(key)
                if key == END_GRAMMAR:
                    generate = False
                    
                break
                
        current_iteration += 1

    return grammar_map
    
def convert_grammar_array_to_map(grammar_map, grammar_to_col):
    map_text = ''
    for g in grammar_map:
        map_text += grammar_to_col[g] + '\n'
    
    return map_text