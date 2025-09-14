from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[3]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define possible names and hobbies
    names = ['John', 'Alice', 'Bob', 'Sara', 'Michael', 'Linda', 'David', 'Mary', 'James', 'Patricia']
    hobbies = ['painting', 'golf', 'reading', 'hiking', 'cooking', 'gaming', 'cycling', 'swimming']

    # Randomly select a name and hobby
    name = random.choice(names)
    hobby = random.choice(hobbies)

    # Randomly generate values related to the problem
    distance = random.randint(5, 50)  # Distance to work in miles
    days_per_week = random.randint(3, 7)  # Days worked per week
    weeks_per_year = random.randint(45, 52)  # Weeks worked per year
    charge_per_mile = round(random.uniform(1.0, 5.0), 2)  # Charge per mile in dollars
    bonus_per_month = random.randint(50, 500)  # Bonus per month in dollars

    # Additional variables for irrelevant information
    extra_distance = random.randint(10, 100)  # Extra miles driven per week
    extra_fee = round(random.uniform(100.0, 1000.0), 2)  # Additional fee in dollars
    borrow_time = random.randint(2, 3)  # Fuel cost per month in dollars
    car_cost = random.randint(10000, 50000)  # Car cost in dollars
    age = random.randint(20, 70)  # Age of the person
    pet_name = random.choice(['Buddy', 'Max', 'Bella', 'Lucy', 'Charlie', 'Luna'])

    # Construct the premises
    problem = [
        f"{name} hires a driving service to get {name} to work each day.",
        f"{name}'s work is {distance} miles away and {name} has to go there and back each day.",
        f"{name} goes to work {days_per_week} days a week for {weeks_per_year} weeks a year.",
        f"{name} gets charged ${charge_per_mile} per mile driven and {name} also gives {name}'s driver a ${bonus_per_month} bonus per month."
    ]

    # Construct the question
    question = f"How much does {name} pay a year for driving to work?"
    original_problem=problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    in_topic_irrelevant_info = [
        f"On weekend, {name} occasionally travels an extra {extra_distance} miles each week for vacation.",
        f"{name}'s friend borrow {name}'s car {borrow_time} times per month.",
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant_info = [
        f"{name} is {age} years old and enjoys {hobby} in {name}'s free time.",
        f"{name} has a pet named {pet_name}.",
        f"{name} plans to take a vacation next summer."
    ]

    # Add irrelevant information based on probability
    irrelevant_infos = in_topic_irrelevant_info + out_topic_irrelevant_info
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the question
    if shuffle:
        random.shuffle(problem)
    problem.append(question)

    # Calculate the answer
    miles_per_day = distance * 2  # Round trip miles per day
    miles_per_week = miles_per_day * days_per_week
    total_miles = miles_per_week * weeks_per_year
    total_mile_charge = total_miles * charge_per_mile
    total_bonus = bonus_per_month * 12  # Months in a year
    answer = round(total_mile_charge + total_bonus,2)


    # Return the problem and the answer
    cot = [f"{name} travels to work and back each day, so the total miles per day is {distance} * 2, which is {miles_per_day}.", f"The total miles per week is {miles_per_day} * {days_per_week}, which is {miles_per_week}.", f"The total miles per year is {miles_per_week} * {weeks_per_year}, which is {total_miles}.", f"The total charge for miles driven is {total_miles} * {charge_per_mile}, which is {total_mile_charge}.", f"The total bonus for the year is {bonus_per_month} * 12, which is {total_bonus}.", f"Therefore, the total amount {name} pays a year is {total_mile_charge} + {total_bonus}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

