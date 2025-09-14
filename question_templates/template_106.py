from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[13]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define possible values for variables
        names = ["Alice", "Bob", "Carlos", "Diana", "Emily", "Frank", "Grace", "Helen", "Ian", "Jasmine", "Sue"]
        items = ["pink plastic flamingos", "garden gnomes", "windmills", "ceramic frogs", "decorative ducks"]
        fractions = ["one third", "one fourth", "one fifth", "half"]
        fraction_values = {"one third": 1/3, "one fourth": 1/4, "one fifth": 1/5, "half": 1/2}
    
        # Randomly select values
        name = random.choice(names)
        item = random.choice(items)
        initial_number = random.choice([12, 16, 18, 20, 24, 30])
        fraction_word = random.choice(fractions)
        fraction_value = fraction_values[fraction_word]
        added_number = random.choice([12, 16, 18, 20, 24, 30])
    
        # Colors
        initial_color = "pink"
        new_color = "white"
    
        # Construct the premise content
        problem = [
            f"{name} lives in a fun neighborhood.",
            f"One weekend, the neighbors decided to play a prank on {name}.",
            f"On Friday morning, the neighbors placed {initial_number} {initial_color} {item} out on {name}'s front yard.",
            f"On Saturday morning, the neighbors took back {fraction_word} of the {item}, painted them {new_color}, and put these newly painted {new_color} {item} back out on {name}'s front yard.",
            f"Then, on Sunday morning, they added another {added_number} {initial_color} {item} to the collection."
        ]
        question = f"At noon on Sunday, how many more {initial_color} {item} were out than {new_color} {item}?"
        original_problem=problem.copy()
        original_problem.append(question)
    
        # Add irrelevant information
        in_topic_irrelevant_infos = [
            f"The neighbors are known for their elaborate pranks in the neighborhood.",
            f"The {item} cost $5 each at the local store.",
            f"{name} was away on a trip during that weekend.",
            f"The prank was featured in the local newspaper."
        ]
        out_topic_irrelevant_infos = [
            f"{name} has a pet dog named Max.",
            f"The weather forecast predicted rain that weekend.",
            f"{name} loves to bake cookies every Sunday.",
            f"The city's annual parade was held on that Saturday."
        ]
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
    
        # Shuffle the order of sentences, except for the first two
        problem_premises = problem[2:]
        if shuffle:
            random.shuffle(problem_premises)
        problem = problem[:2] + problem_premises
    
        # Add the question
        problem.append(question)
    
        # Calculate the answer
        pink_items = initial_number - initial_number * fraction_value
        white_items = initial_number * fraction_value
        pink_items += added_number
        answer = pink_items - white_items
        if answer%1==0:
            break

    # Return the problem and answer
    cot = [f"Initially, there are {initial_number} {initial_color} {item}.", f"On Saturday, {fraction_word} of the {item} are taken back and painted {new_color}. This means {initial_number} * {fraction_value} are painted {new_color}, which is {white_items}.", f"The remaining {item} are still {initial_color}, which is {initial_number} - {white_items}, or {pink_items}.", f"On Sunday, {added_number} more {initial_color} {item} are added, making the total {pink_items} + {added_number}.", f"Finally, the number of {initial_color} {item} is {pink_items}, and the number of {new_color} {item} is {white_items}.", f"Therefore, the difference is {pink_items} - {white_items}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

