from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[68]:


import random
import math

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define name lists
    names = ["Jack", "Alice", "Bob", "Cindy", "Diana", "Evelyn", "Frank", "George",
             "Hannah", "Ian", "Jillian", "Kevin", "Laura", "Mason", "Nina", "Oscar",
             "Paula", "Quentin", "Rachel", "Sam", "Tina", "Uma", "Victor", "Wendy",
             "Xander", "Yara", "Zane"]
    
    # Randomly select names for the main person and friends
    main_person = random.choice(names)
    names.remove(main_person)
    friends = random.sample(names, 3)
    friend1, friend2, friend3 = friends
    
    # Randomly generate the variables
    time_per_quarter_values = [10, 15, 20, 25, 30]  # minutes per quarter for main person
    worse_friends_factors = [0.5, 0.6, 0.7]
    better_friend_factors = [1.5, 1.6, 1.7]

    num_worse_friends = 1
    num_better_friends = 1
    num_friends = 2
    quarter_value = 0.25  # Value of each quarter in dollars
    total_play_time=random.randint(120,240)
    
    time_per_quarter_value = random.choice(time_per_quarter_values)
    worse_friends_factor = random.choice(worse_friends_factors)
    better_friend_factor = random.choice(better_friend_factors)

    
    
    
    time_with_worse=(total_play_time/better_friend_factor)*worse_friends_factor
    money_worse=math.ceil((time_with_worse/time_per_quarter_value))*0.25*num_worse_friends
   
    # Construct the premises
    problem = [
        f"A new arcade opens up and {main_person} decides to play with {num_friends} friends.",
        f"{main_person} needs to pay 1 quarter for playing game for {time_per_quarter_value} minutes.",
        f"One of {main_person}'s friends are significantly worse than {main_person} and {main_person} can only play {worse_friends_factor} times as long as {main_person} play alone.",
        f"One of {main_person}'s friends is significantly better so {main_person} can play {better_friend_factor} times as long as {main_person} play alone.",
        f"When the {main_person} plays with better friend, {main_person} can play for {total_play_time} minutes."
    ]
    
    # Construct the question
    question = f"When the {main_person} plays with worse friend, How much money does the {main_person} spend?."
    original_problem=problem.copy()
    original_problem.append(question)
    
    # Construct in-topic and out-topic irrelevant information
    irrelevant_infos = [
        f"The arcade has a total of {random.randint(10, 100)} game machines.",
        f"Each game machine costs {random.randint(5000, 20000)} dollars.",
        f"{main_person} has {random.randint(50, 500)} followers on social media."
    ]
    
    # Add irrelevant information based on probability

    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors
    #Assume functions introduce_symbol_error and introduce_grammar_error are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the sentences except for the first one
    problem_start = problem[0]
    problem_rest = problem[1:]
    if shuffle:
        random.shuffle(problem_rest)
    problem_shuffled = [problem_start] + problem_rest
    
    # Add the question
    problem_shuffled.append(question)
    
    # Calculate the answer
    answer = money_worse
    
    # Return the problem and the answer
    cot = [f"Calculate the time {main_person} can play with the worse friend: ({total_play_time} / {better_friend_factor}) * {worse_friends_factor} = {time_with_worse}.", f"Calculate the money spent when playing with the worse friend: math.ceil({time_with_worse} / {time_per_quarter_value}) * 0.25 * {num_worse_friends} = {money_worse}."]
    
    return {"cot": cot, 'problem': problem_shuffled, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

