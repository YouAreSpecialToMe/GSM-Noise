from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and items
    names = ["Alice", "Bob", "Carlos", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ivan", "Jake", "Karen", "Luis", "Maria", "Nina", "Oscar", "Paula", "Quincy", "Rachel", "Steve", "Tina", "Umar", "Vera", "Wesley", "Xena", "Yusuf", "Zara"]
    clothing_items = ["T-shirt", "jean", "sweater", "jacket", "shirt", "blouse", "skirt", "short", "coat"]
    footwear_items = ["pair of shoes", "pair of sandals", "pair of boots", "pair of sneakers", "pair of slippers"]
    
    # Randomly select name and items
    name = random.choice(names)
    item1 = random.choice(clothing_items)
    item2 = random.choice(footwear_items)
    
    # Randomly generate quantities and prices
    quantity1 = random.randint(2, 5)
    original_price_item1 = random.randint(5, 20)
    
    discount_item2 = random.choice([10, 20, 30, 40, 50])  # Discount percentage
    original_price_item2 = random.randint(20, 80)
    
    # Extra variables for irrelevant info
    irrelevant_price = random.randint(10, 100)
    irrelevant_discount = random.randint(5, 15)
    irrelevant_year = random.randint(2000, 2025)
    irrelevant_city = random.choice(["New York", "London", "Paris", "Tokyo", "Sydney"])
    
    # Construct the premise content
    problem = [
        f"{name} is shopping at a clothing store.",
        f"The store has a buy one get one 50% off deal on {item1}s.",
        f"{name} buys {quantity1} {item1}s.",
        f"The original price of each {item1} is ${original_price_item1}.",
        f"Then, {name} buys a {item2} that is {discount_item2}% off the original price.",
        f"The original price of the {item2} is ${original_price_item2}.",
    ]
    
    # Construct the question
    question = f"What is the total amount of money {name} spends at the store?"
    original_problem = problem.copy()
    original_problem.append(question)
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The store was established in {irrelevant_year}.",
        f"{name} considered buying an accessory priced at ${irrelevant_price}, but decided against it.",
    ]
    
    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} plans to travel to {irrelevant_city} next summer.")
    irrelevant_infos.append(f"{name} enjoys painting in free time.")
    
    # Randomly add irrelevant information based on probability
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
    
    # Shuffle the order of sentences, except the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    # For item1 (BOGO 50% off)
    full_price_items = quantity1 // 2 + quantity1 % 2
    half_price_items = quantity1 // 2
    cost_item1 = (full_price_items * original_price_item1) + (half_price_items * original_price_item1 * 0.5)
    
    # For item2
    cost_item2 = original_price_item2 * (1 - discount_item2 / 100)
    
    # Total cost
    answer = cost_item1 + cost_item2
    
    # Return the problem and answer
    cot = [f"{name} buys {quantity1} {item1}s. With the buy one get one 50% off deal, the number of full price {item1}s is {quantity1} // 2 + {quantity1} % 2, which is {full_price_items}.", f"The number of half price {item1}s is {quantity1} // 2, which is {half_price_items}.", f"The cost for the {item1}s is ({full_price_items} * {original_price_item1}) + ({half_price_items} * {original_price_item1} * 0.5), which is {cost_item1}.", f"{name} buys a {item2} with a {discount_item2}% discount. The cost of the {item2} is {original_price_item2} * (1 - {discount_item2} / 100), which is {cost_item2}.", f"The total amount of money {name} spends at the store is {cost_item1} + {cost_item2}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
