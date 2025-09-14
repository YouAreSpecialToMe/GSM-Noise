from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[16]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define a list of diverse names
        names = ["Garrett", "Alice", "Brandon", "Cynthia", "David", "Evelyn", "Frank", "Grace", "Helen", "Ian", "Julia", "Kevin"]
        
        # Randomly select a name
        name = random.choice(names)
        
        # Define variables with possible alternative values
        initial_pop_rate = random.randint(10, 50)  # Kernels popped in the first interval
        pop_interval = random.choice([20, 30, 40])  # Time interval in seconds
        multiplier_second = random.randint(2, 4)  # Multiplier for second interval
        multiplier_third = random.randint(3, 5)   # Multiplier for third interval
        factor_fourth = round(random.uniform(0.4, 0.6), 2)  # Factor for fourth interval
        residual_factor = round(random.uniform(0.2, 0.4), 2)  # Fraction of kernels popping after heat
    
         # Resolve percentages for factors
        factor_fourth_percentage = int(factor_fourth * 100)
        residual_factor_percentage = int(residual_factor * 100)
        
        
        # Break the problem into individual premises with variables
        problem = [
            f"{name} is popping popcorn for a snack.",
            f"As the pan of kernels heats up, the kernels start popping faster.",
            f"{initial_pop_rate} pop in the first {pop_interval} seconds of cooking, then {multiplier_second} times that amount in the next {pop_interval} seconds.",
            f"The kernels increase to {multiplier_third} times the initial popping rate in the next {pop_interval} seconds, but in the final {pop_interval} seconds, the popping slows down to {factor_fourth_percentage}% the rate of the past {pop_interval} seconds.",
            f"After {name} takes the pan off the heat, {residual_factor_percentage}% of the number of kernels that popped in the final {pop_interval} seconds of cooking also pop from the residual heat."
        ]
        
       
    
        
        # Construct the question
        question = f"How many pieces of popcorn does {name} have to eat?"

        original_problem=problem.copy()
        original_problem.append(question)
        
        # In-topic irrelevant information
        irrelevant_infos = [
            f"{name} used {random.randint(1, 5)} tablespoons of oil in the pan.",
            f"The pan has a diameter of {random.randint(20, 30)} centimeters.",
            f"{name} plans to watch a movie after making the popcorn.",
            f"The total cooking time is {pop_interval * 4} seconds."
        ]
        
        # Out-topic irrelevant information
        irrelevant_infos.extend([
            f"{name} scored {random.randint(80, 100)}% on a recent math test.",
            f"It is {random.randint(15, 25)} degrees Celsius outside.",
            f"{name} has {random.randint(1, 3)} pet(s) at home."
        ])
        
        # Randomly add irrelevant information based on probability
        for info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(info)
        
        #Add symbol or grammar errors (assuming functions are given)
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(sentence, prob_grammar_error),
                prob_symbol_error
            ) for sentence in problem
        ]
        
        # Shuffle the order of sentences except for the first two
        middle_sentences = problem[2:-1]
        if shuffle:
            random.shuffle(middle_sentences)
        problem[2:-1] = middle_sentences
        
        # Add the question at the end
        problem.append(question)
        
        # Calculate the answer using variables
        pops_first = initial_pop_rate
        pops_second = multiplier_second * initial_pop_rate
        pops_third = multiplier_third * initial_pop_rate
        pops_fourth = factor_fourth * pops_third
        residual_pops = residual_factor * pops_fourth
        answer = pops_first + pops_second + pops_third + pops_fourth + residual_pops
        if answer%1==0:
            break
    
    # Return the problem and answer
    cot = [f"In the first {pop_interval} seconds, {initial_pop_rate} kernels pop, so {pops_first} kernels pop initially.", f"In the next {pop_interval} seconds, the popping rate is {multiplier_second} times the initial rate, resulting in {pops_second} kernels popping.", f"In the following {pop_interval} seconds, the popping rate increases to {multiplier_third} times the initial rate, resulting in {pops_third} kernels popping.", f"In the final {pop_interval} seconds, the popping slows to {factor_fourth} times the rate of the previous interval, resulting in {pops_fourth} kernels popping.", f"After taking the pan off the heat, {residual_factor} of the kernels that popped in the final interval pop from residual heat, resulting in {residual_pops} additional kernels popping.", f"The total number of pieces of popcorn is the sum of all popped kernels: {pops_first} + {pops_second} + {pops_third} + {pops_fourth} + {residual_pops}, which equals {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

