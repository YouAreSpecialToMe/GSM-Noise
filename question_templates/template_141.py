from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name list
    names = ["Alice", "Bob", "Cindy", "David", "Eve", "Frank", "Georgia", "Henry", "Irene", "Jack"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly generate plant-related values
    num_plants = random.randint(10, 50)  # Total number of plants
    num_plants_half_cup = random.randint(1, num_plants // 4)
    num_plants_one_cup = random.randint(1, num_plants // 2)
    num_plants_quarter_cup = num_plants - num_plants_half_cup - num_plants_one_cup
    if num_plants_quarter_cup < 0:
        num_plants_quarter_cup = 0
        num_plants = num_plants_half_cup + num_plants_one_cup
        
    # Construct the premise content
    problem = [
        f"{name}'s plants need to be watered every day.",
        f"She has {num_plants} plants.",
        f"{num_plants_half_cup} of her plants need half of a cup of water.",
        f"{num_plants_one_cup} plants need 1 cup of water.",
        f"The rest need a quarter of a cup of water."
    ]
    
    # Construct the question
    question = f"How many cups of water does {name} need every day for her plants?"

    original_problem = problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    animals_to_water = [
        "horses",
        "cattle",
        "sheep",
        "goats",
        "pigs",
        "chickens",
        "ducks",
        "rabbits",
        "dogs",
        "cats",
        "llamas",
        "alpacas",
        "turkeys",
        "guinea fowl",
        "quail",
        "donkeys",
        "mules",
        "guinea pigs",
        "hamsters",
        "gerbils",
        "ferrets",
        "parrots",
        "canaries",
        "finches"
    ]
    animal = random.choice(animals_to_water)
    irrelevant_infos = [
        f"{name} bought a new watering can that holds 10 cups of water.",
        f"She also needs to water her {animal} every day that drink {random.randint(1, 5)} cups of water each.",
        f"{name} has a garden with {random.randint(5, 20)} different types of animals that need to be watered every day."
    ]
    
    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} is planning to visit her grandparents next month.")
    
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
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    answer = (num_plants_half_cup * 0.5) + (num_plants_one_cup * 1) + (num_plants_quarter_cup * 0.25)
    
    # Return premise and answer as a dictionary
    cot = [f"{num_plants_half_cup} of {name}'s plants need half a cup of water each, which totals to {num_plants_half_cup} * 0.5 cups.", f"{num_plants_one_cup} of {name}'s plants need 1 cup of water each, which totals to {num_plants_one_cup} * 1 cups.", f"The remaining {num_plants_quarter_cup} plants need a quarter of a cup of water each, which totals to {num_plants_quarter_cup} * 0.25 cups.", f"Adding these amounts gives the total water needed: ({num_plants_half_cup} * 0.5) + ({num_plants_one_cup} * 1) + ({num_plants_quarter_cup} * 0.25) = {answer} cups."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}