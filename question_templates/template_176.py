from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and firms
    names = ["Angela", "Bob", "Carol", "David", "Emily", "Frank", "Grace", "Hector", "Isabella", "John"]
    firms = ["interior design firm", "home renovation company", "decor services", "installation specialists"]

    # Randomly select a name and a firm
    name = random.choice(names)
    firm = random.choice(firms)

    # Randomly generate costs and quantities
    standard_cost = random.uniform(100.0, 200.0)  # Standard installation cost
    extra_item_cost = random.uniform(10.0, 25.0)  # Cost per additional item

    # Standard included items
    standard_mirrors = random.randint(2, 5)
    standard_shelves = random.randint(1, 4)
    standard_chandeliers = random.randint(1, 2)
    standard_pictures = random.randint(5, 15)

    # Customer's required items
    customer_mirrors = standard_mirrors + random.randint(0, 5)
    customer_shelves = standard_shelves + random.randint(0, 3)
    customer_chandeliers = standard_chandeliers + random.randint(0, 2)
    customer_pictures = standard_pictures + random.randint(0, 10)

    # Construct the premise content
    problem = [
        f"An {firm} offers installation for ${standard_cost:.2f}.",
        f"It includes hanging {standard_mirrors} mirrors, {standard_shelves} shelves, {standard_chandeliers} chandeliers, and {standard_pictures} pictures.",
        f"They will install additional items for an extra ${extra_item_cost:.2f} per item.",
        f"{name} has {customer_mirrors} mirrors, {customer_shelves} shelves, {customer_chandeliers} chandeliers, and {customer_pictures} pictures that {name} needs installed/hung."
    ]

    # Construct the question
    question = f"How much will this cost {name}?"
    original_problem = problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    in_topic_irrelevant_info = [
        f"The {firm} provides a 1-year warranty on all installations.",
        f"The standard package includes a free consultation session."
    ]

    # Out-of-topic irrelevant information
    out_topic_irrelevant_info = [
        f"{name} is planning a vacation next summer.",
        f"{name} enjoys painting in free time."
    ]

    # Add irrelevant information based on probability
    irrelevant_infos = []
    for info in in_topic_irrelevant_info + out_topic_irrelevant_info:
        if random.random() < prob_irre:
            irrelevant_infos.append(info)

    problem.extend(irrelevant_infos)

    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question
    problem.append(question)

    # Calculate the extra items
    extra_mirrors = max(0, customer_mirrors - standard_mirrors)
    extra_shelves = max(0, customer_shelves - standard_shelves)
    extra_chandeliers = max(0, customer_chandeliers - standard_chandeliers)
    extra_pictures = max(0, customer_pictures - standard_pictures)
    total_extra_items = extra_mirrors + extra_shelves + extra_chandeliers + extra_pictures

    # Calculate the answer
    answer = standard_cost + (total_extra_items * extra_item_cost)

    # Return the problem and answer
    cot = [f"Calculate the extra mirrors: {extra_mirrors} = max(0, {customer_mirrors} - {standard_mirrors}).", f"Calculate the extra shelves: {extra_shelves} = max(0, {customer_shelves} - {standard_shelves}).", f"Calculate the extra chandeliers: {extra_chandeliers} = max(0, {customer_chandeliers} - {standard_chandeliers}).", f"Calculate the extra pictures: {extra_pictures} = max(0, {customer_pictures} - {standard_pictures}).", f"Calculate the total extra items: {total_extra_items} = {extra_mirrors} + {extra_shelves} + {extra_chandeliers} + {extra_pictures}.", f"Calculate the total cost: {answer} = {standard_cost} + ({total_extra_items} * {extra_item_cost})."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
