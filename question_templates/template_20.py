from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[6]:


import random
import math
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    stories = []
    irrelative_informations = []
    
    while True:
        
    
        
        places = ["resort", "hostel", "lodge", "inn", "guesthouse"]
    
    

        item=random.choice(places)
       
    
      
        num1=random.randint(90,120)
        num2=random.randint(10,30)
        num3=random.randint(5,15)
        num4=random.randint(1,10)
        num5=random.randint(2,4)
       
        ans1= num1-num2-num3+num5*num3+num4
        
            
        if ans1<num1:
        
        
            # break down the question into sentences-level.
            story_1 = f"""On a busy Saturday morning, a {item} was completely booked with {num1} guests."""
            stories.append(story_1)
            
            story_2 = f"""{num2} guests elected an early checkout."""
            stories.append(story_2)
            
            story_3 = f"""{num3} guests elected for a late checkout."""
            stories.append(story_3)
    
            story_4 = f"""In the afternoon, {num5} times as many people checked in as those who opted for a late checkout."""
            stories.append(story_4)
    
            story_5 = f"""{num4} more people checked in after dinner was served."""
            stories.append(story_5)

            original_problem=stories.copy()
            
    
            # in-topic irrelative information
            num6 = random.randint(100,200)
            irrelative_info_1 = f"""Each guest pay ${num6} for the {item}."""
            irrelative_informations.append(irrelative_info_1)
    
            num7 = random.randint(100,200)
            irrelative_info_3 =  f"""There are {num7} employees in the {item}."""
            irrelative_informations.append(irrelative_info_3)
            
            # out-topic irrelative information
    
            time = random.randint(22,24)
            irrelative_info_3 = f"""The latest check in time is {time}pm."""
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
            
            question = f"""How many guests does the {item} now have?"""
            original_problem.append(question)
            stories.append(question)
            ans=ans1
            ans=(ans)

            break
        
        # Return the problem and the answer
    cot = [f"The hotel initially has {num1} guests.", f"{num2} guests elected an early checkout, reducing the number of guests to {num1} - {num2}.", f"{num3} guests elected for a late checkout, further reducing the number of guests to {num1} - {num2} - {num3}.", f"In the afternoon, {num5} times as many people checked in as those who opted for a late checkout, adding {num5} * {num3} guests.", f"After dinner, {num4} more people checked in, adding {num4} guests.", f"Therefore, the total number of guests now is {num1} - {num2} - {num3} + {num5} * {num3} + {num4}, which is {ans1}.", f"The final answer is {ans1}, which is {ans}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}

