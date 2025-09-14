from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and items lists
    names = ["Mark", "Alice", "Bob", "Carol", "David", "Eve"]
    items = ["packs of old magic cards", "boxes of rare coins", "bundles of antique stamps", "sets of vintage comic books", "collections of rare baseball cards"]

    # Randomly select a name and item
    name = random.choice(names)
    item = random.choice(items)

    # Generate variables
    attempts = 0
    max_attempts = 10
    profit = -1
    while profit <= 0 and attempts < max_attempts:
        attempts += 1

        num_packs_bought = random.randint(1, 5)
        cost_per_pack = random.randint(10, 30) * 100  # $1000 to $3000

        num_valuable_cards = random.randint(1, 2)
        value_valuable_cards = [random.randint(30, 50) * 100 for _ in range(num_valuable_cards)]  # $3000 to $5000
        value_valuable_cards.sort(reverse=True)

        num_other_cards = random.randint(10, 50)
        avg_value_other_cards = random.randint(1, 10) * 10  # $10 to $100

        total_cost = num_packs_bought * cost_per_pack
        total_income = sum(value_valuable_cards) + num_other_cards * avg_value_other_cards

        profit = total_income - total_cost

    # If after max_attempts profit is still non-positive, set profit to zero
    if profit <= 0:
        profit = 0

    # Construct the premises
    problem = []

    problem.append(f"{name} decides to buy {num_packs_bought} {item} and open them to sell.")

    problem.append(f"{name} buys {num_packs_bought} {item} for ${cost_per_pack} each.")

    if num_valuable_cards == 1:
        problem.append(f"{name} gets 1 card that is worth ${value_valuable_cards[0]}.")
    else:
        problem.append(f"{name} gets 1 card that is worth ${value_valuable_cards[0]} and another card worth ${value_valuable_cards[1]}.")

    problem.append(f"There are {num_other_cards} more cards worth an average of ${avg_value_other_cards} each.")

    # Add the question
    question = f"How much money profit did {name} make?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Construct in-topic irrelevant information
    irrelevant_infos = [
        f"The {item} usually contain {random.randint(5, 15)} cards per pack.",
        f"Unopened {item} are becoming more valuable over time."
    ]

    # Construct out-topic irrelevant information
    cities = ["Paris", "New York", "Tokyo", "Sydney", "Berlin"]
    city = random.choice(cities)
    irrelevant_infos.append(f"{name} plans to travel to {city} next month.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, excluding the first sentence
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Append the question at the end
    problem.append(question)

    # Compute the answer
    total_cost = num_packs_bought * cost_per_pack
    total_income = sum(value_valuable_cards) + num_other_cards * avg_value_other_cards
    answer = total_income - total_cost

    # Return problem and answer
    cot = [f"{name} buys {num_packs_bought} {item} for ${cost_per_pack} each, so the total cost is {num_packs_bought} * {cost_per_pack}, which is {total_cost}.", f"The total income from selling the cards is the sum of the values of the valuable cards, {value_valuable_cards}, plus the value of the other cards, which is {num_other_cards} * {avg_value_other_cards}. This gives a total income of {total_income}.", f"The profit is calculated by subtracting the total cost from the total income, which is {total_income} - {total_cost}, resulting in a profit of {profit}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
