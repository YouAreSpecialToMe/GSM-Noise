from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[18]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define names and days lists
        names = ["Frankie", "Alex", "Sam", "Taylor", "Jordan", "Casey"]
        
        # Select variables
        name = random.choice(names)
       
        # Episode lengths in minutes
      
       
        time1 = random.randint(1, 3)
        time2 = random.randint(1, 3)
        time3 = random.randint(1, 3)
        time4 = random.randint(1, 3)
        total_hours=random.randint(8, 12)
        answer=(total_hours-time4-time2-time3*0.5-time1*2)*2
        
        
        # Construct the problem with placeholders
        problem = [f"{name} watches TV after {name} finishes homework every night.",
                    f" On Monday and Tuesday, {name} watched {time1} 1-hour episode of his favorite show each night.",
                    f" On Wednesday, {name} watched a few episodes of a 30-minute show.",
                    f" On Thursday, {name} finished homework early and watched {time2} 1-hour episode and {time3} 30-minute show.",
                    f" On Friday, {name} got to stay up late for the weekend, so he watched {time4} 1-hour episodes."]
      
        
        # Construct the question
        question = f"If {name} watched {total_hours} hours of TV in all, how many 30-minute episodes did {name} watch on On Wednesday?"
        original_problem=problem.copy()
        original_problem.append(question)
        # Construct irrelevant information
        irrelevant_infos = [
            f"{name} prefers watching TV shows over movies.",
            f"{name}'s favorite genre is comedy.",
            f"{name} is planning a vacation next month."
        ]
        
        # Add irrelevant information based on probability
        for irrelevant_info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(irrelevant_info)
        
        # Apply symbol or grammar errors
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(sentence, prob_grammar_error),
                prob_symbol_error
            ) for sentence in problem
        ]
        
        # Shuffle the sentences except the first one
        first_sentence = problem[0]
        other_sentences = problem[1:]
        if shuffle:
            random.shuffle(other_sentences)
        problem = [first_sentence] + other_sentences
        
        # Add the question
        problem.append(question)
        
        # Calculate the answer
        answer = answer
        if answer>0:
            break
    
    
    # Return the problem and the answer
    cot = [f"Calculate the total hours spent on 1-hour episodes: {time1} on Monday and Tuesday, {time2} on Thursday, and {time4} on Friday.", f"Calculate the total hours spent on 30-minute episodes on Thursday: {time3} * 0.5.", f"Subtract the total hours spent on 1-hour and 30-minute episodes from {total_hours}.", f"Multiply the remaining hours by 2 to find the number of 30-minute episodes watched on Wednesday, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

