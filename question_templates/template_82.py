from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[16]:


import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    while True:
        # Define variable lists
        names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Jamie", "Cameron"]
        # Randomly select a name
        name = random.choice(names)

        # Randomly generate AC-related values
        low_cool_rate = random.randint(1, 5)  # degrees per hour cooled on low
        high_cool_rate = random.randint(low_cool_rate + 1, low_cool_rate + 5)  # degrees per hour cooled on high
        warm_rate = random.randint(1, 5)  # degrees per hour the room warms up when AC is off

        low_hours = random.randint(1, 5)  # hours AC runs on low
        high_hours = random.randint(1, 5)  # hours AC runs on high
        off_hours = random.randint(1, 5)  # hours AC is off

        # Additional irrelevant variables
        outside_temp = random.randint(25, 40)
        ac_power_usage = random.randint(500, 2000)  # in watts
        ac_purchase_price = random.randint(300, 1000)  # in dollars

        # In-topic irrelevant info
        irrelevant_infos = [
            f"The outside temperature is {outside_temp} degrees Celsius.",
            f"The air conditioner consumes {ac_power_usage} watts of power while running.",
            f"{name} bought the air conditioner for ${ac_purchase_price}."
        ]

        # Out-topic irrelevant info
        hobbies = ["painting", "playing guitar", "hiking", "photography", "reading"]
        hobby = random.choice(hobbies)
        siblings = random.randint(0, 5)
        irrelevant_infos.append(f"{name} enjoys {hobby} in their free time and has {siblings} siblings.")

        # Construct the premises
        problem = [
            f"An air conditioner cools a room {low_cool_rate} degrees an hour on low and {high_cool_rate} degrees an hour on high.",
            f"The room will warm up at {warm_rate} degrees an hour with no air conditioner running.",
            f"The air conditioner ran on low for {low_hours} hours, then it was turned up to high for {high_hours} hours.",
            f"Afterward, it was turned off for {off_hours} hours."
        ]

        # Construct the question
        question = f"How many degrees lower than the starting temperature was the final temperature?"
        original_problem = problem.copy()
        original_problem.append(question)

        # Add irrelevant information based on probability
        for irrelevant_info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(irrelevant_info)

        # Add symbol or grammar errors (Assuming functions are given)
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error),
                prob_symbol_error
            ) for p in problem
        ]

        # Shuffle the order of sentences, except for the question
        if shuffle:
            random.shuffle(problem)

        # Append the question at the end
        problem.append(question)

        # Calculate the answer
        total_cooling = (low_cool_rate * low_hours) + (high_cool_rate * high_hours)
        total_warming = warm_rate * off_hours
        answer = total_cooling - total_warming
        if answer > 0:
            break

    # Return problem and answer
    cot = [
        f"The air conditioner cools the room at {low_cool_rate} degrees per hour on low for {low_hours} hours, and at {high_cool_rate} degrees per hour on high for {high_hours} hours. Therefore, the total cooling is ({low_cool_rate} * {low_hours}) + ({high_cool_rate} * {high_hours}), which is {total_cooling}.",
        f"The room warms up at {warm_rate} degrees per hour when the air conditioner is off for {off_hours} hours. Therefore, the total warming is {warm_rate} * {off_hours}, which is {total_warming}.",
        f"The final temperature is the starting temperature minus the total cooling plus the total warming, which is {total_cooling} - {total_warming}, resulting in {answer} degrees lower than the starting temperature."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
