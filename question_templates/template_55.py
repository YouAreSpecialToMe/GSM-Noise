from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define names
    names = ['Alex', 'Jordan', 'Taylor', 'Chris', 'Pat', 'Morgan', 'Jamie', 'Casey', 'Riley', 'Buford']
    
    # Randomly select a name
    name = random.choice(names)
    
    # Define bills and services
    monthly_bills = ['electric bill', 'gas bill', 'water bill', 'internet bill', 'phone bill', 'rent']
    biweekly_payments = ['donation to the church', 'gym membership', 'piano lessons', 'karate class', 'dance class']
    quarterly_payments = ['pest and lawn service', 'quarterly taxes', 'HVAC maintenance', 'insurance premium', 'subscription box']
    
    # Randomly select bills and services
    bill1 = random.choice(monthly_bills)
    monthly_bills.remove(bill1)  # Remove to avoid duplication
    bill2 = random.choice(monthly_bills)
    
    biweekly_service = random.choice(biweekly_payments)
    quarterly_service = random.choice(quarterly_payments)
    
    # Random frequencies
    bill1_checks_per_month = random.randint(1, 2)  # 1 or 2 times per month
    bill2_checks_per_month = random.randint(1, 2)  # 1 or 2 times per month
    biweekly_checks_per_month = random.randint(1, 4)  # 1 to 4 times per month
    quarterly_checks_per_year = random.choice([2, 3, 4])  # 2 to 4 times per year
    
    # Construct the problem statements
    problem = [
        f"{name} writes many checks every year.",
        f"{frequency_phrase(bill1_checks_per_month)} per month {name} writes a check to pay the {bill1}.",
        f"{frequency_phrase(bill2_checks_per_month)} per month {name} writes a check for the {bill2}.",
        f"{frequency_phrase(biweekly_checks_per_month)} per month {name} writes a check to the {biweekly_service}.",
        f"And {quarterly_frequency_phrase(quarterly_checks_per_year)}, {name} writes a check to the {quarterly_service}."
    ]
    original_problem=problem.copy()
    
    # In-topic irrelevant information
    irrelevant_infos = [
        f"{name} also pays the cable bill online every month.",
        f"{name} donates to charity every year during the holidays.",
        f"{name}'s {biweekly_service} increased their fees recently.",
        f"{name} prefers writing checks over using credit cards."
    ]
    
    # Out-topic irrelevant information
    hobbies = ['painting', 'cycling', 'hiking', 'photography', 'cooking']
    hobby = random.choice(hobbies)
    irrelevant_infos.append(f"{name} enjoys {hobby} during the weekends.")
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors. Assume that these functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the problem sentences, except for the first one
    main_problem = problem[:1]
    other_statements = problem[1:]
    if shuffle:
        random.shuffle(other_statements)
    problem = main_problem + other_statements
    
    # Construct the question
    question = f"How many checks does {name} write per year?"
    
    original_problem.append(question)
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    answer = (bill1_checks_per_month + bill2_checks_per_month + biweekly_checks_per_month) * 12 + quarterly_checks_per_year
    
    # Return problem and answer as a dictionary
    cot = [
        f"Calculate the total number of checks written per month by adding {bill1_checks_per_month}, {bill2_checks_per_month}, and {biweekly_checks_per_month}.",
        f"Multiply the monthly total by 12 to get the annual total for monthly checks.",
        f"Add the {quarterly_checks_per_year} checks written quarterly to the annual total.",
        f"The total number of checks {name} writes per year is {answer}."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}

# Helper functions
def frequency_phrase(count):
    if count == 1:
        return 'Once'
    elif count == 2:
        return 'Twice'
    else:
        return f"{count} times"

def quarterly_frequency_phrase(count):
    if count == 4:
        return 'Quarterly'
    elif count == 3:
        return 'Three times per year'
    elif count == 2:
        return 'Twice a year'
    else:
        return f"{count} times per year"
