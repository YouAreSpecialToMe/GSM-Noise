from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and collectible items
    names = ["Elaine", "Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Henry", "Isabella", "Jack", "Karen", "Liam", "Maria"]
    items = ["Pokemon cards", "baseball cards", "stamps", "comic books", "coins", "action figures", "postcards"]
    
    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)
    
    # Randomly generate numerical values
    initial_cards = random.randint(10, 50)  # initial number of items
    first_month_multiplier = random.randint(2, 5)  # multiplier for first month
    second_month_difference = random.randint(-50, 50)
    if second_month_difference == 0:
        second_month_difference = -10  # ensure non-zero
    third_month_multiplier = random.randint(1, 3)  # multiplier for third month
    
    # Additional numeric variables for irrelevant info
    friend_name = random.choice([n for n in names if n != name])
    friend_cards = random.randint(10, 100)
    favorite_color = random.choice(["red", "blue", "green", "yellow", "purple", "orange"])
    pet_animal = random.choice(["dog", "cat", "hamster", "rabbit", "goldfish"])
    pet_name = random.choice(["Buddy", "Max", "Bella", "Charlie", "Molly", "Rocky"])
    
    # Construct the premise, breaking into sentence level
    problem = [
        f"{name} initially had {initial_cards} {item}.",
        f"After a month, {name} collected {first_month_multiplier} times that number.",
        f"In the second month, {name} collected {abs(second_month_difference)} {'more' if second_month_difference > 0 else 'fewer'} {item} than those {name} collected in the first month.",
        f"In the third month, {name} collected {third_month_multiplier} times the combined number of {item} {name} collected in the first and second months."
    ]
    
    # Construct the question
    question = f"How many {item} does {name} have now in total?"
    original_problem = problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{friend_name}, a friend of {name}, also collects {item} and has {friend_cards} of them.",
        f"{name} likes organizing {item} by their rarity and type."
    ]
    
    # Add out-topic irrelevant information
    irrelevant_infos.extend([
        f"{name}'s favorite color is {favorite_color}.",
        f"{name} has a pet {pet_animal} named {pet_name}."
    ])
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors (Assuming functions are given)
    problem = [introduce_symbol_error(introduce_grammar_error(p, prob_grammar_error), prob_symbol_error) for p in problem]
    
    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    first_month_collected = initial_cards * first_month_multiplier
    second_month_collected = first_month_collected + second_month_difference
    third_month_collected = (first_month_collected + second_month_collected) * third_month_multiplier
    answer = initial_cards + first_month_collected + second_month_collected + third_month_collected
    
    # Return premise and answer as a dictionary
    cot = [f"{name} initially had {initial_cards} {item}.", f"After a month, {name} collected {first_month_multiplier} times that number, which is {initial_cards} * {first_month_multiplier} = {first_month_collected}.", f"In the second month, {name} collected {abs(second_month_difference)} {'more' if second_month_difference > 0 else 'fewer'} {item} than those collected in the first month, which is {first_month_collected} + {second_month_difference} = {second_month_collected}.", f"In the third month, {name} collected {third_month_multiplier} times the combined number of {item} collected in the first and second months, which is ({first_month_collected} + {second_month_collected}) * {third_month_multiplier} = {third_month_collected}.", f"Therefore, the total number of {item} {name} has now is {initial_cards} + {first_month_collected} + {second_month_collected} + {third_month_collected} = {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
