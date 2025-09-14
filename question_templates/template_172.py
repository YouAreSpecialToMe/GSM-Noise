from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible names
    names = ["Martin", "Carl", "Christian", "Harry", "Alice", "Bob", "Diana", "Ethan", "Fiona", "George",
             "Hannah", "Ian", "Jenny", "Kevin", "Laura", "Mike", "Nina", "Oliver", "Paula", "Quinn"]
    
    # Randomly select four unique names
    selected_names = random.sample(names, 4)
    name1, name2, name3, name4 = selected_names

    # Randomly generate the initial weight and differences
    weight1 = random.randint(40, 70)  # Base weight for name1
    difference1 = random.randint(10, 20)  # Difference between name1 and name2
    difference2 = random.randint(5, 15)   # Difference between name2 and name3
    difference3 = random.randint(2, 10)   # Difference between name3 and name4

    # Additional variables for irrelevant information
    backpack_weight = random.randint(1, 10)
    age = random.randint(20, 60)
    num_siblings = random.randint(1, 5)
    num_pets = random.randint(0, 3)

    # Construct the premises with variable placeholders
    premises = [
        f"{name1}'s weight is {weight1} kg.",
        f"{name2}'s weight is {difference1} kg more than {name1}'s weight.",
        f"{name3}'s weight is {difference2} kg more than {name2}'s weight.",
        f"{name4}'s weight is {difference3} kg less than {name3}'s weight."
    ]

    # The question
    question = f"What is the weight of {name4}, in kg?"
    original_problem = premises.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    irrelevant_infos_in_topic = [
        f"{name2} carries a backpack weighing {backpack_weight} kg.",
        f"{name3} is {age} years old."
    ]

    # Out-topic irrelevant information
    irrelevant_infos_out_topic = [
        f"{name1} has {num_siblings} siblings.",
        f"{name4} owns {num_pets} pets."
    ]

    # Combine all irrelevant infos
    irrelevant_infos = irrelevant_infos_in_topic + irrelevant_infos_out_topic

    # Randomly add irrelevant information based on probability
    problem = premises.copy()
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Replace variables with their actual values
    # variables = {
    #     'weight1': weight1,
    #     'difference1': difference1,
    #     'difference2': difference2,
    #     'difference3': difference3,
    #     'backpack_weight': backpack_weight,
    #     'age': age,
    #     'num_siblings': num_siblings,
    #     'num_pets': num_pets
    # }

    # Replace variables in the problem statements
    # problem = [p.format(**variables) for p in problem]

    # Add symbol or grammar errors (assumed functions)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error), 
            prob_symbol_error
        ) for sentence in problem
    ]

    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Append the question at the end
    problem.append(question)

    # Calculate the answer using the formula
    # answer = weight1 + difference1 + difference2 - difference3

    answer = weight1 + difference1 + difference2 - difference3

    # Ensure that the answer matches the ground truth when using original values
    # Original problem values:
    # weight1 = 55
    # difference1 = 16
    # difference2 = 8
    # difference3 = 5
    # answer = 55 + 16 + 8 - 5 = 74

    # Return the problem and the computed answer
    cot = [f"{name2}'s weight is {difference1} kg more than {name1}'s weight, so it is {weight1} + {difference1}.", f"{name3}'s weight is {difference2} kg more than {name2}'s weight, so it is {weight1} + {difference1} + {difference2}.", f"{name4}'s weight is {difference3} kg less than {name3}'s weight, so it is {weight1} + {difference1} + {difference2} - {difference3}.", f"Therefore, the weight of {name4} is {answer} kg."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
