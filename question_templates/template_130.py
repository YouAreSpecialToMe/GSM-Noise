from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists for names
    names = ["Alex", "Bailey", "Casey", "Drew", "Emery", "Finley", "Gale", "Harper", "Jordan", "Kendall", "Lee",
             "Morgan", "Nico", "Parker", "Quinn", "Reese", "Riley", "Sage", "Sam", "Sidney", "Taylor", "Toni", "Tracy",
             "Val", "Whitney", "Zion"]

    # Randomly select a name
    name = random.choice(names)

    # Randomly generate variables
    group_size = random.randint(5, 15)  # Similar to 8
    number_of_groups = random.randint(10, 30)  # Number of boxes/groups
    number_crayons = group_size * number_of_groups  # Ensure it's a multiple

    box_weight = random.randint(5, 15)  # 8 ounces
    crayon_weight = random.randint(1, 2)  # 1 ounce

    ounces_per_pound = 16  # Standard

    # Additional variables for irrelevant information
    num_colors = random.randint(10, 50)
    friend_name = random.choice([n for n in names if n != name])
    friend_crayons = random.randint(50, 100)
    age = random.randint(5, 15)
    favorite_color = random.choice(['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'black', 'white'])

    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"{name} has {number_crayons} crayons.",
        f"{name} wants to separate {name}'s crayons into groups of {group_size} and put them into boxes.",
        f"Each box weighs {box_weight} ounces.",
        f"Each crayon weighs {crayon_weight} ounce.",
        f"There are {ounces_per_pound} ounces to a pound."
    ]

    # Construct the question
    question = f"If {name} puts all of {name}'s crayons into boxes, what is the total weight, in pounds, of the crayons and the boxes?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    crayon_like_objects = [
        "colored pencils",
        "markers",
        "oil pastels",
        "chalk",
        "tempera paint sticks",
        "watercolor pencils",
        "wax crayons",
        "beeswax crayons",
        "Kitpas art crayons",
        "Stabilo Woody 3-in-1 pencils",
        "paint pens",
        "gel pens",
        "sidewalk chalk",
        "charcoal sticks",
        "pastel sticks",
        "crayon rocks",
        "washable markers",
        "dot markers",
        "liquid chalk markers",
        "Wonderstix",
        "Crayola Twistables",
        "Kwik Stix tempera paint sticks"
    ]
    box_like_objects = [
        "crate",
        "bin",
        "container",
        "basket",
        "chest",
        "trunk",
        "case",
        "carton",
        "tote",
        "bucket",
        "drawer",
        "cabinet",
        "locker",
        "safe",
        "suitcase",
        "backpack",
        "bag",
        "pouch",
        "hamper",
        "organizer",
        "caddy",
        "toolbox",
        "cooler",
        "jar",
        "canister",
        "tupperware",
        "storage cube",
        "file cabinet",
        "shelf",
        "rack",
        "storage ottoman",
        "storage bench",
        "storage pod",
        "shipping container",
        "barrel",
        "cask",
        "vault",
        "capsule",
        "envelope",
        "folder"
    ]
    box_item = random.choice(box_like_objects)
    cray_item = random.choice(crayon_like_objects)
    irrelevant_infos = [
        f"Each {box_item} weighs {box_weight + random.randint(1, 15)} ounces.",
        f"{friend_name}, who is {name}'s friend, has {friend_crayons} crayons.",
        f"Each {cray_item} weighs {crayon_weight + random.randint(3, 20)} ounce.",
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} is {age} years old.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    # Assume introduce_symbol_error and introduce_grammar_error functions are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the sentences, except for the first one
    first_sentence = problem[0]
    rest_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_sentences)
    problem = [first_sentence] + rest_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    number_of_boxes = number_of_groups
    total_crayon_weight = number_crayons * crayon_weight  # in ounces
    total_box_weight = number_of_boxes * box_weight  # in ounces
    total_weight_ounces = total_crayon_weight + total_box_weight
    total_weight_pounds = total_weight_ounces / ounces_per_pound
    answer = total_weight_pounds

    # Return the problem and answer as a dictionary
    cot = [f"The number of boxes is equal to the number of groups, which is {number_of_groups}.", f"The total weight of the crayons is {number_crayons} * {crayon_weight}, which is {total_crayon_weight} ounces.", f"The total weight of the boxes is {number_of_boxes} * {box_weight}, which is {total_box_weight} ounces.", f"The total weight in ounces is the sum of the crayon weight and the box weight, which is {total_crayon_weight} + {total_box_weight}, or {total_weight_ounces} ounces.", f"Convert the total weight from ounces to pounds by dividing by {ounces_per_pound}, which gives {total_weight_pounds} pounds.", f"Therefore, the total weight in pounds is {total_weight_pounds}, which is the final answer."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
