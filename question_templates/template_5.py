from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[3]:


import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    while True:
        stories = []
        irrelative_informations = []

        names = ["Emma", "Ethan", "Lily", "Noah", "Sophia"]
        items = ['shell', 'bead', 'mirro piece']

        name = random.choice(names)

        item = random.choice(items)

        item_number1 = int(random.randrange(10, 20, 2))
        item_number2 = int(random.randrange(60, 81, 2))
        item_number3 = random.randint(2, 10)

        # break down the question into sentences-level.
        story_1 = f"""{name} is making a mosaic with chips of {item}."""
        stories.append(story_1)

        story_2 = f"""It takes {item_number1} {item} chips to make every square inch of the mosaic."""
        stories.append(story_2)

        story_3 = f""" A bag of {item} chips holds {item_number2} chips."""
        stories.append(story_3)

        story_4 = f""" {name} wants his mosaic to be {item_number3} inches tall."""
        stories.append(story_4)
        original_problem = stories.copy()

        # in-topic irrelative information
        item_money = random.randint(1, 3)
        irrelative_info_1 = f"""Every chip costs for ${item_money} for {name} to buy."""
        irrelative_informations.append(irrelative_info_1)

        people_number = random.randint(2, 4)
        # in-topic irrelative information
        irrelative_info_2 = f"""There are {people_number} friends help {name} do it."""
        irrelative_informations.append(irrelative_info_2)

        # out-topic irrelative information
        tempreture = random.randint(25, 30)
        irrelative_info_3 = f"""Today's tempreture is {tempreture}."""
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

        bag_number = random.randint(3, 5)
        question = f""" If {name} has {bag_number} bags of {item} chips, how many inches long can {name} make {name}'s mosaic?"""
        stories.append(question)
        original_problem.append(question)

        ans = (bag_number * item_number2) / (item_number1 * item_number3)
        if ans % 1 == 0:
            break

        # Return the problem and the answer
    cot = [f"{name} has {bag_number} bags of {item} chips, each containing {item_number2} chips.",
           f"The total number of {item} chips is {bag_number} * {item_number2}.",
           f"Each square inch of the mosaic requires {item_number1} {item} chips, and the mosaic is {item_number3} inches tall.",
           f"The number of inches long the mosaic can be is calculated by dividing the total number of chips by the product of {item_number1} and {item_number3}.",
           f"Therefore, the length of the mosaic is ({bag_number} * {item_number2}) / ({item_number1} * {item_number3}), which is {ans} inches."]

    return {"cot": cot, 'problem': stories, 'answer': ans, 'original_problem': original_problem,
            'irrelevant_infos': irrelative_informations}
