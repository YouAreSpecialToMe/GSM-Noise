from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[8]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define list of names
        names = ['Alice', 'Bob', 'Carl', 'Diana', 'Ethan', 'Fiona', 'George', 'Hannah', 'Ian', 'Julia']
    
        # Define favorite foods
        favorite_foods = ['cheese', 'ham', 'turkey', 'lettuce', 'tomato', 'bacon', 'avocado', 'peanut butter']
    
        # Randomly select a name and favorite food
        name = random.choice(names)
        favorite_food = random.choice(favorite_foods)
    
        # Define variables
        days_in_week = 7  # Number of days in a week
    
        # Random variables
        slices_per_sandwich = random.randint(1, 4)
        days_with_omelets = random.randint(1, days_in_week)
        slices_more_per_omelet = random.randint(1, 2)
        slices_in_mac_and_cheese = random.choice([4, 6, 8, 10, 12, 14])
    
        # Build the problem
        problem = [
            f"{name}'s favorite food is {favorite_food}.",
            f"{name} ate a sandwich every day this week for lunch and used {slices_per_sandwich} slices of {favorite_food} on each sandwich.",
            f"{name} ate {favorite_food} and egg omelets for breakfast {days_with_omelets} days in the week using {slices_more_per_omelet} more slice per omelet than {name} did per sandwich.",
            f"{name} made a big dish of macaroni and {favorite_food} to last for several dinners for the week and used {slices_in_mac_and_cheese} slices of {favorite_food} in it."
        ]
    
        # Construct the question
        question = f"How many slices of {favorite_food} did {name} use?"
        original_problem=problem.copy()
        original_problem.append(question)
    
        # Add in-topic irrelevant information
        in_topic_irrelevant_infos = [
            f"{name} also makes salads that sometimes use {random.randint(1,5)} slices of {favorite_food}.",
            f"{name} bought {random.randint(10,50)} slices of {favorite_food} at the store."
        ]
    
        # Add out-topic irrelevant information
        out_topic_irrelevant_infos = [
            f"{name} enjoys hiking on the weekends.",
            f"{name} has a pet {random.choice(['dog','cat','parrot'])} named {random.choice(['Buddy','Shadow','Max'])}."
        ]
    
        # Randomly add irrelevant information based on probability
        for info in in_topic_irrelevant_infos + out_topic_irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(info)
        irrelevant_infos=in_topic_irrelevant_infos + out_topic_irrelevant_infos
    
        # Add symbol or grammar errors. Assume that these functions are given.
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error),
                prob_symbol_error
            ) for p in problem
        ]
    
        # Shuffle the premises
        if shuffle:
            random.shuffle(problem[1:])  # Don't shuffle the question
    
        # Add the question
        problem.append(question)
    
        # Calculate the answer
        total_sandwich_slices = slices_per_sandwich * days_in_week
        slices_per_omelet = slices_per_sandwich + slices_more_per_omelet
        total_omelet_slices = slices_per_omelet * days_with_omelets
        total_slices = total_sandwich_slices + total_omelet_slices + slices_in_mac_and_cheese
    
        answer = total_slices
        if answer%1==0:
            break

    # Return the problem and answer
    cot = [f"{name} ate a sandwich every day this week, using {slices_per_sandwich} slices of {favorite_food} per sandwich. Therefore, the total slices used for sandwiches is {slices_per_sandwich} * {days_in_week}, which is {total_sandwich_slices}.", f"{name} used {slices_more_per_omelet} more slices per omelet than per sandwich. Therefore, the slices per omelet is {slices_per_sandwich} + {slices_more_per_omelet}, which is {slices_per_omelet}.", f"{name} ate omelets for {days_with_omelets} days, so the total slices used for omelets is {slices_per_omelet} * {days_with_omelets}, which is {total_omelet_slices}.", f"{name} used {slices_in_mac_and_cheese} slices of {favorite_food} in the macaroni and cheese dish.", f"Therefore, the total slices of {favorite_food} used is {total_sandwich_slices} + {total_omelet_slices} + {slices_in_mac_and_cheese}, which is {total_slices}.", f"The final answer is {total_slices}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

