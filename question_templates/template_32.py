from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[12]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define names and items
        names = ['Jim', 'Bob', 'Alex', 'Tom', 'John', 'Mike', 'Steve', 'Emma', 'Olivia', 'Sophia', 'Isabella', 'Mia', 'Charlotte']
        sister_names = ['Sarah', 'Emily', 'Anna', 'Lisa', 'Grace', 'Jessica']
        items = ['pack of gum', 'box of chocolates', 'bag of candies']
    
        # Randomly select a name, sister's name, and an item
        name = random.choice(names)
        sister_name = random.choice(sister_names)
        item = random.choice(items)
    
        # Randomly generate values
        initial_gum = random.randint(10, 30)  # Initial pack size
        chews_per_interval = random.randint(1, 2)  # Pieces chewed per interval
        chews_every = random.randint(1, 3)  # Every n hours
        school_day_length = random.choice([6, 7, 8, 9])  # School day length in hours
        chews_on_way_home = random.randint(0, 2)
        chews_after_dinner = random.randint(0, 2)
    
        # Irrelevant information variables
        money_in_bank = random.randint(1000, 5000)
        favorite_color = random.choice(['blue', 'green', 'red', 'yellow', 'purple'])
        purchase_day = random.randint(1, 28)
        purchase_month = random.randint(1, 12)
        pack_weight = random.uniform(100, 500)  # in grams
    
        # Construct the premise content
        problem = [
            f"{name} has a {initial_gum}-pack of gum.",
            f"He chews {chews_per_interval} piece{'s' if chews_per_interval > 1 else ''} of gum every {chews_every} hour{'s' if chews_every > 1 else ''} he's at school over a school day that lasts {school_day_length} hours.",
            f"He chews {chews_on_way_home} piece{'s' if chews_on_way_home != 1 else ''} on the way home from school and {chews_after_dinner} stick{'s' if chews_after_dinner != 1 else ''} after dinner.",
            f"He also gives half the gum he has remaining to his sister {sister_name} when she asks for some right before bed."
        ]
    
        # Construct the question
        question = f"How many pieces of gum does {name} have left at the end of the day?"
        original_problem=problem.copy()
        original_problem.append(question)
    
        # In-topic irrelevant information
        irrelevant_infos_in_topic = [
            f"The gum pack weighs {pack_weight:.2f} grams.",
            f"{name} bought the gum on {purchase_month}/{purchase_day}."
        ]
    
        # Out-topic irrelevant information
        irrelevant_infos_out_topic = [
            f"{name} has ${money_in_bank} saved up in his bank account.",
            f"{name}'s favorite color is {favorite_color}."
        ]
    
        # Add irrelevant information based on probability
        all_irrelevant_infos = irrelevant_infos_in_topic + irrelevant_infos_out_topic
        for irrelevant_info in all_irrelevant_infos:
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
        main_sentences = problem[:4]
        irrelevant_sentences = problem[4:]
        if shuffle:
            random.shuffle(main_sentences[1:])
            random.shuffle(irrelevant_sentences)
        problem = main_sentences + irrelevant_sentences
    
        # Add the question
        problem.append(question)
    
        # Calculate the answer
        intervals = school_day_length // chews_every
        gum_chewed_at_school = chews_per_interval * intervals
        total_gum_chewed = gum_chewed_at_school + chews_on_way_home + chews_after_dinner
        gum_remaining_before_giving = initial_gum - total_gum_chewed
        answer = gum_remaining_before_giving / 2  # Gives half to sister
        if answer%1==0 and answer>0:
            break

    # Return problem and answer
    cot = [f"Calculate the number of intervals by dividing {school_day_length} by {chews_every}, which gives {intervals}.", f"Calculate the gum chewed at school by multiplying {chews_per_interval} by {intervals}, resulting in {gum_chewed_at_school}.", f"Add the gum chewed on the way home and after dinner to the gum chewed at school to get the total gum chewed: {gum_chewed_at_school} + {chews_on_way_home} + {chews_after_dinner} = {total_gum_chewed}.", f"Subtract the total gum chewed from the initial gum to find the gum remaining before giving: {initial_gum} - {total_gum_chewed} = {gum_remaining_before_giving}.", f"Divide the gum remaining before giving by 2 to find the final answer: {gum_remaining_before_giving} / 2 = {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':all_irrelevant_infos}

