from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[4]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define lists of names and their genders
        names = ["Ryan", "Alice", "Beth", "Cindy", "Derek", "Ethan", "Fiona", "George", "Hannah", "Ivy"]
        genders = {
            "Ryan": "male", "Alice": "female", "Beth": "female", "Cindy": "female", "Derek": "male",
            "Ethan": "male", "Fiona": "female", "George": "male", "Hannah": "female", "Ivy": "female"
        }
        possessive_map = {"male": "his", "female": "her"}
        objective_case_map = {"male": "himself", "female": "herself"}
        pronoun_map = {"male": "he", "female": "she"}
    
        # Randomly select a name and get corresponding gender and pronouns
        name = random.choice(names)
        gender = genders[name]
        possessive = possessive_map[gender]
        objective = objective_case_map[gender]
        pronoun = pronoun_map[gender]
    
        # Randomly generate variables
        allowance_per_week = random.randint(5, 15)  # Allowance per week
        weeks = random.randint(2, 5)  # Number of weeks chores were done
        num_friends = random.randint(1, 5)  # Number of friends
        ice_cream_cost = round(random.uniform(1.0, 3.0), 2)  # Cost per ice cream cone
        ticket_cost = round(random.uniform(5.0, 10.0), 2)  # Cost per movie ticket
    
        # Irrelevant information
        ice_cream_anniversary = random.randint(10, 100)  # Years celebrating
        pet_age = random.randint(1, 10)  # Age of pet
    
        # Construct the problem sentences
        problem = [
            f"{name}'s allowance is ${allowance_per_week} each week {pronoun} completes {possessive} chores.",
            f"{name} did {possessive} chores for {weeks} weeks.",
            f"Then {pronoun} bought ice cream cones for {objective} and {num_friends} friends at ${ice_cream_cost} each.",
            f"Now they all want to go to the movies and tickets cost ${ticket_cost} each."
        ]
    
        # Construct the question
        question = f"How many movie tickets can {name} buy?"
        original_problem=problem.copy()
        original_problem.append(question)
    
        # In-topic irrelevant information
        irrelevant_infos = [
            f"The ice cream shop was celebrating its {ice_cream_anniversary}th anniversary."
        ]
    
        # Out-topic irrelevant information
        irrelevant_infos.append(
            f"{name} has a pet dog that is {pet_age} years old."
        )
    
        # Add irrelevant information based on probability
        for irrelevant_info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(irrelevant_info)
    
        # Add symbol or grammar errors; assume these functions are given
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error),
                prob_symbol_error
            ) for p in problem
        ]
    
        # Shuffle the order of sentences, except for the first one
        first_sentence = problem[0]
        rest_sentences = problem[1:]
        if shuffle:
            random.shuffle(rest_sentences)
        problem = [first_sentence] + rest_sentences
    
        # Add the question at the end
        problem.append(question)
    
        # Calculate the answer
        total_allowance = allowance_per_week * weeks
        total_ice_cream_cost = ice_cream_cost * (1 + num_friends)
        remaining_money = total_allowance - total_ice_cream_cost
        number_of_tickets = remaining_money // ticket_cost
        answer = int(number_of_tickets)
        if remaining_money>0:
            break

    # Return the problem and answer as a dictionary
    cot = [f"{name}'s total allowance for {weeks} weeks is calculated as {allowance_per_week} * {weeks}, which is {total_allowance}.", f"The total cost for ice cream cones for {name} and {num_friends} friends is {ice_cream_cost} * (1 + {num_friends}), which is {total_ice_cream_cost}.", f"The remaining money after buying ice cream is {total_allowance} - {total_ice_cream_cost}, which is {remaining_money}.", f"The number of movie tickets {name} can buy is {remaining_money} // {ticket_cost}, which is {number_of_tickets}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

