from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[5]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define name and item lists
    names = ["Alice", "Bob", "Cindy", "Derek", "Elena", "Frank", "Grace", "Henry", "Irene", "John"]
    pets = ["dog", "cat", "parrot", "hamster"]
    pet_names = ["Buddy", "Mittens", "Polly", "Hammy"]
    investments = ["stocks", "bonds", "real estate", "mutual funds"]
    hobbies = ["painting", "cycling", "hiking", "photography"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly generate house value and percentages
    house_value = random.randint(200000, 500000)  # House value between $200,000 and $500,000
    loan_percentage = random.randint(20, 80)  # Loan between 20% and 80% of house value
    debt_percentage = random.randint(20, 80)  # Uses between 20% and 80% of loan to pay debts
    
    # Additional variables for irrelevant information
    fee = random.randint(500, 5000)  # Bank fee
    pet = random.choice(pets)
    pet_name = random.choice(pet_names)
    investment = random.choice(investments)
    age = random.randint(25, 65)
    hobby = random.choice(hobbies)
    salary = random.randint(50000, 150000)
    
    # Construct the premise content, breaking it down into sentences
    problem = [
        f"{name} decides to get a loan by mortgaging {name}'s home.",
        f"{name}'s house is worth ${house_value}.",
        f"{name} gets a loan worth {loan_percentage}% of that.",
        f"{name} uses {debt_percentage}% of that to pay off {name}'s debts."
    ]
    
    # Construct the question
    question = f"How much money did {name} have leftover after paying debt?"
    original_problem=problem.copy()
    original_problem.append(question)
    
    # In-topic irrelevant information
    irrelevant_infos = [
        f"{name} plans to invest some of the money in {investment}.",
        f"{name} enjoys {hobby} during free time."
    ]
    
    # Out-topic irrelevant information
    irrelevant_infos.extend([
        f"{name} has a pet {pet} named {pet_name}.",
        f"{name} is {age} years old and earns ${salary} per year."
    ])
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors (assumed given functions)
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
    
    # Calculate the answer
    loan_amount = house_value * loan_percentage / 100
    amount_used_to_pay_debts = loan_amount * debt_percentage / 100
    answer = loan_amount - amount_used_to_pay_debts
    answer=round(answer,2)
    
    # Return problem and answer
    cot = [f"{name} gets a loan worth {loan_percentage}% of the house value, which is {house_value}. Therefore, the loan amount is {house_value} * {loan_percentage} / 100, which is {loan_amount}.", f"{name} uses {debt_percentage}% of the loan amount to pay off debts. Therefore, the amount used to pay debts is {loan_amount} * {debt_percentage} / 100, which is {amount_used_to_pay_debts}.", f"The leftover money after paying the debt is the loan amount minus the amount used to pay debts, which is {loan_amount} - {amount_used_to_pay_debts}, resulting in {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

