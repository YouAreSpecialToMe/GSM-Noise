import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names list
    names = ["Adam", "Martha", "Betty", "Tom", "Lucy", "Michael", "Sarah", "James", "Emma", "Oliver"]
    
    # Randomly select 4 different names
    students = random.sample(names, 4)
    student1 = students[0]
    student2 = students[1]
    student3 = students[2]
    student4 = students[3]
    
    # Randomly select class names
    class_names = ["3B", "3C", "2A", "4D", "5E"]
    class_name = random.choice(class_names)
    
    # Randomly generate initial points for student1
    points_student1 = random.randint(30, 70)  # Original was 50 points
    
    # Randomly generate percentage more for student2
    percentage_more = random.choice([10, 20, 30, 40])  # Original was 30%
    
    # Randomly generate difference between student2 and student3
    diff_points = random.randint(20, 50)  # Original was 30 points less
    
    # Multiplier between student3 and student4
    multiplier = random.choice([2, 3, 4])  # Original was 3 times more
    
    # Minimum threshold
    min_threshold = random.randint(350, 500)  # Original was 400 points
    
    # Calculate the points collected
    # points_student2 = points_student1 + (points_student1 * percentage_more / 100)
    points_student2 = points_student1 * (1 + percentage_more / 100)
    # points_student3 = points_student2 - diff_points
    points_student3 = points_student2 - diff_points
    # points_student4 = points_student3 * multiplier
    points_student4 = points_student3 * multiplier
    # total_points = points_student1 + points_student2 + points_student3 + points_student4
    total_points = points_student1 + points_student2 + points_student3 + points_student4
    # missing_points = min_threshold - total_points
    missing_points = min_threshold - total_points
    if missing_points <= 0:
        # Adjust min_threshold to ensure missing_points is positive
        missing_points = random.randint(10, 100)
        min_threshold = total_points + missing_points
    
    # Construct the premises
    problem = [
        f"Students in class {class_name} are collecting school points for behavior.",
        f"If they get enough points in total, they can go on a trip.",
        f"In the class, there are {student1}, {student2}, {student3}, and {student4}.",
        f"{student1} has collected {int(points_student1)} points.",
        f"{student2} was better than {student1} and collected {percentage_more}% more.",
        f"{student4} managed to collect {multiplier} times more points than {student3}, who has {int(diff_points)} points less than {student2}.",
    ]

    import copy
    original_problem = copy.deepcopy(problem)
    
    # Construct the question
    question = f"How many points is the class missing to go on the trip if the minimum threshold is {int(min_threshold)} points?"
    
    # Add in-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"The class {class_name} also participates in the annual sports day.",
        f"The school has a total of {random.randint(500, 1000)} students.",
    ]
    
    # Add out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{random.choice(names)} won the spelling bee competition last year.",
        f"The school's cafeteria serves lunch at noon.",
    ]
    
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    random.shuffle(irrelevant_infos)
    
    # Add irrelevant information based on probability
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
    
    # Shuffle the problem sentences except for the first two
    to_shuffle = problem[1:]
    if shuffle:
        random.shuffle(to_shuffle)
    problem = [problem[0]] + to_shuffle

    # Add the question
    problem.append(question)
    original_problem.append(question)
    
    # Provide the math formulas
    # points_student2 = points_student1 * (1 + percentage_more / 100)
    # points_student3 = points_student2 - diff_points
    # points_student4 = points_student3 * multiplier
    # total_points = points_student1 + points_student2 + points_student3 + points_student4
    # missing_points = min_threshold - total_points
    # answer = missing_points
    
    # Return problem and answer
    cot = [f"{student2} collected {percentage_more}% more points than {student1}, so {student2} has {points_student2} points.", f"{student3} has {diff_points} points less than {student2}, so {student3} has {points_student3} points.", f"{student4} collected {multiplier} times more points than {student3}, so {student4} has {points_student4} points.", f"The total points collected by the class is {points_student1} + {points_student2} + {points_student3} + {points_student4}, which is {total_points}.", f"The class is missing {min_threshold} - {total_points} points to reach the minimum threshold, which is {missing_points}."]
    
    return {"cot": cot, 'problem': problem, 'answer': int(missing_points), 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}