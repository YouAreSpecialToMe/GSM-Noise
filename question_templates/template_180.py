from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and items
    names = ["Suzie", "Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace", "Heidi", "Isaac"]
    flavors = ["strawberry", "grape", "green apple", "watermelon", "blueberry", "orange", "lemon", "mint", "cherry", "pineapple"]
    stores = ["supermarket", "convenience store", "grocery store", "market", "candy shop", "corner store", "mall"]
    
    # Randomly select variables
    name = random.choice(names)
    store = random.choice(stores)
    favorite_flavor = random.choice(flavors)
    
    flavors.remove(favorite_flavor)
    other_flavor1 = random.choice(flavors)
    flavors.remove(other_flavor1)
    other_flavor2 = random.choice(flavors)

    # Set packs
    total_packs = random.randint(4, 10)
    other_packs1 = 1  # pack of other flavor 1
    other_packs2 = 1  # pack of other flavor 2
    favorite_packs = total_packs - other_packs1 - other_packs2

    # Price of other_flavor1
    price_other1 = random.randint(1, 5)
    # Price of other_flavor2 is half of price_other1
    price_other2 = price_other1 / 2

    # Adjust total_cost to ensure price_favorite is positive
    price_favorite = random.uniform(0.5, 5)

    # Calculate total_cost
    total_cost = favorite_packs * price_favorite + other_packs1 * price_other1 + other_packs2 * price_other2
    total_cost = round(total_cost, 2)

    # Construct the problem
    problem = [
        f"{name} loves to chew fruit-flavored gum.",
        f"{name} bought {total_packs} packs of gum the last time {name} was at the {store}.",
        f"{name} got {favorite_packs} packs of {favorite_flavor} gum, {name}'s favorite flavor.",
        f"{name} paid ${price_other1} for a pack of {other_flavor1} gum that {name} also liked.",
        f"{name} wanted to try something new, so {name} paid half as much for a small pack of {other_flavor2} gum.",
    ]

    question = f"If {name} paid ${total_cost} in all, how many dollars did each pack of {favorite_flavor} gum cost?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Construct in-topic irrelevant info
    in_topic_irrelevant_infos = [
        f"{name} chews gum every day after lunch.",
        f"{name} has a collection of gum wrappers from different flavors.",
        f"{name} shares gum with friends at school.",
        f"Each pack of gum contains 10 pieces.",
    ]

    # Construct out-topic irrelevant info
    out_topic_irrelevant_infos = [
        f"{name} also plays the piano.",
        f"{name} is planning a vacation to France.",
        f"{name} has a pet cat named Whiskers.",
        f"{name}'s favorite color is blue.",
    ]

    # Randomly add irrelevant information
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Add symbol or grammar errors. Assume functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question
    problem.append(question)

    # Return the problem and answer
    answer = round(price_favorite, 2)
    cot = [f"{name} paid ${price_other1} for a pack of {other_flavor1} gum and half as much for a small pack of {other_flavor2} gum, which is {price_other2}.", f"The total cost is calculated as {favorite_packs} packs of {favorite_flavor} gum at {price_favorite} each, plus {other_packs1} pack of {other_flavor1} gum at {price_other1}, plus {other_packs2} pack of {other_flavor2} gum at {price_other2}.", f"Therefore, the total cost is {total_cost}.", f"The cost of each pack of {favorite_flavor} gum is {price_favorite}, rounded to two decimal places, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
