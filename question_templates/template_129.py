from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of names and items
    names = ["Cole", "Lamar", "Stacy", "Charlie", "Mei", "Alice", "Bob", "Diana", "Ethan", "Fiona", "George", "Hannah"]
    festivals = ["Easter", "Spring", "Harvest", "Halloween", "Winter"]
    items = ["eggs", "pumpkins", "apples", "candies", "flowers"]

    # Randomly select names without repetition
    hider = random.choice(names)
    names.remove(hider)
    finder1 = random.choice(names)
    names.remove(finder1)
    finder2 = random.choice(names)
    names.remove(finder2)
    finder3 = random.choice(names)
    names.remove(finder3)
    finder4 = random.choice(names)

    # Randomly select a festival and an item
    festival = random.choice(festivals)
    item = random.choice(items)

    # Randomly generate numeric variables
    total_dozen = random.randint(5, 20)  # Total dozens of items hidden
    total_items = total_dozen * 12  # Total items
    finder1_find = random.randint(3, 10)  # Number of items finder1 finds
    multiplier = random.choice([2, 3])  # Multiplier for finder2
    finder2_find = multiplier * finder1_find  # Number of items finder2 finds
    finder3_less = random.randint(1, 5)  # Number less for finder3
    finder3_find = finder2_find - finder3_less  # Number of items finder3 finds
    finder4_fraction = random.choice([2, 4])  # Fraction for finder4 (half or quarter)
    finder4_find = finder3_find / finder4_fraction  # Number of items finder4 finds

    # Construct the premises
    problem = [
        f"{hider} hid {total_dozen} dozen {item} in the yard for the {festival} {item} hunt.",
        f"{finder1} finds {finder1_find} {item}.",
        f"{finder2} finds {'twice' if multiplier == 2 else 'three times'} as many as {finder1}.",
        f"{finder3} finds {finder3_less} less than {finder2}.",
        f"And {finder4} finds {'half' if finder4_fraction == 2 else 'a quarter'} as many as {finder3}.",
    ]

    # Construct the question
    question = f"How many {item} are still hidden in the yard?"

    original_problem = problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    hideable_objects = [
        "keys", "coins", "small toys", "plastic eggs", "marbles",
        "action figures", "garden gnomes", "painted rocks", "time capsule",
        "geocache container", "rubber ducks", "frisbee", "tennis ball",
        "dog treats", "plastic animals", "treasure chest", "puzzle pieces",
        "toy cars", "plastic dinosaurs", "seashells", "pinwheels",
        "fairy garden items", "plastic jewelry", "small flags", "golf balls",
        "plastic letters", "toy soldiers", "miniature houses", "wind chimes",
        "garden markers", "solar lights", "decorative stones", "bottle caps",
        "colorful ribbons", "toy insects", "plastic flowers", "small watering can",
        "miniature garden tools", "bird figurines", "plastic fruits",
        "toy musical instruments", "small plant pots", "decorative buttons",
        "plastic butterflies", "toy boats", "miniature windmills"
    ]
    hidden_item = random.choice(hideable_objects)
    irrelevant_infos = [
        f"{hider} also hid {total_dozen + random.randint(4, 40)} dozen {hidden_item} in the yard.",
        f"{finder1} finds {finder1_find + random.randint(1, 20)} {hidden_item}.",
        f"{finder3} finds {finder3_less + random.randint(1, 15)} {hidden_item} less than {finder2}."
    ]


    # Out-topic irrelevant information
    irrelevant_infos.append(f"{finder2} is planning a vacation next month.")

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

    # Shuffle the order of sentences except for the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences

    # Add the question at the end
    problem.append(question)

    # Calculate the answer
    total_found = finder1_find + finder2_find + finder3_find + finder4_find
    answer = total_items - total_found

    # Return the problem and the answer
    cot = [f"The total number of {item} hidden is {total_dozen} dozen, which is {total_dozen} * 12 = {total_items}.", f"{finder2} finds {multiplier} times as many {item} as {finder1}, which is {finder2_find}.", f"{finder3} finds {finder3_less} less than {finder2}, which is {finder3_find}.", f"{finder4} finds {finder4_fraction} of what {finder3} finds, which is {finder4_find}.", f"The total number of {item} found is {finder1_find} + {finder2_find} + {finder3_find} + {finder4_find} = {total_found}.", f"Therefore, the number of {item} still hidden is {total_items} - {total_found} = {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
