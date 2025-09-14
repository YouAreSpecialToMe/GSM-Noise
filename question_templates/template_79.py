from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[12]:


import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and relevant lists
    names = ["John", "Emily", "Carlos", "Aisha", "Li", "David", "Sarah", "Antonio"]
    colors = ["blue", "green", "red", "yellow", "purple", "orange"]
    pets = ["dog", "cat", "parrot", "fish", "hamster"]

    # Randomly select a name
    name = random.choice(names)

    # Randomly generate travel-related values
    distance_to_friend = random.randint(100, 300)  # Distance to friend's house
    detour_distance = random.randint(5, 20)  # Detour distance
    speed_to_friend = random.randint(50, 80)  # Speed to friend's house
    distance_return = random.randint(200, 400)  # Return trip distance
    speed_return = random.randint(60, 90)  # Speed on return trip

    # Additional variables for irrelevant info
    sleep_time = random.randint(7, 10)
    num_pet = random.randint(1, 5)
    pet = random.choice(pets)
    color = random.choice(colors)

    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"{name} drives to {name}'s friend's house {distance_to_friend} miles away.",
        f"{name} drives at a speed of {speed_to_friend} mph.",
        f"{name} had to take a detour that added {detour_distance} miles to {name}'s trip.",
        f"After {name} gets there {name} takes a route home that is {distance_return} miles but {name} goes {speed_return} mph.",
    ]

    # Construct the question
    question = "How long did the trip take?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The detour was due to road construction.",
        f"{name} sleeped for {sleep_time} hours last night.",
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name}'s favorite color is {color}.")
    irrelevant_infos.append(f"{name} has {num_pet} {pet}(s) at home.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume that introduce_symbol_error and introduce_grammar_error are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    if len(problem) > 1:
        fixed_sentence = problem[0]
        rest_of_sentences = problem[1:]
        if shuffle:
            random.shuffle(rest_of_sentences)
        problem = [fixed_sentence] + rest_of_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    total_time = ((distance_to_friend + detour_distance) / speed_to_friend) + (distance_return / speed_return)
    answer = round(total_time, 2)

    # Return premise and answer as a dictionary
    cot = [f"{name} drives to the friend's house, which is {distance_to_friend} miles away, and takes a detour that adds {detour_distance} miles, making the total distance {distance_to_friend + detour_distance}.", f"The speed to the friend's house is {speed_to_friend} mph, so the time taken is (distance_to_friend + detour_distance) / speed_to_friend.", f"On the return trip, the distance is {distance_return} miles and the speed is {speed_return} mph, so the time taken is distance_return / speed_return.", f"The total time for the trip is the sum of the time to the friend's house and the return trip, which is {total_time}.", f"Rounding the total time to two decimal places gives the final answer, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

