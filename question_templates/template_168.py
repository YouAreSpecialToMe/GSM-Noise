from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible names and tasks
    names = ["Amalia", "Megan", "Dior", "Sophie", "Liam", "Noah", "Emma", "Olivia", "Ethan", "Ava"]
    tasks = ["mow the lawn", "walk the dog", "do laundry", "wash the dishes", "clean the garage", "cook dinner",
             "vacuum the house", "water the plants"]

    # Randomly select names and tasks, ensuring they are unique
    name1, name2, name3 = random.sample(names, 3)
    task1, task2, task3 = random.sample(tasks, 3)

    # Set base time for first person's task
    time1 = random.randint(2, 10)  # Time for the first person
    time2 = random.randint(time1, time1 + 15)  # Second person took 2 hours longer than the first person
    time3 = random.randint(time1, time1 + 12)  # Third person took well over 4 hours longer than the first person

    time2_minus_time1 = time2 - time1
    time3_minus_time1 = time3 - time1

    # Construct the premises with variable placeholders
    problem = [
        f"{name1}, {name2}, and {name3} divided the home chores so that each person had something to do while the others were working.",
        f"{name1}'s work was to {task1}, which took {name1} {time1} hours.",
        f"{name2} had to {task2} and this took {name2} {time2_minus_time1} hours longer than {name1} to complete {name2}'s chore.",
        f"{name3}'s work was to {task3} and {name3} took well over {time3_minus_time1} hours longer than the time {name1} took to {task1}."
    ]

    # Construct the question
    question = "Calculate the total time they all took to do their chores altogether."

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelvant_names = names.copy()
    irrelvant_names.remove(name1)
    irrelvant_names.remove(name2)
    irrelvant_names.remove(name3)
    irrelvant_name1, irrelvant_name2, irrelvant_name3 = random.sample(irrelvant_names, 3)
    irrelvant_tasks = tasks.copy()
    irrelvant_tasks.remove(task1)
    irrelvant_tasks.remove(task2)
    irrelvant_tasks.remove(task3)
    irrelvant_task1, irrelvant_task2, irrelvant_task3 = random.sample(irrelvant_tasks, 3)
    irrelevant_infos = [
        f"{irrelvant_name1}'s took {random.randint(1, 10)} hours to {irrelvant_task1}.",
        f"{irrelvant_name2} had to {irrelvant_task2} and this took {irrelvant_name2} {random.randint(1, 10)} hours longer than {irrelvant_name1} to complete {irrelvant_name2}'s chore.",
        f"{irrelvant_name3}'s work was to {irrelvant_task3} and {irrelvant_name3} took well over {random.randint(1, 10)} hours longer than the time {irrelvant_name1} took to {task1}."
    ]

    # Add out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{name1} enjoys playing chess with friends.",
    ]

    # Combine all irrelevant information
    all_irrelevant_infos = irrelevant_infos + out_topic_irrelevant_infos

    # Add irrelevant information based on probability
    for irrelevant_info in all_irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors; assume functions are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the sentences except the first one
    first_sentence = problem[0]
    middle_sentences = problem[1:]
    if shuffle:
        random.shuffle(middle_sentences)
    problem = [first_sentence] + middle_sentences + [question]

    # Calculate differences

    # Replace placeholders with actual values
    # problem = [sentence.format(
    #     time1=time1,
    #     time2_minus_time1=time2_minus_time1,
    #     time3_minus_time1=time3_minus_time1
    # ) for sentence in problem]

    # Calculate the answer
    answer = time1 + time2 + time3

    # Return the problem and answer
    cot = [f"{name2} took {time2_minus_time1} hours longer than {name1}, so the time taken by {name2} is {time2}.",
           f"{name3} took well over {time3_minus_time1} hours longer than {name1}, so the time taken by {name3} is {time3}.",
           f"The total time taken by {name1}, {name2}, and {name3} is {time1} + {time2} + {time3}, which is {answer}."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': all_irrelevant_infos}
