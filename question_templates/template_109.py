from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[29]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define lists of possible names and items
        male_names = ['Aaron', 'Bob', 'Charlie', 'David', 'Ethan', 'Fred']
        female_names = ['Alice', 'Barbara', 'Carol', 'Diana', 'Emma', 'Barbie']
        friend_names = ['George', 'Henry', 'Ian', 'Jack', 'Kyle', 'Ronnie']
        children_types = ['children', 'kids', 'sons', 'daughters']
        items = ['root beer', 'lemonade', 'iced tea', 'punch', 'soup']
    
        # Randomly select names and item
        main_name = random.choice(male_names)
        wife_name = random.choice(female_names)
        friend_name = random.choice(friend_names)
        children = random.choice(children_types)
        item = random.choice(items)
        pet_name = random.choice(['Buddy', 'Max', 'Bella', 'Lucy', 'Charlie'])
    
        # Randomly generate numeric variables
        n_days = random.randint(2, 5)  # Time until party
        initial_amount = random.randint(20, 50)  # Initial gallons made
        children_amount = random.randint(1, 10)  # Amount children drank
        wife_amount = random.randint(1, 10)  # Amount wife spilled
        friend_amount = random.randint(1, 10)  # Amount friend consumed
        party_people = random.randint(2, 10)  # People who showed up for the party
        ingredients_cost = random.randint(10, 100)  # Irrelevant info
        cooler_cost = random.randint(50, 500)  # Irrelevant info
        pet_age = random.randint(1, 15)  # Irrelevant info
    
        # Construct the problem sentences using variables
        problem = [
            f"{main_name} was preparing for a party to be held in {n_days} days.",
            f"So, {main_name} made {initial_amount} gallons of {item} on the first day and put them in the refrigerator cooler.",
            f"But later that evening, {main_name}'s {children} discovered the delicious nectar and robbed the cooler, drinking {children_amount} of those gallons of {item}.",
            f"On the second day, {main_name}'s wife {wife_name} also discovered the {item} and accidentally spilled {wife_amount} gallons.",
            f"On the third day, {main_name}'s friend {friend_name} visited {main_name}'s house and helped himself to the {item}, further reducing the amount remaining by {friend_amount} gallons.",
            f"On the fourth day, {party_people} people showed up for the party.",
            
        ]
        question=f"If {main_name} and the others shared the remaining {item} equally, how much was available for each to drink during the party?"
        original_problem=problem.copy()
        original_problem.append(question)
        # Construct irrelevant information
        irrelevant_infos = [
            f"{main_name} spent ${ingredients_cost} on ingredients for the {item}.",
            f"The refrigerator cooler was new and cost ${cooler_cost}.",
            f"{main_name} has a pet dog named {pet_name} who is {pet_age} years old."
        ]
    
        # Randomly add irrelevant information
        for irrelevant_info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.insert(random.randint(1, len(problem)-1), irrelevant_info)
    
        # Add symbol or grammar errors. Assume that these functions are given.
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(sentence, prob_grammar_error),
                prob_symbol_error
            ) for sentence in problem
        ]
    
        # Shuffle the problem sentences except the first one
        first_sentence = problem[0]
        rest_sentences = problem[1:]
        if shuffle:
            random.shuffle(rest_sentences)
        problem = [first_sentence] + rest_sentences+[question]
    
        # Calculate the answer
        remaining_amount = initial_amount - children_amount - wife_amount - friend_amount
        total_people = party_people + 1  # Including main_name
        answer =round( remaining_amount / total_people,2)
        if answer>0:
            break
    

    # Return the problem and answer
    cot = [f"Calculate the remaining amount of {item} by subtracting the amounts consumed or spilled: {initial_amount} - {children_amount} - {wife_amount} - {friend_amount} = {remaining_amount}.", f"Include {main_name} in the total number of people sharing the {item}, so the total number of people is {party_people} + 1 = {total_people}.", f"Divide the remaining amount of {item} by the total number of people to find out how much each person can drink: {remaining_amount} / {total_people} = {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

