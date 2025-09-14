from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[2]:


import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    stories = []
    irrelative_informations = []

    names = ["David", "Mike", "John", "Sarah", "Olivia"]
    items = ['orange', 'onion', 'apple']

    name = random.choice(names)

    item = random.choice(items)

    item_number = random.randint(30, 100)

    time1 = round(random.uniform(1, 3), 1)
    time2 = random.randint(4, 10)

    # break down the question into sentences-level.
    story_1 = f"""{name} is peeling and cutting {item}s in preparation for making {item} salad for {name}'s big family reunion barbecue."""
    stories.append(story_1)

    story_2 = f""" It's a big event, so {name} has {item_number} {item}s to get through."""
    stories.append(story_2)

    story_3 = f"""The {item}s are roughly the same size, so it takes about the same amount of time to peel and cut each one."""
    stories.append(story_3)

    story_4 = f""" It takes {name} about {time1} minutes to peel a {item}, but only about {time2} seconds to cut it up."""
    stories.append(story_4)
    original_problem = stories.copy()

    # in-topic irrelative information
    item_money = round(random.uniform(1, 2), 1)
    irrelative_info_1 = f"""Every {item} costs for ${item_money} for {name} to buy."""
    irrelative_informations.append(irrelative_info_1)

    family_number = random.randint(6, 12)
    # in-topic irrelative information
    irrelative_info_2 = f"""There are {family_number} in {name}'s family."""
    irrelative_informations.append(irrelative_info_2)

    # out-topic irrelative information
    people_number2 = random.randint(1, 4)
    irrelative_info_3 = f"""{people_number2} in {name}'s family do not like {item}s"""
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

    question = f""" How long will it take {name} to finish prepping the {item}s?"""
    stories.append(question)
    original_problem.append(question)

    ans = item_number * (time1 * 60 + time2) / 60
    # Return the problem and the answer
    cot = [
        f"To find out how long it will take {name} to finish prepping the {item}s, we first calculate the time it takes to peel and cut one {item}.",
        f"It takes {time1} minutes to peel a {item}, which is equivalent to {time1} * 60 seconds.",
        f"Adding the time to cut the {item}, which is {time2} seconds, the total time to prep one {item} is {time1} * 60 + {time2} seconds.",
        f"Since there are {item_number} {item}s, the total time in seconds is {item_number} * ({time1} * 60 + {time2}).",
        f"Convert the total time from seconds to minutes by dividing by 60, resulting in {ans} minutes."]

    return {"cot": cot, 'problem': stories, 'answer': ans, 'original_problem': original_problem,
            'irrelevant_infos': irrelative_informations}
