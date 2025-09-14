from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define names and animals
    names = ["Wendi", "Alice", "John", "Sophia", "Michael", "Emma", "Olivia"]
    animals = ["chickens", "hens", "ducks", "geese", "turkeys", "quails"]
    feed_units = ["cups", "grams"]

    # Randomly select variables
    name = random.choice(names)
    animal = random.choice(animals)
    feed_unit = random.choice(feed_units)

    # Randomly generate numerical values
    feed_per_animal = random.randint(1, 5)  # per animal per day
    meals_per_day = 3  # Fixed at 3 meals per day
    flock_size = random.randint(10, 30)
    total_daily_feed = feed_per_animal * flock_size

    # Morning and afternoon feeds
    morning_feed = random.randint(1, total_daily_feed // 2)
    afternoon_feed = random.randint(1, (total_daily_feed - morning_feed) // 2)
    final_meal_feed = total_daily_feed - morning_feed - afternoon_feed

    # Additional irrelevant numerical values
    extra_feed = random.randint(5, 15)
    extra_animals = random.randint(5, 20)

    # Construct the problem statements with variable names
    problem = [
        f"Every day, {name} feeds each of her {animal} {feed_per_animal} {feed_unit} of feed to help keep them healthy.",
        f"She gives the {animal} their feed in {meals_per_day} separate meals.",
        f"In the morning, she gives her flock of {animal} {morning_feed} {feed_unit} of feed.",
        f"In the afternoon, she gives her {animal} another {afternoon_feed} {feed_unit} of feed.",
        f"How many {feed_unit} of feed does she need to give her {animal} in the final meal of the day if the size of {name}'s flock is {flock_size} {animal}?"
    ]
    original_problem=problem.copy()
    # Construct in-topic irrelevant information
    irrelevant_infos = [
        f"{name} bought an additional {extra_feed} {feed_unit} of feed yesterday.",
        f"{name} plans to increase her flock by {extra_animals} {animal} next month."
    ]

    # Construct out-topic irrelevant information
    irrelevant_infos.append(f"{name} also owns a farm with {random.randint(1, 10)} cows and {random.randint(1, 10)} sheep.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.insert(random.randint(1, len(problem) - 1), irrelevant_info)

    # Add symbol or grammar errors. Assume the functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in problem
    ]

    # Shuffle the problem sentences (except the last one, which is the question)
    question = problem.pop()
    if shuffle:
        random.shuffle(problem)
    problem.append(question)

    # Calculate the answer
    total_feed_needed = feed_per_animal * flock_size
    answer = total_feed_needed - morning_feed - afternoon_feed

    # Return the problem and the answer
    cot = [f"Calculate the total daily feed needed by multiplying {feed_per_animal} by {flock_size}, which gives {total_daily_feed}.", f"Subtract the {morning_feed} and {afternoon_feed} from {total_daily_feed} to find the feed needed for the final meal, which is {final_meal_feed}.", f"The final answer is the feed needed for the final meal, which is {final_meal_feed}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

