from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define names and items
    names = ["Gene", "Alice", "Bob", "Sophia", "Liam", "Emma", "Noah", "Olivia", "Mason", "Ava"]
    items = ["quilt", "scrapbook", "photo album", "memory collage"]
    materials = ["old souvenir t-shirts", "postcards", "photographs", "concert tickets", "movie stubs"]

    # Randomly select name, item, and material
    name = random.choice(names)
    item = random.choice(items)
    material = random.choice(materials)

    # Generate core variables
    start_age = random.randint(10, 30)
    current_age = random.randint(start_age + 1, start_age + 20)
    vacations_per_year = random.randint(1, 6)

    # Irrelevant variables
    favorite_color = random.choice(["red", "blue", "green", "yellow", "purple"])
    pet_name = random.choice(["Buddy", "Charlie", "Max", "Luna", "Bella"])
    pet_type = random.choice(["dog", "cat", "parrot", "rabbit"])

    # Construct the premises
    problem = [
        f"{name} is sewing a {item} out of {material}.",
        f"{name} has one piece from each vacation {name} has been on.",
        f"Every piece is its own block in the {item}.",
        f"Each row is made of blocks from a different year of vacations.",
        f"{name} goes on {vacations_per_year} vacations a year and has been vacationing since {name} was {start_age} years old.",
        f"{name} is now {current_age} years old."
    ]

    # Construct the question
    question = f"How many blocks does {name} have in total?"
    original_problem=problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} prefers to use fabrics in {favorite_color} color.",
        f"{name} often travels with a {pet_type} named {pet_name}.",
        f"{name} enjoys cooking and recently won a baking competition."
    ]

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
    first_premise = problem[0]
    other_premises = problem[1:]
    if shuffle:
        random.shuffle(other_premises)
    problem = [first_premise] + other_premises

    # Add the question
    problem.append(question)

    # Calculate the answer
    years_of_vacationing = current_age - start_age
    total_vacations = vacations_per_year * years_of_vacationing
    answer = total_vacations

    # Return the problem and answer
    cot = [f"Calculate the number of years {name} has been vacationing by subtracting {start_age} from {current_age}, which gives {years_of_vacationing}.", f"Multiply the number of vacations per year, {vacations_per_year}, by the number of years of vacationing, {years_of_vacationing}, to get the total number of quilt blocks, {total_vacations}.", f"Therefore, the total number of quilt blocks {name} has is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}