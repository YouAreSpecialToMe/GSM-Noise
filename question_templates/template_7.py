from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    stories = []
    irrelative_informations = []
    
    while True:
        
    
        item1s = ['floral', 'woody', 'spicy','citrus']
        item2s = ['herbal', 'musk', 'oceanic','fresh']
        

        
        item1 = random.choice(item1s)
        item2 = random.choice(item2s)
        
        number1 = random.randint(5,10)
        number2 = random.randint(2,10)
        number3 = random.randint(4,8)
        number4 = random.randint(2,6)
    
        if number1*number3-number2*number4>0:
        
        
            # break down the question into sentences-level.
            story_1 = f"""A perfume company is trying to create new scents."""
            stories.append(story_1)
            
            story_2 = f"""They already have {number1} {item2} scents and {number2} {item1} scents available."""
            stories.append(story_2)
            
            story_3 = f"""They need to decide which kind of scent to focus on."""
            stories.append(story_3)
            
            story_4 = f"""They decide to focus on whichever scent sells the most."""
            stories.append(story_4)
    
            story_5 = f"""They monitor their number of sales as part of their research."""
            stories.append(story_5)
            
            story_6 = f"""By the end of the day, they sell {number3} of each of the {item2} scents."""
            stories.append(story_6)
            
            story_7 = f""" They sell {number4} of each of the {item1} scents available."""
            stories.append(story_7)

            original_problem=stories.copy()
            
            
            # in-topic irrelative information
            price1 = random.randint(30,40)
            irrelative_info_1 = f"""The price of each {item2} perfume is ${price1}."""
            irrelative_informations.append(irrelative_info_1)
            
            price2 = random.randint(20,40)
            irrelative_info_2 = f"""The price of each {item1} perfume is ${price2}."""
            irrelative_informations.append(irrelative_info_2)
            
            # out-topic irrelative information
            people_number = random.randint(30,40)
            irrelative_info_3 = f"""The company plan to recruit {people_number} people this year."""
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
            
            question = f"""How many more {item2} scents sold compared with the {item1}scents?"""
            stories.append(question)
            original_problem.append(question)
            
            ans =number1*number3-number2*number4

            break
            
        # Return the problem and the answer
    cot = [f"Calculate the total number of {item2} scents sold by multiplying {number1} by {number3}.", f"Calculate the total number of {item1} scents sold by multiplying {number2} by {number4}.", f"Subtract the total number of {item1} scents sold from the total number of {item2} scents sold to find the difference, which is {ans}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}

