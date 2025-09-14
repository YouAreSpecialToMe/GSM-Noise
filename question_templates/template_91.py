from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[3]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
    # Define variables
        names = ["Hannah", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Ivan"]
        events = ["4th of July", "New Year's Eve", "Diwali", "Chinese New Year", "Guy Fawkes Night"]
    
        city_boxes_options = list(range(5, 21))
        city_fireworks_per_box_options = list(range(10, 31))
        visibility_percent_options = [10, 20, 30, 40, 50, 60, 70, 80]
        hannah_boxes_options = list(range(1, 6))
        hannah_fireworks_per_box_options = list(range(3, 11))
    
        # Randomly assign variables
        name = random.choice(names)
        event = random.choice(events)
        city_boxes = random.choice(city_boxes_options)
        city_fireworks_per_box = random.choice(city_fireworks_per_box_options)
        visibility_percent = random.choice(visibility_percent_options)
        hannah_boxes = random.choice(hannah_boxes_options)
        hannah_fireworks_per_box = random.choice(hannah_fireworks_per_box_options)
    
        # Construct the problem sentences
        problem = [
            f"{name}'s city is having a big display of fireworks for {event}.",
            f"They're going to set off {city_boxes} boxes of {city_fireworks_per_box} fireworks each.",
            f"{name}'s house is at the right angle to see {visibility_percent}% of the city's fireworks.",
            f"{name} will also set off {hannah_boxes} boxes of {hannah_fireworks_per_box} fireworks each in {name}'s backyard."
        ]
    
        # Construct the question
        question = f"How many fireworks will {name} see in total?"
        original_problem=problem.copy()
        original_problem.append(question)
    
        # Construct irrelevant information
        in_topic_irrelevant_infos = [
            f"The city spent ${random.randint(1000,5000)} on the fireworks display.",
            f"The fireworks display lasts for {random.randint(10,60)} minutes.",
            f"There will be {random.randint(1, 5)} food trucks at the event."
        ]
        pet_names = ['Buddy', 'Max', 'Bella', 'Lucy', 'Charlie', 'Molly', 'Daisy']
        out_topic_irrelevant_infos = [
            f"{name} has a pet {random.choice(['dog', 'cat'])} named {random.choice(pet_names)}.",
            f"On {event}, {name} plans to bake a cake.",
            f"{name} is {random.randint(10, 50)} years old."
        ]
        irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    
        # Add irrelevant information based on probability
        for irrelevant_info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(irrelevant_info)
    
        # Apply symbol or grammar errors
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error),
                prob_symbol_error
            ) for p in problem
        ]
    
        # Shuffle sentences except the first
        other_sentences = problem[1:]
        if shuffle:
            random.shuffle(other_sentences)
        problem = [problem[0]] + other_sentences
    
        # Add the question
        problem.append(question)
    
        # Calculate the answer
        city_total_fireworks = city_boxes * city_fireworks_per_box
        visible_fireworks = city_total_fireworks * (visibility_percent / 100)
        hannah_total_fireworks = hannah_boxes * hannah_fireworks_per_box
        answer = visible_fireworks + hannah_total_fireworks
        if answer%1==0:
            break

    # Return the problem and answer
    cot = [f"Calculate the total number of fireworks set off by the city: {city_boxes} * {city_fireworks_per_box} = {city_total_fireworks}.", f"Determine the number of fireworks visible from {name}'s house: {city_total_fireworks} * ({visibility_percent} / 100) = {visible_fireworks}.", f"Calculate the total number of fireworks set off by {name} in the backyard: {hannah_boxes} * {hannah_fireworks_per_box} = {hannah_total_fireworks}.", f"Add the visible city fireworks and the backyard fireworks to find the total number of fireworks {name} will see: {visible_fireworks} + {hannah_total_fireworks} = {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

