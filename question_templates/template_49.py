from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define lists of possible creatures and colors
    creatures = ["jellyfish", "octopus", "seahorse", "starfish", "crab", "lobster"]
    colors = ["green", "blue", "red", "yellow", "purple", "orange"]

    # Randomly select a creature
    creature = random.choice(creatures)

    # Randomly select two colors
    color1, color2 = random.sample(colors, 2)

    # Fractions for large creatures (numerator, denominator)
    fractions = [(1,2), (1,3), (1,4), (1,5), (2,5), (3,5)]
    fraction_large = random.choice(fractions)
    fraction_change = random.choice(fractions)

    # Ensure fractions are not the same
    while fraction_large == fraction_change:
        fraction_change = random.choice(fractions)

    # Number of creatures that changed color
    num_change_color = random.randint(5, 20)

    # Compute the answer using the math formula
    numerator = num_change_color * fraction_large[1] * fraction_change[1]
    denominator = fraction_large[0] * fraction_change[0]
    answer = numerator / denominator

    # Adjust num_change_color until answer is integer
    while answer != int(answer):
        num_change_color += 1
        numerator = num_change_color * fraction_large[1] * fraction_change[1]
        answer = numerator / denominator
        if num_change_color > 100:
            break

    answer = int(answer)

    # Additional variables for irrelevant info
    total_weight = random.randint(100, 500)  # kg
    tank_volume = random.randint(1000, 5000)  # liters
    year = random.randint(1950, 2023)

    # Construct the problem sentences
    problem = [
        f"A tank has numerous {creature} in it.",
        f"A fraction {fraction_large[0]}/{fraction_large[1]} of the {creature} are large, and a fraction {fraction_change[0]}/{fraction_change[1]} of the large {creature} change color from {color1} to {color2} under UV light.",
        f"The other {creature} are small and always stay {color2}.",
        f"When a UV light is turned on, {num_change_color} {creature} changed color."
    ]

    # Construct the question
    question = f"How many {creature} are in the tank?"
    original_problem=problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    irrelevant_infos = [
        f"The total weight of the {creature} is {total_weight} kg.",
        f"The tank was established in {year} and holds {tank_volume} liters of water."
    ]

    # Out-topic irrelevant information
    visitor_name = random.choice(["Alice", "Bob", "Charlie", "Diana"])
    country = random.choice(["Japan", "France", "Brazil", "Australia"])
    irrelevant_infos.append(f"{visitor_name} visited the aquarium last summer during their trip to {country}.")

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

    # Shuffle the sentences except the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences

    # Add the question
    problem.append(question)

    # Return the problem and answer as a dictionary
    cot = [f"Calculate the numerator by multiplying {num_change_color} by {fraction_large[1]} and {fraction_change[1]}, resulting in {numerator}.", f"Calculate the denominator by multiplying {fraction_large[0]} and {fraction_change[0]}, resulting in {denominator}.", f"Divide {numerator} by {denominator} to find the total number of {creature} in the tank, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
