from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define name list
    names = ['Shawnda', 'Alice', 'Beth', 'Clara', 'Diana', 'Ella', 'Fiona', 'Grace', 'Hannah', 'Isabel',
             'Jack', 'Kevin', 'Liam', 'Mike', 'Nathan', 'Oscar', 'Paul', 'Quinn', 'Ryan', 'Steve']

    # Randomly select a name
    name = random.choice(names)

    # Randomly generate values
    cost_per_tire_cents = random.randint(10, 50)  # cost per tire in cents
    num_bicycle_people = random.randint(3, 10)
    num_tricycle_people = random.randint(1, 5)
    num_unicycle_people = random.randint(0, 2)

    # Construct the premise content
    problem = [
        f"{name} decides that her neighborhood kids could really use a bike inflation service.",
        f"{name} decides the best way to charge is by the tire.",
        f"Each tire costs {cost_per_tire_cents} cents to inflate.",
        f"On the first day, {num_bicycle_people} people on bicycles came by to get both tires inflated.",
        f"{num_tricycle_people} people came by to get all their tricycle tires inflated.",
        f"Finally, {num_unicycle_people} person actually came by on a unicycle."
    ]

    # Construct the question
    question = f"How many dollars did {name} make that day?"
    original_problem=problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    in_topic_irrelevant_info = [
        f"{name} invested in an air pump that cost her $50 to start her business.",
        f"{name} plans to expand her service to include bike repairs in the future.",
        f"The neighborhood has a total of 200 kids with bicycles, tricycles, or unicycles."
    ]

    # Add out-topic irrelevant information
    out_topic_irrelevant_info = [
        f"{name} is also a talented musician who plays the violin.",
        f"{name} won a local art competition last week.",
        f"{name}'s favorite subject in school is mathematics."
    ]

    # Combine irrelevant information
    irrelevant_infos = in_topic_irrelevant_info + out_topic_irrelevant_info

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle sentences except the first one
    sentences_to_shuffle = problem[1:]
    if shuffle:
        random.shuffle(sentences_to_shuffle)
    problem = [problem[0]] + sentences_to_shuffle

    # Add the question
    problem.append(question)

    # Calculate the total number of tires
    total_tires = num_bicycle_people * 2 + num_tricycle_people * 3 + num_unicycle_people * 1

    # Calculate the total revenue in cents
    total_revenue_cents = total_tires * cost_per_tire_cents

    # Final answer in dollars
    answer = total_revenue_cents / 100

    # Return the problem and answer as a dictionary
    cot = [f"Calculate the total number of tires by multiplying {num_bicycle_people} by 2, {num_tricycle_people} by 3, and {num_unicycle_people} by 1, then summing them up to get {total_tires}.", f"Calculate the total revenue in cents by multiplying {total_tires} by {cost_per_tire_cents}, resulting in {total_revenue_cents}.", f"Convert the total revenue from cents to dollars by dividing {total_revenue_cents} by 100, resulting in {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

