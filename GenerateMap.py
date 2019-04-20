from queue import Queue

import random
import json

def bfs(grammar, grammar_map, grammar_size, flag_index):
    '''
    This runs a breadth first search on the grammar to find the shortest route
    to the flag. 
    '''
    correct_path = None
    queue = Queue()
    queue.put(grammar_map[-grammar_size:])

    while correct_path == None:
        grammar_path = queue.get()
        grammar_input = grammar_path[-grammar_size:]
        formatted_grammar_input = ','.join(grammar_input)
        possible_columns = grammar[formatted_grammar_input]

        for column in possible_columns:
            if column == flag_index:
                correct_path = grammar_path + [str(column)]
                break

            queue.put(grammar_path + [str(column)])
    
    grammar_map += correct_path[grammar_size:]

def generate_map(
    grammar, min_map_length, max_map_length, auto_complete, use_random_selection, 
    start_index, flag_index, end_index, random_selection_chance=0):
    '''
    Generates a map of fixed length between min and max

    TODO: remove the seed and have it be called in generate and rl instead. Right now
          it is useful for debugging this thing
    '''
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

        if current_iteration > max_map_length:
            if auto_complete:
                bfs(grammar, grammar_map, grammar_size, flag_index)
                
            generate = False
            break

        new_key = None
        if use_random_selection or random_selection_chance > random.uniform(0,1):
            new_key = random.choice(list(grammar_values.keys()))
        else:
            for key in grammar_values:
                current_weight += grammar_values[key]
                
                if current_weight > weight_val:
                    new_key = key
                    break

        if current_iteration < min_map_length and new_key == flag_index:
            continue
        else:
            grammar_map.append(new_key)
            current_iteration += 1

            if new_key == end_index:
                generate = False
                
    return grammar_map
    
def convert_grammar_array_to_map(grammar_map, grammar_to_col):
    map_text = ''
    for g in grammar_map:
        map_text += grammar_to_col[g] + '\n'
    
    return map_text