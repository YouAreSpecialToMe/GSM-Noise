from grammar_error import introduce_grammar_error, introduce_symbol_error
import random
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    stories = []
    irrelative_informations = []
    
    while True:
        
        names = ["Emma", "James", "Lily", "Henry", "Sophia"]
        items = ['cat', 'sheep', 'goat','rabbit']
        
  
        
        name = random.choice(names)
        
        item = random.choice(items)
        
        distance0 = random.randint(1,5)
        distance1 = random.randint(1,5)
        distance2 = random.randint(1,5)
        distance3 = random.randint(1,5)
    
        if distance3*4-distance2-distance1-distance0>0:
        
        
            # break down the question into sentences-level.
            story_1 = f"""{name} has 4 {item}s."""
            stories.append(story_1)
            
            story_2 = f""" They each need a certain amount of exercise per day."""
            stories.append(story_2)
            
            story_3 = f"""The first needs to walk {distance0} mile."""
            stories.append(story_3)
            
            story_4 = f"""The second needs to walk {distance1} miles."""
            stories.append(story_4)
            
            story_5 = f""" The third needs to walk {distance2} miles."""
            stories.append(story_5)
            
            story_6 = f""" On average, they need to walk {distance3} miles per day."""
            stories.append(story_6)
            original_problem=stories.copy()
            
            
            # in-topic irrelative information
            distance4 = random.randint(1,5)
            irrelative_info_1 = f"""{name} also walk {distance4} alone every day"""
            irrelative_informations.append(irrelative_info_1)
            
            item_number = random.randint(1,5)
            # in-topic irrelative information
            irrelative_info_2 = f"""{name}'s father also has {item_number} {item}s"""
            irrelative_informations.append(irrelative_info_2)
            
            # out-topic irrelative information
            distance5 = random.randint(5,10)
            irrelative_info_3 = f"""The length of the road in front of {name}'s house is {distance5} miles"""
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

            question = f"""How many miles does the last {item} need?"""
            stories.append(question)
            original_problem.append(question)
            
            ans = distance3*4-distance2-distance1-distance0

            break
            
        # Return the problem and the answer
    cot = [f"The average distance each {item} needs to walk is {distance3} miles, so the total distance for 4 {item}s is {distance3} * 4.", f"Subtract the distances for the first three {item}s: {distance0}, {distance1}, and {distance2} from the total distance.", f"The remaining distance is the distance the last {item} needs to walk, which is {ans} miles."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}