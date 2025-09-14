from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[3]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
    # Define lists of names and countries
        names = ["Cameron", "Alex", "Jordan", "Taylor", "Morgan", "Riley"]
        countries = ["the Philippines", "Thailand", "Mexico", "Spain", "Greece"]
    
        # Randomly select a name and a country
        name = random.choice(names)
        country = random.choice(countries)
    
        # Randomly generate hotel charges and times
        twelve_hour_charge = random.randint(500, 1500)
        additional_hour_charge = random.randint(50, 150)
        twenty_four_hour_charge = twelve_hour_charge + random.randint(400, 1000)
    
        # Random arrival and departure times
        arrival_hour = random.randint(0, 23)
        arrival_period = "am" if arrival_hour < 12 else "pm"
        arrival_hour_12 = arrival_hour % 12 if arrival_hour % 12 != 0 else 12
        arrival_time = f"{arrival_hour_12} {arrival_period}"
    
        total_stay_hours = random.randint(13, 23)  # Between 13 and 23 hours
        departure_hour = (arrival_hour + total_stay_hours) % 24
        departure_period = "am" if departure_hour < 12 else "pm"
        departure_hour_12 = departure_hour % 12 if departure_hour % 12 != 0 else 12
        departure_time = f"{departure_hour_12} {departure_period}"
    
        # Construct the problem premises
        problem = [
            f"A hotel in {country} charges {twelve_hour_charge} pesos for a 12-hour stay or {twenty_four_hour_charge} pesos for a 24-hour stay.",
            f"After 12 hours, visitors have the option to add {additional_hour_charge} pesos for every additional hour.",
            f"{name} arrives at {arrival_time} at the hotel and wants to leave at {departure_time}.",
            f"He decides to go with the option of adding on {additional_hour_charge} pesos for every hour after the 12-hour mark instead of paying for 24 hours."
        ]
    
        # Construct the question
        question = f"How much money would {name} save?"
        original_problem=problem.copy()
        original_problem.append(question)
    
        # Add in-topic irrelevant information
        irrelevant_infos = [
            f"The hotel offers free Wi-Fi to all guests.",
            f"There is a popular tourist attraction near the hotel."
        ]
    
        # Add out-topic irrelevant information
        irrelevant_infos.append(f"{name} enjoys surfing during his vacations.")
    
        # Add irrelevant information based on probability
        for irrelevant_info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(irrelevant_info)
    
        # Add symbol or grammar errors. Assume that the functions are given.
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error),
                prob_symbol_error
            ) for p in problem
        ]
    
        # Shuffle the order of sentences, except for the first one
        main_premise = problem[0]
        other_sentences = problem[1:]
        if shuffle:
            random.shuffle(other_sentences)
        problem = [main_premise] + other_sentences
    
        # Add the question
        problem.append(question)
    
        # Calculate the answer using the variables
        total_additional_hours = total_stay_hours - 12
        option1_cost = twenty_four_hour_charge
        option2_cost = twelve_hour_charge + total_additional_hours * additional_hour_charge
        answer = option1_cost - option2_cost
        if answer>0:
            break

    # Return premise and answer as a dictionary
    cot = [f"The total additional hours after the initial 12-hour stay is {total_stay_hours} - 12, which is {total_additional_hours}.", f"The cost for staying 24 hours is {twenty_four_hour_charge}, which is the option1_cost.", f"The cost for staying 12 hours plus additional hours is {twelve_hour_charge} + {total_additional_hours} * {additional_hour_charge}, which is {option2_cost}.", f"The amount of money {name} would save is {option1_cost} - {option2_cost}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

