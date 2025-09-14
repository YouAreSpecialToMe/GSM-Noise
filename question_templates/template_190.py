from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and items lists
    names = ["Oscar", "Alice", "Bob", "Emma", "Chris", "Eve", "Liam", "Sophia", "Ethan", "Ava"]
    items = ["lollipops", "candies", "cookies", "apples", "oranges", "pencils", "stickers", "marbles"]

    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)

    # Randomly generate numbers
    start_items = random.randint(20, 50)
    eats_on_way_to_school = random.randint(1, 5)
    max_gives_to_friends = min(20, start_items - eats_on_way_to_school - 1)
    gives_to_friends = random.randint(5, max_gives_to_friends)
    buys_multiplier = random.choice([2, 3])
    eats_that_night = random.randint(1, 5)
    eats_in_morning = random.randint(1, 5)

    # Construct the problem sentences
    problem = [
        f"{name} has {start_items} {item} and eats {eats_on_way_to_school} on {name}'s way to school.",
        f"{name} gives {gives_to_friends} to {name}'s friends.",
        f"{name} buys {buys_multiplier} times as many {item} on {name}'s way home as {name} gave to {name}'s friends.",
        f"{name} eats {eats_that_night} more that night and {eats_in_morning} more in the morning."
    ]

    # Construct the question
    question = f"How many {item} does {name} have?"
    original_problem = problem.copy()

    original_problem.append(question)

    # Add in-topic and out-topic irrelevant information
    irrelevant_infos = [
        f"{name}'s favorite color is {random.choice(['blue', 'green', 'red', 'yellow', 'purple'])}.",
        f"The {item} were originally bought from a store that sells {random.choice(['toys', 'books', 'games', 'clothes'])}.",
        f"It was a {random.choice(['sunny', 'rainy', 'cloudy', 'snowy'])} day.",
        f"{name}'s friend {random.choice(names)} has {random.randint(10, 30)} {random.choice(items)}."
    ]

    # Randomly add irrelevant information based on probability
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

    # Shuffle the order of sentences, keeping the question at the end
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem
    problem.append(question)

    # Calculate the answer using the variables
    answer = (start_items - eats_on_way_to_school - gives_to_friends + (buys_multiplier * gives_to_friends) - eats_that_night - eats_in_morning)

    # Return the problem and answer as a dictionary
    cot = [f"{name} starts with {start_items} {item}.", f"{name} eats {eats_on_way_to_school} {item} on the way to school, leaving {start_items - eats_on_way_to_school}.", f"{name} gives {gives_to_friends} {item} to friends, leaving {start_items - eats_on_way_to_school - gives_to_friends}.", f"{name} buys {buys_multiplier} times as many {item} as given to friends, which is {buys_multiplier * gives_to_friends}.", f"After buying, {name} has {start_items - eats_on_way_to_school - gives_to_friends + (buys_multiplier * gives_to_friends)} {item}.", f"{name} eats {eats_that_night} more {item} that night and {eats_in_morning} more in the morning.", f"Finally, {name} has {answer} {item}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
