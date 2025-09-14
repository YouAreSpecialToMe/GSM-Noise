from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[5]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define name and item lists
        names = ["Alex", "Maria", "Chen", "Fatima", "Liam", "Sofia", "Omar", "Priya", "Jorge", "Kofi", "Satoshi", "Anna"]
        items = ["bars of chocolate", "cookies", "candies", "ice cream cones", "toy cars", "books", "shoes", "bicycles", "cell phones", "chairs"]
    
        # Randomly select a name and an item
        name = random.choice(names)
        item = random.choice(items)
    
        # Randomly generate production-related values
        monthly_production = random.randint(40000, 100000)
        first_week_production = random.randint(5000, 20000)
        second_week_production = first_week_production // 2  # integer division
        third_week_production = first_week_production * 3
        total_first_three_weeks = first_week_production + second_week_production + third_week_production
        fourth_week_production = monthly_production - total_first_three_weeks
    
        # Ensure the fourth_week_production is positive
        while fourth_week_production < 0:
            monthly_production = random.randint(total_first_three_weeks, total_first_three_weeks + 50000)
            fourth_week_production = monthly_production - total_first_three_weeks
    
        # Construct the premise content, breaking it down into sentence level
        problem = [
            f"{name} owns a {item} factory.",
            f"{name} produces {monthly_production} {item} each month.",
            f"{name} produces {first_week_production} {item} the first week.",
            f"The second week, {name} only produces half as much as the first week.",
            f"But, the third week, {name} produces three times as much as the first week."
        ]
    
        # Construct the question
        question = f"How much does {name} produce the fourth week?"
        original_problem=problem.copy()
        original_problem.append(question)
    
        # Add in-topic irrelevant information
        irrelevant_infos = [
            f"{name} started the factory {random.randint(1, 20)} years ago.",
            f"The factory employs {random.randint(50, 500)} workers."
        ]
    
        # Add out-topic irrelevant information
        hobbies = ["painting", "playing guitar", "cycling", "swimming", "hiking", "reading books", "photography"]
        hobby = random.choice(hobbies)
        irrelevant_infos.append(f"{name} is an avid {hobby} enthusiast during {name}'s free time.")
    
        # Add irrelevant information based on probability
        for irrelevant_info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(irrelevant_info)
    
        # Add symbol or grammar errors. Assume these functions are given.
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error), 
                prob_symbol_error
            ) for p in problem
        ]
    
        # Shuffle the order of sentences, except for the first one
        first_sentence = problem[0]
        other_sentences = problem[1:]
        if shuffle:
            random.shuffle(other_sentences)
        problem = [first_sentence] + other_sentences
    
        # Add the question
        problem.append(question)
    
        # Calculate the answer
        answer = fourth_week_production
        if answer%1==0 and  second_week_production%1==0:
            break

    # Return premise and answer as a dictionary
    cot = [f"{name} produces half as much in the second week as in the first week, which is {first_week_production} // 2, resulting in {second_week_production}.", f"In the third week, {name} produces three times as much as in the first week, which is {first_week_production} * 3, resulting in {third_week_production}.", f"The total production for the first three weeks is {first_week_production} + {second_week_production} + {third_week_production}, which is {total_first_three_weeks}.", f"The production for the fourth week is the monthly production minus the total of the first three weeks, which is {monthly_production} - {total_first_three_weeks}, resulting in {fourth_week_production}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

