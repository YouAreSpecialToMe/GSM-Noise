from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[9]:


import random
import math
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    stories = []
    irrelative_informations = []
    
    while True:
        
    
        
        names= ["Alice", "Ethan", "Lily", "James", "Sophia"]
    
        items = ["coins", "buttons", "stones"]
    

        name = random.choice(names)
        item=random.choice(items)
       
    
      
        num1=random.randint(10,20)
        num2=random.randint(2,5)
        num3=random.randint(2,5)
        percent1=random.randint(30,60)
    
        ans1= num1*(100-percent1)*0.01+num2-num3
        
            
        if ans1>0 and ans1%1==0:
        
            # break down the question into sentences-level.
            story_1 = f"""{name} has a bag of {item} with {num1} inside."""
            stories.append(story_1)
            
            story_2 = f"""{name} tripped over a pebble while carrying it and dropped {percent1}% of them."""
            stories.append(story_2)
            
            story_3 = f"""{name} scrambled to search for them but only came up with {num2}."""
            stories.append(story_3)
    
            story_4 = f"""When {name} went back home, {name} inspected the {item} further."""
            stories.append(story_4)
    
            story_5 = f"""{num3} of them {name} picked up wasn't a {item}, but actually a bead, so {name} got rid of it."""
            stories.append(story_5)

            original_problem=stories.copy()
            
    
            # in-topic irrelative information
            num5 = random.randint(2,4)
            irrelative_info_1 = f"""After picking up the {item}, {name} noticed {num5} shiny objects nearby."""
            irrelative_informations.append(irrelative_info_1)
    
            num7 = random.randint(2,4)
            irrelative_info_3 =  f"""{name} has {num7} pet cat named Whiskers who loves playing with {item}."""
            irrelative_informations.append(irrelative_info_3)
            
            # out-topic irrelative information
            
    
            num6 = random.randint(20,80)
            irrelative_info_3 = f"""Earlier that day, {name} had lunch with a friend at a nearby café and spent ${num6}"""
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
            
            question = f"""How many {item} did {name} end up with?"""
            original_problem.append(question)
            stories.append(question)
            ans=ans1
            ans=int(ans)
        

            break
            
        # Return the problem and the answer
    cot = [f"{name} initially has {num1} {item}.", f"{name} dropped {percent1}% of them, which means {name} lost {num1} * (100 - {percent1}) * 0.01 {item}.", f"{name} found {num2} {item} after searching.", f"{num3} of the found items were not {item}, so {name} got rid of them.", f"The total number of {item} {name} ended up with is {ans1}, which is {ans} after rounding."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}
    

