from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[3]:


import random
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    stories = []
    irrelative_informations = []
    
    while True:
        
    
        problems = ['Bump', 'Rough patch', 'Crack','Sinkhole']
        names = ["Alice", "Ben", "Charlotte", "Daniel", "Ella"]
        

        
        name = random.choice(names)
        problem = random.choice(problems)
        
        price1 = random.randint(400,600)
        price2 = random.randint(100,200)
        price3 = random.randint(20,40)
        item_number1 = random.randint(2,5)
       
    
        if price1-item_number1*price3-price2>0:
        
        
            # break down the question into sentences-level.
            story_1 = f"""{name} is fed up with the {problem} in front of his house."""
            stories.append(story_1)
            
            story_2 = f"""If it doesn't get fixed, it's going to do ${price1} worth of damage to his car."""
            stories.append(story_2)
            
            story_3 = f"""Unfortunately, the city council refuses to fix it."""
            stories.append(story_3)
            
            story_4 = f"""The city council will fine {name} ${price2} for unauthorized road maintenance if {name} fixes it on {name}'s own."""
            stories.append(story_4)
    
            story_5 = f"""{name} will also have to buy {item_number1} buckets of asphalt that each cost ${price3}."""
            stories.append(story_5)

            original_problem=stories.copy()
            
            
            # in-topic irrelative information
            salary1 = random.randint(6000,7000)
            irrelative_info_1 = f"""{name} earns ${salary1} each month."""
            irrelative_informations.append(irrelative_info_1)
            
            money1 = random.randint(400,500)
            irrelative_info_2 = f"""{name} has spent ${money1} repairing {name}'s car last year. """
            irrelative_informations.append(irrelative_info_2)
            
            # out-topic irrelative information
            money2 = random.randint(400,500)
            irrelative_info_3 =  f"""{name}'s friend borrows ${money2} from {name}."""
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
            
            
            question = f"""How much money does {name} save by fixing the {problem}?"""
            stories.append(question)
            original_problem.append(question)
            ans =price1-item_number1*price3-price2
           

            break
        
        # Return the problem and the answer
    cot = [f"The cost of damage to the car if the {problem} is not fixed is {price1}.", f"{name} will be fined {price2} for unauthorized road maintenance.", f"{name} needs to buy {item_number1} buckets of asphalt, each costing {price3}.", f"The total cost of fixing the {problem} is {item_number1} * {price3} + {price2}.", f"The money saved by fixing the {problem} is {price1} - ({item_number1} * {price3} + {price2}), which is {ans}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}

