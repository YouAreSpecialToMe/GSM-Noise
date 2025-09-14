from grammar_error import introduce_grammar_error, introduce_symbol_error

import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define place names
    places = ["Science Center", "History Museum", "Aquarium", "Art Gallery", "Zoo", "Botanical Gardens"]
    place = random.choice(places)

    # Days of the week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    # Randomly generate numbers
    monday_visits = random.randint(20, 50)
    multiplier_tuesday = random.randint(1, 5)  # Multiplier for Tuesday
    multiplier_wednesday = random.randint(1, 5)  # Multiplier for Wednesday
    thursday_visits = random.randint(10, 40)
    friday_visits = random.randint(10, 40)

    # Map multipliers to words
    number_words = {1: 'the same number', 2: 'twice', 3: 'three times', 4: 'four times', 5: 'five times'}
    multiplier_tuesday_word = number_words.get(multiplier_tuesday, f"{multiplier_tuesday} times")
    multiplier_wednesday_word = number_words.get(multiplier_wednesday, f"{multiplier_wednesday} times")

    # Construct the premise content
    problem = [
        f"The {place} hosted field trips {days[0]} through {days[-1]} last week.",
        f"On {days[0]}, {monday_visits} classes visited.",
        f"{multiplier_tuesday_word} as many visited on {days[1]} and {multiplier_wednesday_word} as many visited on {days[2]}.",
        f"Another {thursday_visits} classes visited on {days[3]} and {friday_visits} visited on {days[4]}.",
    ]

    # Construct the question
    question = f"In all, how many classes visited the {place} last week?"

    # In-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"The {place} will be closed next week for renovations.",
        f"Last month's field trips were fewer due to bad weather.",
        f"The {place} has a capacity of 200 classes per day."
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant_infos = [
        "Meanwhile, a new movie was released in theaters.",
        "Students are preparing for the upcoming science fair."
    ]

    # Combine and shuffle irrelevant information
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    random.shuffle(irrelevant_infos)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Introduce symbol or grammar errors (assume functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(
                p,
                prob_grammar_error
            ),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem
    original_problem = problem.copy()

    original_problem.append(question)

    # Add the question
    problem.append(question)

    # Calculate the answer
    tuesday_visits = multiplier_tuesday * monday_visits
    wednesday_visits = multiplier_wednesday * tuesday_visits
    total_visits = monday_visits + tuesday_visits + wednesday_visits + thursday_visits + friday_visits
    answer = total_visits

    # Return premise and answer as a dictionary
    cot = [
        f"On Tuesday, {multiplier_tuesday} times as many classes visited as on Monday, so {tuesday_visits} classes visited on Tuesday.",
        f"On Wednesday, {multiplier_wednesday} times as many classes visited as on Tuesday, so {wednesday_visits} classes visited on Wednesday.",
        f"The total number of classes that visited from Monday to Friday is the sum of visits each day: {monday_visits} + {tuesday_visits} + {wednesday_visits} + {thursday_visits} + {friday_visits}, which is {total_visits}.",
        f"Therefore, the total number of classes that visited the {place} last week is {answer}."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
