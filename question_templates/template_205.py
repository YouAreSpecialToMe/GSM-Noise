from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of male and female names
    male_names = ['Billy', 'John', 'Mike', 'Tom', 'David', 'Richard', 'Kevin', 'Mark', 'James', 'Robert']
    female_names = ['Sally', 'Emma', 'Sarah', 'Lucy', 'Anna', 'Jessica', 'Laura', 'Karen', 'Emily', 'Linda']
    
    # Randomly select names
    name_male = random.choice(male_names)
    name_female = random.choice(female_names)
    
    # Ensure the names are not the same
    while name_male == name_female:
        name_female = random.choice(female_names)
    
    # Randomly generate numeric variables
    starting_pay_rate = round(random.uniform(8, 15), 2)
    raise1_amount = round(random.uniform(0.25, 1), 2)
    raise2_amount = round(random.uniform(0.5, 2), 2)
    sally_extra = round(random.uniform(0.25, 2), 2)
    work_hours = random.randint(10, 40)
    
    # Calculate current pay rates
    current_pay_rate_billy = starting_pay_rate + raise1_amount + raise2_amount
    sally_starting_pay_rate = starting_pay_rate + sally_extra
    
    # Construct the premise content
    problem = [
        f"When {name_male} was first hired, {name_male} was paid at a rate of ${starting_pay_rate} per hour.",
        f"After 2 months, {name_male} was given a raise of ${raise1_amount} per hour.",
        f"On {name_male}'s first anniversary at work, {name_male} was given a raise of ${raise2_amount} per hour.",
        f"{name_female} just started working at a different business, and {name_female}'s starting salary is ${sally_extra} more per hour than {name_male}'s starting salary was.",
        f"Both {name_male} and {name_female} work {work_hours} hours."
    ]

    question = f"How much more money will {name_male} earn than {name_female}, in dollars?"
    original_problem = problem.copy()
    original_problem.append(question)

    
    # Construct irrelevant information
    irrelevant_infos = [
        f"{name_male} works at a company that has {random.randint(50, 500)} employees.",
        f"{name_female}'s company is located {random.randint(1, 50)} miles away from {name_male}'s company.",
        f"Both companies have been operating for over {random.randint(5, 50)} years.",
        f"{name_male} enjoys playing {random.choice(['football', 'chess', 'guitar', 'video games', 'basketball'])} on weekends.",
        f"{name_female} is planning a vacation to {random.choice(['Paris', 'New York', 'Tokyo', 'Sydney', 'Rome'])} next month."
    ]
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.insert(random.randint(1, len(problem)-1), irrelevant_info)
    
    # Apply symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem + [question]
    
    # Calculate the answer
    billy_earnings = current_pay_rate_billy * work_hours
    sally_earnings = sally_starting_pay_rate * work_hours
    answer = round(billy_earnings - sally_earnings, 2)
    
    # Return the problem and the answer
    cot = [f"{name_male}'s current pay rate is calculated by adding the starting pay rate of {starting_pay_rate} to the raises of {raise1_amount} and {raise2_amount}, resulting in {current_pay_rate_billy}.", f"{name_female}'s starting pay rate is {starting_pay_rate} plus an extra {sally_extra}, which equals {sally_starting_pay_rate}.", f"The total earnings for {name_male} are calculated by multiplying the current pay rate {current_pay_rate_billy} by the work hours {work_hours}, resulting in {billy_earnings}.", f"The total earnings for {name_female} are calculated by multiplying the starting pay rate {sally_starting_pay_rate} by the work hours {work_hours}, resulting in {sally_earnings}.", f"The difference in earnings between {name_male} and {name_female} is {billy_earnings} - {sally_earnings}, which equals {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
