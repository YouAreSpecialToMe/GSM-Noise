from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define variables
    students_per_class = random.randint(15, 30)
    num_classes = random.randint(2, 5)
    total_students = students_per_class * num_classes
    school_boy_percentage = random.choice([40, 45, 50, 55, 60])
    school_girl_percentage = 100 - school_boy_percentage
    class1_girls = random.randint(5, students_per_class)
    class2_girls = random.randint(5, students_per_class)

    # Ensure valid number of girls in third class
    total_girls_in_school = int(total_students * (school_girl_percentage / 100))
    girls_in_class3 = total_girls_in_school - class1_girls - class2_girls
    if girls_in_class3 < 0 or girls_in_class3 > students_per_class:
        class1_girls = random.randint(5, students_per_class)
        class2_girls = random.randint(5, students_per_class)
        total_girls_in_school = class1_girls + class2_girls + random.randint(0, students_per_class)
        girls_in_class3 = total_girls_in_school - class1_girls - class2_girls
        if girls_in_class3 < 0:
            girls_in_class3 = 0
        elif girls_in_class3 > students_per_class:
            girls_in_class3 = students_per_class

    # Construct the premises
    problem = [
        f"Each class in a school has {students_per_class} students.",
        f"There are {num_classes} classes.",
        f"The school as a whole is {school_boy_percentage}% boys and {school_girl_percentage}% girls.",
        f"The first class has {class1_girls} girls.",
        f"The second class has {class2_girls} girls."
    ]

    # Construct the question
    question = "How many boys are in the third class?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add irrelevant information
    irrelevant_infos = [
        f"The school has {random.randint(10, 50)} teachers.",
        f"{school_girl_percentage + random.randint(1, 10)}% girls in the school are happy."
        f"{school_boy_percentage - random.randint(1, 10)}% boys in the school are not very happy."
    ]

    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Introduce symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the premises except the first one
    if shuffle:
        random.shuffle(problem)

    # Add the question
    problem.append(question)

    # Calculate the answer
    total_students = students_per_class * num_classes
    total_girls_in_school = total_students * (school_girl_percentage / 100)
    girls_in_class3 = total_girls_in_school - class1_girls - class2_girls
    boys_in_class3 = students_per_class - girls_in_class3
    answer = boys_in_class3

    # Return the problem and answer
    cot = [f"Calculate the total number of students in the school by multiplying {students_per_class} by {num_classes}, which gives {total_students}.", f"Calculate the total number of girls in the school by multiplying {total_students} by the percentage of girls ({school_girl_percentage}%), resulting in {total_girls_in_school}.", f"Determine the number of girls in the third class by subtracting the number of girls in the first class ({class1_girls}) and the second class ({class2_girls}) from {total_girls_in_school}, which gives {girls_in_class3}.", f"Calculate the number of boys in the third class by subtracting {girls_in_class3} from {students_per_class}, resulting in {boys_in_class3}.", f"The final answer is the number of boys in the third class, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
