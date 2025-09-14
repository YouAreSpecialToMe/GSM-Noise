from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
# Done
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and item lists
    names = ["Aleksandra", "Sophia", "Liam", "Olivia", "Noah", "Emma", "Ethan", "Mia", "Isabella", "Jacob"]
    soups = ["tomato soup", "chicken noodle soup", "minestrone", "clam chowder"]
    bagels = ["bagel", "sandwich", "burger", "pasta"]
    desserts = ["piece of cake", "slice of pie", "cupcake", "ice cream sundae"]

    # Randomly select a name and food items
    name = random.choice(names)
    soup = random.choice(soups)
    main_course = random.choice(bagels)
    dessert = random.choice(desserts)

    # Randomly assign prices and percentages
    bagel_price = random.randint(2, 10)  # Price of the main course
    soup_percentage_more = random.randint(10, 50)  # Soup is X% more than main course
    cake_fraction = random.choice([0.5, 0.6, 0.75, 0.8])  # Dessert is fraction of main course price

    # Random numbers for irrelevant information
    tip_percentage = random.randint(5, 20)
    appetizer_price = random.randint(3, 8)
    friends = random.randint(1, 4)
    restaurant_age = random.randint(5, 50)
    chef_experience = random.randint(1, 30)

    # Construct the problem, replacing values with variable names
    problem = [
        f"{name} went to a restaurant for dinner.",
        f"{name} ordered some {soup}, a {main_course}, and a {dessert}.",
        f"The {main_course} cost ${bagel_price}, and the {soup} {soup_percentage_more}% more.",
        f"The {dessert} is only {int(cake_fraction * 100)}% of the price of the {main_course}.",
    ]

    # Construct the question
    question = f"How much did {name} need to pay for the dinner {name} ordered?(without counting the tip)"
    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} left a {tip_percentage}% tip on the total bill.",
        f"{name} stop by the grocery store and bought a bottle of water at the cost of ${appetizer_price}.",
        f"{name} was joined by {friends} friends for dinner.",
        f"The restaurant has been open for {restaurant_age} years.",
        f"The chef has {chef_experience} years of experience.",
    ]

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (assumed to be given functions)
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
    soup_price = bagel_price * (1 + soup_percentage_more / 100)
    dessert_price = bagel_price * cake_fraction
    answer = bagel_price + soup_price + dessert_price

    # Return problem and answer as a dictionary
    cot = [f"The {main_course} costs ${bagel_price}.", f"The {soup} costs {soup_percentage_more}% more than the {main_course}, so the price is {bagel_price} * (1 + {soup_percentage_more} / 100), which is {soup_price}.", f"The {dessert} is {cake_fraction * 100}% of the price of the {main_course}, so the price is {bagel_price} * {cake_fraction}, which is {dessert_price}.", f"The total cost for the dinner is the sum of the {main_course}, {soup}, and {dessert} prices, which is {bagel_price} + {soup_price} + {dessert_price}, resulting in {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
