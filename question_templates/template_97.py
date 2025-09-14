from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[3]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define lists of names, species, and places
        names1 = ["Gunther", "Harold", "Thaddeus", "Leonard", "Maximus"]
        names2 = ["Arnold", "Benjamin", "Douglas", "Oliver", "Samuel"]
        species1 = ["gorilla", "orangutan", "baboon", "lemur", "mandrill"]
        species2 = ["chimpanzee", "capuchin", "macaque", "gibbon", "squirrel monkey"]
        hiding_places = ["fern branch", "bush", "cave", "tree hollow", "rock pile"]
    
        # Randomly select names, species, and hiding place
        name1 = random.choice(names1)
        name2 = random.choice(names2)
        species1_choice = random.choice(species1)
        species2_choice = random.choice(species2)
        hiding_place = random.choice(hiding_places)
    
        # Randomly generate numeric variables
        initial_bananas = random.randint(30, 100)
        added_bananas1 = random.randint(10, 40)
        stolen_bananas2 = random.randint(5, 20)
        added_bananas3 = random.randint(3, 10)
    
        # Construct the premise content
        problem = [
            f"{name1}, the {species1_choice}, had {initial_bananas} bananas hidden under a {hiding_place}.",
            f"When {name1} wasn't looking, {name2}, the {species2_choice}, stole half of the bananas from the pile.",
            f"The next day, {name1} added another {added_bananas1} bananas to his pile, but later that evening, {name2} stole another {stolen_bananas2} of the bananas.",
            f"On the third day, {name1} added another {added_bananas3} bananas to his pile and began counting bananas."
        ]
        original_problem=problem.copy()
    
        # Construct irrelevant information
        irrelevant_infos = [
            f"{name1} lives in a troop with several other {species1_choice}s.",
            f"The {species2_choice} often interacts with {name1}'s group.",
            f"{name2} had been eyeing the bananas for days.",
            f"The {hiding_place} was located near a river.",
            f"{name1} enjoys painting in his free time.",
            f"The weather was unusually warm that week.",
            f"There was a meteor shower visible in the night sky."
        ]
    
        # Add irrelevant information based on probability
        for info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(info)
    
        # Add symbol or grammar errors
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error),
                prob_symbol_error
            ) for p in problem
        ]
    
        # Shuffle the order of sentences except for the first one
        if len(problem) > 1:
            first_sentence = problem[0]
            other_sentences = problem[1:]
            if shuffle:
                random.shuffle(other_sentences)
            problem = [first_sentence] + other_sentences
    
        # Add the question
        question = f"How many bananas did {name1} find were in the pile?"
        
        original_problem.append(question)
        problem.append(question)
    
        # Calculate the answer
        bananas_after_theft1 = initial_bananas / 2
        bananas_after_addition1 = bananas_after_theft1 + added_bananas1
        bananas_after_theft2 = bananas_after_addition1 - stolen_bananas2
        final_bananas = bananas_after_theft2 + added_bananas3
        answer = final_bananas
        if answer%1==0:
            break

    # Return the problem and answer
    cot = [f"{name2} stole half of the {initial_bananas} bananas, leaving {bananas_after_theft1} bananas.", f"The next day, {name1} added {added_bananas1} bananas, resulting in {bananas_after_addition1} bananas.", f"Later, {name2} stole {stolen_bananas2} bananas, leaving {bananas_after_theft2} bananas.", f"On the third day, {name1} added {added_bananas3} bananas, resulting in a final count of {final_bananas} bananas."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

