from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[13]:


import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ["Alice", "Beth", "Cindy", "Diana", "Emma", "Millie"]
    items = [
        ("lemonade stand", "pitchers", "cups of lemonade", "lemonade"),
        ("cookie stall", "trays", "cookies", "cookies"),
        ("hotdog cart", "packages", "hotdogs", "hotdogs"),
        ("ice cream truck", "boxes", "ice cream cones", "ice cream"),
        ("popcorn stand", "batches", "bags of popcorn", "popcorn")
    ]

    # Randomly select a name and an item
    name = random.choice(names)
    item, container, unit, product = random.choice(items)

    # Randomly generate values
    supply_cost = random.randint(10, 50)  # Cost to buy supplies
    pitchers = random.randint(2, 5)  # Number of containers made
    units_per_container = random.randint(10, 20)  # Units per container
    price_per_unit = random.choice([round(0.5 * i, 2) for i in range(1, 11)])  # Prices from $0.5 to $5.0
    units_sold_per_hour = random.randint(2, units_per_container)  # Units sold per hour

    # Ensure units_sold_per_hour is less than total_units
    total_units = pitchers * units_per_container
    while units_sold_per_hour >= total_units:
        units_sold_per_hour = random.randint(1, total_units - 1)

    # Construct the premise content, breaking it down into sentences
    problem = [
        f"{name} decides to open a {item}.",
        f"{name} spends ${supply_cost} to buy enough supplies to make {pitchers} {container} of {product}.",
        f"Each {container} holds {units_per_container} {unit}.",
        f"{name} sells each {unit} for ${price_per_unit}.",
        f"{name} sells an average of {units_sold_per_hour} {unit} per hour that {name}'s {item} is open."
    ]

    # Construct the question
    question = f"If {name} sells all of the {product}, how much profit will {name} make per hour that {name} spends running the {item}?"
    original_problem = problem.copy()
    original_problem.append(question)
    # Add in-topic irrelevant information
    advertising_cost = random.randint(0, 20)
    irrelevant_infos = [
        f"{name} spends ${advertising_cost} on advertising."
    ]

    # Add out-topic irrelevant information
    age = random.randint(10, 60)
    hobbies = ['playing soccer', 'painting', 'hiking', 'reading books', 'playing the piano']
    hobby = random.choice(hobbies)
    irrelevant_infos.append(f"{name} is {age} years old and likes {hobby}.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (assume functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    fixed_sentence = problem[0]
    remaining_sentences = problem[1:]
    if shuffle:
        random.shuffle(remaining_sentences)
    problem = [fixed_sentence] + remaining_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    total_units = pitchers * units_per_container
    total_revenue = total_units * price_per_unit
    total_profit = total_revenue - supply_cost
    hours_spent = total_units / units_sold_per_hour
    answer = total_profit / hours_spent
    answer = round(answer, 2)

    # Return problem and answer as a dictionary
    cot = [
        f"Calculate the total number of {unit} by multiplying {pitchers} by {units_per_container}, which gives {total_units}.",
        f"Calculate the total revenue by multiplying {total_units} by {price_per_unit}, resulting in {total_revenue}.",
        f"Calculate the total profit by subtracting {supply_cost} from {total_revenue}, which gives {total_profit}.",
        f"Calculate the hours spent by dividing {total_units} by {units_sold_per_hour}, resulting in {hours_spent}.",
        f"Finally, calculate the profit per hour by dividing {total_profit} by {hours_spent}, which equals {answer}."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
