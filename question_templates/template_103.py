from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define names and tea types
    names = ["Lana", "Emma", "Oliver", "Liam", "Noah", "Ava", "Sophia", "Isabella", "Mia", "Charlotte"]
    tea_types = ["chamomile", "mint", "cinnamon", "green", "black", "oolong", "herbal", "ginger", "lemon", "peppermint"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly select three different tea types
    tea1, tea2, tea3 = random.sample(tea_types, 3)
    
    # Number of rows
    num_rows = random.randint(2, 5)
    
    # Cups per row (even number between 2 and 10)
    cups_per_row = random.randint(1, 5) * 2  # Guarantees even number
    
    # Total cups for tea1 and tea2
    cups_of_tea1_and_tea2 = num_rows * cups_per_row
    
    # Calculate cinnamon_cups to keep total_cups reasonable
    cinnamon_cups_min = 5
    cinnamon_cups_max = min(25, 50 - cups_of_tea1_and_tea2)
    if cinnamon_cups_max < cinnamon_cups_min:
        cinnamon_cups_max = cinnamon_cups_min
    cinnamon_cups = random.randint(cinnamon_cups_min, cinnamon_cups_max)
    
    # Total cups
    total_cups = cups_of_tea1_and_tea2 + cinnamon_cups
    
    # Construct the premise content
    problem = [
        f"{name} is brewing cups of tea for {name}'s friends.",
        f"{name} has {total_cups} cups, and {name} divides these into {num_rows} rows.",
        f"In each row, {name} creates equal amounts of {tea1} and {tea2} tea cups.",
        f"{name} then uses the remaining cups to brew a total of {cinnamon_cups} cups of {tea3} tea."
    ]
    
    # Construct the question
    question = f"How many cups of {tea2} tea are in each row?"
    original_problem=problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name}'s favorite type of tea is {tea3}.",
        f"{name} is preparing for a {random.choice(['birthday', 'wedding', 'graduation', 'garden'])} party.",
        f"{name} bought a new set of {total_cups} cups last week."
    ]
    
    # Add out-topic irrelevant information
    irrelevant_infos.extend([
        f"{name} has a pet {random.choice(['dog', 'cat', 'hamster', 'parrot'])} named {random.choice(['Buddy', 'Max', 'Bella', 'Luna'])}.",
        f"The weather forecast predicts {random.choice(['rain', 'sunshine', 'clouds', 'snow'])} tomorrow."
    ])
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Assume introduce_symbol_error and introduce_grammar_error functions are given
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
    
    # Calculate the answer
    cups_of_tea2_per_row = cups_per_row // 2
    answer = cups_of_tea2_per_row
    
    # Return problem and answer as a dictionary
    cot = [f"{name} divides the {total_cups} cups into {num_rows} rows, creating equal amounts of {tea1} and {tea2} tea cups.", f"The total number of cups for {tea1} and {tea2} is {num_rows} * {cups_per_row}, which is {cups_of_tea1_and_tea2}.", f"In each row, the number of {tea2} tea cups is {cups_per_row} divided by 2, which is {cups_of_tea2_per_row}.", f"Therefore, the answer is {cups_of_tea2_per_row}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

