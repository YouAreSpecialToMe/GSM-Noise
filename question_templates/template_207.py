from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
# Done
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Names
    names = ['Julia', 'Nadine', 'Alice', 'Beth', 'Cindy', 'Diana', 'Emily', 'Fiona', 'Grace', 'Hannah']
    name1, name2 = random.sample(names, 2)

    # Items
    items1 = ['cake', 'pie', 'present', 'book', 'toy']
    item1 = random.choice(items1)

    items2 = ['balloons', 'candles', 'flowers', 'cards', 'ribbons']
    item2 = random.choice(items2)

    items3 = ['tubs of ice cream', 'boxes of chocolates', 'bags of candies', 'packets of cookies', 'bottles of juice']
    item3 = random.choice(items3)

    # Original variable values
    cost_item1_original = 11
    quantity_item2_original = 12
    price_item2_original = 0.5
    quantity_price_item2_original = 2
    quantity_item3_original = 2
    price_item3_original = 7

    # Variables with possible alternative values
    cost_item1_options = [5, 8, 11, 14, 17, 20]
    quantity_item2_options = [6, 12, 18, 24]
    price_item2_options = [0.25, 0.5, 0.75, 1.0]
    quantity_price_item2_options = [2, 4, 6]
    quantity_item3_options = [1, 2, 3, 4]
    price_item3_options = [5, 7, 9, 11]

    # Ensure original values are included
    if cost_item1_original not in cost_item1_options:
        cost_item1_options.append(cost_item1_original)
    if quantity_item2_original not in quantity_item2_options:
        quantity_item2_options.append(quantity_item2_original)
    if price_item2_original not in price_item2_options:
        price_item2_options.append(price_item2_original)
    if quantity_price_item2_original not in quantity_price_item2_options:
        quantity_price_item2_options.append(quantity_price_item2_original)
    if quantity_item3_original not in quantity_item3_options:
        quantity_item3_options.append(quantity_item3_original)
    if price_item3_original not in price_item3_options:
        price_item3_options.append(price_item3_original)

    # Randomly select variable values
    cost_item1 = random.choice(cost_item1_options)
    quantity_item2 = random.choice(quantity_item2_options)
    price_item2 = random.choice(price_item2_options)
    quantity_price_item2 = random.choice(quantity_price_item2_options)
    quantity_item3 = random.choice(quantity_item3_options)
    price_item3 = random.choice(price_item3_options)
    cost_no = random.randint(5, 20)
    # Construct the problem
    problem = [
        f"{name1} and {name2} were given the same amount of allowance by their mother.",
        f"The two girls decided to combine their allowance to surprise their father on his birthday.",
        f"They bought a {item1} which costs ${cost_item1}.",
        f"They also bought {quantity_item2 * quantity_price_item2} {item2} which were sold for ${price_item2} for {quantity_price_item2} {item2}.",
        f"The remaining money was used to buy {quantity_item3} {item3} for ${price_item3} each."
    ]

    question = f"How much did {name1} and {name2}'s mother give each one of them?"
    original_problem = problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"{name1} and {name2} thought about buying a {random.choice(items1)} with a cost of {cost_no}but decided not to.",
        f"The store was offering a discount on {item2} that day."
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"It was a sunny day when {name1} and {name2} went to the store.",
        f"{name1} and {name2} are both in grade {random.randint(1, 12)}.",
        f"Their favorite subject is {random.choice(['math', 'science', 'art', 'music'])}."
    ]

    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Randomly add irrelevant information
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

    # Shuffle sentences except the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question
    problem.append(question)

    # Calculate the answer

    total_cost_item2 = quantity_item2 * price_item2
    total_cost_item3 = quantity_item3 * price_item3
    total_spent = cost_item1 + total_cost_item2 + total_cost_item3
    answer = total_spent / 2

    # Return the problem and answer
    cot = [f"Calculate the total cost of {item2} by multiplying {quantity_item2} by {price_item2}, which gives {total_cost_item2}.", f"Calculate the total cost of {item3} by multiplying {quantity_item3} by {price_item3}, which gives {total_cost_item3}.", f"Add the cost of {item1}, {total_cost_item2}, and {total_cost_item3} to get the total amount spent, which is {total_spent}.", f"Divide the total amount spent by 2 to find out how much {name1} and {name2}'s mother gave each one of them, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
