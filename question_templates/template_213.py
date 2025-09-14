from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
# Done
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ["Frederick", "Alice", "Benjamin", "Clara", "Daniel", "Evelyn", "George", "Hannah"]
    items = ["popsicle sticks", "toy cars", "wooden spoons", "birdhouses", "bookends"]

    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)

    # Randomly generate quantities and costs
    quantity_small = random.choice([100, 200, 300])
    quantity_large = random.choice([400, 500, 600])
    percent_spend = random.choice([10, 20, 30])
    cost_small = random.choice([1, 2, 3, 4])
    cost_large = random.choice([5, 6, 7, 8])
    total_money = random.choice([24, 30, 36])

    # Ensure that the small piece is cheaper per piece
    if cost_small >= cost_large:
        cost_small, cost_large = cost_large, cost_small

    # Ensure that the large piece gives more items per dollar
    while (quantity_small / cost_small) >= (quantity_large / cost_large):
        quantity_large += random.choice([50, 100])

    # Construct the premises
    problem = [
        f"{name} is making {item} to sell and to save money {name} is making {name}'s own {item}.",
        f"{name} can get {quantity_small} {item} from a small piece of wood and {quantity_large} {item} from a large piece of wood.",
        f"{name} has ${total_money} to buy wood for {item}.",
        f"A small piece of wood costs ${cost_small}.",
        f"A large piece of wood costs ${cost_large}."
    ]

    # Construct irrelevant information
    irrelevant_infos = [
        f"{name} plans to sell the {item} at the local fair and use {percent_spend}% of the money to buy some new cloth.",
        f"The {item} are popular gifts during holidays.",
        f"{name} started making {item} as a hobby."
    ]

    # Add in-topic irrelevant information
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

    # Shuffle the premises except the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences

    # Construct the question
    question = f"What is the most {item} {name} can make if {name} buys the cheapest lumber?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Add the question to the problem
    problem.append(question)

    # Calculate the answer
    number_of_large_pieces = total_money // cost_large
    total_items = number_of_large_pieces * quantity_large + (total_money - number_of_large_pieces * cost_large) // cost_small * quantity_small
    answer = total_items

    # Return the problem and the answer
    cot = [f"Calculate how many large pieces of wood {name} can buy with {total_money} by dividing {total_money} by {cost_large}, which gives {number_of_large_pieces}.", f"Calculate the total number of {item} from the large pieces by multiplying {number_of_large_pieces} by {quantity_large}.", f"Calculate the remaining money after buying large pieces by subtracting {number_of_large_pieces} * {cost_large} from {total_money}.", f"Calculate how many small pieces of wood can be bought with the remaining money by dividing it by {cost_small}.", f"Calculate the total number of {item} from the small pieces by multiplying the number of small pieces by {quantity_small}.", f"Add the total number of {item} from large and small pieces to get {total_items}.", f"Therefore, the most {item} {name} can make is {total_items}, which is the final answer."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
