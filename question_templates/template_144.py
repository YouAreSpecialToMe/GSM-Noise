from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names
    names = ["Marcel", "Alex", "John", "Carlos", "Kumar", "Akira", "Vladimir", "Pierre", "Jake", "Li", "Ahmed", "Omar"]
    name = random.choice(names)
    
    # Define item sets with relationships
    item_sets = [
        {
            'types': ('MTB', 'BMX', 'Trekking Bike'),
            'prices': {'MTB': 500, 'Trekking Bike': 450},
            'relation': {'BMX': lambda MTB_price: MTB_price / 2}
        },
        {
            'types': ('Laptop', 'Tablet', 'Desktop'),
            'prices': {'Laptop': 1000, 'Desktop': 800},
            'relation': {'Tablet': lambda Laptop_price: Laptop_price / 2}
        },
        {
            'types': ('Guitar', 'Ukulele', 'Bass'),
            'prices': {'Guitar': 600, 'Bass': 550},
            'relation': {'Ukulele': lambda Guitar_price: Guitar_price / 2}
        },
        {
            'types': ('Sofa', 'Armchair', 'Dining Table'),
            'prices': {'Sofa': 1200, 'Dining Table': 950},
            'relation': {'Armchair': lambda Sofa_price: Sofa_price / 2}
        },
        {
            'types': ('Smartphone', 'Smartwatch', 'Tablet'),
            'prices': {'Smartphone': 700, 'Tablet': 650},
            'relation': {'Smartwatch': lambda Smartphone_price: Smartphone_price / 2}
        }
    ]

    item_set = random.choice(item_sets)
    types = item_set['types']
    prices = item_set['prices']
    relations = item_set['relation']

    item_type1 = types[0]
    item_type2 = types[1]
    item_type3 = types[2]

    # Randomly assign prices
    price_item1 = random.randint(100, 2000) // 50 * 50
    price_item3 = random.randint(100, 2000) // 50 * 50
    price_item2 = relations[item_type2](price_item1)

    # Total items sold
    total_sold = random.randint(150, 1000) // 50 * 50

    # Fraction and percentage sold
    fraction_item3 = random.choice([0.4, 0.5, 0.6])
    percent_item2 = random.choice([10, 15, 20])

    # Construct the problem statements
    problem = [
        f"{name} runs a store. {name}'s main products are three types: {item_type1}, {item_type2}, and {item_type3}.",
        f"The price of one {item_type1} is ${price_item1}, {item_type2} is half the price of an {item_type1}, and a {item_type3} is ${price_item3}.",
        f"In one month, {name} sold a total of {total_sold} items among the types listed.",
        f"{int(fraction_item3 * 100)}% of them were {item_type3}, and {percent_item2}% were {item_type2}s.",
        f"The rest of the sold items were {item_type1} type."
    ]

    # Construct the question
    question = f"How much did {name} earn from selling items during that month?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The profit margin on each {item_type1} is 20%.",
        f"In last month, {name} sold a total of {total_sold} items among the types listed."
        f"The store pays ${random.randint(1000, 5000)} in rent each month."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} loves to go hiking during the weekends.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Assume the functions introduce_symbol_error and introduce_grammar_error are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except the first one
    problem_statements = problem.copy()
    sentences_to_shuffle = problem_statements[1:]
    if shuffle:
        random.shuffle(sentences_to_shuffle)
    problem_statements = [problem_statements[0]] + sentences_to_shuffle
    problem_statements.append(question)

    # Calculate the numbers sold
    num_item3 = int(total_sold * fraction_item3)
    num_item2 = int(total_sold * percent_item2 / 100)
    num_item1 = total_sold - num_item3 - num_item2

    # Calculate earnings
    earnings_item1 = num_item1 * price_item1
    earnings_item2 = num_item2 * price_item2
    earnings_item3 = num_item3 * price_item3

    # Total earnings
    answer = earnings_item1 + earnings_item2 + earnings_item3

    # Return the problem and answer
    cot = [f"Calculate the number of {item_type3} sold: {total_sold} * {fraction_item3} = {num_item3}.", f"Calculate the number of {item_type2} sold: {total_sold} * {percent_item2} / 100 = {num_item2}.", f"Calculate the number of {item_type1} sold: {total_sold} - {num_item3} - {num_item2} = {num_item1}.", f"Calculate earnings from {item_type1}: {num_item1} * {price_item1} = {earnings_item1}.", f"Calculate earnings from {item_type2}: {num_item2} * {price_item2} = {earnings_item2}.", f"Calculate earnings from {item_type3}: {num_item3} * {price_item3} = {earnings_item3}.", f"Total earnings are {earnings_item1} + {earnings_item2} + {earnings_item3} = {answer}."]
    
    return {"cot": cot, 'problem': problem_statements, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
