from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[11]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define names
    names = ["Brianna", "Alex", "Taylor", "Jordan", "Morgan", "Sydney", "Kendall", "Peyton"]
    name = random.choice(names)
    
    # Random assignments of variables
    rooms = random.randint(2,6)*2  # Number of rooms
    people = random.randint(2, 6)   # Number of people
    flashlights_per_person = random.randint(1, 2)  # Flashlights per person
    flashlights_per_room = random.randint(1, 3)  # Flashlights per room

    # For candles
    small_candles_per_room = random.randint(2, 6)
    medium_candles_per_room = random.randint(3, 8)
    
    # Half of the rooms
    half_rooms = rooms // 2

    # Irrelevant items
    pet_types = ["dog", "cat", "parrot", "hamster"]
    pet = random.choice(pet_types)
    pet_count = random.randint(1, 5)
    house_years = random.randint(5, 100)
    garden_size = random.randint(50, 500)

    # Construct the premises with variable placeholders
    problem = [
        f"The power goes out in {name}'s house one night so {name} and {name}'s family gather all their candles and flashlights.",
        f"There are {rooms} rooms in the house and {people} people living there, including {name}.",
        f"There is {flashlights_per_person} flashlight for every person to carry and {flashlights_per_room} for each room.",
        f"They have a variety of candles available; {small_candles_per_room} small candles each for half the rooms and {medium_candles_per_room} medium candles each for the other half of the rooms.",
    ]
    # Construct the question
    question = f"With everything combined, how many candles and flashlights are {name}'s family using when the lights go out?"
    original_problem=problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} has {pet_count} {pet}s.",
        f"The house is {house_years} years old and has a garden of {garden_size} square meters."
    ]

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (assumed functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p_sentence, prob_grammar_error), 
            prob_symbol_error
        ) for p_sentence in problem
    ]

    # Shuffle the order of sentences, except the first one
    body_sentences = problem[1:]
    if shuffle:
        random.shuffle(body_sentences)
    problem = [problem[0]] + body_sentences + [question]
    
    # Calculate the answer using the variables
    total_flashlights = flashlights_per_person * people + flashlights_per_room * rooms
    total_small_candles = small_candles_per_room * half_rooms
    total_medium_candles = medium_candles_per_room * (rooms - half_rooms)
    total_candles = total_small_candles + total_medium_candles
    answer = total_flashlights + total_candles

    # Return the problem and the calculated answer
    cot = [f"Calculate the total number of flashlights: {flashlights_per_person} flashlights per person for {people} people plus {flashlights_per_room} flashlights for each of the {rooms} rooms, which gives {total_flashlights}.", f"Calculate the total number of small candles: {small_candles_per_room} small candles for each of the {half_rooms} rooms, which gives {total_small_candles}.", f"Calculate the total number of medium candles: {medium_candles_per_room} medium candles for each of the remaining {rooms - half_rooms} rooms, which gives {total_medium_candles}.", f"Add the total number of small candles and medium candles to get the total number of candles: {total_small_candles} + {total_medium_candles} = {total_candles}.", f"Add the total number of flashlights and candles to get the final answer: {total_flashlights} + {total_candles} = {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

