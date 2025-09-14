from grammar_error import introduce_grammar_error, introduce_symbol_error
import random
import math


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    stories = []
    irrelative_informations = []

    while True:

        names1 = ["Jordan", "Jason", "Jeffrey", "Ethan", "Liam"]
        names2 = ["Mason", "Noah", "Aiden", "Oliver", "Henry"]
        names3 = ["Jack", "Leo", "Samuel", "Isaac", "Benjamin"]

        items = ["footballs", "soccer balls", "tennis balls", "volleyballs", "dodgeballs"]

        name1 = random.choice(names1)
        name2 = random.choice(names2)
        name3 = random.choice(names3)
        item = random.choice(items)

        num1 = random.randint(2, 4)
        num2 = random.randint(2, 4)
        num4 = random.randint(2, 4)

        ans1 = num4 + num4 * num1 + num4 / num2

        if ans1 > 0 and ans1 % 1 == 0:

            # break down the question into sentences-level.
            story_1 = f"""Coach brought one bag filled with {item} to practice and dumped them all out onto the gym floor before practice began."""
            stories.append(story_1)

            story_2 = f"""After the practice time was over, he asked {name1}, {name2}, and {name3} to pick up the balls and carry them over to the bag."""
            stories.append(story_2)

            story_3 = f"""The three boys picked up and carried all of the balls in one trip."""
            stories.append(story_3)

            story_4 = f"""{name1} carried {num1} times as many balls as {name2}."""
            stories.append(story_4)

            story_5 = f"""{name2} carried {num2} times as many balls as {name3}."""
            stories.append(story_5)
            original_problem = stories.copy()

            # in-topic irrelative information
            num9 = random.randint(4, 6)
            irrelative_info_3 = f"""Each ball weights {num9} lbs"""
            irrelative_informations.append(irrelative_info_3)

            num8 = random.randint(20, 30)
            irrelative_info_3 = f"""There are {num8} people in the team."""
            irrelative_informations.append(irrelative_info_3)

            # out-topic irrelative information
            num7 = random.randint(2, 4)
            irrelative_info_1 = f"""The gym had just been cleaned by {num7} people."""
            irrelative_informations.append(irrelative_info_1)

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

            question = f"""If {name2} had picked up and carried {num4} balls, what is the total number of balls that the coach brought to practice?"""
            stories.append(question)
            original_problem.append(question)
            ans = ans1
            ans = int(ans)
            break
        # Return the problem and the answer
    cot = [f"{name2} carried {num4} balls.",
           f"{name1} carried {num1} times as many balls as {name2}, which is {num4} * {num1}.",
           f"{name3} carried {num2} times fewer balls than {name2}, which is {num4} / {num2}.",
           f"The total number of balls is {num4} + ({num4} * {num1}) + ({num4} / {num2}), which is {ans1}."]

    return {"cot": cot, 'problem': stories, 'answer': ans, 'original_problem': original_problem,
            'irrelevant_infos': irrelative_informations}
