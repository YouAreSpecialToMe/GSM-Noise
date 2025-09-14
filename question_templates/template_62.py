import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names
    names = ["John", "Alice", "Maria", "Liu", "Carlos", "Aisha", "Amir", "Sasha", "Chen", "Fatima", "Jorge"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly assign variables
    num_eggs = random.randint(2, 12)  # Number of eggs in the omelet
    amount_cheese_oz = random.randint(1,6)  # Amount of cheese in oz
    amount_ham_oz = amount_cheese_oz  # Amount of ham is equal to cheese
    
    calories_per_egg = random.choice([70,75,80,85,90])  # Calories per egg
    calories_per_oz_cheese = random.choice([100,110,120,130,140,150])  # Calories per oz of cheese
    calories_per_oz_ham = random.choice([30,35,40,45,50,55,60])  # Calories per oz of ham
    
    # Construct the premise content
    problem = [
        f"{name} makes a {num_eggs}-egg omelet with {amount_cheese_oz} oz of cheese and an equal amount of ham.",
        f"Eggs are {calories_per_egg} calories each.",
        f"Cheese is {calories_per_oz_cheese} calories per ounce.",
        f"Ham is {calories_per_oz_ham} calories per ounce."
    ]

    import copy
    original_problem = copy.deepcopy(problem)
    
    # Construct the question
    question = "How many calories is the omelet?"

    # Construct in-topic irrelevant information
    eggs_type = random.choice(["organic", "free-range", "regular", "omega-3 enriched"])
    favorite_ingredient = random.choice(["spinach","mushrooms","onions","bell peppers","tomatoes"])
    in_topic_irrelevant_infos = [
        f"{name} uses {eggs_type} eggs.",
        f"{name} loves to cook omelets with {favorite_ingredient}."
    ]
    
    # Construct out-topic irrelevant information
    hobby = random.choice(["reading", "swimming", "painting", "jogging", "gardening"])
    pet_animals = ["dog", "cat", "parrot", "hamster", "turtle"]
    pet_animal = random.choice(pet_animals)
    out_topic_irrelevant_infos = [
        f"{name} enjoys {hobby} in free time.",
        f"{name} has a pet {pet_animal}."
    ]
    
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Introduce symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the sentences (except the first one)
    problem_body = problem[1:]
    if shuffle:
        random.shuffle(problem_body)
    problem = [problem[0]] + problem_body
    
    # Add the question at the end
    problem.append(question)
    original_problem.append(question)
    
    # Calculate the answer
    answer = (num_eggs * calories_per_egg) + (amount_cheese_oz * calories_per_oz_cheese) + (amount_ham_oz * calories_per_oz_ham)
    
    # Return problem and answer
    cot = [f"Calculate the calories from the eggs: {num_eggs} * {calories_per_egg}.", f"Calculate the calories from the cheese: {amount_cheese_oz} * {calories_per_oz_cheese}.", f"Calculate the calories from the ham: {amount_ham_oz} * {calories_per_oz_ham}.", f"Add all the calories together to get the total calories of the omelet: ({num_eggs} * {calories_per_egg}) + ({amount_cheese_oz} * {calories_per_oz_cheese}) + ({amount_ham_oz} * {calories_per_oz_ham}) = {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}
