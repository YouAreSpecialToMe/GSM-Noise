from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[18]:


import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    while True:
        # Define a list of possible names
        names = ["Mr. Smith", "Mrs. Johnson", "Dr. Lee", "Ms. Garcia", "Professor Jones", "Mr. Tan", "Lady Williams",
                 "Captain Rogers"]

        # Randomly select a name
        name = random.choice(names)

        # Randomly generate selling_price between $300,000 and $1,000,000
        selling_price = random.randint(6, 20) * 50000  # $300,000 to $1,000,000

        # Randomly select transfer_fee_percent between 1% and 5%
        transfer_fee_percent = random.randint(1, 5)

        # Randomly select brokerage_fee_percent between 2% and 6%
        brokerage_fee_percent = random.randint(2, 6)

        # Randomly generate loan_amount between $100,000 and $500,000
        loan_amount = random.randint(2, 10) * 50000  # $100,000 to $500,000

        # Additional variables for irrelevant information
        property_tax = random.randint(1, 3)  # between 1% and 3%
        maintenance_cost = random.randint(10000, 50000)  # $10,000 to $50,000
        age = random.randint(30, 65)
        hobby = random.choice(["painting", "gardening", "swimming", "cycling", "writing"])
        inheritance = random.randint(50000, 200000)

        # Construct the premise content, breaking it down into sentence level
        problem = [
            f"{name} sold {name}'s house for ${selling_price}.",
            f"{name} paid the transfer fees that amount to {transfer_fee_percent}% of the selling price and also paid a brokerage fee that is {brokerage_fee_percent}% of the selling price.",
            f"{name} also paid ${loan_amount} for the remaining loan amount of the house."
        ]
        question = f"how much is {name}'s net proceeds from selling the house?"
        original_problem = problem.copy()
        original_problem.append(question)

        # Add in-topic irrelevant information
        irrelevant_infos = [
            f"The maintenance costs for the house last year were ${maintenance_cost}.",
            f"{name} is planning to buy a new house soon."
        ]

        # Add out-topic irrelevant information
        irrelevant_infos.append(f"{name} is {age} years old and enjoys {hobby} in {name}'s free time.")
        irrelevant_infos.append(f"{name} recently inherited ${inheritance} from a distant relative.")

        # Add irrelevant information based on probability
        for irrelevant_info in irrelevant_infos:
            if random.random() < prob_irre:
                insert_index = random.randint(1, len(problem))
                problem.insert(insert_index, irrelevant_info)

        # Replace placeholders with actual values and resolve pronouns
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(sentence, prob_grammar_error),
                prob_symbol_error
            )
            for sentence in problem
        ]
        main_problem = problem[:1]
        other_statements = problem[1:]
        if shuffle:
            random.shuffle(other_statements)
        problem = main_problem + other_statements
        problem.append(question)

        # Calculate the answer
        transfer_fee = transfer_fee_percent / 100 * selling_price
        brokerage_fee = brokerage_fee_percent / 100 * selling_price
        answer = selling_price - (transfer_fee + brokerage_fee + loan_amount)
        if answer > 0:
            break

    # Return problem and answer as a dictionary
    cot = [
        f"Calculate the transfer fee by multiplying {transfer_fee_percent}% with {selling_price}, resulting in {transfer_fee}.",
        f"Calculate the brokerage fee by multiplying {brokerage_fee_percent}% with {selling_price}, resulting in {brokerage_fee}.",
        f"Subtract the sum of {transfer_fee}, {brokerage_fee}, and {loan_amount} from {selling_price} to get the net proceeds, which is {answer}."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
