from grammar_error import introduce_grammar_error, introduce_symbol_error
import random
import math

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    stories = []
    irrelative_informations = []
    
    while True:
        
    
        
        names= names = ["Mason", "Olivia", "Liam", "Emma", "Ava"]
        flowers1 = ["roses", "tulips", "daisies"]
        flowers2 = ["lilies", "sunflowers", "orchids"]
        flowers3 = ["pansies", "hydrangeas", "lavender"]
    

        name = random.choice(names)
        item1=random.choice(flowers1)
        item2=random.choice(flowers2)
        item3=random.choice(flowers3)
    
        num1=round(random.uniform(1, 3), 2)
        num2=round(random.uniform(1, 3), 2)
        num3=round(random.uniform(1, 3), 2)
        num4 = random.randint(0,20)
        num5 = random.randint(0,20)
        num6 = random.randint(0,20)
    
        ans1= round(num1)*num4+round(num2)*num5+round(num3)*num6
        
            
        if ans1>0:
        
            # break down the question into sentences-level.
            story_1 = f"""{name} has a flower stand at the Farmers Market."""
            stories.append(story_1)
            
            story_2 = f"""{name} sells three kinds of flowers: {item1}, {item2}, and {item3}."""
            stories.append(story_2)
            
            story_3 = f"""{name} usually sells {item1} for ${num1} per pot, {item2} for ${num2} per pot, and {item3} for ${num3} per pot."""
            stories.append(story_3)
    
            story_4 = f"""{name} has no change today, so {name} has decided to round all {name}'s prices to the nearest dollar."""
            stories.append(story_4)
            original_problem=stories.copy()
    
            
    
            # in-topic irrelative information
            num9 = random.randint(20,80)
            irrelative_info_3 = f"""{name} plans to offer a {num9}% discount on flowers next month."""
            irrelative_informations.append(irrelative_info_3)
           
    
            num8 = random.randint(1000,2000)
            irrelative_info_3 =  f"""{name} rents this flower stand with ${num8} every month."""
            irrelative_informations.append(irrelative_info_3)
            
            # out-topic irrelative information
    
            num7 = random.randint(2,4)
            irrelative_info_1 = f"""{name}'s flower stand has been at the Farmers Market for {num7} years."""
            irrelative_informations.append(irrelative_info_1)
            
            
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
            
            question = f"""If {name} sells {num4} pots of {item1}, {num5} pots of {item2}, and {num6} pots of {item3}, how much will {name} make?"""
            stories.append(question)
            original_problem.append(question)
            ans=ans1
            ans=int(ans)
        
            
            break
            
        # Return the problem and the answer
    cot = [f"{name} rounds the price of {item1} to the nearest dollar, which is round({num1}).", f"{name} rounds the price of {item2} to the nearest dollar, which is round({num2}).", f"{name} rounds the price of {item3} to the nearest dollar, which is round({num3}).", f"The total revenue from selling {num4} pots of {item1} is round({num1}) * {num4}.", f"The total revenue from selling {num5} pots of {item2} is round({num2}) * {num5}.", f"The total revenue from selling {num6} pots of {item3} is round({num3}) * {num6}.", f"The total revenue is the sum of all revenues: round({num1}) * {num4} + round({num2}) * {num5} + round({num3}) * {num6}, which is {ans1}.", f"The final answer is the integer value of {ans1}, which is {ans}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}