from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[31]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define name and item lists
    names = ["Alex", "Bella", "Charlie", "Diana", "Ethan", "Fiona"]
    items1 = ["tattered jeans", "skinny jeans", "ripped jeans", "faded jeans"]
    items2 = ["jogger jeans", "bootcut jeans", "straight jeans", "flared jeans"]
    events = ["dance contest", "fashion show", "music festival", "photo shoot"]
    
    # Randomly select a name and event
    name = random.choice(names)
    event = random.choice(events)
    
    # Randomly select two different jeans
    item1 = random.choice(items1)
    item2 = random.choice(items2)
    
    # Randomly generate values
    tattered_price = random.randint(20, 50)  # Price of item1
    price_diff = random.randint(5, 15)       # Price difference
    total_savings = random.randint(6, 12)    # Total savings
    fraction_savings_item2 = random.choice([1/3, 2/5, 1/2])  # Fraction saved from item2
    fraction_savings_item1 = 1 - fraction_savings_item2  # Fraction saved from item1
    
    # Determine whether item2 costs less or more than item1
    less_more = random.choice(['less', 'more'])
    
    # Compute sale prices
    if less_more == 'less':
        item2_price = tattered_price - price_diff
    else:
        item2_price = tattered_price + price_diff
    
    # Calculate savings from each item
    savings_item2 = total_savings * fraction_savings_item2
    savings_item1 = total_savings - savings_item2
    
    # Original prices
    original_price_item1 = tattered_price + savings_item1
    original_price_item2 = item2_price + savings_item2
    
    # Provide the math formula to calculate the answer
    # answer = original_price_item2 - original_price_item1
    answer = abs(original_price_item2 - original_price_item1)
    answer=round(answer,2)
    

    # Construct the problem premises
    problem = [
        f"{name} wanted to buy new jeans for a {event}.",
        f"At the store, {name} couldn't decide between {item1} and {item2}.",
        f"Since the jeans were on sale, {name} decided to buy them both.",
        f"The {item1} cost ${tattered_price} while the {item2} cost ${price_diff} {less_more} than the {item1}.",
        f"{name} saved a total of ${total_savings:.2f}.",
        f"{name} saved {int(fraction_savings_item2*100)}% of the total savings from the {item2} and the rest from the {item1}."
    ]
    question=[ f"how much more or less do the {item2} originally cost than the {item1}?"]
    original_problem=problem.copy()
    original_problem.append(question)
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The store was having a sale on {random.choice(['jackets', 'shirts', 'hats'])}.",
        f"{name} also considered buying a {random.choice(['belt', 'scarf', 'pair of socks'])}."
    ]
    
    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} enjoys {random.choice(['playing basketball', 'painting', 'reading books'])} during free time.")
    
    # Randomly add irrelevant information based on prob_irre
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.insert(random.randint(1, len(problem)-1), irrelevant_info)
    
    # Add symbol or grammar errors (Assuming functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle sentences except the first one
    first_sentence = problem[0]
    rest_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_sentences)
    problem = [first_sentence] + rest_sentences+question
    
    # Return the problem and the answer
    cot = [f"Determine the price of {item2}. If {item2} costs {less_more} than {item1}, then {item2_price} is calculated as {tattered_price} - {price_diff} if less, or {tattered_price} + {price_diff} if more.", f"Calculate the savings from {item2} as {total_savings} * {fraction_savings_item2}, which is {savings_item2}.", f"Calculate the savings from {item1} as {total_savings} - {savings_item2}, which is {savings_item1}.", f"Determine the original price of {item1} as {tattered_price} + {savings_item1}, which is {original_price_item1}.", f"Determine the original price of {item2} as {item2_price} + {savings_item2}, which is {original_price_item2}.", f"Calculate the final answer as the absolute difference between {original_price_item2} and {original_price_item1}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

