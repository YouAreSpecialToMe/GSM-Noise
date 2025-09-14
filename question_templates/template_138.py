from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of names
    names = ["Sasha", "Julie", "Alex", "Taylor", "Jordan", "Riley", "Casey", "Morgan", "Peyton"]
    genders = ["male", "female"]

    # Randomly select names
    name1 = random.choice(names)
    names.remove(name1)
    name2 = random.choice(names)

    # Randomly generate points and values
    sasha_game1 = random.randint(10, 25)  # Points scored by name1 in the first game
    julie_diff = random.randint(2, 6)  # Points fewer scored by name2 in the first game
    sasha_game2_diff = random.randint(3,
                                      8)  # Points fewer scored by name1 in the second game compared to name2's first game score

    # Additional irrelevant variables
    total_games = random.randint(2, 5)
    coach_name = random.choice(["Coach Smith", "Coach Johnson", "Coach Williams", "Coach Brown"])
    school_name = random.choice(["Lincoln High", "Roosevelt High", "Jefferson High"])
    coach_age = random.randint(30, 60)
    pet_name = random.choice(["Buddy", "Charlie", "Max", "Bella"])

    # Construct the problem, breaking it down into sentences
    problem = [
        f"{name1} and {name2} are best friends playing on opposing basketball teams.",
        f"The teams have two practice games scheduled.",
        f"In the first game, {name1} had the home court advantage and scored {sasha_game1} points.",
        f"{name2} scored {julie_diff} fewer points than {name1} in the same game.",
        f"{name1} always struggles during away games and their second match was at {name2}'s home court.",
        f"{name1} scored {sasha_game2_diff} fewer points in the second game than {name2}'s score in the first game."
    ]

    original_problem = problem.copy()

    # Construct in-topic irrelevant information
    irelevant_names = ["Avery", "Bailey", "Cameron", "Dakota", "Emery", "Finley", "Gray", "Harley", "Indigo", "Jesse",
                       "Kendall", "Lennon", "Marley", "Nico", "Oakley", "Parker", "Quinn", "Reese", "Sage", "Skyler",
                       "Tatum", "Val", "Wren", "Yael", "Zephyr"]
    irrelevant_name = random.choice(irelevant_names)
    irrelevant_infos = [
        f"{name1} scored {random.randint(5, 15)} points in last year's championship game.",
        f"{name2} scored {random.randint(6, 18)} points in last week's practice game.",
        f"In the first game, {irrelevant_name} scored {random.randint(5, 15)} points.",
        f"{irrelevant_name} scored {random.randint(6, 18)} fewer points than {name1} in the first game.",
    ]

    # Construct out-topic irrelevant information
    irrelevant_infos.extend([
        f"{name2} has a pet dog named {pet_name}."
    ])

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

    # Shuffle the middle sentences
    middle_sentences = problem[1:]
    if shuffle:
        random.shuffle(middle_sentences)
    problem = [problem[0]] + middle_sentences

    # Construct the question
    question = f"How many total points did {name1} score during both games?"
    original_problem.append(question)

    problem.append(question)

    # Compute the answer using the variables
    name2_game1 = sasha_game1 - julie_diff
    name1_game2 = name2_game1 - sasha_game2_diff
    answer = sasha_game1 + name1_game2

    # Return the problem and answer
    cot = [f"{name2} scored {julie_diff} fewer points than {name1} in the first game, so {name2}'s score was {sasha_game1} - {julie_diff}, which is {name2_game1}.", f"In the second game, {name1} scored {sasha_game2_diff} fewer points than {name2}'s score in the first game, so {name1}'s score was {name2_game1} - {sasha_game2_diff}, which is {name1_game2}.", f"The total points scored by {name1} in both games is {sasha_game1} + {name1_game2}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
