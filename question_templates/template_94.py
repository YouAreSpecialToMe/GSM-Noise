from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[7]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        names = ['Thomas', 'Michael', 'David', 'Sarah', 'Jessica', 'Emily', 'Daniel', 'Emma']
        bill_values = [10, 20, 50, 100]
        total_withdraws = [500, 600, 700, 800, 900, 1000]
        multipliers = [2, 3, 4]
        final_bill_values = [1, 5, 10]
        
        name = random.choice(names)
        bill_value = random.choice(bill_values)
        total_withdraw = random.choice(total_withdraws)
        lost_bills = random.randint(5, 15)
        multiplier = random.choice(multipliers)
        final_bill_value = random.choice(final_bill_values)
        
        account_balance = random.randint(1000, 5000)
        bank_names = ['First National Bank', 'Central Credit Union', 'Community Savings Bank']
        bank_name = random.choice(bank_names)
        friend_name = random.choice([n for n in names if n != name])
        car_models = ['sedan', 'convertible', 'SUV', 'truck']
        car_model = random.choice(car_models)
        
        problem = [
            f"{name} withdraws ${total_withdraw} in ${bill_value} bills from the bank.",
            f"{name} loses {lost_bills} bills while getting home.",
            f"After that, {name} uses half of the remaining bills to pay for a bill.",
            f"{name} then multiplies his money by {multiplier}.",
            f"He then converts all his money into ${final_bill_value} bills."
        ]
        
        question = f"How many ${final_bill_value} bills does {name} have?"
        original_problem=problem.copy()
        original_problem.append(question)
        
        irrelevant_infos = [
            f"Before withdrawing, {name} had ${account_balance} in his bank account.",
            f"The bank {name} used was {bank_name}.",
            f"{name}'s friend {friend_name} also withdrew some money."
        ]
        
        out_irrelevant_info = f"On the way home, {name} thought about buying a new {car_model} next year."
        irrelevant_infos.append(out_irrelevant_info)
        
        for irrelevant_info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(irrelevant_info)
        
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error), 
                prob_symbol_error
            ) for p in problem
        ]
        
        if shuffle:
            random.shuffle(problem[1:])
    
        # Add the question to the problem
        problem.append(question)
        
        total_bills = total_withdraw // bill_value
        remaining_bills = total_bills - lost_bills
        used_bills = remaining_bills // 2
        remaining_bills -= used_bills
        current_money = remaining_bills * bill_value
        current_money *= multiplier
        num_final_bills = current_money // final_bill_value
        
        answer = num_final_bills
        if answer>0:
            break
    cot = [f"{name} withdraws {total_withdraw} in {bill_value} bills, resulting in {total_bills} total bills.", f"After losing {lost_bills} bills, {name} has {remaining_bills} bills left.", f"{name} uses half of the remaining bills, which is {used_bills}, to pay for a bill.", f"This leaves {name} with {remaining_bills} bills.", f"{name} then multiplies his money by {multiplier}, resulting in {current_money}.", f"Finally, {name} converts all his money into {final_bill_value} bills, resulting in {num_final_bills} bills."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

