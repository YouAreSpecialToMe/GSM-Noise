from grammar_error import introduce_grammar_error, introduce_symbol_error
import random
import math


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define student and teacher names
    students = ["Brinley", "Alex", "Jordan", "Taylor", "Morgan", "Kai", "Casey", "Riley", "Sage", "Quinn", "Darcy",
                "Avery", "Jamie", "Logan", "Skyler"]
    teachers = ["Mr. Smith", "Ms. Johnson", "Mrs. Lee", "Mr. Brown", "Dr. Davis", "Prof. Clark", "Miss Miller",
                "Mr. Bert", "Dr. Nguyen", "Ms. Patel"]

    # Randomly select student and teacher names
    student_name = random.choice(students)
    teacher_name = random.choice(teachers)

    # Number of tests per semester
    total_tests = 6
    number_of_scores_given = total_tests - 1  # First five test scores

    # Generate random scores for the first five tests
    scores = [random.randint(60, 100) for _ in range(number_of_scores_given)]
    sum_scores = sum(scores)
    min_score = min(scores)

    # Calculate possible average range after dropping the lowest score
    max_possible_average = (sum_scores - min_score + 100) / (total_tests - 1)
    min_possible_average = (sum_scores - min_score) / (total_tests - 1)

    # Set the desired average
    desired_average = random.randint(math.ceil(min_possible_average) + 1, math.floor(max_possible_average))

    # Calculate the required score on the sixth test
    s6 = desired_average * (total_tests - 1) - sum_scores + min_score

    # Adjust if s6 is less than the minimum score
    # if s6 < min_score or s6 > 100:
    #     desired_average = round((sum_scores - min_score) / (total_tests - 1))
    #     s6 = random.randint(60, 100)

    # Build the problem premise
    problem = [
        f"{student_name} is in {teacher_name}'s math class.",
        f"{teacher_name} gives {total_tests} tests each semester.",
        f"{teacher_name} allows the students to remove the lowest score from the average each semester.",
        f"{student_name} has scores of {', '.join(map(str, scores))} on the first {number_of_scores_given} tests.",
    ]

    question = f"What score does {student_name} need on the {number_to_ordinal(total_tests)} test to get an average of {desired_average}?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add irrelevant information
    irrelevant_infos = [
        f"The class average on the last test was {random.randint(60, 100)}.",
        f"{student_name} has scores of {random.randint(0, 100)} on the last semester math test.",
        f"{teacher_name} allows students to retake one test last semester.",
    ]

    # Randomly add irrelevant sentences to the problem
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Introduce symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences except the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences + [question]
    # Mathematical formula to calculate the answer
    # If s6 >= min_score:
    #     answer = desired_average * (total_tests - 1) - sum(scores) + min_score
    # Else:
    #     desired_average = (sum(scores) - min_score) / (total_tests - 1)
    #     answer = s6 (any value between 60 and 100)
    answer = s6

    # Return the problem and the answer
    cot = [f"Calculate the sum of the scores: {sum_scores} = sum({scores}).",
           f"Identify the minimum score: {min_score} = min({scores}).",
           f"To achieve the desired average of {desired_average}, calculate the required score on the sixth test: {s6} = {desired_average} * ({total_tests} - 1) - {sum_scores} + {min_score}."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}

def number_to_ordinal(n):
    # Converts a number to its ordinal representation
    if 11 <= n % 100 <= 13:
        suffix = 'th'
    else:
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        suffix = suffixes.get(n % 10, 'th')
    return str(n) + suffix