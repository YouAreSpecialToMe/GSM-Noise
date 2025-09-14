from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define possible names
    names = ['Mr. Smith', 'Mrs. Lee', 'Dr. Brown', 'Ms. Gomez', 'Sir Arthur', 'Lady Jane', 'Professor Green',
             'Captain Marvel']

    # Define possible farm names
    farms = ['Farm Alpha', 'Farm Beta', 'Orchard Farm', 'Green Acres', 'Sunnydale', 'Hidden Valley', 'Maple Farm',
             'Riverbend Farm']

    # Define possible numbers for goats in Farm X and Farm Y
    goats_x_options = list(range(30, 100))
    goats_y_options = list(range(30, 100))

    # Define possible number of goats sold from Farm X
    sold_x_options = list(range(5, 20))

    # Additional variables for in-topic irrelevant info
    additional_animals_options = ['chickens', 'cows', 'sheep', 'ducks', 'pigs', 'horses']
    additional_animals_number_options = list(range(10, 50))

    milk_production_options = list(range(100, 1000))  # liters per day

    # Out-topic irrelevant info
    hobbies = ['chess', 'golf', 'piano', 'painting', 'sailing', 'dancing', 'skating']
    vehicles = ['car', 'bike', 'boat', 'plane', 'motorcycle', 'truck']

    # Randomly assign variables
    name = random.choice(names)
    farm_x = random.choice(farms)
    farms.remove(farm_x)
    farm_y = random.choice(farms)

    goats_x = random.choice(goats_x_options)
    goats_y = random.choice(goats_y_options)
    sold_x = random.choice(sold_x_options)
    sold_y = sold_x * 2  # As per the problem

    # For in-topic irrelevant info
    additional_animals = random.choice(additional_animals_options)
    additional_animals_number = random.choice(additional_animals_number_options)

    milk_production = random.choice(milk_production_options)

    # Out-topic irrelevant info
    hobby = random.choice(hobbies)
    vehicle = random.choice(vehicles)

    # Construct problem sentences
    problem_wq = [
        f"{name} has two farms, {farm_x} and {farm_y}.",
        f"{name} has {goats_x} goats in {farm_x} and {goats_y} goats in {farm_y}.",
        f"{name} sold {sold_x} goats from {farm_x} and twice as many goats from {farm_y}.",
        f"How many goats are left in the two farms altogether?"
    ]

    problem = problem_wq[:-1]
    question = problem[-1]
    original_problem = problem.copy()


    # Construct the in-topic irrelevant info
    irrelevant_info_in_topic = [
        f"{farm_x} also has {additional_animals_number} {additional_animals}.",
        f"{name} sold {sold_x + random.randint(3, 10)} {additional_animals} from {farm_x} and twice as many goats from {farm_y}."
    ]

    # Construct out-topic irrelevant info
    irrelevant_info_out_topic = [
        f"{name} enjoys playing {hobby} in his spare time.",
        f"{name} recently bought a new {vehicle}."
    ]

    # Combine irrelevant infos
    irrelevant_infos = irrelevant_info_in_topic + irrelevant_info_out_topic

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences + [question]

    # Compute the answer
    goats_left_x = goats_x - sold_x
    goats_left_y = goats_y - sold_y
    answer = goats_left_x + goats_left_y

    # Return premise and answer as a dictionary
    cot = [f"{name} sold {sold_x} goats from {farm_x}, so the number of goats left in {farm_x} is {goats_x} - {sold_x}, which is {goats_left_x}.", f"{name} sold twice as many goats from {farm_y}, which is {sold_y} goats. Therefore, the number of goats left in {farm_y} is {goats_y} - {sold_y}, which is {goats_left_y}.", f"The total number of goats left in both farms is {goats_left_x} + {goats_left_y}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
