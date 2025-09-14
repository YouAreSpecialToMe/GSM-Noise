from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[5]:


import random
import math
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    stories = []
    irrelative_informations = []
    
    while True:
        
    
        
        names = ["Jack", "Olivia", "Mason", "Isabella", "Ethan"]
        spaces = ["hallway", "garage", "studio", "office", "kitchen"]
    
    

        name = random.choice(names)
        item=random.choice(spaces)
       
    
      
        num1=random.randint(8,12)
        num2=random.randint(8,12)
        num3=random.randint(4,9)
        num4=random.randint(15,25)
        num5=random.randint(8,20)
       
        ans1= math.ceil(2*(num1*num2+num2*num3)/num4)*num5
        
            
        if ans1>0:
        
        
            # break down the question into sentences-level.
            story_1 = f"""{name} is painting a {item} with four walls."""
            stories.append(story_1)
            
            story_2 = f"""The north and south walls are {num1} x {num2} feet."""
            stories.append(story_2)
            
            story_3 = f"""The east and west walls are {num3} x {num2} feet."""
            stories.append(story_3)
    
            story_4 = f"""A gallon of paint can cover {num4} square feet and costs ${num5}."""
            stories.append(story_4)

            original_problem=stories.copy()
            
    
            # in-topic irrelative information
            num5 = random.randint(2,4)
            irrelative_info_1 = f"""{num5} friends of {name} help {name} paint the {item}."""
            irrelative_informations.append(irrelative_info_1)
    
            num7 = random.randint(3,7)
            irrelative_info_3 =  f"""There are {num7} lamps in the {item}."""
            irrelative_informations.append(irrelative_info_3)
            
            # out-topic irrelative information
            
    
            num6 = random.randint(8000,10000)
            irrelative_info_3 = f"""The salary for {name} is ${num6} each month."""
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
            
            question = f"""How much will it cost to paint the {item}?"""
            original_problem.append(question)
            stories.append(question)
            ans=ans1
            ans=(ans)
        
            break
        
        # Return the problem and the answer
    cot = [f"Calculate the total area of the north and south walls: 2 * ({num1} * {num2}).", f"Calculate the total area of the east and west walls: 2 * ({num3} * {num2}).", f"Add the areas of all walls: 2 * ({num1} * {num2}) + 2 * ({num3} * {num2}).", f"Divide the total area by the coverage of one gallon of paint: (2 * ({num1} * {num2}) + 2 * ({num3} * {num2})) / {num4}.", f"Round up to the nearest whole number to determine the number of gallons needed: math.ceil((2 * ({num1} * {num2}) + 2 * ({num3} * {num2})) / {num4}).", f"Multiply the number of gallons by the cost per gallon: math.ceil((2 * ({num1} * {num2}) + 2 * ({num3} * {num2})) / {num4}) * {num5}.", f"The total cost to paint the room is {ans}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}

