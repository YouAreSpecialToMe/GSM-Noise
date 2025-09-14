from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[3]:


import random
import math
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    stories = []
    irrelative_informations = []
    
    while True:
        
    
        
        names = ["Oliver", "Ella", "Grace", "Henry", "Sophia"]
        snacks = ["muffins", "crackers", "granola bars", "candies", "biscuits"]
    

        name = random.choice(names)
        item=random.choice(snacks)
       
    
      
        num1=random.randint(30,50)
        num2=random.randint(3,6)
        num3=random.randint(2,5)
       
    
    
        
        ans1= num1-num2*5-num3*7
        
            
        if ans1>0:
        
        
            # break down the question into sentences-level.
            story_1 = f"""{name} buys 1 bag of {item} a week."""
            stories.append(story_1)
            
            story_2 = f"""The bag has {num1} {item}."""
            stories.append(story_2)
            
            story_3 = f"""{name} puts {num2} {item} in {name}'s son's lunch box 5 days a week."""
            stories.append(story_3)
    
            story_4 = f"""{name}'s husband eats {num3} {item} a day for 7 days."""
            stories.append(story_4)
            
            story_5 = f"""{name} eats the rest of the {item}."""
            stories.append(story_5)

            original_problem=stories.copy()
    
    
    
    
    
    
    
            # in-topic irrelative information
            num5 = random.randint(20,30)
            irrelative_info_1 = f"""One pack of {item} costs ${num5}."""
            irrelative_informations.append(irrelative_info_1)
            
            num6 = random.randint(2,3)
            irrelative_info_2 = f"""{name} also eat {num6} apples per week."""
            irrelative_informations.append(irrelative_info_2)
            
            # out-topic irrelative information
            num7 = random.randint(45,60)
            irrelative_info_3 =  f"""{name}'s weight is {num7}kg."""
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
            
            question = f"""How many cookies does {name} eat?"""
            original_problem.append(question)
            stories.append(question)
            ans=ans1
            ans=(ans)
        
            break
        
        # Return the problem and the answer
    cot = [f"{name} puts {num2} {item} in {name}'s son's lunch box 5 days a week, which totals to {num2} * 5.", f"{name}'s husband eats {num3} {item} a day for 7 days, which totals to {num3} * 7.", f"The total number of {item} consumed by {name}'s son and husband is {num2} * 5 + {num3} * 7.", f"The bag has {num1} {item}, so the remaining {item} that {name} eats is {num1} - ({num2} * 5 + {num3} * 7), which is {ans1}.", f"Therefore, the final answer is {ans1}, which is equal to {ans}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}

