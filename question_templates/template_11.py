from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[3]:


import random
import math


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    stories = []
    irrelative_informations = []

    while True:

        items = ["Garden", "Plant bed", "Landscaped area"]
        names = ["Lily", "Oscar", "Amelia", "Jack", "Grace"]

        name = random.choice(names)
        item = random.choice(items)

        number1 = random.randint(80, 150)
        number2 = random.randint(8, 12)
        number3 = round(random.uniform(0.7, 1.5), 2)
        number4 = random.randint(10, 20)
        price = random.randint(2, 10)

        ans1 = math.floor(number1 / (number2 / 12 + number3)) - number4
        if ans1 > 0:

            # break down the question into sentences-level.
            story_1 = f"""{name} has a {item} that is {number1} feet long."""
            stories.append(story_1)

            story_2 = f"""{name} wants to fill {name}'s {item} with plants."""
            stories.append(story_2)

            story_3 = f"""{name}'s flowers grow {number2} inches wide, so {name} needs to leave {number3} feet between every plant."""
            stories.append(story_3)

            story_4 = f"""{name} already owns {number4} flowers."""
            stories.append(story_4)

            story_5 = f"""Each plant costs ${price} at the store."""
            stories.append(story_5)

            original_problem = stories.copy()

            # in-topic irrelative information
            money = random.randint(300, 400)
            irrelative_info_1 = f"""{name}'s parents give {name} ${money} to buy flowers."""
            irrelative_informations.append(irrelative_info_1)

            number5 = random.randint(10, 20)
            irrelative_info_2 = f"""{name} also buy {number5} pens from another store."""
            irrelative_informations.append(irrelative_info_2)

            # out-topic irrelative information
            tree_numbers = random.randint(10, 20)
            irrelative_info_3 = f"""There are total {tree_numbers} trees around the {item}."""
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

            question = f""" How much money will {name} spend at the store to fill up {name}'s {item}?"""
            stories.append(question)
            original_problem.append(question)
            ans = math.floor((number1 / (number2 / 12 + number3) - number4)) * price
            ans = int(ans)

            break

        # Return the problem and the answer
    cot = [
        f"Calculate the number of additional plants needed by dividing the length of the {item} by the sum of the width of a plant in feet and the space between plants, then subtracting the number of plants {name} already owns. This is calculated as math.floor({number1} / ({number2} / 12 + {number3})) - {number4}, which gives {ans1}.",
        f"Multiply the number of additional plants needed by the cost per plant to find the total cost. This is calculated as {ans1} * {price}, which gives {ans}."]

    return {"cot": cot, 'problem': stories, 'answer': ans, 'original_problem': original_problem,
            'irrelevant_infos': irrelative_informations}
