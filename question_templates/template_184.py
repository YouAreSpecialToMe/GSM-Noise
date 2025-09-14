from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Colors
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'black', 'white', 'gray', 'silver', 'gold']
    colors_used = random.sample(colors, 4)
    R_color = colors_used[0]
    G_color = colors_used[1]
    B_color = colors_used[2]
    Y_color = colors_used[3]

    # Numeric variables
    R_number = random.randint(10, 20)  # Number of R_color cars
    D1 = random.randint(1, R_number - 1)  # Difference between R_number and G_number
    G_number = R_number - D1  # Number of G_color cars
    M = random.randint(2, 5)  # Multiplier for B_number
    B_number = M * G_number  # Number of B_color cars
    Y_number = random.randint(10, 30)  # Number of Y_color cars
    Total = R_number + G_number + B_number + Y_number  # Total number of cars

    # Break down the problem into sentences
    problem = []

    # Sentence 1
    s1 = f"A bumper car rink has {R_number} {R_color} cars."
    problem.append(s1)

    # Sentence 2
    s2 = f"The rink has {D1} fewer {G_color} cars than they have {R_color} cars."
    problem.append(s2)

    # Sentence 3
    s3 = f"The rink has {M} times the number of {B_color} cars as they have {G_color} cars."
    problem.append(s3)

    # Sentence 4
    s4 = f"The rink also has {Y_color} cars."
    problem.append(s4)
    original_problem = problem.copy()
    question = f"If the rink has {Total} cars in total how many {Y_color} cars do they have?"
    original_problem.append(question)

    # Construct irrelevant information
    in_topic_irrelevant_infos = [
        f"The {Y_color} cars are the oldest ones in the rink.",
        f"A new shipment of {random.randint(5,15)} {random.choice(colors)} cars will arrive next week.",
        f"The {R_color} cars are the most popular among kids."
    ]
    out_topic_irrelevant_infos = [
        f"The rink owner also owns a {random.choice(['restaurant', 'bowling alley', 'arcade center'])} nearby.",
        f"It was raining on the day the count was made."
    ]

    # Add irrelevant information
    for irr_info in in_topic_irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irr_info)
    for irr_info in out_topic_irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irr_info)

    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Introduce symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle sentences except the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question
    
    problem.append(question)

    # Calculate the answer
    answer = Total - (R_number + G_number + B_number)

    # Return the problem and the answer
    cot = [f"The number of green cars is {R_number} - {D1}, which is {G_number}.", f"The number of blue cars is {M} times the number of green cars, which is {M} * {G_number}, resulting in {B_number}.", f"The total number of cars is {Total}. Therefore, the number of yellow cars is {Total} - ({R_number} + {G_number} + {B_number}), which equals {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
