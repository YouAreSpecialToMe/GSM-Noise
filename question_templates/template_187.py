from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name list
    names = ["Larry", "Alice", "Mohammed", "Li Wei", "Carlos", "Fatima", "Svetlana", "Akira", "Priya", "John"]
    name = random.choice(names)
    
    # Variables
    num_cats = random.randint(1, 5)
    ratio_dogs_to_cats = random.randint(2, 5)
    diff_rabbits_dogs = -random.randint(1, 5)  # Rabbits fewer than dogs
    ratio_fish_to_rabbits = random.randint(2, 5)
    ratio_gerbils_to_fish_denominator = random.choice([2, 3, 4, 5])
    neighbour_pets = random.randint(1, 10)
    
    # Compute numbers
    num_dogs = ratio_dogs_to_cats * num_cats
    num_rabbits = num_dogs + diff_rabbits_dogs  # diff_rabbits_dogs is negative
    num_fish = ratio_fish_to_rabbits * num_rabbits
    
    # Adjust num_fish to be divisible by ratio_gerbils_to_fish_denominator
    while num_fish % ratio_gerbils_to_fish_denominator != 0:
        num_fish += 1
    num_gerbils = num_fish // ratio_gerbils_to_fish_denominator
    
    # Compute the total number of pets
    answer = num_cats + num_dogs + num_rabbits + num_fish + num_gerbils
    
    # Construct the problem sentences
    problem = [
        f"{name} loves taking care of animals.",
        f"{name} has {num_cats} cats.",
        f"{name} has {ratio_dogs_to_cats} times as many dogs as cats.",
        f"{name} has {-diff_rabbits_dogs} fewer rabbits than dogs.",
        f"{name} has a fish tank with {ratio_fish_to_rabbits} times the number of fish as rabbits.",
        f"{name} also has a collection of gerbils that's 1/{ratio_gerbils_to_fish_denominator} the number of fish {name} has."
    ]
    
    # Construct the question
    question = f"How many pets does {name} have?"
    original_problem = problem.copy()
    original_problem.append(question)
    # Add in-topic and out-topic irrelevant information
    irrelevant_infos = [
        f"{name} volunteers at the local animal shelter every weekend.",
        f"{name} is training for a marathon next month.",
        f"{name} enjoys painting landscapes in free time.",
        f"{name}'s neighbor has {neighbour_pets} dogs."
    ]
    
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)
    
    # Introduce symbol or grammar errors (assumed given functions)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        )
        for sentence in problem
    ]
    
    # Shuffle sentences except the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem
    
    # Append the question
    problem.append(question)
    
    # Return the problem and the answer
    cot = [f"{name} has {num_cats} cats.", f"The number of dogs is {ratio_dogs_to_cats} times the number of cats, which is {num_dogs}.", f"The number of rabbits is {diff_rabbits_dogs} fewer than the number of dogs, which is {num_rabbits}.", f"The number of fish is {ratio_fish_to_rabbits} times the number of rabbits, which is {num_fish}.", f"The number of gerbils is 1/{ratio_gerbils_to_fish_denominator} of the number of fish, which is {num_gerbils}.", f"Therefore, the total number of pets is {num_cats} + {num_dogs} + {num_rabbits} + {num_fish} + {num_gerbils}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
