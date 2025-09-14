from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[18]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define name lists
        names = ["Greg", "Alice", "Bob", "Carla", "Derek", "Emily", "Frank", "Grace", "Hannah", "Ian"]
        
        # Randomly select a name
        name = random.choice(names)
        
        # Randomly generate variables
        num_times_per_day = random.randint(2, 5)  # Number of times the alarm rings per day
        first_ring = random.randint(1, 5)  # Number of times it rings the first time
        second_ring_factor = random.choice([2, 3, 4])  # How many times longer the second ring is
        third_ring_factor = random.choice([0.5, 0.75])  # How much of the second ring the third ring is
        
        # Additional irrelevant variables
        previous_day_rings = random.randint(10, 20)
        future_day = random.randint(1, 30)
        pet_animals = ["dog", "cat", "rabbit", "hamster"]
        pet = random.choice(pet_animals)
        pet_age = random.randint(1, 15)
        
        # Construct the premise content
        problem = [
            f"{name} has an alarm set to ring three times a day as a reminder.",
            f"When the alarm goes off, it continues to ring until {name} turns it off.",
            f"The first time it went off today, it rang {first_ring} times.",
            f"The second time it went off, it rang for {second_ring_factor} times as long as the first time.",
            f"The third time, it rang for {third_ring_factor} as long as the second time."
        ]
        
        # Construct the question
        question = "How many times did the alarm ring in all today?"
        original_problem=problem.copy()
        original_problem.append(question)
        
        # Add in-topic irrelevant information
        irrelevant_infos = [
            f"The alarm rang {previous_day_rings} times yesterday.",
            f"{name} plans to set the alarm for an additional time {future_day} days from now."
        ]
        
        # Add out-topic irrelevant information
        irrelevant_infos.append(f"{name} has a {pet} that is {pet_age} years old.")
        
        # Add irrelevant information based on probability
        for irrelevant_info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(irrelevant_info)
        
        # Add symbol or grammar errors (assumed functions)
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error),
                prob_symbol_error
            ) for p in problem
        ]
        
        # Shuffle the order of sentences
        if shuffle:
            random.shuffle(problem[1:])
        problem.append(question)
        
        # Calculate the answer
        first_time_rings = first_ring
        second_time_rings = first_ring * second_ring_factor
        third_time_rings = second_time_rings * third_ring_factor
        total_rings = first_time_rings + second_time_rings + third_time_rings
        answer = int(total_rings)
        if answer %1==0:
            break
    
    
    # Return the problem and answer
    cot = [f"The first time the alarm went off, it rang {first_ring} times, so {first_time_rings} is equal to {first_ring}.", f"The second time it went off, it rang for {second_ring_factor} times as long as the first time, so {second_time_rings} is equal to {first_ring} * {second_ring_factor}.", f"The third time, it rang for {third_ring_factor} as long as the second time, so {third_time_rings} is equal to {second_time_rings} * {third_ring_factor}.", f"The total number of rings is the sum of all three times: {first_time_rings} + {second_time_rings} + {third_time_rings}, which is {total_rings}.", f"Therefore, the final answer is {total_rings}, which is equal to {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

