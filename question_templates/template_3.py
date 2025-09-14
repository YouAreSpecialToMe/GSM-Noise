from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[4]:


import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    while True:
        stories = []
        irrelative_informations = []

        names = ["Joseph", "Andrew", "Grace", "Jessica", "David"]
        items = ['video game', 'hat', 'pen']

        name = random.choice(names)

        item = random.choice(items)

        item_number1 = random.randint(10, 30)
        item_number2 = random.randint(1, 10)

        discount = random.randint(30, 80)
        price1 = random.randint(10, 20)
        price2 = random.randint(20, 50)

        # break down the question into sentences-level.
        story_1 = f"""{name} gets {item_number1} new {item}s."""
        stories.append(story_1)

        story_2 = f""" Each {item} cost ${price1}."""
        stories.append(story_2)

        story_3 = f""" {name} gets them for {discount}% off."""
        stories.append(story_3)

        story_4 = f"""  {name} decides {name} doesn't like {item_number2} of them and sells them for {price2}."""
        stories.append(story_4)
        original_problem = stories.copy()

        # in-topic irrelative information
        ir_money = random.randint(1000, 2000)
        irrelative_info_1 = f"""At beginning, {name} has ${ir_money}."""
        irrelative_informations.append(irrelative_info_1)

        item_number4 = random.randint(1, 5)
        # in-topic irrelative information
        irrelative_info_2 = f"""{name} likes {item_number4} {item}s very much."""
        irrelative_informations.append(irrelative_info_2)

        # out-topic irrelative information

        item_number3 = random.randint(1, 5)
        irrelative_info_3 = f"""{name} gives {item_number3} {item}s to {name}'s friend."""
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

        question = f""" How much money was {name} out?"""
        stories.append(question)
        original_problem.append(question)

        ans = item_number1 * price1 * (100 - discount) * 0.01 - price2
        if ans > 0:
            break

        # Return the problem and the answer
    cot = [
        f"{name} buys {item_number1} {item}s, each costing {price1}. The total cost before discount is {item_number1} * {price1}.",
        f"The discount is {discount}%, so the discounted cost is {item_number1} * {price1} * (100 - {discount}) * 0.01.",
        f"{name} sells {item_number2} {item}s for {price2}.",
        f"The total money {name} is out is the discounted cost minus the selling price, which is {ans}."]

    return {"cot": cot, 'problem': stories, 'answer': ans, 'original_problem': original_problem,
            'irrelevant_infos': irrelative_informations}
