from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible values
    teacher_names = ["Mr. Jackson", "Ms. Smith", "Mrs. Thompson", "Mr. Brown", "Ms. Garcia", "Mrs. Wilson", "Mr. Khan",
                     "Ms. Patel", "Mr. O'Neill", "Mrs. Müller"]
    grades = ["first-grade", "second-grade", "third-grade", "fourth-grade", "fifth-grade", "sixth-grade"]

    # Randomly assign variables
    teacher_name = random.choice(teacher_names)
    grade = random.choice(grades)
    num_students = random.randint(20, 35)  # Number of students
    glue_sticks_per_student = random.randint(1, 3)  # Glue sticks per student
    pack_size = random.choice([4, 6, 8, 10, 12])  # Glue sticks in a pack

    # Additional variables for irrelevant info
    pencil_packs = random.randint(5, 15)
    pencils_per_pack = random.choice([10, 12, 24])
    teacher_hobby = random.choice(["hiking", "painting", "reading", "gardening"])
    weather_forecast = random.choice(["rain", "sunny", "cloudy", "snow"])

    # Construct the premise content, breaking it down into sentences
    problem_wq = [
        f"{teacher_name}'s {grade} class has {num_students} students.",
        f"{teacher_name} wants to give each student {glue_sticks_per_student} glue sticks.",
        f"The glue sticks come in packs of {pack_size}.",
        f"How many packs will {teacher_name} need to buy so every student can have {glue_sticks_per_student} glue sticks,",
        f"assuming {teacher_name} can only buy whole packs and {teacher_name} expects to have some extra glue sticks left over?"
    ]

    original_problem = problem_wq.copy()

    question = problem_wq[-2] + " " + problem_wq[-1]

    problem = problem_wq[:-2]

    # Construct in-topic irrelevant information
    colors = ['green', 'yellow', 'pink', 'red', 'brown', 'purple']
    color = random.choice(colors)
    in_topic_irrelevant_infos = [
        f"{teacher_name} wants to give each student {glue_sticks_per_student + random.randint(1, 5)} {color} sticks.",
        f"{teacher_name} bought {pencil_packs} packs of pencils last week.",
        f"The {color} sticks come in packs of {pack_size + random.randint(5, 20)}.",
    ]

    # Construct out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{teacher_name} enjoys {teacher_hobby} on weekends.",
    ]

    # Add irrelevant information based on probability
    for info in in_topic_irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    for info in out_topic_irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Add symbol or grammar errors (Assuming introduce_symbol_error and introduce_grammar_error functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        )
        for p in problem
    ]

    # Shuffle the order of sentences, except for the question
    if shuffle:
        random.shuffle(problem)
    problem.append(question)

    # Calculate the answer
    total_glue_sticks_needed = num_students * glue_sticks_per_student
    packs_needed = -(-total_glue_sticks_needed // pack_size)  # Ceiling division

    answer = packs_needed

    # Return the problem and answer as a dictionary
    cot = [f"Calculate the total number of glue sticks needed by multiplying {num_students} by {glue_sticks_per_student}, which gives {total_glue_sticks_needed}.", f"Determine the number of packs needed by performing ceiling division of {total_glue_sticks_needed} by {pack_size}, resulting in {packs_needed}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
