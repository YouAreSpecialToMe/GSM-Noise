from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[7]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define lists of possible values for variables
    names = ["Tim", "Max", "Ethan", "Lucas", "Oliver", "Liam"]
    friend_names = ["Allen", "Jake", "Ryan", "Mason", "Noah", "Jack"]
    items = ["watermelon drink", "apple drink", "peach drink", "orange drink"]
    events = ["pool party", "picnic", "birthday party", "family reunion", "barbecue"]
    
    # Randomly select names, item, and event
    name = random.choice(names)
    friend_name = random.choice(friend_names)
    while friend_name == name:
        friend_name = random.choice(friend_names)
    item = random.choice(items)
    event = random.choice(events)
    
    # Randomly generate recipe-related values
    juice_per_gallon = random.randint(1, 5)  # cups of juice per gallon
    fruits_per_cup = random.randint(4, 10)  # fruits per cup of juice
    regular_gallons = random.randint(2, 10)  # gallons to make for the event
    extra_gallons = random.randint(1, 3)  # extra gallons for friend
    tart_multiplier = random.randint(2, 3)  # times as tart the extra batch is
    
    # Other irrelevant numeric variables
    people_at_event = random.randint(10, 50)  # number of people at the event
    cost_per_fruit = random.uniform(0.10, 0.50)  # cost per fruit in dollars
    time_to_make_per_gallon = random.randint(5, 15)  # time to make one gallon in minutes
    friend_age = random.randint(20, 50)
    
    # Construct the premise content, breaking it down into sentences
    problem = [
        f"{name} wanted to make {item} for a {event}.",
        f"For a gallon of {item}, {name}'s recipe called for {juice_per_gallon} cups of fresh {item.split()[0]} juice.",
        f"{name} found that {fruits_per_cup} {item.split()[0]}s would yield 1 cup of juice.",
        f"{name} figured {name} would need to make {regular_gallons} gallons of {item} for the {event}.",
        f"{name}'s best friend {friend_name} asked if {name} could make an extra {extra_gallons} gallon(s) for him,  using {tart_multiplier} as much {item.split()[0]} juice per gallon to make it taste stronger.",
    ]
    
    # Construct the question
    question = f"How many {item.split()[0]}s will {name} need?"
    original_problem=problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"There will be {people_at_event} people attending the {event}.",
        f"Each {item.split()[0]} costs ${cost_per_fruit:.2f} at the store.",
    ]
    
    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{friend_name} is {friend_age} years old.")
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors (assume functions are given)
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
    total_juice = (regular_gallons * juice_per_gallon) + (extra_gallons * juice_per_gallon * tart_multiplier)
    total_fruits = total_juice * fruits_per_cup
    answer = total_fruits
    
    # Return premise and answer as a dictionary
    cot = [f"{name} needs to make {regular_gallons} gallons of {item} for the {event}, using {juice_per_gallon} cups of juice per gallon.", f"{friend_name} asked for an extra {extra_gallons} gallon(s) with {tart_multiplier} times the juice, so the total juice needed is ({regular_gallons} * {juice_per_gallon}) + ({extra_gallons} * {juice_per_gallon} * {tart_multiplier}), which is {total_juice} cups.", f"Since {fruits_per_cup} {item.split()[0]}s yield 1 cup of juice, the total number of {item.split()[0]}s needed is {total_juice} * {fruits_per_cup}, which is {total_fruits}.", f"Therefore, the final answer is {total_fruits} {item.split()[0]}s."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

