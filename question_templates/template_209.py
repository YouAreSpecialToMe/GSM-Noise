from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
# Done


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define town names
    towns = ["Springfield", "Riverside", "Laketown", "Greenfield", "Hill Valley", "Gotham", "Metropolis", "Duckburg", "Bedrock", "Pawnee"]
    
    # Randomly select a town name
    town = random.choice(towns)
    
    # Randomly generate the variables
    first_year_homes = random.randint(5, 50)  # Homes built in first year
    second_year_multiplier = random.randint(2, 5)  # Multiplier for second year
    third_year_multiplier = random.choice([2, 2, 2, 3])  # Multiplier for third year, more likely to be 2 (double)
    
    # Additional irrelevant variables
    parks_to_renovate = random.randint(1, 10)
    current_population = random.randint(1000, 50000)
    festival_name = random.choice(["Harvest Festival", "Spring Fair", "Founders Day", "Winter Carnival"])
    extra_homes = random.randint(10, 100)
    avg_income = random.randint(30000, 100000)
    
    # Construct the premises, replacing variables
    problem = [
        f"{town} is expanding and wants to build several new homes across the next three years.",
        f"In the first year, {town} will build {first_year_homes} homes.",
        f"In the next year, {town} will build {second_year_multiplier} times this many homes.",
        f"In the third year, {town} will count how many homes they have built and multiply the amount by {third_year_multiplier}.",
        f"The town plans to renovate {parks_to_renovate} parks during the same period.",
        f"The population of {town} is currently {current_population} people.",
        f"{town} is known for its annual {festival_name}."
    ]
    
    # Construct the question
    question = f"How many homes will {town} have built over the next three years?"
    original_problem = problem.copy()
    original_problem.append(question)
    
    # In-topic irrelevant information
    irrelevant_infos = [
        f"The town also plans to plant {extra_homes} trees in the next three years.",
        f"The average income in {town} is ${avg_income}.",
    ]
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors. Assume that these functions are given.
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
    first_year_homes_built = first_year_homes
    second_year_homes_built = first_year_homes * second_year_multiplier
    cumulative_two_years = first_year_homes_built + second_year_homes_built
    third_year_homes_built = cumulative_two_years * third_year_multiplier
    answer = first_year_homes_built + second_year_homes_built + third_year_homes_built
    
    # Return premise and answer as a dictionary
    cot = [f"In the first year, {town} will build {first_year_homes} homes, so the total number of homes built in the first year is {first_year_homes_built}.", f"In the second year, {town} will build {second_year_multiplier} times the number of homes built in the first year, which is {first_year_homes} * {second_year_multiplier}, resulting in {second_year_homes_built} homes.", f"The cumulative number of homes built in the first two years is {first_year_homes_built} + {second_year_homes_built}, which is {cumulative_two_years}.", f"In the third year, {town} will double the cumulative number of homes built in the first two years, which is {cumulative_two_years} * {third_year_multiplier}, resulting in {third_year_homes_built} homes.", f"Therefore, the total number of homes built over the three years is {first_year_homes_built} + {second_year_homes_built} + {third_year_homes_built}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
