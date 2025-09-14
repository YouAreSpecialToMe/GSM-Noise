from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    stories = []
    irrelative_informations = []
    
    while True:
        
    
        rooms = ['Living room', 'Dining room', 'Family room','Dining room']
        names = ["Jack", "Liam", "Grace", "Sophie", "Mason"]

        name = random.choice(names)
        room = random.choice(rooms)
        
        price1 = random.randint(8,20)
        price2 = random.randint(1,4)
        price3 = random.randint(1,5)
        price4 = random.randint(30,40)
        size1= random.randint(15,22)
        size2= random.randint(15,22)
       
    
        if size1*size2*(price1+price2+price3+price4)>0:
        
        
            # break down the question into sentences-level.
            story_1 = f"""{name} is replacing the carpet in {name}'s {room}."""
            stories.append(story_1)
            
            story_2 = f"""The new carpet {name}'s chosen costs ${price1} per square foot."""
            stories.append(story_2)
            
            story_3 = f"""There is an additional cost of ${price2} per square foot for padding underneath."""
            stories.append(story_3)
            
            story_4 = f"""{name}'s contractor charges ${price3} per square foot to remove the old carpet."""
            stories.append(story_4)
    
            story_5 = f"""The contractor charges ${price4} per square foot to install the new carpet."""
            stories.append(story_5)
    
            story_6 = f"""{name}'s {room} measures {size1} feet by {size2} feet."""
            stories.append(story_6)

            original_problem=stories.copy()
            
            
            # in-topic irrelative information
            salary1 = random.randint(6000,7000)
            irrelative_info_1 = f"""{name} earns ${salary1} each month."""
            irrelative_informations.append(irrelative_info_1)
            
            rent = random.randint(1000,2000)
            irrelative_info_2 = f"""{name} pays ${rent} for the house. """
            irrelative_informations.append(irrelative_info_2)
            
            # out-topic irrelative information
            years = random.randint(2,5)
            irrelative_info_3 =  f"""{name} has been living in this city for {years}."""
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
            
            question = f""" How much will it cost {name} to replace the carpet?"""
            stories.append(question)
            original_problem.append(question)
            
            ans =size1*size2*(price1+price2+price3+price4)
           

            break
        # Return the problem and the answer
    cot = [f"Calculate the area of {name}'s {room} by multiplying its dimensions: {size1} feet by {size2} feet.", f"The total cost per square foot is the sum of the costs: {price1} (new carpet) + {price2} (padding) + {price3} (removal) + {price4} (installation).", f"Multiply the area by the total cost per square foot to find the total cost: {size1} * {size2} * ({price1} + {price2} + {price3} + {price4}) = {ans}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}

