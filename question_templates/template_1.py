from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[6]:


import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    stories = []
    irrelative_informations = []

    names = ["James", "Emily", "John", "David", "William"]
    items = ['CD', 'board game', 'book']

    name = random.choice(names)

    item = random.choice(items)

    first_item_numbers = random.randint(5, 20)

    second_item_numbers = random.randint(2, 4)

    third_item_numbers = random.randint(4, 6)

    fourth_item_numbers = random.randint(7, 8)

    fifth_item_numbers = random.randint(1, 10)

    # break down the question into sentences-level.
    story_1 = f"""{name} loves {item}."""
    stories.append(story_1)

    story_2 = f"""{name}'s  parents give {name} {first_item_numbers} {item}s for {name}'s birthday."""
    stories.append(story_2)

    story_3 = f"""{name} saves up enough money to buy {second_item_numbers} {item}s per month for a year, and then the following year {name} starts buying {third_item_numbers} {item}s a month."""
    stories.append(story_3)

    story_4 = f""" For the third year {name} buys {fourth_item_numbers} {item}s a month as {name} has a new part-time job that makes him more money."""
    stories.append(story_4)

    story_5 = f""" {name} also gets {fifth_item_numbers} {item}s for Christmas every year"""
    stories.append(story_5)

    original_problem = stories.copy()

    # in-topic irrelative information
    item_money = random.randint(20, 100)
    irrelative_info_1 = f"""Every {item} costs for ${item_money} for {name} to buy."""
    irrelative_informations.append(irrelative_info_1)

    part_time_salary = random.randint(20, 40)
    # in-topic irrelative information
    irrelative_info_2 = f"""The part-time job salary is ${part_time_salary} per hour."""
    irrelative_informations.append(irrelative_info_2)

    # out-topic irrelative information
    ir_money = random.randint(1000, 2000)
    irrelative_info_3 = f"""{name}'s parent give {name} ${ir_money} per year as the pocket money."""
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

    question = f"""How many {item} does {name} have after 3 years?"""
    stories.append(question)
    original_problem.append(question)

    ans = first_item_numbers + second_item_numbers * 12 + third_item_numbers * 12 + fourth_item_numbers * 12 + fifth_item_numbers * 3

    # Return the problem and the answer
    cot = [f"{name} starts with {first_item_numbers} {item}s from his birthday.",
           f"He buys {second_item_numbers} {item}s per month for the first year, which totals {second_item_numbers} * 12.",
           f"In the second year, he buys {third_item_numbers} {item}s per month, totaling {third_item_numbers} * 12.",
           f"In the third year, he buys {fourth_item_numbers} {item}s per month, totaling {fourth_item_numbers} * 12.",
           f"He also receives {fifth_item_numbers} {item}s for Christmas each year, totaling {fifth_item_numbers} * 3.",
           f"Adding all these together gives the total number of {item}s: {first_item_numbers} + {second_item_numbers} * 12 + {third_item_numbers} * 12 + {fourth_item_numbers} * 12 + {fifth_item_numbers} * 3, which equals {ans}."]

    return {"cot": cot, 'problem': stories, 'answer': ans, 'original_problem': original_problem,
            'irrelevant_infos': irrelative_informations}
