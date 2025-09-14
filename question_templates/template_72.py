import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name list
    names = ["Leo", "Alice", "Bob", "Cindy", "Diana", "Ethan", "Fiona", "Gina"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly generate sticker counts
    initial_stickers = random.randint(50, 200)  # Stickers two years ago
    collected_last_year = random.randint(10, 100)  # Stickers collected last year
    times_this_year = random.randint(2, 5)  # Multiplier for this year's stickers
    
    # Construct the premise content
    problem = [
        f"{name} collects stickers.",
        f"Two years ago, {name} had {initial_stickers} stickers in {name}'s collection.",
        f"Last year, {name} collected {collected_last_year} stickers.",
        f"This year, {name} collected {times_this_year} times the number of stickers as the previous year."
    ]
    
    import copy
    original_problem = copy.deepcopy(problem)

    # Construct the question
    question = f"How many stickers does {name} have in {name}'s collection?"
    
    # Add in-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"{name} organizes the stickers by color and size.",
        # f"{name} traded stickers with friends and got {random.randint(5, 20)} new ones.",
    ]
    
    # Add out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{name} has a pet dog named Rover.",
        f"{name}'s favorite subject in school is math.",
    ]
    
    # Add irrelevant information based on probability
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)
    
    # Add symbol or grammar errors. Assume these functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences
    
    # Add the question
    problem.append(question)
    original_problem.append(question)

    # Calculate the answer
    collected_this_year = times_this_year * collected_last_year
    answer = initial_stickers + collected_last_year + collected_this_year
    
    # Return the problem and answer
    cot = [f"This year, {name} collected {times_this_year} times the number of stickers as last year, which is {times_this_year} * {collected_last_year}, resulting in {collected_this_year} stickers.", f"The total number of stickers in {name}'s collection is {initial_stickers} + {collected_last_year} + {collected_this_year}, which equals {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}