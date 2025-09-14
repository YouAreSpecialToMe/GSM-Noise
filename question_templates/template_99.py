from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[3]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define names and items
        names = ["Henry", "Alice", "Bob", "Carmen", "Diana", "Mark", "Nancy", "Oliver", "Penny", "Quincy"]
        items = ["cookies", "cakes", "muffins", "cupcakes", "pies", "brownies", "bread loaves", "pastries"]
    
        # Randomly select a name and an item
        name = random.choice(names)
        item = random.choice(items)
    
        # Randomly generate variables
        last_year_baked = random.randint(20, 100)  # Last year's baked amount (unknown to the solver)
        extra_ratio = random.randint(1, 4)         # Desired multiple compared to last year
        over_baked = random.randint(5, 20)         # Extra baked over intended amount
        items_dropped = random.randint(1, 10)      # Number of items dropped
        total_items = (last_year_baked * extra_ratio + over_baked) - items_dropped  # Total items after dropping
    
        # Construct the premise content, breaking it down into sentence level
        problem = [
            f"{name} is making {item} for a local baking competition.",
            f"{name} wants to make {extra_ratio} times as many as {name} did last year.",
            f"When {name} finishes baking, {name} realizes {name} actually baked {over_baked} more {item} than {name} meant to.",
            f"{name} drops {items_dropped} of {name}'s {item} as {name} is putting them out to cool, and now has a total of {total_items} {item}.",
        ]
    
        # Construct the question
        question = f"How many {item} did {name} bake last year?"
        original_problem=problem.copy()
        original_problem.append(question)
    
        # Add in-topic irrelevant information
        irrelevant_infos = [
            f"{name}'s neighbor gave {name} a recipe that can bake {random.randint(10, 50)} {item} per batch.",
            f"{name} plans to share the {item} with {random.randint(5, 15)} friends after the competition.",
        ]
    
        # Add out-topic irrelevant information
        irrelevant_infos.append(
            f"{name} recently started learning {random.choice(['piano', 'painting', 'gardening'])} in {random.randint(2010, 2023)}."
        )
    
        # Add irrelevant information based on probability
        for irrelevant_info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(irrelevant_info)
    
        # Add symbol or grammar errors. Assume that the functions are given
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(sentence, prob_grammar_error),
                prob_symbol_error
            ) for sentence in problem
        ]
    
        # Shuffle the order of sentences, except for the first one
        first_sentence = problem[0]
        rest_sentences = problem[1:]
        if shuffle:
            random.shuffle(rest_sentences)
        problem = [first_sentence] + rest_sentences
    
        # Add the question
        problem.append(question)
    
        # Calculate the answer
        answer = (total_items + items_dropped - over_baked) / extra_ratio
        if answer>0 and answer%1==0:
            break

    # Return the problem and the answer
    cot = [f"{name} wants to make {extra_ratio} times as many {item} as last year, so he plans to bake {last_year_baked} * {extra_ratio}.", f"However, he actually baked {over_baked} more {item} than intended, so the total becomes {last_year_baked} * {extra_ratio} + {over_baked}.", f"After dropping {items_dropped} {item}, the total is {total_items}.", f"To find out how many {item} {name} baked last year, we solve ({total_items} + {items_dropped} - {over_baked}) / {extra_ratio}, which gives us {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

