from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define list of names
    names = ["John", "Alice", "Bob", "Maria", "Satoshi", "Lena", "Ahmed", "Li Wei", "Priya", "Carlos"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly generate values
    tree_height = random.randint(50, 100)  # Tree height in feet
    usable_percentage = random.randint(50, 100)  # Usable percentage
    log_length = random.randint(2, 10)  # Length of each log in feet
    planks_per_log = random.randint(2, 10)  # Planks per log
    price_per_plank = round(random.uniform(0.5, 5.0), 2)  # Price per plank in dollars
    
    # Additional variables for irrelevant info
    tree_weight = random.randint(500, 2000)  # Weight in pounds
    weather = random.choice(['sunny', 'rainy', 'cloudy', 'windy', 'snowy'])
    day_of_week = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    ir_money = random.randint(1000, 5000)
    gender = random.choice(['boy', 'girl'])
    
    # Construct the premise content
    problem = [
        f"{name} cuts down a {tree_height}-foot tree.",
        f"{name} can make logs out of {usable_percentage}% of it.",
        f"{name} cuts it into {log_length}-foot logs.",
        f"From each of those logs, {name} cuts {planks_per_log} planks.",
        f"{name} then sells each plank for ${price_per_plank}."
    ]
    
    # Construct the question
    question = f"How much does {name} make?"

    original_problem = problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The tree weighs {tree_weight} pounds.",
        f"It was a {weather} {day_of_week} when {name} cut down the tree."
    ]
    
    # Add out-topic irrelevant information
    out_topic_irrelevant_info = f"{name} is a {gender} who has more than ${ir_money} saved up."
    
    irrelevant_infos.append(out_topic_irrelevant_info)
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Introduce symbol or grammar errors
    problem = [introduce_symbol_error(introduce_grammar_error(p, prob_grammar_error), prob_symbol_error) for p in problem]
    
    # Shuffle the order of sentences
    if shuffle:
        random.shuffle(problem)
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    total_usable_length = tree_height * (usable_percentage / 100)
    number_of_logs = total_usable_length / log_length
    number_of_planks = number_of_logs * planks_per_log
    total_income = number_of_planks * price_per_plank
    answer = round(total_income, 2)
    
    # Return premise and answer as a dictionary
    cot = [f"{name} can use {usable_percentage}% of the {tree_height}-foot tree, which is {tree_height} * ({usable_percentage} / 100) = {total_usable_length} feet.", f"He cuts the usable part into logs of {log_length} feet each, resulting in {total_usable_length} / {log_length} = {number_of_logs} logs.", f"From each log, he cuts {planks_per_log} planks, resulting in {number_of_logs} * {planks_per_log} = {number_of_planks} planks.", f"He sells each plank for ${price_per_plank}, so he makes {number_of_planks} * {price_per_plank} = {total_income} dollars.", f"Rounding the total income gives the final answer: {answer} dollars."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}