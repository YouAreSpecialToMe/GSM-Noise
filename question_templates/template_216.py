from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
import math
# Done
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names list
    names = ["Alex", "Taylor", "Jordan", "Sydney", "Robin", "Donny"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly select min_temp between 35 and 65
    min_temp = random.randint(35, 65)
    
    # mug1_temp between min_temp - 10 and min_temp - 1, ensure it's >= 1
    min_mug1_temp = min_temp - 10
    max_mug1_temp = min_temp - 1
    mug1_temp = random.randint(min_mug1_temp, max_mug1_temp)
    
    # pour1_volume between 2 and 8
    pour1_volume = random.randint(2, 8)
    
    # pour2_volume between 1 and 5
    pour2_volume = random.randint(1, 5)
    
    total_volume = pour1_volume + pour2_volume
    
    # Compute the required mug2_temp
    numerator = min_temp * total_volume - mug1_temp * pour1_volume
    denominator = pour2_volume
    mug2_temp_min = numerator / denominator
    answer = math.ceil(mug2_temp_min)
    
    # Construct the problem statements
    problem = [
        f"{name} can only drink water if it's at least {min_temp} degrees.",
        f"{name} has two mugs of water.",
        f"One mug is {mug1_temp} degrees.",
        "The other is an unknown temperature.",
        f"If {name} pours {pour1_volume} ounces of water from the {mug1_temp}-degree mug into the water bottle and {pour2_volume} ounces from the other mug, {name} is now able to drink the water.",
    ]
    
    # Construct the question
    question = "At least how many degrees is the second mug?"
    original_problem = problem.copy()
    original_problem.append(question)
    # In-topic irrelevant information
    water_bottle_capacity = random.randint(total_volume + 1, total_volume + 10)
    total_water = total_volume
    in_topic_irrelevant_info = [
        f"The water bottle can hold up to {water_bottle_capacity} ounces of water.",
        f"{name} plans to drink all {total_water} ounces of water."
    ]
    
    # Out-topic irrelevant information
    num_mugs = random.randint(2, 10)
    favorite_number = random.randint(1, 100)
    out_topic_irrelevant_info = [
        f"{name} owns {num_mugs} coffee mugs.",
        f"{name}'s favorite number is {favorite_number}."
    ]
    
    irrelevant_infos = in_topic_irrelevant_info + out_topic_irrelevant_info
    
    # Add irrelevant information based on probability
    for info in (in_topic_irrelevant_info + out_topic_irrelevant_info):
        if random.random() < prob_irre:
            problem.append(info)
    
    # Assume introduce_grammar_error and introduce_symbol_error are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the sentences, except the first one
    if len(problem) > 1:
        sentences_to_shuffle = problem[1:]
        if shuffle:
            random.shuffle(sentences_to_shuffle)
        problem = [problem[0]] + sentences_to_shuffle
    
    # Add the question
    problem.append(question)
    
    # Return the problem and the answer
    cot = [f"The total volume of water is {pour1_volume} + {pour2_volume}, which is {total_volume}.", f"To find the minimum temperature of the second mug, calculate the numerator as {min_temp} * {total_volume} - {mug1_temp} * {pour1_volume}, which is {numerator}.", f"The denominator is simply {pour2_volume}.", f"Divide the numerator by the denominator to get {mug2_temp_min}.", f"The minimum temperature of the second mug is the ceiling of {mug2_temp_min}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
