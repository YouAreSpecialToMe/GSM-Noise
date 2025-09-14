from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[12]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define name and item lists
    names = ["Sidney", "Alex", "Jordan", "Taylor", "Casey", "Morgan", "Blake", "Jamie", "Riley", "Parker", "Pat", "Leslie", "Kendall", "Bailey", "Quinn", "Skyler"]
    items = ["meatball sub sandwich", "chicken wrap","sushi roll", "taco", "pancake", "cheese pizza", "falafel wrap", "burrito", "quesadilla"]
    
    # Randomly select person names, ensuring they are different
    name1 = random.choice(names)
    names.remove(name1)
    name2 = random.choice(names)
    
    # Randomly select an item
    item = random.choice(items)
    
    # Randomly generate variables
    meatballs_per_sandwich = random.randint(2, 8)
    initial_sandwiches = random.randint(5, 8)
    sandwiches_eaten_by_person2 = random.randint(2, min(5, initial_sandwiches))
    additional_sandwiches_ordered = random.randint(1, 5)
    
    # Additional variables for irrelevant info
    sandwich_price = random.randint(3, 10)
    calories_per_sandwich = random.randint(200, 800)
    favorite_drink = random.choice(["cola", "iced tea", "lemonade", "water", "orange juice"])
    money_in_wallet = random.randint(20, 100)
    total_customers_in_store = random.randint(10, 50)
    
    # Construct the premises
    problem = [
        f"One {item} contains {meatballs_per_sandwich} meatballs.",
        f"{name1} ordered {initial_sandwiches} {item}s.",
        f"Then {name2} ate {sandwiches_eaten_by_person2} of {name1}'s {item}s.",
        f"So {name1} ordered another {additional_sandwiches_ordered} {item}s."
    ]
    
    # Construct the question
    question = f"How many meatballs were in the {item}s that remained?"
    original_problem=problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"Each {item} costs ${sandwich_price}.",
        f"Each {item} has about {calories_per_sandwich} calories."
    ]
    
    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name2} likes to drink {favorite_drink}.")
    irrelevant_infos.append(f"{name1} has ${money_in_wallet} in {name1}'s wallet.")
    irrelevant_infos.append(f"There are {total_customers_in_store} customers in the store.")
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors. Assume that introduce_symbol_error and introduce_grammar_error functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_of_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_of_sentences)
    problem = [first_sentence] + rest_of_sentences
    
    # Add the question at the end
    problem.append(question)
    
    # Calculate the answer
    final_sandwiches = initial_sandwiches - sandwiches_eaten_by_person2 + additional_sandwiches_ordered
    answer = final_sandwiches * meatballs_per_sandwich
    
    # Return problem and answer as a dictionary
    cot = [f"{name1} initially ordered {initial_sandwiches} {item}s.", f"{name2} ate {sandwiches_eaten_by_person2} of {name1}'s {item}s.", f"So, the remaining {item}s are {initial_sandwiches} - {sandwiches_eaten_by_person2}.", f"{name1} then ordered another {additional_sandwiches_ordered} {item}s.", f"Therefore, the total number of {item}s that remained is {initial_sandwiches} - {sandwiches_eaten_by_person2} + {additional_sandwiches_ordered}, which is {final_sandwiches}.", f"Each {item} contains {meatballs_per_sandwich} meatballs.", f"Thus, the total number of meatballs in the remaining {item}s is {final_sandwiches} * {meatballs_per_sandwich}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

