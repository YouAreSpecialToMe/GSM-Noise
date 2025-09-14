from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of names, professions, and projects
    names = ["Jean", "Maria", "Linda", "Kate", "Sophia", "Ella", "Mia", "Emma"]
    professions = ["makeup artist", "personal trainer", "private tutor", "piano instructor", "dance coach"]
    projects = ["movie", "play", "concert", "television show", "music video"]
    
    # Randomly select a name, profession, and project
    name = random.choice(names)
    artist_profession = random.choice(professions)
    project = random.choice(projects)
    
    # Randomly generate numerical values
    rate = random.randint(100, 500)  # Charges per hour
    hours_per_day = random.randint(1, 8)  # Hours required each day
    days_per_week = random.randint(1, 7)  # Days per week
    weeks = random.randint(1, 12)  # Number of weeks
    discount = random.randint(0, 30)  # Discount percentage
    
    # Irrelevant numerical values
    project_cost = random.randint(50000, 1000000)
    friend_name = random.choice(["Mike", "Tom", "Chris", "Anna", "Lucy"])
    charity_amount = random.randint(1000, 10000)
    
    # Construct the premise content
    problem = [
        f"{name}'s {artist_profession} charges {name} ${rate} an hour.",
        f"{name} requires very expensive services for a {project} {name} is in and it takes {hours_per_day} hours to do each day and {name} needs it done {days_per_week} times a week.",
        f"The {project} takes {weeks} weeks to finish.",
        f"After the {project} is done the {artist_profession} gives {name} a {discount}% discount because of the amount of work done."
    ]
    
    # Construct the question
    question = f"How much did {name} pay?"
    original_problem = problem.copy()
    original_problem.append(question)
    # In-topic irrelevant information
    irrelevant_infos = [
        f"This {project} is expected to cost ${project_cost} in total.",
        f"{name}'s friend {friend_name} is also working on the {project}.",
        f"{name} plans to donate ${charity_amount} to charity after the {project}."
    ]
    
    # Out-topic irrelevant information
    irrelevant_infos.append(f"{name} recently adopted a puppy.")
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors (assumed functions)
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
    total_hours = hours_per_day * days_per_week * weeks
    total_cost = rate * total_hours
    final_cost = total_cost * (1 - discount / 100)
    answer = final_cost
    
    # Return the problem and answer
    cot = [f"{name} requires services for {hours_per_day} hours each day, {days_per_week} times a week, for {weeks} weeks. Therefore, the total hours are {hours_per_day} * {days_per_week} * {weeks}, which is {total_hours}.", f"The total cost before discount is {rate} per hour times {total_hours} hours, which is {total_cost}.", f"The discount is {discount}%, so the final cost is {total_cost} * (1 - {discount} / 100), which is {final_cost}.", f"Therefore, the final answer is {final_cost}, which is equal to {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
