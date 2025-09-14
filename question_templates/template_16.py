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
        
    
        
        pools = ["water tank", "fountain", "hot tub", "pond"]
        names = ["Sarah", "Liam", "Ava", "Ethan", "Mia"]
    
    

        name = random.choice(names)
        item=random.choice(pools)
       
    
        num1=5.9
        num2=random.randint(10,15)
        num3=random.randint(20,27)
        num4=random.randint(3,7)
        price1=round(random.uniform(0.1, 0.3), 1)
    
        
        ans1= num2*num3*num4*num1*price1
        
            
        if ans1>0:
        
        
            # break down the question into sentences-level.
            story_1 = f"""The {name} family is getting ready for summer and needs to have their {item} filled."""
            stories.append(story_1)
            
            story_2 = f"""The company instructed them to measure to find the volume of the {item}."""
            stories.append(story_2)
            
            story_3 = f"""They then need to multiply the volume by {num1} to calculate how many gallons of water they need."""
            stories.append(story_3)
    
            story_4 = f"""The cost for the company to come and fill the pool is ${price1} per gallon."""
            stories.append(story_4)
            
            story_5 = f"""{name} measured and found the {item} is {num2} feet wide, {num3} feet long, and {num4} feet deep."""
            stories.append(story_5)

            original_problem=stories.copy()
    
    
    
    
    
            # in-topic irrelative information
            num3 = random.randint(1,4)
            irrelative_info_1 = f"""The item has been built for {num3} years."""
            irrelative_informations.append(irrelative_info_1)
            
            num4 = random.randint(200000,300000)
            irrelative_info_2 = f"""{name} earn ${num4} every year."""
            irrelative_informations.append(irrelative_info_2)
            
            # out-topic irrelative information
            num5 = random.randint(3,7)
            irrelative_info_3 =  f"""{num5} people are in {name}'s family."""
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
            
            question = f"""How much will it cost to fill the pool?"""
            stories.append(question)
            original_problem.append(question)
            ans=ans1
            ans=(ans)
        
            

            break
        # Return the problem and the answer
    cot = [f"Calculate the volume of the {item} by multiplying its width, length, and depth: {num2} * {num3} * {num4}.", f"Multiply the volume by {num1} to find out how many gallons of water are needed.", f"Multiply the number of gallons by the cost per gallon, {price1}, to find the total cost.", f"The total cost to fill the {item} is {ans1}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}

