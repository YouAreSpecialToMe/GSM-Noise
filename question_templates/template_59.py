from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[6]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define name and item lists
    names = ["Alice", "Beth", "Cindy", "Diana", "Clara", "Sheila", "Bob", "Tom", "Jack", "Emily", "Sarah", "Michael"]
    items = ['pomegranates', 'apples', 'oranges', 'bananas', 'grapes']
    
    # Randomly select names and items
    name1 = random.choice(names)
    names.remove(name1)
    name2 = random.choice(names)
    item = random.choice(items)
    
    # Randomly generate purchase-related values
    day1 = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    day2 = random.choice(["the next day", "the following day", "a day later"])  # Ensure day2 is after day1 in narrative
    quantity = random.randint(10, 100)  # Quantity of items bought
    price1 = random.randint(1, 20) * 5  # Price per item on day1, multiples of $5 between $5 and $100
    price2 = price1 + random.randint(1, 4) * 10  # Price per item on day2, $10 to $40 more than day1 price
    
    voucher_amount = random.randint(1, 10) * 2  # Voucher amount between $2 and $20
    discount_percentage = random.choice([5, 10, 15, 20])  # Discount percentages available
    
    # Additional variables for irrelevant information
    irrelevant_item_cost = random.randint(100, 1000)
    irrelevant_year = random.randint(2000, 2022)
    irrelevant_savings = random.randint(1000, 5000)
    
    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"On {day1}, {name1} bought {quantity} {item} at ${price1} each.",
        f"At the till {name1} got ${voucher_amount} off because {name1} had a voucher.",
        f"{day2.capitalize()}, the price shot to ${price2} per {item[:-1]}, but the store also offered a {discount_percentage}% discount on the total cost.",
        f"{name2} took advantage of the discount and bought {quantity} {item}.",
    ]
    
    # Construct the question
    question = f"What is the difference between the final prices paid for the {item} on the two days?"
    original_problem=problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The {item} were imported from overseas at a cost of ${irrelevant_item_cost} to the store.",
        f"The store had been open since {irrelevant_year}.",
    ]
    
    # Add out-topic irrelevant information
    all_genders = ['boy', 'girl']
    gender = random.choice(all_genders)
    out_topic_irrelevant_info = f"{name1} is a {gender} who has more than ${irrelevant_savings} saved up."
    irrelevant_infos.append(out_topic_irrelevant_info)
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors. Assume that the functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    remaining_sentences = problem[1:]
    if shuffle:
        random.shuffle(remaining_sentences)
    problem = [first_sentence] + remaining_sentences
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    # First person's total payment
    total_cost1 = quantity * price1
    final_price1 = total_cost1 - voucher_amount
    # Second person's total payment
    total_cost2 = quantity * price2
    discount_amount = total_cost2 * discount_percentage / 100
    final_price2 = total_cost2 - discount_amount
    # Difference between the final prices
    answer = abs(final_price2 - final_price1)
    
    # Return premise and answer as a dictionary
    cot = [f"On {day1}, {name1} bought {quantity} {item} at ${price1} each, making the total cost {quantity} * {price1}, which is {total_cost1}.", f"At the till, {name1} got ${voucher_amount} off, so the final price paid was {total_cost1} - {voucher_amount}, which is {final_price1}.", f"On {day2}, the price per {item[:-1]} was ${price2}. {name2} bought {quantity} {item}, making the total cost {quantity} * {price2}, which is {total_cost2}.", f"The store offered a {discount_percentage}% discount, so the discount amount was {total_cost2} * {discount_percentage} / 100, which is {discount_amount}.", f"The final price paid by {name2} was {total_cost2} - {discount_amount}, which is {final_price2}.", f"The difference between the final prices paid on the two days is |{final_price2} - {final_price1}|, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

