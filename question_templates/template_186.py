from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define list of possible names and items
    names = ["Alice", "Bob", "Carlos", "Diana", "Ethan", "Fiona", "George", "Hannah", "Irene", "Jack", "Karen", "Liam", "Monica", "Nathan", "Olivia", "Peter", "Quincy", "Rachel", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xavier", "Yvonne", "Zach"]
    items = ["Junebugs", "weeds", "snails", "caterpillars", "slugs", "aphids", "grasshoppers", "ladybugs", "spiders", "beetles", "ants"]

    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)

    # Define days of the week
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    # Select 5 consecutive days
    start_day_index = random.randint(0, 2)
    day1 = days[start_day_index]
    day2 = days[start_day_index + 1]
    day3 = days[start_day_index + 2]
    day4 = days[start_day_index + 3]
    day5 = days[start_day_index + 4]

    # Randomly generate numbers
    removed_day1 = random.randint(10, 50)
    multiplier = random.randint(2, 3)
    removed_day2 = multiplier * removed_day1
    removed_day3 = multiplier * removed_day1
    removed_day4 = random.randint(10, 60)
    removed_day5 = random.randint(10, 70)

    # Irrelevant information
    total_plants = random.randint(5, 20)
    garden_size = random.randint(50, 200)
    weekend_activities = ["visited a museum", "went hiking", "read a book", "watched a movie", "attended a concert"]
    weekend_activity = random.choice(weekend_activities)

    # Construct the problem premises
    problem = [
        f"{name} hand-picks {item} off of {name}'s plants every summer.",
        f"On {day1}, {name} removed {removed_day1} {item}.",
        f"On both {day2} and {day3}, {name} removed {multiplier} times as many {item} as {name} did on {day1}.",
        f"{day4} {name} removed {removed_day4} and on {day5} {name} removed {removed_day5}.",
    ]

    # Construct the question
    question = f"What is the average number of {item} that {name} removes per day?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Construct in-topic irrelevant information
    irrelevant_infos = [
        f"{name} has a garden with {total_plants} different types of plants.",
        f"The size of the garden is {garden_size} square meters."
    ]

    # Construct out-topic irrelevant information
    irrelevant_infos.append(f"Over the weekend, {name} {weekend_activity}.")

    # Add irrelevant information based on probability
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
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question
    problem.append(question)

    # Calculate the answer
    total_removed = removed_day1 + removed_day2 + removed_day3 + removed_day4 + removed_day5
    answer = total_removed / 5

    # Return problem and answer as a dictionary
    cot = [f"On {day1}, {name} removed {removed_day1} {item}.", f"On both {day2} and {day3}, {name} removed {multiplier} times as many {item} as on {day1}, which is {removed_day2} and {removed_day3} respectively.", f"On {day4}, {name} removed {removed_day4} {item}, and on {day5}, {name} removed {removed_day5} {item}.", f"The total number of {item} removed over the 5 days is {removed_day1} + {removed_day2} + {removed_day3} + {removed_day4} + {removed_day5}, which is {total_removed}.", f"The average number of {item} removed per day is {total_removed} / 5, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
