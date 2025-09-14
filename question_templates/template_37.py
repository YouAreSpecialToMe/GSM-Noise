from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define name and item lists
    names = ["James", "Alice", "Juan", "Li", "Fatima", "Sanjay", "Olivia", "Wei", "Mohammed", "Aisha"]
    suit_items = ["suits", "jackets", "blazers", "coats"]
    pants_items = ["dress pants", "trousers", "slacks", "jeans"]
    shirt_items = ["dress shirts", "shirts", "blouses", "t-shirts"]
    
    # Randomly select a name and items
    name = random.choice(names)
    suit_item = random.choice(suit_items)
    pants_item = random.choice(pants_items)
    shirt_item = random.choice(shirt_items)
    
    # Randomly generate quantities and prices
    num_suits = random.randint(5, 20)  # Number of suits
    num_pants = random.randint(5, 20)  # Number of pants
    shirts_per_suit = random.randint(1, 5)  # Shirts per suit
    suit_cost = random.randint(500, 1000)  # Cost per suit
    shirt_cost = random.randint(30, 150)  # Cost per shirt
    pants_cost_denominator = random.randint(2, 6)  # Pants cost is 1/n of suit cost
    
    # Additional variables for irrelevant info
    accessory_items = ["ties", "belts", "hats", "scarves"]
    num_accessories = random.randint(1, 10)
    accessory_cost = random.randint(10, 100)  # Cost per accessory
    favorite_color = random.choice(["red", "blue", "green", "black", "white", "yellow"])
    hobby = random.choice(["painting", "cycling", "reading", "swimming", "gaming"])
    
    # Construct the premises, replacing values with variables
    problem = [
        f"{name} buys a new wardrobe.",
        f"{name} buys {num_suits} {suit_item} and {num_pants} {pants_item}.",
        f"{name} also buys {shirts_per_suit} {shirt_item} per {suit_item[:-1]}.",
        f"The {suit_item} cost ${suit_cost} each and the {pants_item} cost 1/{pants_cost_denominator} that cost.",
        f"The {shirt_item} were ${shirt_cost} each."
    ]
    
    # Construct the question
    question = f"How much did everything cost?"
    original_problem=problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} also considered buying {num_accessories} {random.choice(accessory_items)}, but decided against it.",
        f"The store was offering a special discount on {random.choice(accessory_items)}."
    ]
    
    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} enjoys {hobby} in {name}'s free time.")
    irrelevant_infos.append(f"{name}'s favorite color is {favorite_color}.")
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors. You can assume that introduce_symbol_error and introduce_grammar_error functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences, except for the first one
    if len(problem) > 1:
        first_sentence = problem[0]
        other_sentences = problem[1:]
        if shuffle:
            random.shuffle(other_sentences)
        problem = [first_sentence] + other_sentences
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    total_suit_cost = num_suits * suit_cost
    pants_cost = suit_cost / pants_cost_denominator
    total_pants_cost = num_pants * pants_cost
    num_shirts = shirts_per_suit * num_suits
    total_shirt_cost = num_shirts * shirt_cost
    answer = total_suit_cost + total_pants_cost + total_shirt_cost
    
    # Return problem and answer as a dictionary
    cot = [f"{name} buys {num_suits} {suit_item}, each costing {suit_cost}. Therefore, the total cost for the {suit_item} is {num_suits} * {suit_cost}, which is {total_suit_cost}.", f"The {pants_item} cost 1/{pants_cost_denominator} of the {suit_item} cost. Therefore, each {pants_item} costs {suit_cost} / {pants_cost_denominator}, which is {pants_cost}.", f"The total cost for the {num_pants} {pants_item} is {num_pants} * {pants_cost}, which is {total_pants_cost}.", f"{name} buys {shirts_per_suit} {shirt_item} per {suit_item[:-1]}, resulting in a total of {shirts_per_suit} * {num_suits} {shirt_item}, which is {num_shirts}.", f"The total cost for the {shirt_item} is {num_shirts} * {shirt_cost}, which is {total_shirt_cost}.", f"Therefore, the total cost for everything is {total_suit_cost} + {total_pants_cost} + {total_shirt_cost}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
