from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ["Alice", "Bob", "Carlos", "Diana", "Emily", "Frank", "Grace", "Hector", "Isabel", "Jack", "Karen", "Leo"]
    items = ["coffee", "tea", "hot chocolate", "espresso", "latte", "smoothie"]

    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)

    # Randomly generate variables related to the problem
    normal_cost = random.randint(2, 10)  # Normal cost per pound ($)
    percent_increase = random.randint(5, 50)  # Percentage increase (%)
    daily_use = round(random.uniform(0.5, 2.0), 1)  # Pounds per day
    days = random.randint(3, 14)  # Number of days
    donut_cost = random.randint(1, 5)  # Cost of donut ($)

    # Create additional variables for irrelevant information
    favorite_item = random.choice(["bagel", "muffin", "croissant"])
    favorite_item_cost = random.randint(1, 5)
    store_open_year = random.randint(1900, 2023)
    hobby = random.choice(["painting", "cycling", "reading", "gaming"])

    # Construct the premises with variable names in braces
    problem = [
        f"{name} goes to the store to buy some {item}.",
        f"The normal brand of {item} {name} buys costs ${normal_cost} per pound.",
        f"{name} had to buy a more expensive brand that costs {percent_increase}% more since {name}'s favorite brand was sold out.",
        f"{name} decides to buy {days} days' worth of {item} and {name} uses {daily_use} pounds of {item} per day.",
        f"{name} also decided to buy a {favorite_item} for ${donut_cost}."
    ]

    # Construct the question
    question = f"How much did everything cost?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    items2 = ["soda", "juice", "milkshake", "iced tea", "lemonade", "kombucha"]
    item2 = random.choice(items2)
    irrelevant_infos = [
        f"The {favorite_item} usually costs ${favorite_item_cost} but was on sale.",
        f"{name} decided to buy {random.randint(2, 10)} pounds of {item2} but {item2} was out of stock.",
        f"The normal brand of {item2} costs ${normal_cost} per pound.",
    ]

    # Add out-topic irrelevant information
    out_topic_irrelevant_info = f"{name}'s hobby is {hobby} during free time."
    irrelevant_infos.append(out_topic_irrelevant_info)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume that these functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    new_price_per_pound = normal_cost * (1 + percent_increase / 100)
    total_coffee_cost = days * daily_use * new_price_per_pound
    answer = total_coffee_cost + donut_cost

    # Return premise and answer as a dictionary
    cot = [f"The normal cost per pound of {item} is {normal_cost}. The more expensive brand costs {percent_increase}% more, so the new price per pound is {normal_cost} * (1 + {percent_increase} / 100), which is {new_price_per_pound}.", f"{name} buys {days} days' worth of {item}, using {daily_use} pounds per day. Therefore, the total coffee cost is {days} * {daily_use} * {new_price_per_pound}, which is {total_coffee_cost}.", f"{name} also buys a donut for {donut_cost}. Therefore, the total cost is {total_coffee_cost} + {donut_cost}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}

