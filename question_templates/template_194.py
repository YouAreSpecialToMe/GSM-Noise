from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible values for variables
    names = ["Sally", "Alice", "Bob", "Carol", "Dave", "Jenny", "Tom"]
    vacation_places = ["seashore", "mountains", "city", "countryside", "island", "beach", "forest"]
    stores = ["trinket shop", "gift shop", "souvenir shop", "candy store", "market", "bazaar"]
    items_on_sale = ["taffy", "chocolate", "candy", "fudge", "cookies", "ice cream"]
    additional_items = ["seashells", "postcards", "keychains", "stickers", "toy cars", "bookmarks"]
    genders = ["girl", "boy"]
    
    # Randomly select values for variables
    name = random.choice(names)
    vacation_place = random.choice(vacation_places)
    store = random.choice(stores)
    sale_item = random.choice(items_on_sale)
    additional_item = random.choice(additional_items)
    gender = random.choice(genders)
    
    # Randomly generate monetary values
    parents_money = random.randint(5, 50)  # Money given by parents
    taffy_price = round(random.uniform(1.0, 10.0), 2)  # Price per pound
    taffy_lbs_bought = random.randint(2, 10)  # Pounds of item bought
    # Ensure even number for the deal
    if taffy_lbs_bought % 2 != 0:
        taffy_lbs_bought += 1
    additional_item_price = round(random.uniform(1.0, 5.0), 2)
    magnet_quantity = random.randint(1, 10)
    magnet_price_each = round(random.uniform(0.1, 1.0), 2)
    
    # Construct the premise content
    problem = [
        f"{name} went to the {vacation_place} for vacation.",
        f"{name}'s parents gave {name} ${parents_money} to buy whatever {name} wanted.",
        f"At the {store}, {sale_item} was on sale for \"Buy 1 pound at ${taffy_price}, get 1 pound 1/2 off.\"",
        f"{name} scooped up {taffy_lbs_bought} pounds.",
        f"{name} also bought a mixed bag of {additional_item} for ${additional_item_price} and {magnet_quantity} magnets that were ${magnet_price_each} each."
    ]

    # Construct the question
    question = f"How much money does {name} have left?"
    original_problem = problem.copy()

    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The {store} had been open for {random.randint(1, 100)} years.",
        f"{name} also considered buying a {random.choice(['hat', 'scarf', 'pair of sunglasses', 'keychain'])}."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} is a {gender} who loves to read books.")
    irrelevant_infos.append(f"The weather at the {vacation_place} was {random.choice(['sunny', 'rainy', 'cloudy', 'windy'])}.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume these functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question
    problem.append(question)

    # Calculate the answer
    full_price_pounds = taffy_lbs_bought // 2
    half_price_pounds = taffy_lbs_bought - full_price_pounds
    taffy_total_cost = (full_price_pounds * taffy_price) + (half_price_pounds * (taffy_price / 2))
    magnets_total_cost = magnet_quantity * magnet_price_each
    total_spending = taffy_total_cost + additional_item_price + magnets_total_cost
    answer = parents_money - total_spending

    # Round the answer to 2 decimal places
    answer = round(answer, 2)

    # Return problem and answer as a dictionary
    cot = [f"{name} bought {taffy_lbs_bought} pounds of taffy. The full price pounds are {taffy_lbs_bought} // 2, which is {full_price_pounds}.", f"The half price pounds are {taffy_lbs_bought} - {full_price_pounds}, which is {half_price_pounds}.", f"The total cost for taffy is ({full_price_pounds} * {taffy_price}) + ({half_price_pounds} * ({taffy_price} / 2)), which is {taffy_total_cost}.", f"The total cost for magnets is {magnet_quantity} * {magnet_price_each}, which is {magnets_total_cost}.", f"The total spending is {taffy_total_cost} + {additional_item_price} + {magnets_total_cost}, which is {total_spending}.", f"The amount of money {name} has left is {parents_money} - {total_spending}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
