from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[29]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
    # Define names and items
        names = ["Joe", "Alice", "Bob", "Cindy", "Daniel", "Emma", "Frank", "Grace"]
        items = ["shirt", "shorts", "jacket", "hat", "shoes", "dress", "skirt", "jeans"]
        
        # Randomly select a name
        name = random.choice(names)
        
        # Determine pronoun based on gender
        male_names = ["Joe", "Bob", "Daniel", "Frank"]
        pronoun = "he" if name in male_names else "she"
        possessive_pronoun = "his" if name in male_names else "her"
        
        # Randomly select two different items
        item1 = random.choice(items)
        item2 = random.choice([item for item in items if item != item1])
        
        # Randomly generate variables
        total_money = random.randint(30, 100)
        discount = random.randint(10, 50)
        price1 = random.randint(10, 50)
        price2 = random.randint(10, 50)
        
    
        # Build the problem with variable names
        problem = [
            f"{name} has ${total_money} to buy an outfit for {possessive_pronoun} new field trip.",
            f"There is a {discount}% off sale at the clothing store.",
            f"The {item1} {pronoun} picks out has a price of ${price1}.",
            f"{name} also picks out a {item2} for ${price2}.",
        ]
        
        # Construct in-topic irrelevant information
        irrelevant_infos = [
            f"The store also sells accessories like belts and sunglasses.",
            f"{name}'s friend recommended this store.",
            f"The field trip is scheduled for next month."
        ]
        question=[ f"Assuming that sales tax is included, how much money will {name} have left after the purchase?"]
        original_problem=problem.copy()
        original_problem.append(question)
        
        # Construct out-topic irrelevant information
        irrelevant_out_topic = f"{name} enjoys playing basketball on weekends."
        irrelevant_infos.append(irrelevant_out_topic)
        
        # Randomly add irrelevant information based on probability
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
        first_sentence = problem[0]
        other_sentences = problem[1:]
        if shuffle:
            random.shuffle(other_sentences)
        problem = [first_sentence] + other_sentences+question
        
        # Compute the answer using the variables
        total_cost = (price1 + price2) * (1 - discount / 100)
        answer = total_money - total_cost
        answer=round(answer,2)
    
        if answer>0:
            break
        

    # Return the problem and answer
    cot = [f"{name} picks out a {item1} for {price1} and a {item2} for {price2}.", f"The total cost before discount is {price1} + {price2}.", f"The discount is {discount}%, so the total cost after discount is (1 - discount / 100) times the total cost before discount, which is {total_cost}.", f"The amount of money {name} has left after the purchase is {total_money} - {total_cost}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

