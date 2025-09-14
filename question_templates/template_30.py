from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Names list
    names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Cameron', 'River', 'Skyler', 'Reese', 'Charlie', 'Drew', 'Casey', 'Riley']

    # Items list
    items = ['watermelons', 'peppers', 'oranges', 'apples', 'bananas', 'pears', 'strawberries', 'pineapples', 'grapes', 'tomatoes', 'cucumbers']

    # Randomly select child name and buyer name
    child_name = random.choice(names)
    buyer_name = random.choice([name for name in names if name != child_name])

    # Randomly select three different items
    item_list = random.sample(items, 3)
    item1 = item_list[0]
    item2 = item_list[1]
    item3 = item_list[2]

    # Randomly generate costs and quantities
    pepper_cost = random.randint(5, 20)
    watermelon_cost = 3 * pepper_cost
    orange_cost = watermelon_cost - 5
    while orange_cost <= 0:
        pepper_cost = random.randint(5, 20)
        watermelon_cost = 3 * pepper_cost
        orange_cost = watermelon_cost - 5

    num_watermelons = random.randint(1, 10)
    num_peppers = random.randint(5, 30)
    num_oranges = random.randint(5, 20)

    # Construct the problem sentences
    problem = [
        f"{child_name}'s mother sells {item1}, {item2}, and {item3} at the local store.",
        f"A {item1[:-1]} costs three times what each {item2[:-1]} costs.",
        f"A {item3[:-1]} costs 5 less than what a {item1[:-1]} costs.",
        f"{buyer_name} is sent to the store to buy {num_watermelons} {item1}, {num_peppers} {item2}, and {num_oranges} {item3}.",
    ]
    question=f"What's the total amount of money {buyer_name} will spend if each {item2[:-1]} costs {pepper_cost}$?"
    original_problem=problem.copy()
    original_problem.append(question)

    # Add irrelevant information based on probability
    irrelevant_info_in_topic = [
        f"{child_name}'s mother recently started selling fresh {random.choice(items)} as well.",
        f"The store is known for its high-quality {random.choice(items)}.",
        f"This week, there's a discount on {random.choice(items)}."
    ]

    irrelevant_info_out_topic = [
        f"{buyer_name} enjoys playing soccer on weekends.",
        f"Last summer, {child_name} went on a trip to Europe.",
        f"{buyer_name} has a pet {random.choice(['dog', 'cat', 'parrot', 'rabbit'])} named {random.choice(names)}."
    ]
    irrelevant_infos=irrelevant_info_in_topic + irrelevant_info_out_topic

    for info in irrelevant_info_in_topic + irrelevant_info_out_topic:
        if random.random() < prob_irre:
            problem.append(info)

    # Add symbol or grammar errors. Assume the functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_sentences)
    problem = [first_sentence] + rest_sentences+[question]

    # Calculate the answer
    answer = num_watermelons * watermelon_cost + num_peppers * pepper_cost + num_oranges * orange_cost

    # Return the problem and answer as a dictionary
    cot = [f"The cost of a {item1[:-1]} is three times the cost of a {item2[:-1]}, so {watermelon_cost} = 3 * {pepper_cost}.", f"The cost of a {item3[:-1]} is 5 less than the cost of a {item1[:-1]}, so {orange_cost} = {watermelon_cost} - 5.", f"The total amount of money {buyer_name} will spend is calculated by multiplying the number of each item by its cost and summing them up: {num_watermelons} * {watermelon_cost} + {num_peppers} * {pepper_cost} + {num_oranges} * {orange_cost}, which equals {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
