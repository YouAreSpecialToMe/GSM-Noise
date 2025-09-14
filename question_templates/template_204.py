from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
import math

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible values for variables
    school_names = ["Maple Ridge Middle School", "Pine Valley Academy", "Sunnydale Intermediate School", "Riverside Preparatory School", "Oakwood Junior High", "Cedar Falls Middle School"]
    grades_from_options = [4, 5, 6]
    grades_to_options = [7, 8, 9]
    students_per_grade_options = [8, 10, 12, 15]
    group_size_options = [5, 8, 10]
    time_per_group_options = [30, 45, 60]
    total_students_options = [500, 600, 700, 800]
    established_year_options = list(range(1950, 2023))
    mascot_options = ["Eagles", "Tigers", "Wolves", "Knights", "Panthers"]

    # Randomly select values for variables
    school_name = random.choice(school_names)
    grades_from = random.choice(grades_from_options)
    grades_to = random.choice([g for g in grades_to_options if g > grades_from])
    students_per_grade = random.choice(students_per_grade_options)
    group_size = random.choice(group_size_options)
    time_per_group = random.choice(time_per_group_options)
    total_students = random.choice(total_students_options)
    established_year = random.choice(established_year_options)
    mascot = random.choice(mascot_options)

    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"{school_name} has students in grades {grades_from} – {grades_to} and each year they are challenged to earn as many Accelerated Reader points as they can.",
        f"The {students_per_grade} students in each grade with the most points get to try an escape room set up by the teachers.",
        f"Only {group_size} students can try the escape room at a time.",
        f"They have {time_per_group} minutes to try and escape."
    ]

    # Construct the question
    question = f"If every group uses their full {time_per_group} minutes, how long will it take for everyone to try the escape room?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The school has a total of {total_students} students.",
        f"The school was established in {established_year}.",
        f"The school's mascot is the {mascot}."
    ]

    # Add out-topic irrelevant information
    city_names = ["Springfield", "Riverside", "Franklin", "Greenville", "Bristol"]
    city_name = random.choice(city_names)
    out_topic_irrelevant_info = f"The school's football team recently won a championship in {city_name}."
    irrelevant_infos.append(out_topic_irrelevant_info)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. You do not have to generate these functions. Assume that they are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question
    problem.append(question)

    # Calculate the answer
    # Number of grades
    num_grades = grades_to - grades_from + 1
    # Total number of students participating
    total_students_participating = students_per_grade * num_grades
    # Number of groups (round up if not divisible)
    num_groups = math.ceil(total_students_participating / group_size)
    # Total time
    answer = num_groups * time_per_group

    # Return premise and answer as a dictionary
    cot = [f"Calculate the number of grades by subtracting {grades_from} from {grades_to} and adding 1, resulting in {num_grades}.", f"Determine the total number of students participating by multiplying {students_per_grade} by {num_grades}, which gives {total_students_participating}.", f"Calculate the number of groups needed by dividing {total_students_participating} by {group_size} and rounding up, resulting in {num_groups}.", f"Finally, calculate the total time by multiplying {num_groups} by {time_per_group}, which equals {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
