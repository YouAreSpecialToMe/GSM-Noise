from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ["Grandpa", "Grandma", "Uncle Joe", "Aunt Sally", "Cousin Bob", "Sister Sue", "Brother Tom", "Friend Jack",
             "Neighbor Lisa", "Colleague Tim"]
    items = ["jelly beans", "chocolate bars", "cookies", "candies", "muffins", "marshmallows", "cupcakes",
             "licorice sticks", "lollipops", "pretzels"]

    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)

    # Sizes
    sizes = ["small", "medium", "large"]

    # Randomly generate numerical values
    num_large = random.randint(50, 100)  # Number of large items to fill up
    medium_multiplier = random.choice([1.5, 2, 2.5, 3])  # Multiplier for medium-sized items
    small_to_medium = random.randint(2, 5)  # Conversion factor from small to medium items

    # Construct the premise content
    problem = [
        f"{name} loves to eat {item}, but how many {item} {name} can eat depends on the size of the {item}.",
        f"It takes {num_large} large {item} to fill {name} up.",
    ]
    multiplier_text = {
        1.5: "one and a half times as many",
        2: "twice as many",
        2.5: "two and a half times as many",
        3: "three times as many"
    }[medium_multiplier]
    problem.append(f"{name} can eat {multiplier_text} medium-sized {item} as large {item}.")
    problem.append(f"And eating {small_to_medium} small {item} is the same as eating 1 medium-sized {item}.")

    # Construct the question
    question = f"How many small {item} can {name} eat?"

    original_problem = problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    irre_items = items.copy()
    irre_items.remove(item)
    irre_item = random.choice(irre_items)
    irre_names = names.copy()
    irre_names.remove(name)
    irre_name = random.choice(irre_names)
    in_topic_irrelevant_infos = [
        f"It takes {num_large + random.randint(1, 10)} large {irre_item} to fill {name} up.",
        f"It takes {num_large + random.randint(1, 10)} samll {item} to fill {name}'s friend {irre_name} up.",
        f"{name} can eat {multiplier_text} medium-sized {irre_item} as large {irre_item}.",
        f"{name}'s friend {irre_name} can eat {multiplier_text} medium-sized {item} as large {item}.",
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{name} is {random.randint(30, 80)} years old.",
    ]

    # Add irrelevant information based on probability
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
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

    # Shuffle the order of sentences, except for the first one
    intro = problem[0]
    rest = problem[1:]  # Exclude the question
    if shuffle:
        random.shuffle(rest)
    problem = [intro] + rest + [question]

    # Calculate the answer
    num_medium = num_large * medium_multiplier
    num_small = num_medium * small_to_medium
    answer = num_small

    # Return the problem and the answer
    cot = [f"{name} can eat {medium_multiplier} times as many medium-sized {item} as large {item}. Therefore, the number of medium-sized {item} is {num_large} * {medium_multiplier}, which is {num_medium}.", f"Since eating {small_to_medium} small {item} is the same as eating 1 medium-sized {item}, the number of small {item} is {num_medium} * {small_to_medium}, which is {num_small}.", f"Therefore, the final answer is {num_small}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
