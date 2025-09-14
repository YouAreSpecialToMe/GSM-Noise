from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Original variables
    name = 'Elvira'
    age = 30
    budget = 1500
    main_item = 'computer'
    accessories_description = 'with a screen, keyboard and mouse'
    main_item_cost = 1090
    item1 = 'scanner'; item1_cost = 157
    item2 = 'CD burner'; item2_cost = 74
    item3 = 'printer'; item3_cost = 102

    # Compute answer using original variables
    answer = budget - (main_item_cost + item1_cost + item2_cost + item3_cost)

    # Randomly select name and gender
    names_genders = [
        ('Alex', 'male'), 
        ('Jordan', 'female'), 
        ('Elvira', 'female'), 
        ('Carlos', 'male'), 
        ('Fatima', 'female'), 
        ('Yang', 'male'), 
        ('Priya', 'female'), 
        ('Oliver', 'male'), 
        ('Sofia', 'female'), 
        ('Liam', 'male'),
        ('Elena', 'female'),
        ('Daniel', 'male')
    ]
    name, gender = random.choice(names_genders)
    if gender == 'male':
        possessive_pronoun = 'his'
        subject_pronoun = 'he'
    else:
        possessive_pronoun = 'her'
        subject_pronoun = 'she'

    # Random age between 18 and 60
    age = random.randint(18, 60)

    # Randomly select main item and accessories
    main_items = [
        ('computer', 'with a screen, keyboard and mouse'),
        ('laptop', 'with an extra charger and carrying case'),
        ('smartphone', 'with a case and screen protector'),
        ('gaming console', 'with two extra controllers'),
        ('camera', 'with a lens kit and tripod')
    ]
    main_item, accessories_description = random.choice(main_items)
    main_item_cost = random.randint(500, 2000)

    # Randomly select 3 additional items
    additional_items = [
        ('scanner', (50, 200)),
        ('CD burner', (30, 100)),
        ('printer', (75, 250)),
        ('external hard drive', (50, 200)),
        ('webcam', (25, 150)),
        ('speakers', (40, 200)),
        ('graphics tablet', (80, 300)),
        ('VR headset', (150, 500)),
        ('microphone', (30, 150)),
        ('headphones', (25, 200))
    ]
    selected_items = random.sample(additional_items, 3)
    item1, (item1_min, item1_max) = selected_items[0]
    item1_cost = random.randint(item1_min, item1_max)
    item2, (item2_min, item2_max) = selected_items[1]
    item2_cost = random.randint(item2_min, item2_max)
    item3, (item3_min, item3_max) = selected_items[2]
    item3_cost = random.randint(item3_min, item3_max)

    # Calculate total cost and budget
    total_cost = main_item_cost + item1_cost + item2_cost + item3_cost
    money_left = random.randint(20, 500)
    budget = total_cost + money_left

    # Recalculate the answer using new variables
    answer = budget - total_cost

    # Construct the problem sentences
    problem = [
        f"For {possessive_pronoun} {age}th birthday, {name} chose a new {main_item} {accessories_description} as a gift.",
        f"{subject_pronoun.capitalize()} has a budget of €{budget} donated by {possessive_pronoun} whole family and thinks that {subject_pronoun} will be able to keep a little money to afford a garment.",
        f"{subject_pronoun.capitalize()} goes to a store and chooses a {main_item} that costs €{main_item_cost} {accessories_description}.",
        f"{subject_pronoun.capitalize()} also takes a {item1} for €{item1_cost}, a {item2} worth €{item2_cost}, and a {item3} for €{item3_cost}."
    ]
    question = f"How much money will {subject_pronoun} have left for {possessive_pronoun} clothing?"
    original_problem = problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    in_topic_irrelevant_info = [
        f"The {main_item} comes with a 2-year warranty.",
        f"{name} plans to use the {main_item} for work and entertainment.",
        f"The store is offering a discount on {item3}s next week.",
        f"{name} considered buying a {random.choice(additional_items)[0]} but decided not to."
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant_info = [
        f"{name} enjoys {random.choice(['swimming', 'hiking', 'painting', 'reading'])} during {possessive_pronoun} free time.",
        f"The weather forecast predicts rain on {name}'s birthday.",
        f"{name}'s friend {random.choice([n for n, g in names_genders if n != name])} is planning a surprise party.",
        f"{name} recently adopted a {random.choice(['dog', 'cat', 'parrot'])}."
    ]

    # Add irrelevant information based on probability
    irrelevant_infos = in_topic_irrelevant_info + out_topic_irrelevant_info
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question

    problem.append(question)

    # Return problem and answer as a dictionary
    cot = [f"Calculate the total cost of the items by adding {main_item_cost}, {item1_cost}, {item2_cost}, and {item3_cost} to get {total_cost}.", f"Subtract the {total_cost} from the {budget} to find out how much money is left, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
