from grammar_error import introduce_grammar_error, introduce_symbol_error

import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and items
    names = ["Mr. Johnson", "Mr. Smith", "Mr. Lee", "Mr. Patel", "Mr. García", "Mr. Chen"]
    friend_names = ["his friend", "his colleague", "his neighbor", "his brother", "his cousin"]
    items = ["watch", "bracelet", "necklace", "ring", "painting", "vase", "sculpture"]

    # Randomly select a name and an item
    name = random.choice(names)
    friend = random.choice(friend_names)
    item = random.choice(items)

    # Randomly generate original price, discount and selling percentages
    original_price = random.randint(1000, 5000)
    discount_percentage = random.choice([70, 75, 80, 85, 90])  # For variety
    selling_percentage = random.choice([110, 115, 120, 125])  # For variety

    # Construct irrelevant variables
    other_item_price = random.randint(500, 3000)
    other_year = random.randint(2000, 2023)

    # Break the problem into premises
    problem = [
        f"A ${original_price} {item} was put on sale so that {name} bought it at {discount_percentage}% of its original price.",
        f"{name} then sold the {item} to {friend} at {selling_percentage}% of the price that {name} bought it.",

    ]
    question = f"What is the percentage discount obtained by {friend} from the original price?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Construct irrelevant information
    irrelevant_infos = [
        f"{name} also bought a different item for ${other_item_price}.",
        f"The {item} was originally made in {other_year}.",
        f"{friend} enjoys playing tennis on weekends.",
        f"{name} has been working at his company for 10 years."
    ]

    # Add irrelevant information based on probability
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.insert(random.randint(0, len(problem) - 1), info)

    # Add symbol or grammar errors. Assume that these functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of statements except for the question
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem + [question]

    # Calculate the answer
    price_bought = original_price * discount_percentage / 100
    price_sold = price_bought * selling_percentage / 100
    discount_obtained = (original_price - price_sold) / original_price * 100
    answer = round(discount_obtained, 2)

    # Return the problem and the answer
    cot = [
        f"{name} bought the {item} at {discount_percentage}% of its original price, which is {original_price} * {discount_percentage} / 100, resulting in {price_bought}.",
        f"{name} then sold the {item} to {friend} at {selling_percentage}% of the price he bought it, which is {price_bought} * {selling_percentage} / 100, resulting in {price_sold}.",
        f"The percentage discount obtained by {friend} from the original price is calculated as ({original_price} - {price_sold}) / {original_price} * 100, which is {discount_obtained}.",
        f"Therefore, the final answer is rounded to {answer}."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
