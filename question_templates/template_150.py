from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Charlie", "Sam", "Jamie", "Robin"]
    items = ["sticker", "postcard", "stamp", "coin", "pin", "badge"]
    designs = ["snowflake", "truck", "rose", "star", "butterfly", "cat", "dog", "flower", "heart", "ship"]
    
    # Randomly select a name and an item
    name = random.choice(names)
    names.remove(name)
    item = random.choice(items)
    
    # Randomly select three different designs
    design_choices = designs.copy()
    random.shuffle(design_choices)
    design_1 = design_choices.pop()
    design_2 = design_choices.pop()
    design_3 = design_choices.pop()
    
    # Randomly generate quantities
    design_1_qty = random.randint(5, 30)  # Base quantity
    delta_1 = random.randint(1, 10)  # Difference between design_1_qty and design_2_qty
    delta_2 = random.randint(5, 15)  # Difference between design_2_qty and design_3_qty
    
    design_2_qty = design_1_qty + delta_1
    design_3_qty = design_2_qty - delta_2
    
    # Construct the premise content, replacing pronouns with names
    problem = [
        f"{name} bought {design_1_qty} {design_1} {item}s at the store.",
        f"{name} bought {delta_1} more {design_2} {item}s than {design_1} {item}s.",
        f"{name} bought {delta_2} fewer {design_3} {item}s than {design_2} {item}s."
    ]
    
    # Construct the question
    question = f"How many {item}s did {name} buy in all?"

    original_problem = problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name}'s friend {random.choice(names)} bought {random.randint(1, 10)} more {design_1} {item}s than {name}.",
        f"{name}'s friend {random.choice(names)} bought {random.randint(1, 10)} fewer {design_2} {item}s than {name}.",
        f"{name} bought {random.randint(1, 10)} {design_3} {item}s at another store last month.",
    ]
    
    # Add out-topic irrelevant information
    pets = ["dog", "cat", "parrot", "hamster", "rabbit"]
    pet = random.choice(pets)
    pet_name = random.choice(names)
    out_topic_irrelevant_info = f"{name} has a pet {pet} named {pet_name}."
    irrelevant_infos.append(out_topic_irrelevant_info)
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors; assume these functions are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences
    if shuffle:
        random.shuffle(problem)
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    answer = design_1_qty + design_2_qty + design_3_qty
    
    # Return premise and answer as a dictionary
    cot = [f"{name} bought {design_1_qty} {design_1} {item}s.", f"{name} bought {delta_1} more {design_2} {item}s than {design_1} {item}s, which means {design_2_qty} {design_2} {item}s.", f"{name} bought {delta_2} fewer {design_3} {item}s than {design_2} {item}s, which means {design_3_qty} {design_3} {item}s.", f"In total, {name} bought {design_1_qty} + {design_2_qty} + {design_3_qty} {item}s, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
