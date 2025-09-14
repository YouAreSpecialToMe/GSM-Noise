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
        
    
        
        names1 = ["Blake", "Liam", "Jack", "Noah", "Aiden"]
        names2 = ["Kelly", "Emma", "Sophia", "Ava", "Mia"]
        fields = ["soccer field", "track", "basketball court", "tennis court", "baseball field"]
    

        name1 = random.choice(names1)
        name2 = random.choice(names2)
        item=random.choice(fields)
       
    
        time1=random.randint(10,30)
        num1=random.randint(90,110)
        num2=random.randint(10,17)
        num3=random.randint(30,45)
        num4=random.randint(30,40)
    
    
        
        ans1= abs(2*num2*num1-(num1+num3*num4)*2)
        
            
        if ans1>0:
        
        
            # break down the question into sentences-level.
            story_1 = f"""{name1} and {name2} are having a contest to see who can run the most in {time1} minutes."""
            stories.append(story_1)
            
            story_2 = f"""They decide to do it on a {item} field that is {num1} yards long."""
            stories.append(story_2)
            
            story_3 = f"""{name1} runs back and forth {num2} times."""
            stories.append(story_3)
    
            story_4 = f"""{name2} runs back and forth once and then decides that {name2} doesn't want to run next to {name1}."""
            stories.append(story_4)
            
            story_5 = f"""{name2} starts to run to the {num3}-yard line and back."""
            stories.append(story_5)
    
            story_6 = f"""{name2} does this {num4} times."""
            stories.append(story_6)

            original_problem=stories.copy()
    
    
    
    
    
            # in-topic irrelative information
            num5 = random.randint(20,30)
            irrelative_info_1 = f"""The loser will give the winner ${num5}."""
            irrelative_informations.append(irrelative_info_1)
            
            num6 = random.randint(2,3)
            irrelative_info_2 = f"""They do the contest {num6} times a week."""
            irrelative_informations.append(irrelative_info_2)
            
            # out-topic irrelative information
            num7 = random.randint(3,7)
            irrelative_info_3 =  f"""{name1} is {num7} years older than {name2}."""
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
            
            question = f"""How much farther does the winner run than the loser?"""
            stories.append(question)
            original_problem.append(question)
            ans=ans1
            ans=(ans)
        
            break
        # Return the problem and the answer
    cot = [f"{name1} runs back and forth {num2} times on a field that is {num1} yards long. This means {name1} runs a total of 2 * {num2} * {num1} yards.", f"{name2} runs back and forth once on the same field, then runs to the {num3}-yard line and back {num4} times. This means {name2} runs a total of (2 * {num1}) + ({num3} * {num4} * 2) yards.", f"The difference in distance run by the winner and the loser is the absolute value of the difference between these two distances: abs(2 * {num2} * {num1} - ((2 * {num1}) + ({num3} * {num4} * 2))).", f"Therefore, the answer is {ans1}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}
    

