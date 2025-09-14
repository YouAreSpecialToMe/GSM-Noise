from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists for names and items
    names = ["Alice", "Beth", "Cindy", "Diana", "Mary", "Bob", "Tom", "Jenny", "Laura", "Sam"]
    items = ["potted plants", "flower pots", "bonsai trees", "succulents", "herb plants", "cactus plants"]

    # Randomly select a name and item
    name = random.choice(names)
    item = random.choice(items)

    # Randomly generate values for the variables
    num_new_items_received_yesterday = random.randint(10, 30)  # Number of new items received
    num_items_per_ledge = random.randint(1, 5)  # Number of items per ledge
    num_window_ledges = random.randint(10, 50)  # Number of window ledges
    num_items_given_away_per_ledge = random.randint(1, num_items_per_ledge)  # Number of items given away per ledge

    # Irrelevant variables
    num_extra_items = random.randint(10, 50)
    pet_names = ["Buddy", "Max", "Charlie", "Bella", "Luna", "Lucy"]
    pet_name = random.choice(pet_names)
    hobby = random.choice(["painting", "cycling", "reading", "swimming", "hiking", "photography"])

    # Construct the problem sentences
    problem = [
        f"{name} is an avid gardener.",
        f"Yesterday, {name} received {num_new_items_received_yesterday} new {item} from her favorite plant nursery.",
        f"She already has {num_items_per_ledge} {item} on each of the {num_window_ledges} window ledges of her large country home.",
        f"Feeling generous, she has decided that she will give {num_items_given_away_per_ledge} {item} from each ledge to friends and family tomorrow."
    ]

    # Construct the question
    question = f"How many {item} will {name} remain with?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} plans to buy more {item} next week.",
        f"The plant nursery is offering a discount on {item}."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} recently adopted a puppy named {pet_name}.")
    irrelevant_infos.append(f"{name}'s favorite hobby is {hobby}.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
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

    # Calculate the answer
    num_items_before_giving = num_items_per_ledge * num_window_ledges + num_new_items_received_yesterday
    num_items_given_away = num_items_given_away_per_ledge * num_window_ledges
    answer = num_items_before_giving - num_items_given_away

    # Return the problem and answer as a dictionary
    cot = [f"{name} has {num_items_per_ledge} {item} on each of the {num_window_ledges} window ledges, and she received {num_new_items_received_yesterday} new {item} yesterday.", f"The total number of {item} before giving any away is {num_items_per_ledge} * {num_window_ledges} + {num_new_items_received_yesterday}, which is {num_items_before_giving}.", f"{name} decides to give away {num_items_given_away_per_ledge} {item} from each ledge.", f"The total number of {item} given away is {num_items_given_away_per_ledge} * {num_window_ledges}, which is {num_items_given_away}.", f"Therefore, the number of {item} {name} will remain with is {num_items_before_giving} - {num_items_given_away}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
