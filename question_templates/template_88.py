from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[5]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define possible names and pets
    names = ["Madeline", "Isabella", "Olivia", "Sophia", "Emma", "Liam", "Noah", "James", "William", "Ethan"]
    pets = ["dog", "cat", "rabbit", "hamster", "parrot", "turtle", "goldfish", "lizard", "ferret", "guinea pig"]

    # Randomly select a name and a pet
    name = random.choice(names)
    pet = random.choice(pets)

    # Define pronouns based on name
    gender_pronoun_map = {
        "Madeline": "she",
        "Isabella": "she",
        "Olivia": "she",
        "Sophia": "she",
        "Emma": "she",
        "Liam": "he",
        "Noah": "he",
        "James": "he",
        "William": "he",
        "Ethan": "he"
    }

    possessive_pronoun_map = {
        "Madeline": "her",
        "Isabella": "her",
        "Olivia": "her",
        "Sophia": "her",
        "Emma": "her",
        "Liam": "his",
        "Noah": "his",
        "James": "his",
        "William": "his",
        "Ethan": "his"
    }

    pronoun = gender_pronoun_map[name]
    possessive_pronoun = possessive_pronoun_map[name]

    # Randomly generate costs and other variables
    food_cost_per_week = random.randint(15, 35)
    treats_cost_per_month = random.randint(10, 30)
    medicine_cost_per_month = random.randint(80, 120)
    weeks_per_month = random.randint(4, 5)
    months_per_year = 12  # usually constant

    # Irrelevant information variables
    owner_age = random.randint(20, 60)
    pet_age = random.randint(1, 15)
    ir_money = random.randint(1000, 5000)
    random_amount = random.randint(50, 300)  # For in-topic irrelevant money amount

    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"Every month, {name} has to buy food, treats, and medicine for {possessive_pronoun} {pet}.",
        f"Food costs ${food_cost_per_week} per week.",
        f"Treats cost ${treats_cost_per_month} per month.",
        f"Medicine costs ${medicine_cost_per_month} per month."
    ]

    # Construct the question
    question = f"How much money does {name} spend on {possessive_pronoun} {pet} per year if there are {weeks_per_month} weeks in a month?"
    original_problem=problem.copy()
    original_problem.append(question)
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name}'s {pet} is {pet_age} years old.",
        f"{name}'s friend spends ${random_amount} per year on pet toys for {name}'s friend's pet."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos_out_topic = [
        f"{name} is {owner_age} years old.",
        f"{name} has saved up ${ir_money} in total."
    ]

    # Combine irrelevant information
    irrelevant_infos.extend(irrelevant_infos_out_topic)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Apply symbol or grammar errors (Assumed to be external functions)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    if len(problem) > 1:
        first_sentence = problem[0]
        other_sentences = problem[1:]
        if shuffle:
            random.shuffle(other_sentences)
        problem = [first_sentence] + other_sentences

    # Add the question at the end
    problem.append(question)

    # Calculate the answer
    total_monthly_cost = (food_cost_per_week * weeks_per_month) + treats_cost_per_month + medicine_cost_per_month
    answer = total_monthly_cost * months_per_year

    # Return problem and answer as a dictionary
    cot = [f"Calculate the total monthly cost by adding the cost of food, treats, and medicine. The food cost is {food_cost_per_week} per week, and there are {weeks_per_month} weeks in a month, so the total food cost is {food_cost_per_week} * {weeks_per_month}.", f"Add the treats cost of {treats_cost_per_month} and the medicine cost of {medicine_cost_per_month} to the total food cost to get the total monthly cost, which is {total_monthly_cost}.", f"Multiply the total monthly cost by the number of months in a year, {months_per_year}, to find the total annual cost, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

