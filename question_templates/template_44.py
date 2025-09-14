from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define lists for random selection
    teacher_names = ['Mr. Roper', 'Ms. Smith', 'Mrs. Johnson', 'Dr. Brown', 'Mr. Anderson', 'Miss Davis', 'Professor Miller', 'Mrs. Wilson', 'Miss Taylor', 'Dr. Thomas']
    sports = ['football players', 'basketball players', 'soccer players', 'volleyball players', 'baseball players']
    activities_1 = ['cheerleaders', 'dancers', 'singers', 'actors', 'orchestra members']
    activities_2 = ['band members', 'drama club members', 'debate team members', 'science club members', 'math club members']
    destinations = ['an away game', 'a competition', 'a field trip', 'a science fair', 'a debate tournament']

    # Define original variable values
    orig_total_students = 30
    orig_percentage_sport = 20
    orig_percentage_activity = 25

    orig_sport_group = 'football players'
    orig_activity_group1 = 'cheerleaders'
    orig_activity_group2 = 'band members'
    orig_destination = 'an away game'

    # Randomly select variables
    teacher_name = random.choice(teacher_names)
    total_students = random.randint(20, 40)
    sport_group = random.choice(sports)
    activity_group1 = random.choice(activities_1)
    activity_group2 = random.choice(activities_2)
    percentage_sport = random.randint(10, 30)
    percentage_activity = random.randint(10, 50)
    destination = random.choice(destinations)

    # Build the variable dictionary
    vars = {
        'teacher_name': teacher_name,
        'total_students': total_students,
        'sport_group': sport_group,
        'percentage_sport': percentage_sport,
        'activity_group1': activity_group1,
        'activity_group2': activity_group2,
        'percentage_activity': percentage_activity,
        'destination': destination
    }

    # Construct the premise content, breaking it down into sentences
    problem = [
        f"In {vars['teacher_name']}'s class of {vars['total_students']} students, {vars['percentage_sport']}% of the class are {vars['sport_group']}.",
        f"Out of the remaining class, {vars['percentage_activity']}% of the students are {vars['activity_group1']} or {vars['activity_group2']}.",
        f"These 3 groups of students will need to leave early today to travel to {vars['destination']}."
    ]

    # Construct the question
    question = f"How many students are leaving early?"
    original_problem=problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{vars['teacher_name']} recently assigned a project to the class.",
        f"The {vars['sport_group']} won their last game.",
        f"The {vars['activity_group1']} and {vars['activity_group2']} are preparing for an event next week."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.extend([
        f"{vars['teacher_name']} enjoys hiking on weekends.",
        f"The weather today is sunny and warm."
    ])

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    # Assume introduce_symbol_error and introduce_grammar_error are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    if len(problem) > 1:
        first_sentence = problem[0]
        rest_sentences = problem[1:]
        if shuffle:
            random.shuffle(rest_sentences)
        problem = [first_sentence] + rest_sentences

    # Add the question
    problem.append(question)

    # Compute the answer using the variables
    number_sport = vars['total_students'] * (vars['percentage_sport'] / 100)
    remaining_students = vars['total_students'] - number_sport
    number_activity = remaining_students * (vars['percentage_activity'] / 100)
    answer = number_sport + number_activity

    # Round the answer to an integer
    answer = int(round(answer))

    # Return the problem and the answer
    cot = [f"Calculate the number of {percentage_sport}% {sport_group} in the class: {total_students} * ({percentage_sport} / 100) = {number_sport}.", f"Subtract the number of {sport_group} from the total students to find the remaining students: {total_students} - {number_sport} = {remaining_students}.", f"Calculate the number of {percentage_activity}% {activity_group1} or {activity_group2} from the remaining students: {remaining_students} * ({percentage_activity} / 100) = {number_activity}.", f"Add the number of {sport_group} and {activity_group1} or {activity_group2} to find the total number of students leaving early: {number_sport} + {number_activity} = {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
