from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible alternative values
    names = ["Tyson", "Evelyn", "Mohammed", "Li", "Anika", "Carlos", "Fatima", "Sven"]
    sandwich_types = ["muffaletta sandwiches", "club sandwiches", "paninis", "tacos", "pita wraps"]
    meat_costs = [5.0, 6.0, 7.0, 8.0, 9.0]  # per pound
    cheese_costs = [2.0, 3.0, 4.0, 5.0]  # per pound
    meat_per_sandwiches = [0.5, 1.0, 1.5, 2.0]  # pounds per sandwich
    people_per_sandwiches = [2, 4, 5, 6]
    total_people_options = [10, 15, 20, 25, 30, 35, 40]
    other_food_items = ["salad", "fruit platter", "nachos", "cookies", "brownies"]
    bread_costs = [1.0, 1.5, 2.0, 2.5]
    game_durations = [2, 3, 4, 5]
    majors = ["engineering", "biology", "history", "mathematics"]
    number_of_pets_options = [0, 1, 2, 3]

    # Randomly select values
    name = random.choice(names)
    sandwich_type = random.choice(sandwich_types)
    meat_cost = random.choice(meat_costs)
    cheese_cost = random.choice(cheese_costs)
    meat_per_sandwich = random.choice(meat_per_sandwiches)
    cheese_per_sandwich = meat_per_sandwich  # Assuming equal amounts of meat and cheese
    people_per_sandwich = random.choice(people_per_sandwiches)
    total_people = random.choice(total_people_options)

    other_food_item = random.choice(other_food_items)
    bread_cost = random.choice(bread_costs)
    game_duration = random.choice(game_durations)
    major_subject = random.choice(majors)
    number_of_pets = random.choice(number_of_pets_options)

    # Construct the premise content, breaking it down into individual sentences
    problem = [
        f"{name} decided to make {sandwich_type} for the big game.",
        f"Each sandwich required {meat_per_sandwich} pound(s) each of meat and cheese and would serve {people_per_sandwich} people.",
        f"There would be {total_people} people in total watching the game.",
        f"The meat cost ${meat_cost} per pound and the cheese cost ${cheese_cost} per pound."
    ]

    # Construct the question
    question = f"How much money would {name} spend on the meat and cheese to make enough sandwiches to serve {total_people} people?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The bread for each sandwich costs ${bread_cost} per loaf.",
        f"{name} also made {other_food_item} for the game.",
        f"{other_food_item} cost ${cheese_cost + random.randint(3, 10)} per pound."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} is studying {major_subject} in college.")
    irrelevant_infos.append(f"{name} has {number_of_pets} pet(s).")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors, assume the functions are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    remaining_sentences = problem[1:]
    if shuffle:
        random.shuffle(remaining_sentences)
    problem = [first_sentence] + remaining_sentences

    # Add the question at the end
    problem.append(question)

    # Calculate the answer
    sandwiches_needed = total_people / people_per_sandwich
    total_meat = sandwiches_needed * meat_per_sandwich
    total_cheese = sandwiches_needed * cheese_per_sandwich
    total_meat_cost = total_meat * meat_cost
    total_cheese_cost = total_cheese * cheese_cost
    answer = total_meat_cost + total_cheese_cost

    # Return the problem and answer
    cot = [f"Calculate the number of sandwiches needed by dividing {total_people} by {people_per_sandwich}, which gives {sandwiches_needed}.", f"Calculate the total amount of meat needed by multiplying {sandwiches_needed} by {meat_per_sandwich}, resulting in {total_meat}.", f"Calculate the total amount of cheese needed by multiplying {sandwiches_needed} by {cheese_per_sandwich}, resulting in {total_cheese}.", f"Calculate the total cost of meat by multiplying {total_meat} by {meat_cost}, which gives {total_meat_cost}.", f"Calculate the total cost of cheese by multiplying {total_cheese} by {cheese_cost}, which gives {total_cheese_cost}.", f"Add {total_meat_cost} and {total_cheese_cost} to find the total cost, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}

