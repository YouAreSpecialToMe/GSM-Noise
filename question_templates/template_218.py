from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
from fractions import Fraction
# Done
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define list of names
    names = ["Alice", "Beth", "Cindy", "Diana", "Emma", "Fiona", "Grace", "Hannah",
             "Isla", "Julia", "Katherine", "Laura", "Nina", "Olivia", "Paula",
             "Rachel", "Sophia", "Tina", "Victoria", "Wendy", "Zoe"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly generate numbers within reasonable range
    total_students = random.randint(20, 40)  # Total number of students
    pencils_per_student = random.randint(5, 15)  # Pencils per student at the beginning

    # Define possible fractions
    fractions = [Fraction(1,2), Fraction(1,3), Fraction(1,4), Fraction(1,5), Fraction(2,3), Fraction(3,4)]

    fraction_used_after_two_months = random.choice(fractions)
    fraction_remaining_at_end = random.choice(fractions)

    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"There are {total_students} students in {name}'s class.",
        f"Each student started the year with {pencils_per_student} pencils.",
        f"After two months, {fraction_used_after_two_months} of the total pencils in class were used.",
        f"At the end of the year, only {fraction_remaining_at_end} of the remaining pencils were left."
    ]
    
    # Construct the question
    question = f"How many pencils were left?"
    original_problem = problem.copy()
    original_problem.append(question)
    # In-topic irrelevant information (related to pencils or school)
    in_topic_irrelevant_infos = [
        f"The class won a prize for the best attendance.",
        f"The school bought new laptops for the computer lab.",
        f"{name} was appointed as the class monitor.",
        f"Each student also received {random.randint(1,5)} notebooks at the beginning of the year."
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{name} has a pet {random.choice(['dog', 'cat', 'parrot', 'hamster'])}.",
        f"{name} loves to play the {random.choice(['guitar', 'piano', 'violin', 'drums'])}."
    ]

    # Randomly add in-topic and out-topic irrelevant information based on prob_irre
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors
    # Assuming introduce_symbol_error and introduce_grammar_error functions are given
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
    
    # Add the question at the end
    problem.append(question)
    
    # Calculate the answer
    total_pencils_start = total_students * pencils_per_student
    pencils_used_after_two_months = total_pencils_start * fraction_used_after_two_months
    remaining_pencils_after_two_months = total_pencils_start - pencils_used_after_two_months
    pencils_left_at_end = remaining_pencils_after_two_months * fraction_remaining_at_end
    answer = int(pencils_left_at_end)
    
    # Return problem and answer as a dictionary
    cot = [f"Calculate the total number of pencils at the start: {total_students} * {pencils_per_student} = {total_pencils_start}.", f"Calculate the number of pencils used after two months: {total_pencils_start} * {fraction_used_after_two_months} = {pencils_used_after_two_months}.", f"Calculate the remaining pencils after two months: {total_pencils_start} - {pencils_used_after_two_months} = {remaining_pencils_after_two_months}.", f"Calculate the pencils left at the end of the year: {remaining_pencils_after_two_months} * {fraction_remaining_at_end} = {pencils_left_at_end}.", f"The final answer is the integer value of {pencils_left_at_end}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
