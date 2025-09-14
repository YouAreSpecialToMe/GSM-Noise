from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
# Done
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name list
    names = ["Bethany", "Trey", "Shaelyn", "Quinn", "Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Chris", "Lee", "Charlie", "Sam", "Jamie", "Taylor"]
    
    # Randomly select four distinct names
    random_names = random.sample(names, 4)
    name1 = random_names[0]
    name2 = random_names[1]
    name3 = random_names[2]
    name4 = random_names[3]
    
    # Randomly generate laps or times
    laps_name1 = random.randint(10, 20)  # Laps run by name1
    laps_diff_2 = random.randint(1, 10)  # Name2 runs this many more laps than name1
    laps_divisor_3 = random.choice([2, 3])  # Name3 runs half or one-third as many laps as name2
    laps_diff_4 = random.randint(1, 5)  # Name4 runs this many fewer laps than name3
    
    # Additional irrelevant information
    extra_info_number = random.randint(5, 50)
    extra_info_year = random.randint(1990, 2023)
    extra_info_money = random.randint(100, 1000)
    
    # Construct the premise content
    problem = [
        f"{name1} can run {laps_name1} laps on the track in one hour.",
        f"{name2} can run {laps_diff_2} more laps than {name1}.",
        f"{name3} can run {'half' if laps_divisor_3 == 2 else 'one-third'} as many laps as {name2}.",
        f"{name4} can run {laps_diff_4} fewer laps than {name3}."
    ]
    
    # Construct the question
    question = f"How many more (or less) laps can {name1} run compared to {name4}?"
    original_problem = problem.copy()
    original_problem.append(question)
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name4} bought {extra_info_number} energy bars last week.",
        f"In {extra_info_year}, {name2} won a marathon.",
        f"{name3} has ${extra_info_money} in their bank account.",
        f"{name1} and {name4} practice running together every weekend.",
    ]
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors
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
    laps_name2 = laps_name1 + laps_diff_2
    laps_name3 = laps_name2 // laps_divisor_3
    laps_name4 = laps_name3 - laps_diff_4
    answer = laps_name1 - laps_name4
    
    # Return premise and answer as a dictionary
    cot = [f"{name2} can run {laps_diff_2} more laps than {name1}, so {name2} runs {laps_name1} + {laps_diff_2} laps, which is {laps_name2}.", f"{name3} can run {'half' if laps_divisor_3 == 2 else 'one-third'} as many laps as {name2}, so {name3} runs {laps_name2} // {laps_divisor_3} laps, which is {laps_name3}.", f"{name4} can run {laps_diff_4} fewer laps than {name3}, so {name4} runs {laps_name3} - {laps_diff_4} laps, which is {laps_name4}.", f"The difference in laps between {name1} and {name4} is {laps_name1} - {laps_name4}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
