from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define name and item lists
    names = ["Julia", "Emma", "Sofia", "Olivia", "Liam", "Noah", "Mason", "Ethan", "Michael"]
    item_names = ["plastic spoons", "candles", "wine glasses", "napkins", "forks", "plates"]
    food_items = ["stew", "pasta", "soup", "salad", "curry"]

    # Randomly select names and items
    name = random.choice(names)
    husband_names = [n for n in names if n != name]
    husband = random.choice(husband_names)
    item = random.choice(item_names)
    food = random.choice(food_items)

    # Randomly generate variables
    spoons_in_husband_package = random.randint(3,7)
    spoons_used_cooking = random.randint(1,5)
    spoons_in_julia_package = random.randint(5,15)  # x

    total_spoons = spoons_in_julia_package + spoons_in_husband_package - spoons_used_cooking

    # Alternative variables for irrelevant information
    guests = random.randint(4,20)
    price_spoons_julia = random.randint(2,10) * spoons_in_julia_package  # total cost
    price_spoons_husband = random.randint(2,10) * spoons_in_husband_package

    # Construct the premise content
    problem = [
        f"{name} was preparing for a dinner party at {name}'s house, where {name} intended to serve {food}.",
        f"{name} noticed that {name} was out of {item}, so {name} bought a new package of {item}.",
        f"Later, {name}'s friend {husband} also bought a package of {spoons_in_husband_package} new {item} and gave them to {name}.",
        f"While {name} was making the {food}, {name} used {spoons_used_cooking} of the {item} to sample the {food}.",
        f"Later, when {name} went to set the table, {name} had a total of {total_spoons} {item}."
    ]

    # Construct the question
    question = f"How many {item} were in the package that {name} bought?"
    original_problem=problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} had invited {guests} guests to the dinner party.",
        f"The total cost of the {item} {name} bought was ${price_spoons_julia}.",
        f"{husband} spent ${price_spoons_husband} on the {item} he bought."
    ]

    # Add out-topic irrelevant information
    all_genders = ['boy', 'girl']
    gender = random.choice(all_genders)
    ir_money = random.randint(1000, 5000)
    out_topic_irrelevant_info = f"{name} is a {gender} who has more than ${ir_money} saved up."
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
    first_sentence = problem[0]
    rest_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_sentences)
    problem = [first_sentence] + rest_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    answer = spoons_in_julia_package

    # Return premise and answer as a dictionary
    cot = [f"{name} received {spoons_in_husband_package} {item} from {husband} and used {spoons_used_cooking} {item} while cooking.", f"The total number of {item} {name} had was {total_spoons}.", f"Therefore, the number of {item} in the package that {name} bought is {total_spoons} - {spoons_in_husband_package} + {spoons_used_cooking}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
