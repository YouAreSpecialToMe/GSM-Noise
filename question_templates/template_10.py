from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    stories = []
    irrelative_informations = []
    
    while True:
        
    
        items = ["oranges", "pears", "peaches", "plums", "mangoes"]
        names = ["Emily", "Lucas", "Sophia", "Ethan", "Chloe"]
        

        
        name = random.choice(names)
        item = random.choice(items)
        
        percent = random.randint(30,60)
        number1 = random.randint(20,40)
        times1 = random.randint(2,5)
        times2 = random.randint(2,5)
        number=random.randint(400,600)
       
        ans= number-times1*number1-times2*percent*number1*0.01-number1-percent*number1*0.01
        if ans>0 and ans%1==0:
        
        
            # break down the question into sentences-level.
            story_1 = f"""While {name} is gathering {item} from {name}'s family's orchard, {name}'s sister comes outside to help {name}."""
            stories.append(story_1)
            
            story_2 = f"""{name} gathers {number1} {item} from the tallest trees."""
            stories.append(story_2)
            
            story_3 = f"""{name} gathers {percent}% this amount from the shortest trees."""
            stories.append(story_3)
            
            story_4 = f"""{name} gathers more {item} from the average trees."""
            stories.append(story_4)
    
            story_5 = f"""Compared with {name}, {name}'s sister gathers {times1} times as many {item} from the tallest trees."""
            stories.append(story_5)
    
            story_6 = f"""{name}'s sister gathers {times2} times as many {item} from the shortest trees."""
            stories.append(story_6)
    
            story_7 = f"""{name} doesn't take any from the average trees."""
            stories.append(story_7)

            original_problem=stories.copy()
            
            
            # in-topic irrelative information
            number3 = random.randint(300,400)
            irrelative_info_1 = f"""{name}'s parents also get {number3} {item}s from the tallest tree ."""
            irrelative_informations.append(irrelative_info_1)
            
            number4 = random.randint(300,400)
            irrelative_info_2 = f"""{name}'s brother also get {number4} {item}s from the average tree ."""
            irrelative_informations.append(irrelative_info_2)
            
            # out-topic irrelative information
            tree_numbers = random.randint(50,70)
            irrelative_info_3 =  f"""There are total {tree_numbers} trees in the orchard ."""
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
            
            question = f""" If the sisters have gathered a combined total of {number} {item}s, how many {items}s did {name} gather from the average trees?"""
            stories.append(question)
            original_problem.append(question)
            ans=number-times1*number1-times2*percent*number1*0.01-number1-percent*number1*0.01
            ans=int(ans)
            

            break
            
        # Return the problem and the answer
    cot = [f"{name} gathers {number1} {item} from the tallest trees.", f"{name} gathers {percent}% of this amount from the shortest trees, which is {percent} * {number1} * 0.01.", f"{name}'s sister gathers {times1} times as many {item} from the tallest trees, which is {times1} * {number1}.", f"{name}'s sister gathers {times2} times as many {item} from the shortest trees, which is {times2} * {percent} * {number1} * 0.01.", f"The total number of {item} gathered by both sisters is {number}.", f"The number of {item} Joanne gathered from the average trees is calculated as {number} - {times1} * {number1} - {times2} * {percent} * {number1} * 0.01 - {number1} - {percent} * {number1} * 0.01, which is {ans}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}

