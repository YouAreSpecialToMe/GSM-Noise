from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[9]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define possible alternative values
        names = ["George", "Oliver", "Luke", "Nathan", "Thomas", "Henry", "James", "Alex", "Michael", "Liam"]
        num_implants_list = [1, 2, 3, 4, 5]
        base_price_options = [1000, 1500, 2000, 2500, 3000]
        features = ["porcelain crown", "gold crown", "titanium crown", "ceramic crown"]
        feature_costs = [500, 700, 800, 600]
        deposits = [x*100 for x in range(1,11)]
        wages = [x for x in range(10,31)]
    
        # Randomly assign values
        name = random.choice(names)
        num_implants = random.choice(num_implants_list)
        base_price_per_implant = random.choice(base_price_options)
        feature_index = random.randint(0, len(features)-1)
        feature = features[feature_index]
        extra_feature_cost = feature_costs[feature_index]
        deposit = random.choice(deposits)
        hourly_wage = random.choice(wages)
    
        # Construct the problem premises
        problem = [
            f"{name} needs to pay for dental work.",
            f"{name} needs {num_implants} implants.",
            f"Each implant has a base price of ${base_price_per_implant}.",
            f"For one of the implants, {name} wants a {feature}. That feature costs an extra ${extra_feature_cost}.",
            f"{name} has already put down a deposit of ${deposit}.",
            f"{name} makes ${hourly_wage} per hour at work."
        ]
    
        # Construct the question
        question = f"How many hours does {name} need to work before {name} has enough to pay for the dental work?"
        original_problem=problem.copy()
        original_problem.append(question)
    
        # In-topic irrelevant information
        irrelevant_in_topic = [
            f"The dentist has over 20 years of experience."
        ]
    
        # Out-topic irrelevant information
        irrelevant_out_topic = [
            f"{name} has a pet dog named Max.",
            f"{name} enjoys playing basketball on weekends.",
            f"{name} is saving up to buy a new car that costs $20,000.",
            f"{name}'s favorite color is blue."
        ]
    
        # Combine irrelevant infos
        irrelevant_infos = irrelevant_in_topic + irrelevant_out_topic
    
        # Randomly add irrelevant infos based on probability
        for info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(info)
    
        # Shuffle the problem premises
        if shuffle:
            random.shuffle(problem)
    
        # Add symbol or grammar errors
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error),
                prob_symbol_error
            ) for p in problem
        ]
    
        question = introduce_symbol_error(
            introduce_grammar_error(question, prob_grammar_error),
            prob_symbol_error
        )
    
        # Calculate the answer
        total_cost = (num_implants * base_price_per_implant) + extra_feature_cost - deposit
        answer = total_cost / hourly_wage
        if answer%1==0:
            break

    # Return the problem and answer
    cot = [f"Calculate the total cost of the dental work by multiplying the number of implants {num_implants} by the base price per implant {base_price_per_implant}, adding the extra feature cost {extra_feature_cost}, and subtracting the deposit {deposit}. This gives us {total_cost}.", f"Determine the number of hours {name} needs to work by dividing the total cost {total_cost} by the hourly wage {hourly_wage}. This results in {answer} hours."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

