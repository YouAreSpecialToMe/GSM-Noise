from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[54]:


import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    while True:
        # Define possible names
        names = ["Alex", "Taylor", "Jamie", "Jordan", "Morgan", "Casey", "Riley", "Chris", "Sam"]

        # Randomly select a name
        name = random.choice(names)

        # Randomly generate homework-related numbers
        total_problems = random.randint(50, 200)  # Total number of problems
        monday_problems = random.randint(5, 20)  # Problems completed on Monday
        tuesday_multiplier = random.randint(2, 5)  # Times more problems completed on Tuesday
        wednesday_denominator = random.choice(
            [2, 3, 4, 5])  # Denominator for fraction of remaining problems completed on Wednesday
        wednesday_fraction = 1 / wednesday_denominator

        # Ensure total problems are enough
        total_completed_monday_tuesday = monday_problems + tuesday_multiplier * monday_problems
        if total_completed_monday_tuesday >= total_problems:
            total_problems = total_completed_monday_tuesday + random.randint(10, 50)
        remaining_after_tuesday = total_problems - total_completed_monday_tuesday

        # Calculate Wednesday problems
        wednesday_problems = remaining_after_tuesday * wednesday_fraction
        remaining_after_wednesday = remaining_after_tuesday - wednesday_problems

        # Construct the premise content
        problem = [
            f"{name} is way behind on {name}'s math homework.",
            f"{name} has {total_problems} math problems to complete in total.",
            f"{name} completes {monday_problems} problems on Monday night.",
            f"On Tuesday, {name} completes {tuesday_multiplier} times as many problems as {name} did on Monday.",
            f"On Wednesday, {name} completes one-{wednesday_denominator} of the remaining math problems."
        ]

        # Construct the question
        question = f"How many math problems does {name} have left to complete on Thursday?"

        original_problem = problem.copy()
        original_problem.append(question)

        # Add in-topic irrelevant information
        irrelevant_infos = [
            f"{name} plans to finish all the problems by Friday.",
            f"{name}'s friend still have {random.randint(20, 30)} problems.",
            f"The math homework is due in {random.randint(1, 7)} days."
        ]

        # Add out-topic irrelevant information
        irrelevant_infos.append(f"{name} also has {random.randint(1, 3)} science projects due this week.")

        # Add irrelevant information based on probability
        for irrelevant_info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(irrelevant_info)
        # Assume introduce_symbol_error and introduce_grammar_error functions are given
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error),
                prob_symbol_error
            ) for p in problem
        ]

        # Shuffle the order of sentences, except for the first one
        first_sentence = problem[0]
        other_sentences = problem[1:]
        if shuffle:
            random.shuffle(other_sentences)
        problem = [first_sentence] + other_sentences

        # Add the question
        problem.append(question)

        # Calculate the answer
        total_completed = monday_problems + (tuesday_multiplier * monday_problems) + wednesday_problems
        answer = total_problems - total_completed
        if answer % 1 == 0:
            break
        # Return the problem and answer
    cot = [f"{name} completes {monday_problems} problems on Monday.",
           f"On Tuesday, {name} completes {tuesday_multiplier} times as many problems as on Monday, which is {tuesday_multiplier} * {monday_problems}.",
           f"The total number of problems completed by the end of Tuesday is {monday_problems} + {tuesday_multiplier} * {monday_problems}, which is {total_completed_monday_tuesday}.",
           f"The remaining problems after Tuesday are {total_problems} - {total_completed_monday_tuesday}, which is {remaining_after_tuesday}.",
           f"On Wednesday, {name} completes one-{wednesday_denominator} of the remaining problems, which is {remaining_after_tuesday} * {wednesday_fraction}, resulting in {wednesday_problems} problems completed.",
           f"The remaining problems after Wednesday are {remaining_after_tuesday} - {wednesday_problems}, which is {remaining_after_wednesday}.",
           f"The total number of problems completed by Wednesday is {monday_problems} + ({tuesday_multiplier} * {monday_problems}) + {wednesday_problems}, which is {total_completed}.",
           f"Therefore, the number of problems left to complete on Thursday is {total_problems} - {total_completed}, which is {answer}."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
