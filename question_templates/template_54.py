from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[3]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
    # Define list of possible names
        names = ['Alex', 'Jordan', 'Taylor', 'Casey', 'Jamie', 'Morgan', 'Cameron', 'Sydney', 'Robin', 'Debra']
        
        # Randomly select a name
        name = random.choice(names)
        
        # Randomly generate the variables
        initial_leave_bees = random.randint(10, 100)  # Number of bees leaving in the first 6 hours
        fraction_options = [1/2, 1/3, 1/4, 2/3]
        fraction_return_second_period = random.choice(fraction_options)  # Fraction of bees returning in the next 6 hours
        multiple_options = [2, 3, 4]
        multiple_leave_third_period = random.choice(multiple_options)  # Multiple of bees leaving in the third 6 hours
    
        # Additional numbers for irrelevant info
        total_bee_population = random.randint(200, 1000)  # Total number of bees in the hive
        number_of_hives = random.randint(1, 10)
        beekeeper_years = random.randint(1, 20)
    
        # Premises
        problem = [
            f"{name} is monitoring a beehive to see how many bees come and go in a day.",
            f"{name} sees {initial_leave_bees} bees leave the hive in the first 6 hours, and then {name} sees {int(fraction_return_second_period*100)}% that many bees return in the next 6 hours.",
            f"{name} sees {multiple_leave_third_period} times as many bees as {name} saw first leave the hive fly from the hive and leave in the next 6 hours.",
            f"Then every bee that left before that hadn't already returned returns to the hive in the next 6 hours."
        ]
    
        # Question
        question = f"How many bees did {name} see return to the hive in the last 6 hours of the day?"
        original_problem=problem.copy()
        original_problem.append(question)
    
        # In-topic irrelevant information
        irrelevant_infos = [
            f"The total bee population in the hive is {total_bee_population} bees.",
            f"{name} has been a beekeeper for {beekeeper_years} years.",
            f"There are {number_of_hives} hives in the apiary."
        ]
    
        # Out-topic irrelevant information
        out_topic_info = f"{name} enjoys painting and has recently started learning the guitar."
        irrelevant_infos.append(out_topic_info)
    
        # Add irrelevant information based on probability
        for info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(info)
        
        # Add symbol or grammar errors (assuming functions are given)
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error), 
                prob_symbol_error
            ) for p in problem
        ]
        
        # Shuffle the premises except for the first one
        premises = problem[1:-1]
        if shuffle:
            random.shuffle(premises)
        problem = [problem[0]] + premises + [problem[-1], question]
        
        # Calculate the answer
        # Bees that left in first period: initial_leave_bees
        # Bees that returned in second period: fraction_return_second_period * initial_leave_bees
        bees_returned_second_period = fraction_return_second_period * initial_leave_bees
        bees_left_in_first_period_unreturned = initial_leave_bees - bees_returned_second_period
    
        # Bees that left in third period: multiple_leave_third_period * initial_leave_bees
        bees_left_third_period = multiple_leave_third_period * initial_leave_bees
    
        # Total bees that left and hadn't returned before last period:
        total_bees_left_unreturned = bees_left_in_first_period_unreturned + bees_left_third_period
    
        # In the last period, all these bees return
        answer = total_bees_left_unreturned
        if answer%1==0:
            break

    # Return problem and answer
    cot = [f"{name} sees {initial_leave_bees} bees leave the hive in the first 6 hours.", f"In the next 6 hours, {fraction_return_second_period} of those bees return, which is {bees_returned_second_period}.", f"The number of bees that left in the first period and hadn't returned is {initial_leave_bees} - {bees_returned_second_period}, which is {bees_left_in_first_period_unreturned}.", f"In the third 6 hours, {multiple_leave_third_period} times as many bees as initially left fly from the hive, which is {bees_left_third_period}.", f"The total number of bees that left and hadn't returned before the last period is {bees_left_in_first_period_unreturned} + {bees_left_third_period}, which is {total_bees_left_unreturned}.", f"In the last 6 hours, all these bees return, so the answer is {total_bees_left_unreturned}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

