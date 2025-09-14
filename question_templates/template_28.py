from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[6]:


import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    while True:
        # Define alternative names
        names = ["Felix", "Alex", "Jordan", "Taylor", "Casey", "Quinn", "Riley", "Morgan", "Avery", "Sam"]

        # Define alternative costs per branch
        cost_per_branch_options = [0.10, 0.15, 0.20, 0.25, 0.30, 0.50]

        # Define alternative total money made
        total_money_options = [50, 70, 84, 91, 105, 112, 126, 140, 154]

        # Define alternative durations
        duration_options = [5, 6, 7, 8]

        # Randomly assign variables
        name = random.choice(names)
        cost_per_branch = random.choice(cost_per_branch_options)
        total_money = random.choice(total_money_options)
        duration = random.choice(duration_options)

        # Construct problem sentences
        problem = [
            f"{name} notices that kids in the neighborhood are always getting things stuck in trees.",
            f"Since {name} is an expert tree climber, {name} decided to start charging kids to get their stuff out.",
            f"{name} charges based on how high {name} has to climb.",
            f"Every branch {name} has to climb up costs ${cost_per_branch:.2f}.",
            f"During {duration} days, {name} made ${total_money}."
        ]

        # Construct irrelevant information
        in_topic_irrelevant_infos = [
            f"{name} invested ${random.randint(10, 100)} in new climbing gear.",
            f"{name} helps his neighbors with gardening.",
            f"The tallest tree {name} climbed was {random.randint(20, 50)} feet high.",
            f"{name} spends {random.randint(1, 5)} hours climbing trees each day.",
            f"On weekends, {name} volunteers at the local animal shelter."
        ]

        out_topic_irrelevant_infos = [
            f"{name}'s favorite color is {random.choice(['blue', 'green', 'red', 'yellow', 'purple'])}.",
            f"{name} plays {random.choice(['soccer', 'basketball', 'chess', 'piano'])} in free time.",
            f"{name} has a pet {random.choice(['dog', 'cat', 'parrot'])} named {random.choice(['Buddy', 'Max', 'Bella'])}.",
            f"{name} received a {random.choice(['bike', 'skateboard', 'guitar'])} for a birthday gift."
        ]

        # Add irrelevant information based on probability
        irrelevant_infos = []
        for info in in_topic_irrelevant_infos + out_topic_irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(info)

        # Add the question
        question = f"On average, how many branches did {name} climb per day?"
        original_problem = problem.copy()
        original_problem.append(question)

        # Shuffle the sentences except the question
        if shuffle:
            random.shuffle(problem[1:])

        # Introduce symbol or grammar errors
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(sentence, prob_grammar_error),
                prob_symbol_error
            ) for sentence in problem
        ]

        # Add the question at the end
        problem.append(question)

        # Calculate the answer
        total_branches = total_money / cost_per_branch
        average_branches_per_day = total_branches / duration
        answer = average_branches_per_day
        if answer % 1 == 0:
            break

    # Return the problem and the answer
    cot = [
        f"Calculate the total number of branches climbed by dividing {total_money} by {cost_per_branch}, which gives {total_branches}.",
        f"Determine the average number of branches climbed per day by dividing {total_branches} by {duration}, resulting in {average_branches_per_day}.",
        f"Thus, the answer is {average_branches_per_day}."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
