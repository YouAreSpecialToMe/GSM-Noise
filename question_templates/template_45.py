from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[6]:


import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    while True:
        # Define names
        names = ["Alice", "Beth", "Cindy", "Diana", "Eva", "Frank", "George", "Hannah", "Ivan", "Judy"]
        name1 = random.choice(names)
        names.remove(name1)
        name2 = random.choice(names)

        # Randomly generate tank capacity
        tank_capacity = random.choice([10000, 15000, 18000, 20000, 25000])

        # Random fractions for the work done
        # Wanda's fraction on first day
        wanda_fraction_first_num = random.randint(1, 3)
        wanda_fraction_first_den = random.randint(wanda_fraction_first_num + 1, 5)
        wanda_fraction_first = wanda_fraction_first_num / wanda_fraction_first_den

        # Ms. B's fraction of Wanda's work on first day
        msb_fraction_of_wanda_first_num = random.randint(1, 3)
        msb_fraction_of_wanda_first_den = random.randint(msb_fraction_of_wanda_first_num + 1, 5)
        msb_fraction_of_wanda_first = msb_fraction_of_wanda_first_num / msb_fraction_of_wanda_first_den

        # Wanda's fraction on second day
        wanda_fraction_second_num = random.randint(1, 3)
        wanda_fraction_second_den = random.randint(wanda_fraction_second_num + 1, 5)
        wanda_fraction_second = wanda_fraction_second_num / wanda_fraction_second_den

        # Ms. B's fraction on second day
        msb_fraction_second_num = random.randint(1, 3)
        msb_fraction_second_den = random.randint(msb_fraction_second_num + 1, 5)
        msb_fraction_second = msb_fraction_second_num / msb_fraction_second_den

        # Problem premises
        problem = [
            f"A tank has a capacity of {tank_capacity} gallons.",
            f"{name1} and {name2} decided to pump water from a pond to fill the tank in two days.",
            f"On the first day, working in shifts, {name1} filled {wanda_fraction_first_num}/{wanda_fraction_first_den} of the tank's capacity with water, and {name2} pumped {msb_fraction_of_wanda_first_num}/{msb_fraction_of_wanda_first_den} as much water as {name1} pumped into the tank that day.",
            f"On the second day, {name1} pumped {wanda_fraction_second_num}/{wanda_fraction_second_den} of the amount of water {name1} pumped on the previous day, while {name2} only pumped {msb_fraction_second_num}/{msb_fraction_second_den} of the number of gallons {name2} pumped on the first day."
        ]

        # Question
        question = "How many gallons of water are remaining for the tank to be full?"
        original_problem = problem.copy()
        original_problem.append(question)

        # In-topic irrelevant information
        irrelevant_infos = [
            f"{name1} loves watching sunsets by the pond.",
            f"{name2} brought sandwiches for their lunch break."
        ]

        # Out-topic irrelevant information
        irrelevant_out_topic = [
            f"{name1} won a painting competition last week.",
            f"{name2} is planning a trip to the mountains."
        ]

        # Add irrelevant information based on probability
        for info in irrelevant_infos + irrelevant_out_topic:
            if random.random() < prob_irre:
                problem.append(info)

        # Replace variables in the problem
        # variables = {
        #     'tank_capacity': tank_capacity,
        #     'name1': name1,
        #     'name2': name2,
        #     'wanda_fraction_first_num': wanda_fraction_first_num,
        #     'wanda_fraction_first_den': wanda_fraction_first_den,
        #     'msb_fraction_of_wanda_first_num': msb_fraction_of_wanda_first_num,
        #     'msb_fraction_of_wanda_first_den': msb_fraction_of_wanda_first_den,
        #     'wanda_fraction_second_num': wanda_fraction_second_num,
        #     'wanda_fraction_second_den': wanda_fraction_second_den,
        #     'msb_fraction_second_num': msb_fraction_second_num,
        #     'msb_fraction_second_den': msb_fraction_second_den
        # }
        # problem = [sentence.format(**variables) for sentence in problem]

        # Add symbol or grammar errors
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(sentence, prob_grammar_error),
                prob_symbol_error
            ) for sentence in problem
        ]

        # Shuffle sentences except the first one
        first_sentence = problem[0]
        other_sentences = problem[1:]
        if shuffle:
            random.shuffle(other_sentences)
        problem = [first_sentence] + other_sentences
        problem.append(question)

        # Calculations
        wanda_first_day = wanda_fraction_first * tank_capacity
        msb_first_day = msb_fraction_of_wanda_first * wanda_first_day
        wanda_second_day = wanda_fraction_second * wanda_first_day
        msb_second_day = msb_fraction_second * msb_first_day
        total_pumped = wanda_first_day + msb_first_day + wanda_second_day + msb_second_day
        answer = tank_capacity - total_pumped

        if answer > 0 and answer % 1 == 0:
            break

    cot = [
        f"On the first day, Wanda filled {wanda_fraction_first} of the tank's capacity, which is {wanda_first_day} gallons.",
        f"Ms. B pumped {msb_fraction_of_wanda_first} of the amount Wanda pumped on the first day, which is {msb_first_day} gallons.",
        f"On the second day, Wanda pumped {wanda_fraction_second} of the amount she pumped on the first day, which is {wanda_second_day} gallons.",
        f"Ms. B pumped {msb_fraction_second} of the amount she pumped on the first day, which is {msb_second_day} gallons.",
        f"The total amount of water pumped into the tank is {wanda_first_day} + {msb_first_day} + {wanda_second_day} + {msb_second_day}, which is {total_pumped} gallons.",
        f"The remaining amount of water needed to fill the tank is {tank_capacity} - {total_pumped}, which is {answer} gallons."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
