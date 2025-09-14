from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[3]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define name and item lists
        store_names = ["Foot Locker", "Shoe Palace", "Sneaker City", "Sole Mates", "Happy Feet"]
        item_names = ["tennis shoes", "running shoes", "sandals", "boots", "flip-flops", "dress shoes"]
    
        # Randomly select a store name and an item
        store_name = random.choice(store_names)
        item_name = random.choice(item_names)
    
        # Randomly generate sales-related values
        initial_sales = random.randint(10, 50)  # Pairs sold on the first day
        sales_multiplier_day2 = random.choice([2, 3])  # Times the sales increase on the next day
        sales_multiplier_day3 = random.choice([0.5, 0.75])  # Fraction of prior day's sales on the last day
        returns = random.randint(1, 10)  # Pairs returned because they didn't fit
    
        # Additional random data for irrelevant information
        store_age = random.randint(1, 50)  # Age of the store
        employee_count = random.randint(5, 30)  # Number of employees
        competitor_sales = random.randint(50, 200)  # Sales by a competing store
        discount_rate = random.randint(10, 50)  # Discount rate offered during the sale
    
        # Construct the premise content
        problem = [
            f"A shoe store named {store_name} was having a weekend sale on a brand of popular {item_name}.",
            f"On Friday the store sold {initial_sales} pairs of {item_name}.",
            f"The next day they sold {sales_multiplier_day2} times that number of shoes.",
            f"On the last day of the sale they sold {sales_multiplier_day3} times the amount that they did the day before, but {returns} people returned their pairs because they didn't fit."
        ]
    
        # Construct the question
        question = f"How many {item_name} were sold by the end of the sale?"
        original_problem=problem.copy()
        original_problem.append(question)
    
        # Add in-topic irrelevant information
        irrelevant_infos = [
            f"The store has been open for {store_age} years.",
            f"There are {employee_count} employees working at {store_name}.",
            f"A competing store sold {competitor_sales} pairs of shoes during the same weekend.",
            f"The store offered a {discount_rate}% discount on all {item_name} during the sale."
        ]
    
        # Add out-topic irrelevant information
        owner_name = random.choice(["Alex", "Jordan", "Taylor", "Casey", "Morgan"])
        owner_age = random.randint(25, 60)
        out_topic_irrelevant_info = f"The store owner, {owner_name}, is {owner_age} years old."
        irrelevant_infos.append(out_topic_irrelevant_info)
    
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
    
        # Shuffle the order of sentences, except for the first one
        if shuffle:
            random.shuffle(problem[1:])
    
        # Add the question
        problem.append(question)
    
        # Calculate the answer
        day1_sales = initial_sales
        day2_sales = initial_sales * sales_multiplier_day2
        day3_sales = day2_sales * sales_multiplier_day3
        total_sales = day1_sales + day2_sales + day3_sales - returns
        answer = total_sales
        if answer%1==0:
            break

    # Return problem and answer as a dictionary
    cot = [f"On the first day, the store sold {initial_sales} pairs of {item_name}, so {day1_sales} pairs were sold.", f"On the second day, the store sold {sales_multiplier_day2} times the number of shoes sold on the first day, which is {initial_sales} * {sales_multiplier_day2}, resulting in {day2_sales} pairs sold.", f"On the last day, the store sold {sales_multiplier_day3} times the amount sold the day before, which is {day2_sales} * {sales_multiplier_day3}, resulting in {day3_sales} pairs sold.", f"Six people returned their pairs, so the total sales are {day1_sales} + {day2_sales} + {day3_sales} - {returns}, which equals {total_sales}.", f"Therefore, the total number of {item_name} sold by the end of the sale is {total_sales}, which is the final answer."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

