from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[29]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Step 1: Define lists of dog breeds
    small_breeds = ["Chihuahua", "Pomeranian", "Maltese", "Shih Tzu", "Toy Poodle", "Yorkshire Terrier", "Papillon", "Affenpinscher", "Havanese"]
    medium_breeds = ["Beagle", "French Bulldog", "Bulldog", "Cocker Spaniel", "Corgi", "Dachshund", "Boston Terrier", "Jack Russell Terrier"]
    giant_breeds = ["Great Dane", "Newfoundland", "Saint Bernard", "English Mastiff", "Bernese Mountain Dog", "Leonberger"]
    
    # Step 2: Randomly select breeds
    first_dog_breed = random.choice(small_breeds)
    second_dog_breed = random.choice(medium_breeds)
    
    # Ensure third dog breed is different from the first
    third_dog_breed = random.choice(small_breeds)
    while third_dog_breed == first_dog_breed:
        third_dog_breed = random.choice(small_breeds)
        
    fourth_dog_breed = random.choice(giant_breeds)
    
    # Step 3: Assign weights with defined relationships
    # Randomly select first dog's weight
    first_dog_weight = random.randint(5, 15)  # in pounds
    
    # Second dog's weight is multiplier * first dog's weight
    second_dog_multiplier = random.choice([2, 3, 4])
    second_dog_weight = second_dog_multiplier * first_dog_weight
    
    # Third dog's weight is fraction of second dog's weight
    # To ensure integer weights, choose multipliers that result in integer weights
    # Possible multipliers (numerator, denominator)
    third_multipliers = []
    for denominator in [2, 4, 5]:
        for numerator in range(1, denominator):
            if (second_dog_weight * numerator) % denominator == 0:
                third_multipliers.append((numerator, denominator))
    if not third_multipliers:
        # If no suitable multipliers, default to 1/2
        third_dog_multiplier_num = 1
        third_dog_multiplier_den = 2
    else:
        third_dog_multiplier_num, third_dog_multiplier_den = random.choice(third_multipliers)
    third_dog_weight = (second_dog_weight * third_dog_multiplier_num) // third_dog_multiplier_den
    
    # Fourth dog's weight is multiple of third dog's weight
    fourth_dog_multiplier = random.choice([10, 11, 20, 22, 44])
    fourth_dog_weight = fourth_dog_multiplier * third_dog_weight
    
    # Build the problem sentences
    problem = [
        f"Four dogs sat in a line within the veterinarian's waiting room.",
        f"The first dog was the {first_dog_breed}, who weighed only {first_dog_weight} pounds.",
        f"Next to {first_dog_breed} sat a {second_dog_breed}, who weighed {second_dog_multiplier} times as much as the {first_dog_breed}.",
        f"Next to the {second_dog_breed} sat a {third_dog_breed}, who weighed {third_dog_multiplier_num}/{third_dog_multiplier_den} as much as the {second_dog_breed}.",
        f"And at the end of the line sat a {fourth_dog_breed}, who weighed {fourth_dog_multiplier} times the weight of the {third_dog_breed}.",
    ]
    
    question = f"How much did the {fourth_dog_breed} weigh, in pounds?"
    original_problem=problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The {first_dog_breed} loves to play fetch.",
        f"The {second_dog_breed} had a shiny collar.",
        f"The clinic has a waiting time of around 30 minutes.",
    ]
    
    # Add out-topic irrelevant information
    out_topic_irrelevant_info = f"There was a cat sleeping on a chair in the waiting room."
    irrelevant_infos.append(out_topic_irrelevant_info)
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors. Assume the functions introduce_symbol_error and introduce_grammar_error are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    remaining_sentences = problem[1:]
    if shuffle:
        random.shuffle(remaining_sentences)
    problem = [first_sentence] + remaining_sentences
    
    # Add the question at the end
    problem.append(question)
    
    # Calculate the answer
    answer = fourth_dog_weight  # Final answer in pounds
    
    # Return problem and answer as a dictionary
    cot = [f"The second dog weighs {second_dog_multiplier} times as much as the first dog, so its weight is {second_dog_multiplier} * {first_dog_weight}, which is {second_dog_weight}.", f"The third dog weighs {third_dog_multiplier_num}/{third_dog_multiplier_den} as much as the second dog, so its weight is ({second_dog_weight} * {third_dog_multiplier_num}) // {third_dog_multiplier_den}, which is {third_dog_weight}.", f"The fourth dog weighs {fourth_dog_multiplier} times the weight of the third dog, so its weight is {fourth_dog_multiplier} * {third_dog_weight}, which is {fourth_dog_weight}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

