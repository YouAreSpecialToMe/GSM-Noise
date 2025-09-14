from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
import math

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define lists of possible names, animals, feeds, etc.
    names = ['John', 'Sarah', 'Miguel', 'Emma', 'Liam', 'Chloe', 'Alex', 'Zoey']
    animals = ['horses', 'cows', 'sheep', 'goats']
    treats = ['sugar cubes', 'apples', 'molasses', 'candy']
    vegetables = ['carrots', 'beets', 'turnips', 'pumpkins']
    main_feeds = ['hay', 'alfalfa', 'silage', 'straw']
    supplements = ['oats', 'corn', 'barley']

    # Randomly select variables
    name = random.choice(names)
    animal = random.choice(animals)
    treat = random.choice(treats)
    vegetable = random.choice(vegetables)
    main_feed = random.choice(main_feeds)
    supplement = random.choice(supplements)

    # Quantities and weights
    treat_qty = random.randint(1, 5)  # Quantity of treats
    treat_weight = 1  # Weight per unit in pounds

    veg_qty = random.randint(2, 6)  # Quantity of vegetables
    veg_weight = random.choice([10, 12, 15])  # Weight per bag in pounds

    main_feed_qty = random.randint(30, 50)  # Quantity of main feed
    main_feed_weight = random.choice([50, 75, 100])  # Weight per bale in pounds

    supp_qty = random.randint(15, 25)  # Quantity of supplements
    supp_weight = random.choice([50, 65, 80])  # Weight per sack in pounds

    truck_capacity = random.choice([2000, 2250, 2500])  # Truck capacity in pounds

    # Irrelevant information
    irrelevant_infos = [
        f"{name} owns a total of {random.randint(5, 50)} {animal} on the farm.",
        f"The farm has been in {name}'s family for {random.randint(50, 150)} years.",
        f"The farm covers an area of {random.randint(100, 1000)} acres."
    ]

    irrelevant_infos_out = [
        f"{name} enjoys playing {random.choice(['guitar', 'piano', 'violin'])} in their free time.",
        f"{name}'s favorite color is {random.choice(['blue', 'green', 'red', 'yellow'])}."
    ]

    # Build the problem statements
    problem_statements = [
        f"{name} is buying feed for {name}'s {animal}.",
        f"{name} buys a variety of {main_feed}, {supplement}, {vegetable} and {treat}.",
        f"Since {treat} are a rare treat, {name} only buys {treat_qty} 1-pound boxes of them for the whole stable.",
        f"{name} only wants enough {vegetable} to feed the {animal} while the vegetables are fresh, so {name} buys {veg_qty} {veg_weight}-pound bags.",
        f"{main_feed.capitalize()} is the main diet of {name}'s {animal}, so {name} buys {main_feed_qty} {main_feed_weight}-pound bales.",
        f"{supplement.capitalize()} is a staple to supplement the {main_feed}, so {name} buys {supp_qty} {supp_weight}-pound sacks.",
        f"{name}'s farm truck can carry {truck_capacity} pounds at a time."
    ]
    question=f"How many trips does {name} need to transport all the feed?"
    original_problem=problem_statements.copy()
    original_problem.append(question)

    # Add irrelevant information based on probability
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem_statements.insert(random.randint(1, len(problem_statements)-1), info)
    for info in irrelevant_infos_out:
        if random.random() < prob_irre:
            problem_statements.insert(random.randint(1, len(problem_statements)-1), info)

    # Add symbol or grammar errors
    problem_statements = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem_statements
    ]

    # Shuffle the problem statements except for the first one
    first_statement = problem_statements[0]
    rest_statements = problem_statements[1:]
    if shuffle:
        random.shuffle(rest_statements)

    problem_statements = [first_statement] + rest_statements+[question]

    # Calculate the answer
    total_weight = (
        treat_qty * treat_weight +
        veg_qty * veg_weight +
        main_feed_qty * main_feed_weight +
        supp_qty * supp_weight
    )
    trips = math.ceil(total_weight / truck_capacity)
    answer = trips

    # Return problem and answer as a dictionary
    problem_text = ' '.join(problem_statements)
    cot = [f"Calculate the total weight of the treats: {treat_qty} * {treat_weight}.", f"Calculate the total weight of the vegetables: {veg_qty} * {veg_weight}.", f"Calculate the total weight of the main feed: {main_feed_qty} * {main_feed_weight}.", f"Calculate the total weight of the supplements: {supp_qty} * {supp_weight}.", f"Add all the weights to get the total weight: {total_weight}.", f"Divide the total weight by the truck capacity {truck_capacity} and round up to the nearest whole number to get the number of trips: {trips}.", f"The answer is the number of trips: {answer}."]
    
    return {"cot": cot, 'problem': problem_statements, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
