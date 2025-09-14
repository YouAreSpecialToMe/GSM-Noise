from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define name, item, and flower lists
    names = ["Rose", "Alice", "Beth", "Cindy", "Diana", "Eve", "Fiona", "Gina", "Henry", "Ivan", "Jack", "Kevin"]
    items = ["vase", "basket", "pot", "jar", "bucket", "flower pot"]
    flowers = ["flowers", "roses", "daisies", "tulips", "lilies", "orchids"]

    # Randomly select a name, item, and flower type
    name = random.choice(names)
    item = random.choice(items)
    flower = random.choice(flowers)

    # Number of batches
    num_batches = 4

    # Possible values for flowers picked and petals per flower
    collect1_flowers_list = [3, random.randint(2, 6), random.randint(7, 10)]
    collect1_petals_list = [5, random.randint(4, 9)]
    collect2_flowers_list = [4, random.randint(2, 6), random.randint(7, 10)]
    collect2_petals_list = [6, random.randint(4, 9)]
    collect3_flowers_list = [5, random.randint(2, 6), random.randint(7, 10)]
    collect3_petals_list = [4, random.randint(4, 9)]
    collect4_flowers_list = [6, random.randint(2, 6), random.randint(7, 10)]
    collect4_petals_list = [7, random.randint(4, 9)]

    drop_num_per_batch_list = [1, random.randint(1, 2)]

    # Randomly select values
    collect_flower_numbers = [
        random.choice(collect1_flowers_list),
        random.choice(collect2_flowers_list),
        random.choice(collect3_flowers_list),
        random.choice(collect4_flowers_list),
    ]
    collect_petals_numbers = [
        random.choice(collect1_petals_list),
        random.choice(collect2_petals_list),
        random.choice(collect3_petals_list),
        random.choice(collect4_petals_list),
    ]
    drop_num_per_batch = random.choice(drop_num_per_batch_list)

    # Construct the problem sentences
    problem = [
        f"{name} is out picking {flower} for a {item} {name} wants to fill.",
        f"{name} starts off by picking {collect_flower_numbers[0]} {flower} with {collect_petals_numbers[0]} petals each.",
        f"{name} then picks {collect_flower_numbers[1]} {flower} with {collect_petals_numbers[1]} petals each.",
        f"{name} then adds another {collect_flower_numbers[2]} {flower} with {collect_petals_numbers[2]} petals each.",
        f"Lastly, {name} picks {collect_flower_numbers[3]} {flower} with {collect_petals_numbers[3]} petals each.",
        f"As {name} is carrying these {flower} over to fill the {item}, {name} drops {drop_num_per_batch} of each and the wind blows them away.",
        f"{name} puts the remaining {flower} in the {item}."
    ]

    # Construct the question
    question = f"How many petals in total are on the {flower} in the {item}?"
    original_problem=problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    colors = ["red", "blue", "yellow", "pink", "white", "purple"]
    materials = ["ceramic", "glass", "plastic", "metal", "wooden"]
    collecting_time = random.randint(10, 120)
    irrelevant_infos = [
        f"The {flower} are of {random.choice(colors)} color.",
        f"The {item} is made of {random.choice(materials)}.",
        f"It took {name} {collecting_time} minutes to pick the {flower}."
    ]

    # Add out-topic irrelevant information
    hobbies = ["reading", "swimming", "painting", "cycling", "hiking"]
    out_topic_irrelevant_info = f"{name} enjoys {random.choice(hobbies)} in their spare time."
    irrelevant_infos.append(out_topic_irrelevant_info)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (assumed functions)
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
    total_petals = 0
    for i in range(num_batches):
        flowers_left = collect_flower_numbers[i] - drop_num_per_batch
        petals = flowers_left * collect_petals_numbers[i]
        total_petals += petals

    answer = total_petals

    # Return the problem and answer as a dictionary
    cot = [f"For each batch of flowers, calculate the number of flowers left by subtracting {drop_num_per_batch} from the number of flowers picked in that batch.", f"Multiply the number of flowers left by the number of petals per flower to get the total petals for that batch.", f"Add the total petals from each batch to get the overall total petals, which is {total_petals}.", f"The final answer is the total number of petals, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
