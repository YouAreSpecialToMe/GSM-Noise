from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of diverse names and school types
    names = ["Ali", "John", "Maria", "Chen", "Aisha", "Carlos", "Fatima", "David", "Sofia", "Wei"]
    school_types = ["private school", "public school", "charter school", "international school"]

    # Randomly select different names for two deans
    name1 = random.choice(names)
    name2 = random.choice([n for n in names if n != name1])

    # Randomly select school types for each dean
    school_type1 = random.choice(school_types)
    school_type2 = random.choice([s for s in school_types if s != school_type1])

    # Randomly assign number of classes for each dean
    class_count1 = random.randint(1, 3)
    class_count2 = random.randint(1, 3)

    # Randomly assign class capacity for the first dean
    capacity1 = random.randint(80, 200)

    # Randomly select a capacity ratio as a simple fraction
    possible_ratios = [(1, 2), (1, 4), (1, 5), (1, 8), (1, 10), (2, 5), (3, 5)]
    capacity_ratio_fraction = random.choice(possible_ratios)
    capacity_ratio = capacity_ratio_fraction[0] / capacity_ratio_fraction[1]

    # Calculate class capacity for the second dean
    capacity2 = capacity1 * capacity_ratio
    capacity2 = round(capacity2)

    # Prepare variables for irrelevant information
    total_students1 = random.randint(100, 500)
    year_founded1 = random.randint(1950, 2020)
    total_students2 = random.randint(100, 500)
    year_founded2 = random.randint(1950, 2020)
    hobby = random.choice(["play chess", "go hiking", "practice yoga", "paint landscapes"])

    # Construct the problem premises with variable placeholders
    problem = [
        f"{name1} is a dean of a {school_type1} where {name1} teaches {class_count1} class{'es' if class_count1 > 1 else ''}.",
        f"{name2} is also a dean of a {school_type2}.",
        f"{name2} has {class_count2} class{'es' if class_count2 > 1 else ''} in {name2}'s school.",
        f"Each class has {capacity_ratio_fraction[0]}/{capacity_ratio_fraction[1]} the capacity of {name1}'s class which has the capacity of {capacity1} students."
    ]
    question = f"What is the combined capacity of both schools?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name1}'s {school_type1} was founded in {year_founded1}.",
        f"{name2}'s {school_type2} has {total_students2} students enrolled.",
        f"Both schools are located in the same city."
    ]

    # Add out-topic irrelevant information
    out_topic_irrelevant_info = f"{name1} and {name2} {hobby} together every weekend."
    irrelevant_infos.append(out_topic_irrelevant_info)

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

    # Shuffle the order of sentences, except the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question
    
    problem.append(question)

    # Calculate the answer
    total_capacity1 = class_count1 * capacity1
    total_capacity2 = class_count2 * capacity2
    answer = total_capacity1 + total_capacity2

    # Return the problem and answer as a dictionary
    cot = [f"The capacity of each class for {name2} is {capacity1} * {capacity_ratio}, which is {capacity2}.", f"The total capacity for {name1}'s school is {class_count1} * {capacity1}, which is {total_capacity1}.", f"The total capacity for {name2}'s school is {class_count2} * {capacity2}, which is {total_capacity2}.", f"The combined capacity of both schools is {total_capacity1} + {total_capacity2}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
