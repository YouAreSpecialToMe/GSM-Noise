from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names
    names = ["Alex", "Jordan", "Taylor", "Sam", "Jamie", "Morgan"]
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly generate variables ensuring integer solutions
    diff_first_second = random.randint(2, 6)  # Difference between first and second set
    factor_third_second = 0.5  # Fixed factor

    # Possible values for the second set to ensure T is integer
    possible_S_values = [4, 6, 8, 10]
    S = random.choice(possible_S_values)
    
    # Calculate F and T
    F = S + diff_first_second
    T = factor_third_second * S
    
    # Total balls retrieved
    total_balls = F + S + T

    # Construct the premise content
    problem = [
        f"{name} is retrieving tennis balls from the court after a tennis match.",
        f"In the first of three sets, {name} had to retrieve {diff_first_second} more balls than in the second set.",
        f"In the third set, {name} retrieved half as many balls as in the second.",
        f"{name} retrieved {int(total_balls)} tennis balls in all."
    ]
    
    # Construct the question
    question = f"How many tennis balls did {name} retrieve in the first set of the match?"
    original_problem = problem.copy()

    original_problem.append(question)
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} played the match on a sunny day.",
        f"The match lasted for {random.randint(1,5)} hours.",
        f"{name} used a brand new racket for the match.",
        f"{name} is planning to go on vacation next week."
    ]

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (assumed functions)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the sentences except the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question
    problem.append(question)

    # Calculate the answer
    answer = F

    # Return the problem and the answer
    cot = [f"The number of balls retrieved in the first set is {diff_first_second} more than in the second set, so {F} = {S} + {diff_first_second}.", f"In the third set, {name} retrieved half as many balls as in the second set, so {T} = {factor_third_second} * {S}.", f"The total number of balls retrieved is the sum of balls from all sets: {total_balls} = {F} + {S} + {T}.", f"Therefore, the number of tennis balls retrieved in the first set is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}