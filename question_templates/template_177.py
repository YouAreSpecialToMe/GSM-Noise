from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names list
    names = ["Tom", "Alice", "Bob", "Cindy", "David", "Eva", "Frank", "Grace"]

    # Randomly select a name
    name = random.choice(names)

    # Randomly generate house-related values
    number_of_bedrooms = random.randint(2, 6)  # Number of bedrooms
    dimensions_x = random.randint(10, 30)  # Length of bedroom in feet
    dimensions_y = random.randint(10, 30)  # Width of bedroom in feet
    living_room_multiplier = random.randint(2, 10)  # Living room size multiplier
    rest_area = random.randint(500, 2000)  # Rest of the house area in sq ft

    # Variables for irrelevant info
    garage_area = random.randint(200, 500)  # Garage area in sq ft
    garden_area = random.randint(400, 1500)  # Garden area in sq ft
    house_age = random.randint(1, 100)  # Age of the house in years
    number_of_bathrooms = random.randint(1, 5)  # Number of bathrooms

    # Construct the premise content, breaking it into sentences
    problem = [
        f"{name} has {number_of_bedrooms} bedrooms in {name}'s house.",
        f"They measure {dimensions_x} by {dimensions_y} feet each.",
        f"The living room is {living_room_multiplier} times bigger than one bedroom.",
        f"The rest of the house is {rest_area} square feet."
    ]

    # Construct the question
    question = f"What is the total area, in square feet, of the house?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The house has a garage that is {garage_area} square feet.",
        f"The garden outside is {garden_area} square feet."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"The house is {house_age} years old.")
    irrelevant_infos.append(f"{name} has {number_of_bathrooms} bathrooms in the house.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors; assume functions are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one


    # Add the question
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem + [question]

    # Calculate the answer
    bedroom_area = dimensions_x * dimensions_y
    total_bedroom_area = number_of_bedrooms * bedroom_area
    living_room_area = bedroom_area * living_room_multiplier
    total_area = total_bedroom_area + living_room_area + rest_area

    # Assign to answer variable
    answer = total_area

    # Return problem and answer as dictionary
    cot = [f"Each bedroom measures {dimensions_x} by {dimensions_y} feet, so the area of one bedroom is {dimensions_x} * {dimensions_y}, which is {bedroom_area} square feet.", f"There are {number_of_bedrooms} bedrooms, so the total area of all bedrooms is {number_of_bedrooms} * {bedroom_area}, which is {total_bedroom_area} square feet.", f"The living room is {living_room_multiplier} times bigger than one bedroom, so its area is {bedroom_area} * {living_room_multiplier}, which is {living_room_area} square feet.", f"The rest of the house is {rest_area} square feet.", f"Therefore, the total area of the house is {total_bedroom_area} + {living_room_area} + {rest_area}, which is {total_area} square feet.", f"The final answer is {total_area} square feet."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
