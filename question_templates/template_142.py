from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name list
    names = ['Alice', 'Beth', 'Cindy', 'Diana', 'Emily', 'Fiona', 'Caroline', 'Grace', 'Hannah', 'Isabel']
    name = random.choice(names)

    # Define number of children
    num_children = 4  # Keeping it consistent

    # First child's height in feet
    first_height_feet_options = [5, 6, 7]
    first_height_feet = random.choice(first_height_feet_options)

    # Convert first child's height to inches
    first_height_inches = first_height_feet * 12  # 1 foot = 12 inches

    # Differences in heights between children
    second_difference_options = [2, 3, 4]  # inches taller than first child
    second_difference = random.choice(second_difference_options)

    third_difference_options = [3, 4, 5]  # inches shorter than second child
    third_difference = random.choice(third_difference_options)

    fourth_difference_options = [2, 3, 4]  # inches taller than third child
    fourth_difference = random.choice(fourth_difference_options)

    # Additional variables for irrelevant info (in-topic)
    ages_options = [30, 35, 40, 45]
    age = random.choice(ages_options)
    pet_types = ['cat', 'dog', 'parrot', 'rabbit']
    pet = random.choice(pet_types)
    pet_name = random.choice(names)

    # Additional variables for irrelevant info (out-topic)
    car_model = ['Tesla', 'BMW', 'Audi', 'Toyota']
    car = random.choice(car_model)
    car_color = ['red', 'blue', 'black', 'white']
    color = random.choice(car_color)

    # Construct the premises
    problem = [
        f"{name} has {num_children} children.",
        f"The first child is {first_height_feet} feet tall.",
        f"The second child is {second_difference} inches taller than the first child.",
        f"The third child is {third_difference} inches shorter than the second child.",
        f"And the fourth child is {fourth_difference} inches taller than the third child."
    ]

    # Construct the question
    question = f"How tall is the fourth child, in inches?"

    original_problem = problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    irrelevant_infos = [
        f"The sixth child is {random.choice(first_height_feet_options)} feet taller the fourth child.",
        f"The fifth child is {random.choice(first_height_feet_options)} inches taller than the fourth child.",
        f"The fifth child is {random.choice(first_height_feet_options) + random.randint(1, 3)} inches shorter than the fourth child.",
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant_info = f"{name} drives a {color} {car}."
    irrelevant_infos.append(out_topic_irrelevant_info)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (assuming functions given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_of_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_of_sentences)
    problem = [first_sentence] + rest_of_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    first_child_height = first_height_inches  # in inches
    second_child_height = first_child_height + second_difference
    third_child_height = second_child_height - third_difference
    fourth_child_height = third_child_height + fourth_difference
    answer = fourth_child_height  # in inches

    # Return problem and answer as a dictionary
    cot = [f"The first child's height is {first_height_feet} feet, which is {first_height_inches} inches.", f"The second child is {second_difference} inches taller than the first child, making the second child's height {first_child_height} + {second_difference}, which is {second_child_height} inches.", f"The third child is {third_difference} inches shorter than the second child, making the third child's height {second_child_height} - {third_difference}, which is {third_child_height} inches.", f"The fourth child is {fourth_difference} inches taller than the third child, making the fourth child's height {third_child_height} + {fourth_difference}, which is {fourth_child_height} inches.", f"Therefore, the fourth child is {fourth_child_height} inches tall."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}

