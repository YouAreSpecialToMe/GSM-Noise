from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
from fractions import Fraction

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define potential names
    names = ["Mrs. Smith", "Mr. Johnson", "Dr. Lee", "Prof. Martínez", "Miss Patel", "Ms. Nguyen", 
             "Mr. O'Connor", "Madame Dubois", "Señorita Garcia", "Frau Müller", "Dr. Ahmed", 
             "Sir Williams", "Lady Adams"]
    name = random.choice(names)
    
    # Define total plants
    total_plants = random.randint(100, 500)
    
    # Define fraction for indoor plants
    indoor_denominator = random.choice([2, 3, 4, 5, 6])
    fraction_indoor = Fraction(1, indoor_denominator)
    
    # Remaining plants after indoor plants
    remaining_after_indoor = 1 - fraction_indoor
    
    # Define fraction for outdoor plants (of the remaining plants after indoor plants)
    outdoor_denominator = random.choice([2, 3, 4, 5, 6])
    outdoor_numerator = random.randint(1, outdoor_denominator - 1)
    fraction_outdoor = Fraction(outdoor_numerator, outdoor_denominator)


    
    # Ensure that flowering plants fraction is positive
    flowering_fraction = remaining_after_indoor * (1 - fraction_outdoor)
    if flowering_fraction <= 0:
        outdoor_numerator = outdoor_denominator - 1
        fraction_outdoor = Fraction(outdoor_numerator, outdoor_denominator)
        flowering_fraction = remaining_after_indoor * (1 - fraction_outdoor)

    variables = {
        'name': name,
        'total_plants': total_plants,
        'indoor_denominator_word': {2: 'half', 3: 'third', 4: 'fourth', 5: 'fifth', 6: 'sixth'}.get(indoor_denominator, str(indoor_denominator)),
        'outdoor_numerator_word': {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}.get(outdoor_numerator, str(outdoor_numerator)),
        'outdoor_denominator_word': {2: 'half', 3: 'third', 4: 'fourth', 5: 'fifth', 6: 'sixth'}.get(outdoor_denominator, str(outdoor_denominator)),
    }

    # Construct the problem statements
    problem = [
        f"There are {total_plants} plants in {name}'s garden.",
        f"One-{variables['indoor_denominator_word']} of {name}'s plants are indoor plants.",
        f"{variables['outdoor_numerator_word']}-{variables['outdoor_denominator_word']} of the remaining are outdoor plants while the rest are flowering plants.",
    ]
    
    question = "What percent of the plants are flowering plants?"
    original_problem = problem.copy()
    original_problem.append(question)
    
    # Mapping for variables

    
    # In-topic irrelevant information
    irrelevant_in_topic = [
        f"{name} also has a greenhouse with exotic plants.",
        f"The garden was established 10 years ago by {name}.",
    ]
    
    # Out-topic irrelevant information
    irrelevant_out_topic = [
        f"{name} enjoys painting in her free time.",
        f"{name}'s favorite color is green.",
    ]
    
    # Combine all irrelevant information
    all_irrelevant_info = irrelevant_in_topic + irrelevant_out_topic
    for info in all_irrelevant_info:
        if random.random() < prob_irre:
            problem.append(info)
    
    # Apply symbol and grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in problem
    ]
    
    # Shuffle the order of sentences except for the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    indoor_plants = total_plants * fraction_indoor
    remaining_plants = total_plants - indoor_plants
    outdoor_plants = remaining_plants * fraction_outdoor
    flowering_plants = remaining_plants - outdoor_plants
    answer = (flowering_plants / total_plants) * 100
    
    # Return the problem and the answer
    cot = [f"Calculate the number of indoor plants: {total_plants} * {fraction_indoor} = {indoor_plants}.", f"Calculate the remaining plants after accounting for indoor plants: {total_plants} - {indoor_plants} = {remaining_plants}.", f"Calculate the number of outdoor plants: {remaining_plants} * {fraction_outdoor} = {outdoor_plants}.", f"Calculate the number of flowering plants: {remaining_plants} - {outdoor_plants} = {flowering_plants}.", f"Calculate the percentage of flowering plants: ({flowering_plants} / {total_plants}) * 100 = {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': all_irrelevant_info}
