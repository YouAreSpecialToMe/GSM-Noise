from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[8]:


import random
import math
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):

    stories = []
    irrelative_informations = []
    
    while True:
    
        names = ["Charlie", "Megan", "Lucas", "Ava", "Jackson"]
    
        items = ["butterflies", "clouds", "planes", "kites", "balloons"]

        name = random.choice(names)
        item=random.choice(items)
    
        num1=random.randint(0,150)
        num2=random.randint(0,150)
        num3=random.randint(0,150)
        num5=random.randint(0,150)
        num4 = random.randint(0,150)
    
    
        ans1= (num1+num5+num2+num3+num4)/7
        
            
        if ans1>0 and ans1%1==0:
        
            # break down the question into sentences-level.
            story_1 = f"""{name} wants to count things and decided to count how many {item} there are in the sky over the next week."""
            stories.append(story_1)
            
            story_2 = f"""On days one and two, {name} saw a total of {num1} {item}."""
            stories.append(story_2)
            
            story_3 = f"""On day three, {name} saw {num5}."""
            stories.append(story_3)
    
            story_4 = f"""On days four and five, {name} saw {num2} {item}."""
            stories.append(story_4)
    
            story_5 = f"""On day six, {name} saw {num3} {item}."""
            stories.append(story_5)
    
            story_6 = f"""On day seven, {name} saw {num4} {item}."""
            stories.append(story_6)
            original_problem=stories.copy()
    
    
            # in-topic irrelative information
            num9 = random.randint(1,3)
            irrelative_info_3 = f"""{name} has {num9} pair of binoculars that {name} uses to count the {item}."""
            irrelative_informations.append(irrelative_info_3)
    
            num8 = random.randint(20,30)
            irrelative_info_3 =  f"""The counting spot was in a park with {num8} trees and open spaces."""
            irrelative_informations.append(irrelative_info_3)
            
            # out-topic irrelative information
            num7 = random.randint(2,4)
            irrelative_info_1 = f"""{name} has {num7} pet dogs that often joins {name} on these outdoor trips."""
            irrelative_informations.append(irrelative_info_1)
            
            
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
            
            question = f"""On average, how many {item}s did {name} see in a day?"""
            stories.append(question)
            original_problem.append(question)
            ans=ans1
            ans=int(ans)
            break
        # Return the problem and the answer
    cot = [f"Calculate the total number of {item} seen over the week: {num1} + {num5} + {num2} + {num3} + {num4}.", f"Divide the total by 7 to find the average number of {item} seen per day: ({num1} + {num5} + {num2} + {num3} + {num4}) / 7, which is {ans1}.", f"Convert the average to an integer: {ans1} becomes {ans}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}

