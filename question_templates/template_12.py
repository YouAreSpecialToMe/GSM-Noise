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
        
    
        
        names = ["Lily", "Oscar", "Amelia", "Jack", "Grace"]
        act1s=["hiking", "biking", "fishing", "surfing", "kayaking"]
        act2s=["snorkeling", "diving", "jogging", "climbing", "sunbathing"]
        act3s= ["museum tours", "concerts", "workshops", "cooking classes", "art exhibits"]
        act4s=["exploring", "shopping", "visiting landmarks", "taking a city tour", "photographing nature"]
        

        
        name = random.choice(names)
        act1 = random.choice(act1s)
        act2 = random.choice(act2s)
        act3 = random.choice(act3s)
        act4 = random.choice(act4s)
        
        
        percent1 = random.randint(20,50)
        percent2 = random.randint(20,50)
        num1=random.randint(2,5)
        num2=random.randint(2,3)
        time1=random.randint(3,8)
       
        ans1= ((time1+time1*0.5+num1*num2)/percent1)
        if ans1>0 and ans1%1==0:
        
        
            # break down the question into sentences-level.
            story_1 = f"""{name} decides to do several activities while out on vacation."""
            stories.append(story_1)
            
            story_2 = f"""{name} spends {time1} hours {act1} and half that time {act2}."""
            stories.append(story_2)
            
            story_3 = f"""{name} also watched {num1} different {act3} which were {num2} hours each."""
            stories.append(story_3)
    
            story_4 = f"""This was {percent1}% of the time {name} spent."""
            stories.append(story_4)
            
            story_5 = f"""{name} spent {percent2}% of {name}'s time {act4}."""
            stories.append(story_5)

            original_problem=stories.copy()
    
    
    
    
            # in-topic irrelative information
            people = random.randint(2,5)
            irrelative_info_1 = f"""{name} takes vacation with {people} friends."""
            irrelative_informations.append(irrelative_info_1)
            
            time2 = random.randint(10,20)
            irrelative_info_2 = f"""One of {name}'s friend spends {time2} hours swimming."""
            irrelative_informations.append(irrelative_info_2)
            
            # out-topic irrelative information
            money = random.randint(3000,4000)
            irrelative_info_3 =  f"""{name} spends ${money} on {name}'s vacation."""
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
            
            question = f"""How much time did {name} spend {act4}?"""
            stories.append(question)
            original_problem.append(question)
            ans=((time1+time1*0.5+num1*num2)/percent1)*percent2
            ans=int(ans)
        

            break
         # Return the problem and the answer
    cot = [f"{name} spends {time1} hours {act1} and half that time {act2}, which totals to {time1 + time1 * 0.5} hours.", f"{name} also watched {num1} different {act3} which were {num2} hours each, totaling {num1 * num2} hours.", f"The total time spent on these activities is {time1 + time1 * 0.5 + num1 * num2} hours.", f"This total time is {percent1}% of the time {name} spent, so the total time spent on vacation is {ans1} hours.", f"{name} spent {percent2}% of {name}'s time {act4}, which is {ans} hours."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}

