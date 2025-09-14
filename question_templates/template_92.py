from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[7]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):

    # Names list
    names = ["Martha", "Beth", "Cindy", "Diana", "Charlotte", "Helen", "Grace", "Olivia", "Eleanor", "Liam", "Noah", "James"]
    knitter_name = random.choice(names)
    
    # Number of grandchildren from 1 to 5
    num_grandchildren = random.randint(1, 5)

    # Determine if they're twins or triplets
    if num_grandchildren == 2:
        twins_triplets = "twins"
    elif num_grandchildren == 3:
        twins_triplets = "triplets"
    else:
        twins_triplets = None
    
    # Items to make; select 3 to 6 random items
    possible_items = ["hat", "scarf", "sweater", "mittens", "socks", "gloves", "vest", "poncho", "blanket", "cardigan"]
    num_items = random.randint(3, 6)
    items_to_make = random.sample(possible_items, num_items)
    
    # Skeins needed per item, randomly assigned from 1 to 15
    skeins_per_item = {}
    for item in items_to_make:
        skeins_needed = random.randint(1, 15)
        skeins_per_item[item] = skeins_needed
    
    # Construct the problem
    problem = []
    
    # First sentence
    problem.append(f"{knitter_name} is knitting winter wear for {num_grandchildren} grandchildren.")
    
    # Second sentence, if twins or triplets
    if twins_triplets:
        problem.append(f"They're {twins_triplets}, so they are all the same size.")
    
    # Third sentence, list items
    item_list_str = ', '.join(items_to_make[:-1]) + f", and {items_to_make[-1]}"
    problem.append(f"{knitter_name} wants to make a {item_list_str} for each of them.")
    
    # Fourth sentence, list skeins per item
    skeins_info = []
    for item in items_to_make:
        skeins = skeins_per_item[item]
        if skeins == 1:
            skeins_info.append(f"{skeins} skein for a {item}")
        else:
            skeins_info.append(f"{skeins} skeins for a {item}")
    skeins_info_str = ', '.join(skeins_info[:-1]) + f", and {skeins_info[-1]}."
    problem.append(f"It takes {skeins_info_str}")
    original_problem=problem.copy()
    
    # Construct in-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"{knitter_name} has been knitting for over {random.randint(5, 50)} years.",
        f"The grandchildren live in a city where winter lasts for {random.randint(3,6)} months."
    ]
    
    # Construct out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{knitter_name}'s favorite color is {random.choice(['blue', 'green', 'red', 'yellow'])}.",
        f"A new shopping mall opened in {knitter_name}'s town last week."
    ]
    
    # Add irrelevant information based on probability
    for info in in_topic_irrelevant_infos + out_topic_irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)
    irrelevant_infos=in_topic_irrelevant_infos + out_topic_irrelevant_infos
    
    # Add symbol or grammar errors (assuming the functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the sentences except for the first one
    first_sentence = problem[0]
    rest_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_sentences)
    problem = [first_sentence] + rest_sentences
    
    # Add the question
    problem.append(f"How many skeins of wool will {knitter_name} need to buy?")
    original_problem.append(f"How many skeins of wool will {knitter_name} need to buy?")
    
    # Calculate the answer using the variables
    # total_skeins_per_grandchild = sum of skeins_per_item values
    total_skeins_per_grandchild = sum(skeins_per_item[item] for item in items_to_make)
    # total_skeins = num_grandchildren * total_skeins_per_grandchild
    total_skeins = num_grandchildren * total_skeins_per_grandchild
    # Final answer
    answer = total_skeins
    
    # Return problem and answer as a dictionary
    cot = [f"Calculate the total skeins needed per grandchild by summing the skeins required for each item in {items_to_make}. This gives {total_skeins_per_grandchild}.", f"Multiply the total skeins per grandchild, {total_skeins_per_grandchild}, by the number of grandchildren, {num_grandchildren}, to get the total skeins needed, which is {total_skeins}.", f"The final answer is the total skeins needed, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

