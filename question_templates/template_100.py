from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[5]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define teams and steakhouses
    teams = ["basketball team", "soccer team", "volleyball team", "swimming team", "hockey team"]
    steakhouses = ["Steakhouse", "BBQ Grill", "Chophouse", "Meat Lovers' Paradise", "Grill House"]
    team = random.choice(teams)
    steakhouse = random.choice(steakhouses)
    
    # Define player names
    names = ["Alice", "Bob", "Cindy", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]
    player_names = random.sample(names, 5)
    player1_name, player2_name, player3_name, player4_name, player5_name = player_names
    
    # Player 1 steak size in ounces
    player1_steak_ounce_options = [4, 6, 8, 10, 12]
    player1_steak_ounce = random.choice(player1_steak_ounce_options)
    
    # Player 2 beef tips
    player2_beef_tips_number_options = [6, 8, 10, 12]
    player2_beef_tips_number = random.choice(player2_beef_tips_number_options)
    player2_beef_tips_size_options = [1, 2]
    player2_beef_tips_size = random.choice(player2_beef_tips_size_options)
    
    # Player 3 steak size in pounds
    player3_steak_pounds_options = [1, 1.5, 2]
    player3_steak_pounds = random.choice(player3_steak_pounds_options)
    
    # Player 4 and 5 meals
    meals = ["vegetarian meal", "potato salad", "califlower salad", "noodle"]
    player4_meal = random.choice(meals)
    player5_meal = random.choice(meals)
    
    # Construct the problem
    problem = [
        f"The {team} went to the {steakhouse} to eat dinner.",
        f"The first player, {player1_name}, ate a {player1_steak_ounce}-ounce steak.",
        f"The second player, {player2_name}, ate beef tips, containing {player2_beef_tips_number} beef tips, each {player2_beef_tips_size} ounce(s) in size.",
        f"The third player, {player3_name}, ate a {player3_steak_pounds}-pound steak.",
        f"And the fourth and fifth players, {player4_name} and {player5_name}, ordered {player4_meal} and {player5_meal}, respectively."
    ]
    
    question = "In total, how many ounces of meat were consumed by the team?"
    original_problem=problem.copy()
    original_problem.append(question)
    
    # In-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"The {steakhouse} is famous for its desserts.",
        f"The players left a generous tip for the waiter.",
        f"The meal took place on a sunny afternoon.",
        f"The {team} had a game earlier that day and won.",
        f"The {steakhouse} was offering a discount on beverages."
    ]
    
    # Out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"The city festival is starting next week.",
        f"Traffic was heavy on the way to the {steakhouse}.",
        f"It was someone's birthday at the {steakhouse} that night.",
        f"The local newspaper featured an article about the {team}.",
        f"The team's bus driver is {random.choice(names)}."
    ]
    
    # Add irrelevant information based on probability
    irrelevant_infos = []
    if random.random() < prob_irre:
        irrelevant_infos.append(random.choice(in_topic_irrelevant_infos))
    if random.random() < prob_irre:
        irrelevant_infos.append(random.choice(out_topic_irrelevant_infos))
    problem.extend(irrelevant_infos)
    
    # Shuffle the order of sentences, except for the first one
    if shuffle:
        random.shuffle(problem[1:])
    
    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    def meal_contains_meat(meal):
        meat_meals = ["steak", "beef", "chicken", "fish", "pork", "lamb", "turkey", "steak sandwich"]
        for meat in meat_meals:
            if meat.lower() in meal.lower():
                return True
        return False
    
    meat_player1 = player1_steak_ounce
    meat_player2 = player2_beef_tips_number * player2_beef_tips_size
    meat_player3 = player3_steak_pounds * 16
    
    answer = meat_player1 + meat_player2 + meat_player3
    
    # Return the problem and the answer
    cot = [f"The first player ate a steak weighing {player1_steak_ounce} ounces, so {meat_player1} ounces of meat were consumed.", f"The second player ate {player2_beef_tips_number} beef tips, each {player2_beef_tips_size} ounce(s) in size, totaling {meat_player2} ounces of meat.", f"The third player ate a steak weighing {player3_steak_pounds} pounds, which is equivalent to {meat_player3} ounces of meat.", f"In total, the team consumed {meat_player1} + {meat_player2} + {meat_player3} ounces of meat, which equals {answer} ounces."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

