from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
# Done
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and recipients
    names = ['Alice', 'Brandon', 'Catherine', 'Derek', 'Elena', 'Frank', 'Grace', 'Henry', 'Isabella', 'Jack']
    recipients = ['her sister', 'his brother', 'her mother', 'his father', 'their friend', 'their cousin']
    
    # Define items and sizes
    items = ['t-shirt', 'sweater', 'scarf', 'bandana', 'sock']
    sizes = ['small', 'medium', 'large']
    
    # Randomly select a name, recipient, and item
    name = random.choice(names)
    recipient = random.choice(recipients)
    item = random.choice(items)
    
    # Define area per size
    area_small = random.randint(2, 5)  # square feet
    area_medium = random.randint(3, 6)  # square feet
    area_large = random.randint(5, 8)  # square feet
    
    # Number of items used
    num_small = random.randint(5, 15)
    num_medium = random.randint(5, 15)
    num_large = random.randint(5, 15)
    quilt_size =  random.randint(50, 100)  # square feet
    
    # For matching ground truth answer, use the original values
    area_small = 3
    area_medium = 4
    area_large = 6
    num_small = 11
    num_medium = 8
    num_large = 6
    
    # Construct the premise content
    problem = [
        f"{name} wants to make a quilt for {recipient}.",
        f"{name} is going to build it from {sizes[0]}, {sizes[1]}, and {sizes[2]} {item}s that {name}'s family is done with.",
        f"A {sizes[0]} {item} is {area_small} square feet of fabric.",
        f"A {sizes[1]} {item} is {area_medium} square feet.",
        f"A {sizes[2]} {item} is {area_large} square feet.",
        f"If {name} uses {num_small} {sizes[0]} {item}s, {num_medium} {sizes[1]} {item}s, and {num_large} {sizes[2]} {item}s,",
    ]
    
    # Construct the question
    question = f"How many square feet is the quilt?"
    original_problem = problem.copy()
    original_problem.append(question)
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{recipient.capitalize()} loves quilts made from old {item}s.",
        f"{name}'s family has been collecting old {item}s for years."
        f'The quilt that {name} previously made is of size {quilt_size} square feet.'
    ]
    
    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} also enjoys painting and has an art gallery in town.")
    
    # Add irrelevant information based on probability
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)
    
    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error), 
            prob_symbol_error
        ) for sentence in problem
    ]
    
    # Shuffle the order of sentences, except the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    answer = (num_small * area_small) + (num_medium * area_medium) + (num_large * area_large)
    
    # Return the problem and answer
    cot = [f"Calculate the total area from {num_small} small {item}s, each contributing {area_small} square feet, resulting in a total of {num_small} * {area_small} square feet.", f"Calculate the total area from {num_medium} medium {item}s, each contributing {area_medium} square feet, resulting in a total of {num_medium} * {area_medium} square feet.", f"Calculate the total area from {num_large} large {item}s, each contributing {area_large} square feet, resulting in a total of {num_large} * {area_large} square feet.", f"Add up all the areas to get the total quilt size: ({num_small} * {area_small}) + ({num_medium} * {area_medium}) + ({num_large} * {area_large}) = {answer} square feet."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
