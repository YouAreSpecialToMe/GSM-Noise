from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[21]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
        # Define names
    while True:
        names = ["Mr. Julius", "Ms. Smith", "Dr. Allen", "Professor Green", "Engineer Brown", "Farmer Johnson"]
    
        # Define tree species
        trees_species1 = ["White Oak", "Red Maple", "Birch", "Pine", "Cedar"]
        trees_species2 = ["Lodgepole Pine", "Douglas Fir", "Spruce", "Hemlock", "Aspen"]
    
        # Randomly select name and tree species
        name = random.choice(names)
        tree1 = random.choice(trees_species1)
        tree2 = random.choice([t for t in trees_species2 if t != tree1])
    
        # Default variables (original problem values)
        white_oak_first_day = 20  # default value
        lodgepole_multiplier = 2.0  # default value
        white_oak_increase_second_day = 10  # default value
        lodgepole_percent_increase_second_day = 0.25  # default value
    
        # Randomize variables
        white_oak_first_day = random.randint(10, 50)
        lodgepole_multiplier = random.choice([1, 1.5, 2, 2.5, 3])
        white_oak_increase_second_day = random.randint(5, 20)
        lodgepole_percent_increase_second_day = random.choice([0.1, 0.2, 0.25, 0.5, 0.75, 1.0])
    
        # Calculate number of trees planted
        lodgepole_first_day = int(lodgepole_multiplier * white_oak_first_day)
        white_oak_second_day = white_oak_first_day + white_oak_increase_second_day
        lodgepole_second_day = (lodgepole_first_day + lodgepole_percent_increase_second_day * lodgepole_first_day)
    
        total_trees = white_oak_first_day + lodgepole_first_day + white_oak_second_day + lodgepole_second_day
    
        # Construct the problem statements
        problem = []
        problem.append(f"To participate in the local community tree-planting campaign, {name} planted {white_oak_first_day} trees of {tree1} and {lodgepole_multiplier} times as many {tree2} as {tree1} on the first day.")
        problem.append(f"On the second day, {name} planted {white_oak_increase_second_day} more {tree1} trees and {lodgepole_percent_increase_second_day * 100}% more {tree2} trees than {name} planted on the first day.")
        problem.append(f"Calculate the total number of trees planted by {name} in the two days.")
        original_problem=problem.copy()
    
        # In-topic irrelevant information
        in_topic_irrelevant_infos = [
            f"The {tree1} is known for its high-quality wood.",
            f"The tree-planting campaign aims to plant 1000 trees in the community park.",
            f"The {tree2} is native to the region and supports local wildlife."
        ]
    
        # Out-topic irrelevant information
        out_topic_irrelevant_infos = [
            f"{name} also volunteers at the local animal shelter.",
            f"Besides planting trees, {name} enjoys painting landscapes.",
            f"{name} has been living in the town for 20 years."
        ]
    
        # Randomly add irrelevant information
        for info in in_topic_irrelevant_infos + out_topic_irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(info)
        irrelevant_infos=in_topic_irrelevant_infos + out_topic_irrelevant_infos
    
        # Add symbol or grammar errors
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error),
                prob_symbol_error
            ) for p in problem
        ]
    
        # Shuffle sentences except the last one (the question)
        question = problem[-1]
        
        original_problem.append(question)
        problem = problem[:-1]
        if shuffle:
            random.shuffle(problem)
        problem.append(question)
    
        # Calculate the answer
        answer = total_trees
        if answer%1==0:
            break

    # Return problem and answer
    cot = [f"{name} planted {white_oak_first_day} trees of {tree1} on the first day.", f"He also planted {lodgepole_multiplier} times as many {tree2} as {tree1}, which is {lodgepole_first_day} {tree2} trees.", f"On the second day, {name} planted {white_oak_increase_second_day} more {tree1} trees, making it {white_oak_second_day} {tree1} trees in total.", f"He also planted {lodgepole_percent_increase_second_day * 100}% more {tree2} trees than the first day, which is {lodgepole_second_day} {tree2} trees.", f"The total number of trees planted by {name} in the two days is {total_trees}.", f"Therefore, the final answer is {total_trees}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

