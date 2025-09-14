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
        
    
        
        names = ["Emily", "Noah", "Sophia", "James", "Olivia"]
        items = ["band", "orchestra", "dance troupe", "theater group", "singing ensemble"]
        sexes = ["male", "female"]
    

        name = random.choice(names)
        item = random.choice(items)
        sex = random.choice(sexes)
    
        num1=random.randint(50,70)
        num2=random.randint(2,6)
      
        percent1=random.randint(40,60)
        percent2=100-percent1
        percent3=random.randint(30,55)
    
       
        if sex=='female':
            ans1=num1*0.01*percent2*(100-percent3)*0.01+num2
        else:
            ans1=num1*0.01*percent1*(100-percent3)*0.01+num2
            
        if ans1>0 and ans1%1==0:
        
        
            # break down the question into sentences-level.
            story_1 = f"""{name} is part of a {item} that has {num1} members."""
            stories.append(story_1)
            
            story_2 = f"""{percent1}% of the {item} members are boys, and {percent2}% are girls."""
            stories.append(story_2)
            
            story_3 = f"""The {item} decides to perform with just its {sex} members."""
            stories.append(story_3)
    
            story_4 = f"""On the day of the performance, however, {percent3}% the people performing can't make it to the show because their bus breaks down."""
            stories.append(story_4)
            
            story_5 = f"""The {item}'s {num2} teachers then decide to perform with them."""
            stories.append(story_5)

            original_problem=stories.copy()
    
    
    
    
            # in-topic irrelative information
            time = random.randint(2,4)
            irrelative_info_1 = f"""It takes {time} hours to get the performance place."""
            irrelative_informations.append(irrelative_info_1)
            
            num3 = random.randint(6,10)
            irrelative_info_2 = f"""There are {num3} teachers in the {item}."""
            irrelative_informations.append(irrelative_info_2)
            
            # out-topic irrelative information
            num5 = random.randint(16,20)
            irrelative_info_3 =  f"""The average age for the members is {num5}."""
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
            
            question = f"""How many people sang in the performance?"""
            stories.append(question)
            original_problem.append(question)
            ans=ans1
            ans=int(ans)
        

            break
        # Return the problem and the answer
    cot = [f"The {item} has {num1} members, and {percent2}% of them are {sex}.", f"On the day of the performance, {percent3}% of the {sex} members can't make it.", f"The number of {sex} members who can perform is {num1} * 0.01 * {percent2} * (100 - {percent3}) * 0.01.", f"The {item}'s {num2} teachers decide to perform with them.", f"Therefore, the total number of people who sang in the performance is the number of {sex} members who can perform plus {num2} teachers, which is {ans1}.", f"The final answer is {ans}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}
    

