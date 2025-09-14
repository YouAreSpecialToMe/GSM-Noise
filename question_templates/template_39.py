from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define name list
    names = ["Alex", "Jamila", "Kai", "Maria", "Jamaal", "Oliver", "Aria", "Liam", "Noah", "Isabella"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly generate initial weight, increase percent, decrease amount
    initial_weight = random.randint(5, 50)  # initial weight in pounds
    increase_percent = random.choice([10, 20, 25, 50, 75, 100])  # percent increase
    decrease_amount = random.randint(1, 10)  # decrease in pounds

    # Additional variables for irrelevant info
    # In-topic irrelevant info
    total_exercises = random.randint(1, 10)
    time_of_day = random.choice(['morning', 'afternoon', 'evening'])
    weight_brand = random.choice(['Rogue', 'York', 'Eleiko', 'Ivanko'])
    
    # Out-topic irrelevant info
    favorite_movie = random.choice(['Inception', 'Titanic', 'Avatar', 'The Matrix'])
    car_color = random.choice(['red', 'blue', 'black', 'white'])
    
    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"{name} is at the gym in the {time_of_day}.",
        f"{name} has been using a {initial_weight}-pound weight.",
        f"{name} increases the weight that {name} uses by {increase_percent}%.",
        f"It turns out to be too heavy, so {name} uses a weight {decrease_amount} pounds lighter than that."
    ]
    
    # Construct the question
    question = f"What is the weight, in pounds, that {name} now uses?"
    original_problem=problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} performs {total_exercises} different exercises at the gym.",
        f"The weights are of the brand {weight_brand}."
    ]
    
    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name}'s favorite movie is {favorite_movie}.")
    irrelevant_infos.append(f"{name}'s car is {car_color}.")
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors (Assuming functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences, except for the first one
    context = problem[0]
    rest = problem[1:]
    if shuffle:
        random.shuffle(rest)
    problem = [context] + rest
    
    # Add the question at the end
    problem.append(question)
    
    # Calculate the answer
    increased_weight = initial_weight * (1 + increase_percent / 100)
    final_weight = increased_weight - decrease_amount
    answer = final_weight
    answer=round(answer,2)
    
    # Return premise and answer as a dictionary
    cot = [f"{name} increases the weight by {increase_percent}%, so the new weight is {initial_weight} * (1 + {increase_percent} / 100), which is {increased_weight}.", f"Since the weight is too heavy, {name} uses a weight {decrease_amount} pounds lighter, which is {increased_weight} - {decrease_amount}, resulting in {final_weight}.", f"Therefore, the weight that {name} now uses is {final_weight} pounds."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
