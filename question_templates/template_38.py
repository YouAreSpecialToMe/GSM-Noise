from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define name and item lists
    names = ["Alex", "Sam", "Jordan", "Taylor", "Morgan", "Riley", "Casey", "Jamie"]
    
    cookie_types = ["peanut butter cookies", "macadamia nut cookies", "oatmeal raisin cookies", 
                    "double chocolate cookies", "lemon cookies", "gingerbread cookies",
                    "white chocolate cookies", "snickerdoodle cookies"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly select three different cookie types
    types = random.sample(cookie_types, 3)
    type1 = types[0]
    type2 = types[1]
    type3 = types[2]
    
    # Randomly generate initial quantities for each cookie type
    initial_q1 = random.randint(5, 15)
    initial_q2 = random.randint(5, 15)
    initial_q3 = random.randint(5, 15)
    
    # Quantities eaten for early day snack (one of each flavor)
    snack_eaten_q1 = 1
    snack_eaten_q2 = 1
    snack_eaten_q3 = 1
    
    # Quantity eaten for lunch (eat 2 of type1 cookies)
    lunch_eaten_q1 = 2
    
    # Quantity given to friends (2 of type3 cookies)
    given_q3 = 2
    
    # Quantity baked for dinner (4 of each flavor)
    baked_q1 = 4
    baked_q2 = 4
    baked_q3 = 4
    
    # Distraction variables
    extra_baked_q1 = random.randint(0, 5)
    extra_baked_q2 = random.randint(0, 5)
    extra_baked_q3 = random.randint(0, 5)
    
    favorite_beverage = random.choice(["milk", "tea", "coffee"])
    friend_names = random.sample(names, 2)
    age = random.randint(8, 60)
    money_saved = random.randint(500, 10000)
    
    # Construct the premise content, breaking it down into sentences
    problem = [
        f"{name} has {initial_q1} {type1}, {initial_q2} {type2}, and {initial_q3} {type3}.",
        f"{name} ate {snack_eaten_q1} {type1}, {snack_eaten_q2} {type2}, and {snack_eaten_q3} {type3} for an early day snack.",
        f"{name} ate {lunch_eaten_q1} {type1} for lunch.",
        f"{name} gives {given_q3} {type3} to {name}'s friends.",
        f"Then, {name} bakes {baked_q1} {type1}, {baked_q2} {type2}, and {baked_q3} {type3} for dinner."
    ]
    
    # Construct the question
    question = f"How many cookies does {name} have now?"
    original_problem=problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name}'s favorite beverage is {favorite_beverage}.",
        f"{name} is {age} years old."
    ]
    
    # Add out-topic irrelevant information
    out_topic_irrelevant_info = f"{name} has saved up ${money_saved} for a trip."
    irrelevant_infos.append(out_topic_irrelevant_info)
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors. You do not have to generate these functions. Assume that they are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences, except for the first one
    problem_first = problem[0]
    problem_rest = problem[1:]
    if shuffle:
        random.shuffle(problem_rest)
    problem = [problem_first] + problem_rest
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    total_cookies = (initial_q1 + initial_q2 + initial_q3)
    total_cookies -= (snack_eaten_q1 + snack_eaten_q2 + snack_eaten_q3)
    total_cookies -= lunch_eaten_q1
    total_cookies -= given_q3
    total_cookies += (baked_q1 + baked_q2 + baked_q3)
    answer = total_cookies
    
    # Return premise and answer as a dictionary
    cot = [f"Start with the initial number of cookies: {initial_q1} {type1}, {initial_q2} {type2}, and {initial_q3} {type3}.", f"Subtract the cookies eaten for an early day snack: {snack_eaten_q1} {type1}, {snack_eaten_q2} {type2}, and {snack_eaten_q3} {type3}.", f"Subtract the {lunch_eaten_q1} {type1} eaten for lunch.", f"Subtract the {given_q3} {type3} given to friends.", f"Add the cookies baked for dinner: {baked_q1} {type1}, {baked_q2} {type2}, and {baked_q3} {type3}.", f"The total number of cookies now is {total_cookies}, which is the final answer."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
