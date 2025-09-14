from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[27]:


import random
import math
from datetime import datetime, timedelta


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    stories = []
    irrelative_informations = []

    while True:

        names = ["Alice", "Ethan", "Lily", "James", "Sophia"]

        name = random.choice(names)

        start_date = datetime.now() + timedelta(days=random.randint(1, 365))
        # Generate a random end date that is after the start_date
        end_date = start_date + timedelta(days=random.randint(120, 150))
        date1 = start_date.strftime("%Y-%m-%d")
        date2 = end_date.strftime("%Y-%m-%d")
        diff_days = (end_date - start_date).days

        num1 = random.randint(20, 40)
        num3 = random.randint(3400, 3600)
        ans1 = num1 * num3 / diff_days

        if ans1 > 0:
            # break down the question into sentences-level.
            story_1 = f"""For a New Year's resolution, {name} wants to lose {num1} lbs. by {name}'s birthday, which is {date2}."""
            stories.append(story_1)

            story_2 = f"""Today is {date1}."""
            stories.append(story_2)

            original_problem = stories.copy()

            # in-topic irrelative information
            num5 = random.randint(130, 160)
            irrelative_info_1 = f"""Now, {name} is {num5} lbs"""
            irrelative_informations.append(irrelative_info_1)

            num7 = random.randint(2, 4)
            irrelative_info_2 = f"""{name} eats {num7} apples a week"""
            irrelative_informations.append(irrelative_info_2)

            # out-topic irrelative information

            num6 = random.randint(20, 80)
            irrelative_info_3 = f"""{name} is considering joining a local gym, but the membership costs ${num6} a month."""
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

            question = f"""If {name} needs to burn {num3} calories to lose a pound, how much of a calorie deficit (net amount of calories burned vs. calories consumed) does {name} need each day to reach {name}'s goal?"""
            stories.append(question)
            original_problem.append(question)
            ans = ans1
            ans = round(ans, 2)

            break
        # Return the problem and the answer
    cot = [f"The number of days between {date1} and {date2} is calculated as {diff_days}.", f"To lose {num1} lbs, {name} needs to burn {num3} calories per pound. Therefore, the total calories to burn is {num1} * {num3}.", f"The daily calorie deficit needed is the total calories to burn divided by the number of days, which is {num1} * {num3} / {diff_days}, resulting in {ans1}."]
    
    return {"cot": cot, 'problem': stories, 'answer': ans,'original_problem':original_problem,'irrelevant_infos':irrelative_informations}          

