from grammar_error import introduce_grammar_error, introduce_symbol_error

import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name lists
    names = ["Tobias", "Chikote", "Igneous", "Luna", "Amarok", "Fenrir", "Sirius", "Echo"]
    forests = ["Whispering Woods", "Shadow Forest", "Mystic Pines", "Moonlit Grove"]
    moon_phases = ["full moon", "new moon", "crescent moon", "gibbous moon"]

    # Randomly select three different names
    name1, name2, name3 = random.sample(names, 3)

    # Randomly select a forest and a moon phase
    forest = random.choice(forests)
    moon = random.choice(moon_phases)

    # Randomly generate howl durations
    howl_duration1 = random.randint(10, 60)  # Duration in seconds
    multiplier2 = random.randint(2, 5)  # Multiplier for the second wolf's howl duration
    howl_duration2 = howl_duration1 * multiplier2
    howl_duration3 = howl_duration1 + howl_duration2  # As long as the other two combined

    # Other variables for irrelevant information
    irrelevant_animals = ["foxes", "owls", "rabbits", "bears"]
    animal = random.choice(irrelevant_animals)
    animal_count = random.randint(1, 5)
    distance = random.randint(1, 20)
    river_names = ["Silver Stream", "Crystal River", "Whispering Brook", "Golden Creek"]
    river = random.choice(river_names)

    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"{name1}, {name2}, and {name3} are three little wolves who live in the {forest} and howl at the {moon} every night.",
        f"When {name1} howls, each howl lasts for a total of {howl_duration1} seconds.",
        f"{name2} howls for {multiplier2} times as long as {name1}.",
        f"And {name3} howls for as long as {name1} and {name2} combined."
    ]

    # Construct the question
    question = f"What is the combined length of time, in minutes, of the three wolves' howls?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"Last night, the wolves saw {animal_count} {animal} in the forest.",
        f"The wolves' howls can be heard from {distance} miles away.",
        f"{name1} is the youngest among the three wolves.",
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"There is a river called the {river} flowing through the {forest}.")

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
    intro = problem[0]
    rest = problem[1:]
    if shuffle:
        random.shuffle(rest)
    problem = [intro] + rest

    # Add the question
    problem.append(question)

    # Calculate the answer
    total_seconds = howl_duration1 + howl_duration2 + howl_duration3
    answer = total_seconds / 60  # Convert to minutes

    # Round answer to 2 decimal places
    answer = round(answer, 2)

    # Return premise and answer as a dictionary
    cot = [
        f"{name2} howls for {multiplier2} times as long as {name1}, which is {howl_duration1} * {multiplier2}, resulting in {howl_duration2} seconds.",
        f"{name3} howls for as long as {name1} and {name2} combined, which is {howl_duration1} + {howl_duration2}, resulting in {howl_duration3} seconds.",
        f"The total duration of the howls is {howl_duration1} + {howl_duration2} + {howl_duration3}, which is {total_seconds} seconds.",
        f"Convert the total duration to minutes by dividing {total_seconds} by 60, resulting in {answer} minutes."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
