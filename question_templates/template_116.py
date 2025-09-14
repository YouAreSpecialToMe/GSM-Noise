from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and recipe lists
    names = ['Antoine', 'Isabella', 'Li Wei', 'Carlos', 'Amina', 'Satoshi', 'Maria', 'Ahmed', 'Yuki', 'Priya']
    recipes = ['French onion soup', 'beef stew', 'chili con carne', 'tomato bisque', 'clam chowder', 'vegetable curry',
               'pumpkin soup', 'mushroom risotto']

    # Randomly select a name and a recipe
    name = random.choice(names)
    recipe = random.choice(recipes)

    # Randomly generate recipe-related values
    onions_per_recipe = random.randint(1, 5)  # pounds of onions per recipe
    doubles_amount = random.choice([True, False])
    serves = random.randint(4, 12)  # number of servings
    onion_price = round(random.uniform(0.50, 3.00), 2)  # cost per pound of onions
    beef_stock_boxes = random.randint(1, 5)  # number of boxes of beef stock
    beef_stock_price = round(random.uniform(1.00, 5.00), 2)  # cost per box of beef stock

    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"{name}'s {recipe} recipe calls for {onions_per_recipe} pounds of onions.",
    ]

    if doubles_amount:
        problem.append(f"{name} likes to double that amount.")

    problem.append(f"{name}'s {recipe} serves {serves} people.")
    problem.append(f"The onions are currently on sale for ${onion_price:.2f} a pound.")
    problem.append(
        f"{name} also needs {beef_stock_boxes} boxes of beef stock, that are also on sale for ${beef_stock_price:.2f} a box.")

    original_problem = problem.copy()

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} is preparing for a large dinner party.",
        f"The green are currently on sale for ${random.uniform(1, 3.00) + onion_price:.2f} a pound."
    ]

    # Add out-topic irrelevant information
    hobbies = ['playing the guitar', 'learning Spanish', 'running marathons', 'collecting stamps',
               'painting landscapes', 'writing poetry']
    hobby = random.choice(hobbies)
    irrelevant_infos.append(f"In {name}'s free time, {name} enjoys {hobby}.")

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
    main_problem_sentences = problem[1:]  # exclude the first sentence
    if shuffle:
        random.shuffle(main_problem_sentences)
    problem = [problem[0]] + main_problem_sentences

    # Construct the question
    question = f"What is the cost per serving? (Round to the nearest integer.)"
    problem.append(question)
    original_problem.append(question)

    # Calculate the answer
    total_onions_needed = onions_per_recipe * (2 if doubles_amount else 1)
    total_onion_cost = total_onions_needed * onion_price
    total_beef_stock_cost = beef_stock_boxes * beef_stock_price
    total_cost = total_onion_cost + total_beef_stock_cost
    cost_per_serving = total_cost / serves
    answer = round(cost_per_serving)

    # Return premise and answer as a dictionary
    cot = [f"{name} needs {onions_per_recipe} pounds of onions for the recipe. Since {name} likes to double that amount, the total onions needed are {onions_per_recipe} * 2, which is {total_onions_needed}.", f"The cost of onions is {total_onions_needed} * {onion_price}, which is {total_onion_cost}.", f"{name} also needs {beef_stock_boxes} boxes of beef stock, costing {beef_stock_boxes} * {beef_stock_price}, which is {total_beef_stock_cost}.", f"The total cost of ingredients is {total_onion_cost} + {total_beef_stock_cost}, which is {total_cost}.", f"The cost per serving is {total_cost} / {serves}, which is {cost_per_serving}.", f"Rounding {cost_per_serving} to the nearest integer gives the final answer, {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
