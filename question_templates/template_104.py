from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible names
    names = ['Becky', 'Jake', 'Silvia', 'Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace',
             'Helen', 'Ivan', 'Judy', 'Karl', 'Laura', 'Mike', 'Nina', 'Oscar', 'Paul', 'Quinn',
             'Rachel', 'Steve', 'Tina', 'Uma', 'Victor', 'Wendy', 'Xavier', 'Yvonne', 'Zach']

    # Randomly select three different names
    person_names = random.sample(names, 3)
    name1 = person_names[0]
    name2 = person_names[1]
    name3 = person_names[2]

    while True:
        # Randomly select number of pizzas and slices per pizza
        num_pizzas = random.randint(2, 5)
        slices_per_pizza = random.choice([6, 8, 10, 12])

        total_slices_available = num_pizzas * slices_per_pizza

        # Randomly select D, the difference in slices between name1 and name2
        D = random.randint(1, 5)

        # Calculate the maximum possible M
        max_M = (total_slices_available + 3 * D) // 4

        # Ensure max_M is greater than D + 1
        if max_M < D + 1:
            continue  # Regenerate num_pizzas and slices_per_pizza

        # Randomly select M within a valid range
        M = random.randint(D + 1, max_M)

        # Calculate the number of slices name2 ate
        J = M - D

        # Calculate the number of slices name3 ate
        S = 2 * J

        # Ensure J and S are positive
        if J <= 0 or S <= 0:
            continue  # Regenerate parameters

        # Calculate total slices eaten
        total_slices_eaten = M + J + S

        # Ensure total slices eaten does not exceed total slices available
        if total_slices_eaten > total_slices_available:
            continue  # Regenerate parameters

        # All conditions met, break the loop
        break

    # Construct the problem premises
    problem = [
        f"{name1}, {name2}, and {name3} shared {num_pizzas} pizzas.",
        f"Each pizza had {slices_per_pizza} slices.",
        f"{name1} ate {D} more slices than {name2} did.",
        f"{name3} ate twice as many slices as {name2} did.",
    ]
    question = f"If {name1} ate {M} slices, how many total slices did they eat?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Construct irrelevant information
    irrelevant_infos = [
        f"{name1} loves extra cheese on pizza.",
        f"{name2} skipped breakfast that day.",
        f"The pizzas were delivered late due to traffic.",
        f"{name3} has a pet cat named Whiskers."
    ]

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.insert(random.randint(1, len(problem)-1), irrelevant_info)

    # Add symbol or grammar errors (assumed functions)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in problem
    ]

    # Shuffle the problem sentences except the first one and the question
    first_sentence = problem[0]
    other_sentences = problem[1:-1]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences + [question]

    # Math formulas to calculate the answer
    # Number of slices name2 ate
    J = M - D
    # Number of slices name3 ate
    S = 2 * J
    # Total slices eaten
    answer = M + J + S

    # Construct the chain of thought
    cot = [
        f"{name1} ate {D} more slices than {name2} did, so {name2} ate {M} - {D} = {J} slices.",
        f"{name3} ate twice as many slices as {name2} did, so {name3} ate 2 * {J} = {S} slices.",
        f"The total number of slices they ate is {M} + {J} + {S} = {answer} slices."
    ]

    return {
        "cot": cot,
        'problem': problem,
        'answer': answer,
        'original_problem': original_problem,
        'irrelevant_infos': irrelevant_infos
    }