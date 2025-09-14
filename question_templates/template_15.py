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
        
    
        
        roles = ["instructor", "professor", "tutor", "educator", "mentor"]
        subjects=['math','physics','chemistry','biology']
    
    

        
        role = random.choice(roles)
        subject=random.choice(subjects)
       
    
        num1=random.randint(4,7)
        num2=random.randint(1,3)
      
        percent1=random.randint(20,30)
        percent2=random.randint(31,50)
        
        ans1= math.ceil((num1*(100-percent2)*0.01-num2)/(percent1*num1*0.01))
        
            
        if ans1>0:
        
        
            # break down the question into sentences-level.
            story_1 = f"""A {role} uses a {num1}-inch piece of chalk to write {subject} equations on a chalkboard for the {role}'s students."""
            stories.append(story_1)
            
            story_2 = f"""The {role} likes to conserve chalk, so the {role} tries to only use {percent1}% of the chalk each day."""
            stories.append(story_2)
            
            story_3 = f"""Since the {role} cannot write with a very small piece of chalk, the {role} recycles the chalk when it is smaller than {num2} inches."""
            stories.append(story_3)
    
            story_4 = f"""On Monday, the {role} used a new piece of chalk."""
            stories.append(story_4)
            
            story_5 = f"""The {role}'s students needed extra help that day, so the {role} ended up writing more than usual."""
            stories.append(story_5)
    
            story_6 = f"""The {role} used up {percent2}% of the chalk by the end of the day."""
            stories.append(story_6)

            original_problem=stories.copy()
    
    
    
    
            # in-topic irrelative information
            num3 = random.randint(30,40)
            irrelative_info_1 = f"""One pack of chalk contains {num3} chalks."""
            irrelative_informations.append(irrelative_info_1)
            
            num4 = random.randint(10,20)
            irrelative_info_2 = f"""Each pack of chalk costs ${num4}."""
            irrelative_informations.append(irrelative_info_2)
            
            # out-topic irrelative information
            num5 = random.randint(30,40)
            irrelative_info_3 =  f"""The age of the {role} is {num5}."""
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
            
            question = f"""If the {role} goes back to using only {percent1}% of the chalk each day, how many days does the {role} have before the {role} has to recycle this piece?"""
            stories.append(question)
            original_problem.append(question)
            ans=ans1
            ans=int(ans)

            break
            
        # Return the problem and the answer
    cot = [f"The {role} starts with a {num1}-inch piece of chalk and uses {percent2}% of it on the first day.", f"This means the remaining chalk is {num1} * (100 - {percent2}) * 0.01 inches.", f"The {role} recycles the chalk when it is smaller than {num2} inches.", f"The {role} uses {percent1}% of the chalk each subsequent day.", f"Calculate the number of days before the chalk is less than {num2} inches: ({num1} * (100 - {percent2}) * 0.01 - {num2}) / ({percent1} * {num1} * 0.01).", f"The number of days is the ceiling of this value, which is {ans1}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}

