from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ["Melanie", "Sophia", "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Jamie", "Riley", "Drew"]
    items = ["toothpick sculpture", "popsicle stick bridge", "matchstick house", "paper airplane fleet", "clay model", "origami collection"]
    
    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)
    
    # Generate appropriate values for the problem
    per_week_options = [5, 10, 12, 15, 20]
    per_week = random.choice(per_week_options)
    total_required_multiplier = random.randint(20, 50)
    total_required = per_week * total_required_multiplier
    weeks_saved_options = list(range(1, total_required_multiplier))
    weeks_saved = random.choice(weeks_saved_options)
    saved_so_far = per_week * weeks_saved
    remaining_toothpicks = total_required - saved_so_far
    
    # Adjust weeks_saved if necessary to ensure remaining_toothpicks is a multiple of per_week
    if remaining_toothpicks % per_week != 0:
        adjustment = remaining_toothpicks % per_week
        weeks_saved -= adjustment // per_week
        saved_so_far = per_week * weeks_saved
        remaining_toothpicks = total_required - saved_so_far
    
    # Calculate the answer
    # answer = (total_required - per_week * weeks_saved) / per_week
    answer = (total_required - per_week * weeks_saved) // per_week

    # Build the problem with variables in {variable_name} format
    problem = [
        f"{name} found a blueprint online for a {item} {name} wanted to make.",
        f"It requires {total_required} toothpicks.",
        f"{name}'s mom puts toothpicks in {name}'s sandwiches when she serves them for lunch.",
        f"{name} started saving them and has saved {per_week} toothpicks each week for the past {weeks_saved} weeks.",
    ]
    
    # Construct the question
    question = f"If {name} continues saving toothpicks at the same rate, how many more weeks will it take {name} to collect {total_required} toothpicks?"
    original_problem = problem.copy()
    original_problem.append(question)
    # Insert in-topic and out-topic irrelevant information
    project_deadline = random.randint(2, 10)
    friend_toothpicks = random.randint(50, 200)
    sports = ["soccer", "basketball", "tennis", "chess", "swimming"]
    sport = random.choice(sports)
    num_pets = random.randint(1, 5)
    year_of_birth = random.randint(1990, 2010)

    irrelevant_infos = [
        f"{name} needs to submit the {item} for a school project in {project_deadline} weeks.",
        f"{name}'s friend is also making a {item} that requires {friend_toothpicks} toothpicks.",
        f"{name} plays {sport} on weekends.",
        f"{name} has {num_pets} pet(s) at home.",
        f"{name} was born in {year_of_birth}."
    ]

    
    # Randomly add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            # irrelevant_info_formatted = irrelevant_info.format(
            #     name=name,
            #     item=item,
            #     project_deadline=project_deadline,
            #     friend_toothpicks=friend_toothpicks,
            #     sport=sport,
            #     num_pets=num_pets,
            #     year_of_birth=year_of_birth
            # )
            problem.append(irrelevant_info)
    
    # Replace variables in the problem statements
    # problem = [p.format(name=name, item=item, total_required=total_required, per_week=per_week, weeks_saved=weeks_saved) for p in problem]
    # question = question.format(name=name, total_required=total_required)
    
    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences except the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem
    problem.append(question)
    
    # Return the problem and answer as a dictionary
    cot = [f"{name} has saved {per_week} toothpicks each week for the past {weeks_saved} weeks, which totals to {saved_so_far} toothpicks.", f"The total number of toothpicks required is {total_required}. Therefore, the remaining toothpicks needed are {total_required} - {saved_so_far}, which is {remaining_toothpicks}.", f"To find out how many more weeks it will take to collect the remaining toothpicks, divide {remaining_toothpicks} by {per_week}. This gives {answer} more weeks."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
