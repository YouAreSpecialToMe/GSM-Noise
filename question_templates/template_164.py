from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error):
    # Define name and item lists
    names = ["Alice", "Brandon", "Catherine", "Daniel", "Evelyn", "Frank", "Grace", "Henry", "Isabella", "Jacob"]
    items = ["used cars", "laptops", "smartphones", "bicycles", "watches", "books", "furniture", "appliances"]


    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)

    # Randomly generate sale-related values
    num_items_sold = random.randint(5, 20)  # Number of items sold
    price_per_item = random.randint(5000, 50000)  # Price per item
    acquisition_cost_percentage = random.randint(20, 60)  # Acquisition cost percentage
    commission_rate = random.randint(5, 15)  # Commission rate percentage

    # Additional variables for irrelevant information
    year = random.randint(1990, 2023)
    total_employees = random.randint(50, 500)
    hobby = random.choice(["painting", "cycling", "photography", "gardening"])
    saving_amount = random.randint(10000, 50000)

    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"{name} gets a job selling {item}.",
        f"{name} sold {num_items_sold} {item} that cost ${price_per_item} each.",
        f"The company paid {acquisition_cost_percentage}% of that price to acquire the {item}.",
        f"{name} got a {commission_rate}% commission on the profits."
    ]

    # Construct the question
    question = f"How much did {name} make?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_items = ["tablets", "headphones", "earphones", "speakers", "cameras", "televisions", "refrigerators"]
    irrelevant_item = random.choice(irrelevant_items)
    irrelevant_infos = [
        f"{irrelevant_item} costs ${random.randint(500, 5000)} in the store.",
        f"The company paid {random.randint(20, 60)}% of the price to acquire {irrelevant_item}.",
        f"{name}'s friend gets a job selling {irrelevant_item}.",
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} enjoys {hobby} in free time and has saved ${saving_amount}.")

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
    rest_sentences = problem[1:]
    random.shuffle(rest_sentences)
    problem = [first_sentence] + rest_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    acquisition_cost_per_item = price_per_item * (acquisition_cost_percentage / 100)
    profit_per_item = price_per_item - acquisition_cost_per_item
    total_profit = profit_per_item * num_items_sold
    answer = total_profit * (commission_rate / 100)

    # Return problem and answer as a dictionary
    cot = [f"The acquisition cost per {item} is {price_per_item} * ({acquisition_cost_percentage} / 100), which is {acquisition_cost_per_item}.", f"The profit per {item} is {price_per_item} - {acquisition_cost_per_item}, which is {profit_per_item}.", f"The total profit from selling {num_items_sold} {item} is {profit_per_item} * {num_items_sold}, which is {total_profit}.", f"The commission {name} makes is {total_profit} * ({commission_rate} / 100), which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}