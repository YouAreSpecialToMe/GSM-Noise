from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names
    names = ["Alex", "Jordan", "Taylor", "Casey", "Drew", "Morgan", "Harper", "Riley", "Bryce", "Sam", "Jamie",
             "Cameron"]

    # Randomly select a name
    name = random.choice(names)

    # Number of friends
    num_friends = random.randint(2, 6)  # Between 2 and 6 friends

    # Total people (including the main person)
    total_people = 1 + num_friends

    # Number of slices per pizza
    slices_per_pizza = random.choice([8, 10, 12, 14, 16])

    # Number of people in group1 (including the main person)
    num_group1 = random.randint(1, total_people - 1)  # At least 1, less than total_people

    # Number of people in group2
    num_group2 = total_people - num_group1

    # Fractions eaten by each group
    fractions = [2 / 3, 3 / 4, 4 / 5]
    fraction_eaten_group1 = random.choice(fractions)
    fraction_eaten_group2 = random.choice(fractions)

    # Construct the premise
    problem = [
        f"{name} and {num_friends} of {'his' if random.choice([True, False]) else 'her'} friends each ordered their own pizzas after practice.",
        f"Each pizza had {slices_per_pizza} slices.",
        f"{name} and {num_group1 - 1} friends ate {fraction_eaten_group1:.2f} of their pizzas.",
        f"The {num_group2} remaining friends ate {fraction_eaten_group2:.2f} of their pizzas."
    ]

    # Construct the question
    question = f"How many slices of pizza were {name} and {'his' if random.choice([True, False]) else 'her'} friends left?"

    original_problem = problem.copy()
    original_problem.append(question)

    names2 = ["Avery", "Quinn", "Charlie", "Skylar", "Frankie", "Sage", "Phoenix", "Remy", "Emerson", "Finley", "Blair",
              "Lennon"]
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{random.choice(names2)} and his friends ate {slices_per_pizza + random.randint(10, 20)} slices of {random.choice(names2)} and his friends' pizzas.",
        f"Each burger had {slices_per_pizza + random.randint(1, 5)} slices.",
        f"The {num_group2 + random.randint(1, total_people)} remaining friends ate {fraction_eaten_group2:.2f} of their burgers."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} loves reading books in their free time.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume these functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_sentences)
    problem = [first_sentence] + rest_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    total_slices = total_people * slices_per_pizza
    slices_eaten_group1 = num_group1 * slices_per_pizza * fraction_eaten_group1
    slices_eaten_group2 = num_group2 * slices_per_pizza * fraction_eaten_group2
    slices_eaten = slices_eaten_group1 + slices_eaten_group2
    answer = total_slices - slices_eaten

    # Return the problem and answer
    cot = [f"Calculate the total number of slices by multiplying the total number of people, {total_people}, by the number of slices per pizza, {slices_per_pizza}. This gives {total_slices}.", f"Calculate the slices eaten by {name} and {num_group1 - 1} friends by multiplying the number of people in group 1, {num_group1}, by the number of slices per pizza, {slices_per_pizza}, and the fraction they ate, {fraction_eaten_group1}. This gives {slices_eaten_group1}.", f"Calculate the slices eaten by the {num_group2} remaining friends by multiplying the number of people in group 2, {num_group2}, by the number of slices per pizza, {slices_per_pizza}, and the fraction they ate, {fraction_eaten_group2}. This gives {slices_eaten_group2}.", f"Add the slices eaten by both groups to get the total slices eaten, {slices_eaten}.", f"Subtract the total slices eaten, {slices_eaten}, from the total number of slices, {total_slices}, to find the number of slices left, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
