from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random
import math
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):

    stories = []
    irrelative_informations = []
    
    while True:
        
    
        
        names = ["Aiden", "Bella", "Caleb", "Daisy", "Evan"]
        works= ["cleaning", "landscaping", "gardening", "maintenance", "organizing"]
   
        name = random.choice(names)
        work = random.choice(works)
    
        num1=random.randint(2,7)
        num2=random.randint(3,8)
        num3=random.randint(2,4)
        num4=random.randint(2,5)
        price1=random.randint(2,4)
        price2=random.randint(4,8)
        income=random.randint(100,200)
    
       
        ans1= income-(num1+num2)*(num3*price1+num4*price2)
        if ans1>0:
        
        
            # break down the question into sentences-level.
            story_1 = f"""{name} has started {name}'s own {work} business and is calculating how much profit he will make from his clients."""
            stories.append(story_1)
            
            story_2 = f"""He already has {num1} clients but is talking to another {num2} potential clients and feels confident enough to include them in {name}'s calculations."""
            stories.append(story_2)
            
            story_3 = f"""Each client's home will need {num3} bottles of bleach and {num4} packs of cloths to clean."""
            stories.append(story_3)
    
            story_4 = f"""Bottles of bleach will cost ${price1} each, and packs of cloths will cost ${price2} each."""
            stories.append(story_4)
            
            story_5 = f"""These are his only expenses."""
            stories.append(story_5)
    
            story_6 = f"""He calculates that his total income each week will be ${income}."""
            stories.append(story_6)

            original_problem=stories.copy()
    
    
            # in-topic irrelative information
            times = random.randint(2,4)
            irrelative_info_1 = f"""{name} goes for a travel {times} times a year."""
            irrelative_informations.append(irrelative_info_1)
            
            time2 = random.randint(4,10)
            irrelative_info_2 = f"""It takes {time2} hours to finishing one business."""
            irrelative_informations.append(irrelative_info_2)
            
            # out-topic irrelative information
            num5 = random.randint(20000,30000)
            irrelative_info_3 =  f"""{name} bought a car last year. The price is ${num5}."""
            irrelative_informations.append(irrelative_info_3)
            
            for irrelative_information in irrelative_informations:
                if random.random() < prob_irre:
                    stories.append(irrelative_information)
            
            first_story = stories[0]
            remaining_stories = stories[1:]
            if shuffle:
                random.shuffle(remaining_stories)
            stories = [first_story] + remaining_stories
            # Add symbol or grammar errors
            stories = [
                introduce_symbol_error(
                    introduce_grammar_error(p, prob_grammar_error),
                    prob_symbol_error
                ) for p in stories
            ]
            
            question = f"""Profit is the difference between total income and total expenses, so how much profit, in dollars, will {name} make each week?"""
            stories.append(question)
            original_problem.append(question)
            ans=income-(num1+num2)*(num3*price1+num4*price2)
            ans=int(ans)
        

            break
         # Return the problem and the answer
    cot = [f"{name} has {num1} clients and is considering {num2} potential clients, making a total of {num1 + num2} clients.", f"Each client's home requires {num3} bottles of bleach at ${price1} each and {num4} packs of cloths at ${price2} each.", f"The total expense for cleaning supplies per client is {num3} * {price1} + {num4} * {price2}.", f"The total expenses for all clients is (num1 + num2) * (num3 * price1 + num4 * price2).", f"The profit is calculated as total income minus total expenses: {income} - (num1 + num2) * (num3 * price1 + num4 * price2).", f"Therefore, the final answer is {ans}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}

