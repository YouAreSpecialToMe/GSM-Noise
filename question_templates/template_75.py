import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and grades
    names = ["Audrey", "Ben", "Catherine", "David", "Emily", "Frank", "Grace", "Henry", "Isabelle", "Jack"]
    grade_levels = ["5th", "6th", "7th", "8th"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly select the current grade
    current_grade_index = random.randint(0, len(grade_levels) - 2)
    current_grade = grade_levels[current_grade_index]
    next_grade = grade_levels[current_grade_index + 1]
    
    # Randomly generate percentages and question counts
    passing_percentage = random.randint(60, 80)  # From 60% to 80%
    first_test_correct_percentage = random.randint(40, passing_percentage - 10)
    first_test_total_questions = random.randint(50, 100)
    second_test_total_questions = random.randint(30, 50)
    
    # Other irrelevant variables
    total_students = random.randint(100, 500)
    class_average = random.randint(50, 75)
    hobby = random.choice(["painting", "playing soccer", "reading books", "gardening", "collecting stamps"])
    
    # Construct the premises
    problem = [
        f"{name} has to take two math tests to pass {current_grade} grade.",
        f"{name} must correctly answer {passing_percentage}% of the total questions to move on to the {next_grade} grade.",
        f"The first test has {first_test_total_questions} questions and {name} gets {first_test_correct_percentage}% of them correct.",
        f"The second test has {second_test_total_questions} questions."
    ]
    
    import copy
    original_problem = copy.deepcopy(problem)

    # Construct the question
    question = f"How many questions does {name} need to get right on the second test to move onto the {next_grade} grade?"
    
    # Add in-topic irrelevant information
    in_topic_irrelevant = [
        f"The average score of the class is {class_average}%.",
        f"There are {total_students} students in {name}'s school."
    ]
    
    # Add out-topic irrelevant information
    out_topic_irrelevant = f"{name} enjoys {hobby} during free time."
    
    # Combine irrelevant info
    irrelevant_infos = in_topic_irrelevant + [out_topic_irrelevant]
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors. Assume these functions are given.
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
    
    # Append the question at the end
    problem.append(question)
    original_problem.append(question)

    # Calculate the total number of questions
    total_questions = first_test_total_questions + second_test_total_questions
    
    # Calculate the total number of correct answers needed to pass
    total_required_correct = total_questions * passing_percentage / 100
    
    # Calculate the number of correct answers in the first test
    first_test_correct = first_test_total_questions * first_test_correct_percentage / 100
    
    # Calculate the required correct answers in the second test
    required_second_test_correct = total_required_correct - first_test_correct
    
    # Round up to nearest whole number
    answer = max(0, int(required_second_test_correct + 0.9999999999999))
    
    # Ensure answer does not exceed total questions in second test
    if answer > second_test_total_questions:
        answer = second_test_total_questions
    
    # Return the problem and answer as a dictionary
    cot = [f"Calculate the total number of questions by adding {first_test_total_questions} and {second_test_total_questions}, which gives {total_questions}.", f"Determine the total number of correct answers needed to pass by calculating {total_questions} * {passing_percentage} / 100, resulting in {total_required_correct}.", f"Calculate the number of correct answers in the first test by computing {first_test_total_questions} * {first_test_correct_percentage} / 100, which equals {first_test_correct}.", f"Find the required number of correct answers on the second test by subtracting {first_test_correct} from {total_required_correct}, giving {required_second_test_correct}.", f"Round up {required_second_test_correct} to the nearest whole number to get {answer}.", f"Ensure that {answer} does not exceed {second_test_total_questions}. If it does, set {answer} to {second_test_total_questions}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}