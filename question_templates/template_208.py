from grammar_error import introduce_grammar_error, introduce_symbol_error

import random


# Done
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ["Alice", "Beth", "Cindy", "Diana", "Emma", "Fiona", "Grace", "Hannah", "Ivy", "Julia", "Sara"]
    items = ['jacket', 'dress', 'sweater', 'coat', 'scarf']
    plural_items = ['pairs of shoes', 'hats', 'bracelets', 'gloves', 'socks']

    # Randomly select a name and items
    name = random.choice(names)
    item1 = random.choice(items)
    item2 = random.choice(plural_items)

    # Define quantities and costs
    quantity_item1 = 1  # Number of item1 to buy
    quantity_item2 = random.randint(1, 5)  # Number of item2 to buy
    cost_item1 = random.randint(100, 200)  # Cost of item1
    cost_item2 = random.randint(10, 50)  # Cost of item2
    babysitting_times = random.randint(2, 6)  # Babysitting times
    babysitting_earning = random.randint(3, 10)  # Earning per babysitting
    mow_earning = random.randint(2, 10)  # Earning per mowing
    initial_savings = random.randint(5, 20)  # Existing savings

    # Other irrelevant variables
    siblings = random.randint(1, 5)
    age = random.randint(10, 18)
    pet = random.choice(['dog', 'cat', 'hamster', 'rabbit'])
    pet_name = random.choice(['Buddy', 'Max', 'Charlie', 'Bella', 'Lucy'])
    favorite_subject = random.choice(['math', 'science', 'history', 'art'])

    # Construct the premise
    problem = [
        f"{name} wants to buy herself {quantity_item1} {item1} and {quantity_item2} {item2}.",
        f"The {item1} {name} wants costs ${cost_item1} and each {item2} costs ${cost_item2}.",
        f"{name} babysits the neighbor's kids {babysitting_times} times, earning ${babysitting_earning} each time {name} babysits them.",
        f"{name}'s parents pay {name} ${mow_earning} each time {name} mows the lawn.",
        f"If {name} already had ${initial_savings} saved before {name} started babysitting,",
    ]

    question = f"How many times must {name} mow the lawn before {name} can afford the {item1} and {item2}?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Create in-topic irrelevant information
    irrelevant_infos = [
        f"{name} has {siblings} siblings.",
        f"{name} is {age} years old.",
        f"{name} has a pet {pet} named {pet_name}.",
        f"{name}'s favorite subject is {favorite_subject}."
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
    initial_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [initial_sentence] + other_sentences + [question]

    # Calculate the answer
    total_cost = quantity_item1 * cost_item1 + quantity_item2 * cost_item2
    total_babysitting = babysitting_times * babysitting_earning
    money_before_mowing = total_babysitting + initial_savings
    money_needed = total_cost - money_before_mowing
    answer = -(-money_needed // mow_earning)  # Ceiling division

    # Return the problem and answer
    cot = [
        f"Calculate the total cost of {quantity_item1} {item1} and {quantity_item2} {item2} by multiplying their quantities with their respective costs: {total_cost} = {quantity_item1} * {cost_item1} + {quantity_item2} * {cost_item2}.",
        f"Calculate the total earnings from babysitting by multiplying the number of times {name} babysits with the earnings per babysitting: {total_babysitting} = {babysitting_times} * {babysitting_earning}.",
        f"Add the initial savings to the total babysitting earnings to find the money {name} has before mowing: {money_before_mowing} = {total_babysitting} + {initial_savings}.",
        f"Subtract the money {name} has before mowing from the total cost to find the money needed: {money_needed} = {total_cost} - {money_before_mowing}.",
        f"Calculate the number of times {name} must mow the lawn by dividing the money needed by the earnings per mowing and rounding up: {answer} = -(-{money_needed} // {mow_earning})."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
