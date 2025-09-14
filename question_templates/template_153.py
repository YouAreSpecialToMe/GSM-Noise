from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define possible names and vehicles
    names = ["Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah", "Bill"]
    vehicles = ["truck", "SUV", "sedan", "convertible", "motorcycle", "van"]

    # Randomly select a name and a vehicle
    name = random.choice(names)
    vehicle = random.choice(vehicles)

    # Define features
    features = ["king cab upgrade", "towing package", "leather seats", "running boards",
                "upgraded exterior light package"]

    leather_percent = random.randint(30, 100)

    # Randomly generate base price and feature costs
    base_price = random.randint(20000, 50000)  # Base price of vehicle
    king_cab_upgrade_cost = random.randint(5000, 10000)  # King cab upgrade cost
    leather_seats_cost = king_cab_upgrade_cost * leather_percent / 100  # Leather seats cost
    running_boards_less = random.randint(100, round(leather_seats_cost))
    running_boards_cost = leather_seats_cost - 500  # Running boards cost
    exterior_light_package_cost = random.randint(1000, 2000)  # Exterior light package cost

    # Decide towing package cost (could be zero)
    include_towing_package = random.choice([True, False])
    if include_towing_package:
        towing_package_cost = random.randint(500, 2000)
    else:
        towing_package_cost = 0

    # Break down the problem into premises and replace values with variable names
    problem_sentences = []
    problem_sentences.append(f"{name} is ordering a new {vehicle}.")
    problem_sentences.append(
        f"{name} has decided to purchase a two-ton {vehicle} with several added features: {', '.join(features)}.")
    problem_sentences.append(
        f"The base price of the {vehicle} is ${base_price}, and the other features are at extra cost.")
    problem_sentences.append(
        f"The king cab upgrade is an extra ${king_cab_upgrade_cost}." 
        f"Leather seats are {leather_percent}% the cost of the king cab upgrade."
        f"Running boards are ${running_boards_less} less than the leather seats."
        f"The upgraded exterior light package is ${exterior_light_package_cost}.")

    if towing_package_cost > 0:
        problem_sentences.append(f"The towing package costs an additional ${towing_package_cost}.")
    else:
        problem_sentences.append(f"The towing package is included at no extra cost.")

    # Construct the question
    question = f"What is the total cost of {name}'s new {vehicle}, in dollars?"

    original_problem = problem_sentences.copy()
    original_problem.append(question)

    # Add in-topic and out-topic irrelevant information
    # In-topic irrelevant information
    fuel_efficiency = random.randint(15, 35)  # Example of in-topic irrelevant info
    color = random.choice(["red", "blue", "black", "white", "silver", "green"])

    in_topic_irrelevant_info = [
        f"{name}'s friend with auto-driving costs ${random.randint(1000, 5000)} more than the {vehicle}.",
        f"The base price of the {vehicle} is ${base_price-random.randint(1000, 5000)} last year but now changed.",
    ]

    # Out-topic irrelevant information
    pet = random.choice(["dog", "cat", "parrot", "rabbit", "hamster"])
    out_topic_irrelevant_info = f"{name} has a pet {pet} at home."

    irrelevant_infos = in_topic_irrelevant_info + [out_topic_irrelevant_info]

    # Randomly include irrelevant information based on prob_irre
    if random.random() < prob_irre:
        problem_sentences.append(random.choice(in_topic_irrelevant_info))

    if random.random() < prob_irre:
        problem_sentences.append(out_topic_irrelevant_info)

    # Introduce symbol or grammar errors
    problem_sentences = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        )
        for sentence in problem_sentences
    ]

    # Shuffle the sentences after the first one
    main_sentences = problem_sentences[1:]
    if shuffle:
        random.shuffle(main_sentences)
    problem_sentences = [problem_sentences[0]] + main_sentences + [question]

    # Calculate the answer using the variables
    # Leather seats cost is one-third of king cab upgrade cost
    # leather_seats_cost = king_cab_upgrade_cost / 3

    # Running boards cost is $500 less than leather_seats_cost
    # running_boards_cost = leather_seats_cost - 500

    # Total cost is sum of base price and all feature costs
    answer = base_price + king_cab_upgrade_cost + leather_seats_cost + running_boards_cost + exterior_light_package_cost + towing_package_cost

    # Return the problem and answer
    cot = [f"The cost of leather seats is one-third of the king cab upgrade cost, which is {king_cab_upgrade_cost} / 3, resulting in {leather_seats_cost}.", f"The cost of running boards is $500 less than the leather seats, which is {leather_seats_cost} - 500, resulting in {running_boards_cost}.", f"The total cost of {name}'s new {vehicle} is the sum of the base price, king cab upgrade cost, leather seats cost, running boards cost, exterior light package cost, and towing package cost, which is {base_price} + {king_cab_upgrade_cost} + {leather_seats_cost} + {running_boards_cost} + {exterior_light_package_cost} + {towing_package_cost}, resulting in {answer}."]
    
    return {"cot": cot, 'problem': problem_sentences, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
