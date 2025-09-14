from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[2]:


import random
from math import floor  # Import only the floor function


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    stories = []
    irrelative_informations = []

    items = ['chair', 'stool', 'seat']
    places = ['cinema', 'stadium', 'concert']
    persons1 = ['teacher', 'worker', 'manager']
    persons2 = ['professor', 'doctor', 'athlete']

    while True:
        place = random.choice(places)
        item = random.choice(items)

        person1 = random.choice(persons1)
        person2 = random.choice(persons2)

        percent_one = random.randint(10, 30)

        percent_two = random.randint(10, 30)

        row_number = random.randint(5, 20)
        item_number = random.randint(20, 40)
        total_number = row_number * item_number

        # Check if the occupation calculations yield integers
        occupied_by_person1 = percent_one * 0.01 * total_number
        remaining_after_person1 = total_number - occupied_by_person1
        occupied_by_person2 = percent_two * 0.01 * remaining_after_person1

        if occupied_by_person1.is_integer() and occupied_by_person2.is_integer():

            # break down the question into sentences-level.
            story_1 = f"""The {place} has {row_number} rows of seats"""
            stories.append(story_1)

            story_2 = f"""There are {item_number} {item}s in each row."""
            stories.append(story_2)

            story_3 = f"""  {percent_one}% of the {item}s were occupied by the {person1}s. {percent_two}% of the remaining {item}s were occupied by the {person2}s and the rest were occupied by the students."""
            stories.append(story_3)
            original_problem = stories.copy()

            # in-topic irrelative information
            percent_three = random.randint(10, 40)
            irrelative_info_1 = f"""{percent_three}% {item}s are blue. The rest is red."""
            irrelative_informations.append(irrelative_info_1)

            place_number = random.randint(2, 5)
            # in-topic irrelative information
            irrelative_info_2 = f"""There are {place_number} {item}s in the city"""
            irrelative_informations.append(irrelative_info_2)

            # out-topic irrelative information
            percent_four = random.randint(50, 70)
            irrelative_info_3 = f"""{percent_four}% students wear the uniform."""
            irrelative_informations.append(irrelative_info_3)

            for irrelative_information in irrelative_informations:
                if random.random() < prob_irre:
                    stories.append(irrelative_information)

            if shuffle:
                random.shuffle(stories)

            stories = [
                introduce_symbol_error(
                    introduce_grammar_error(p, prob_grammar_error),
                    prob_symbol_error
                ) for p in stories
            ]

            question = f""" How many students were there in the {place}? """
            stories.append(question)
            original_problem.append(question)

            ans = int((row_number * item_number * (1 - (percent_one) * 0.01)) * (1 - (percent_two) * 0.01))

            break
        # Return the problem and the answer
    cot = [
        f"Calculate the total number of seats by multiplying {row_number} by {item_number}, which gives {total_number}.",
        f"Calculate the number of seats occupied by administrators as {percent_one}% of {total_number}, which is {occupied_by_person1}.",
        f"Subtract the seats occupied by administrators from the total number of seats to get the remaining seats, which is {remaining_after_person1}.",
        f"Calculate the number of seats occupied by parents as {percent_two}% of the remaining seats, which is {occupied_by_person2}.",
        f"The number of students is the remaining seats after subtracting those occupied by parents, which is {ans}."]

    return {"cot": cot, 'problem': stories, 'answer': ans, 'original_problem': original_problem,
            'irrelevant_infos': irrelative_informations}
