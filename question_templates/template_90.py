from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
   

    # Define possible alternative names and items
    names = ["Leila", "Jack", "Chase", "Mia", "Noah", "Emma", "Oliver", "Ava", "Liam", "Sophia"]
    items = ["cucumbers", "tomatoes", "lettuce", "carrots", "peppers", "spinach", "onions", "avocados", "celery", "radishes"]
    quantities = list(range(1, 11))
    prices = list(range(1, 6))

    # Randomly select names, ensuring uniqueness
    person1 = random.choice(names)
    remaining_names = [n for n in names if n != person1]
    person2 = random.choice(remaining_names)
    remaining_names.remove(person2)
    person3 = random.choice(remaining_names)

    # Randomly select items, ensuring uniqueness
    item_list = items.copy()
    item1_random = random.choice(item_list)
    item_list.remove(item1_random)
    item2_random = random.choice(item_list)
    item_list.remove(item2_random)
    item3_random = random.choice(item_list)

    # Randomly assign quantities and prices
    quantity1_random = random.choice(quantities)
    quantity2_random = random.choice(quantities)
    quantity3_random = random.choice(quantities)

    price1_random = random.choice(prices)
    price2_random = random.choice(prices)
    price3_random = random.choice(prices)

    # Construct the premise content
    problem = [
        f"{person1} buys {quantity1_random} {item1_random} from the market.",
        f"{item1_random.capitalize()} cost ${price1_random} each.",
        f"{person2} buys {quantity2_random} {item2_random} from the grocery store.",
        f"{item2_random.capitalize()} cost ${price2_random} each.",
        f"{person3} buys {quantity3_random} {item3_random} from the farmer's market.",
        f"{item3_random.capitalize()} cost ${price3_random} each."
    ]

    # Construct the question
    question = "Together, how much did the three of them spend to make a salad for the potluck?"
    original_problem=problem.copy()
    original_problem.append(question)

    # Add in-topic and out-topic irrelevant information
    irrelevant_infos = [
        f"{person1} is excited about making a new recipe.",
        f"The grocery store had a discount on {item2_random} today.",
        f"{person3} loves to cook with fresh ingredients.",
        f"{person2} is training for a marathon next month."
    ]

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (functions assumed to be given)
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

    # Calculate the answer using randomized variables
    answer = (quantity1_random * price1_random) + (quantity2_random * price2_random) + (quantity3_random * price3_random)
    # Return the problem and the answer
    cot = [f"{person1} buys {quantity1_random} {item1_random} at ${price1_random} each, costing a total of {quantity1_random} * {price1_random}.", f"{person2} buys {quantity2_random} {item2_random} at ${price2_random} each, costing a total of {quantity2_random} * {price2_random}.", f"{person3} buys {quantity3_random} {item3_random} at ${price3_random} each, costing a total of {quantity3_random} * {price3_random}.", f"Together, they spend a total of ({quantity1_random} * {price1_random}) + ({quantity2_random} * {price2_random}) + ({quantity3_random} * {price3_random}), which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

