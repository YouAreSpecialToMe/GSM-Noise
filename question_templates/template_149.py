from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name list
    names = ["John", "Alice", "Bob", "Cindy", "David", "Elena"]

    # Randomly select a name
    name = random.choice(names)

    # Randomly generate the variables
    periods_per_day_normal = random.randint(4, 8)  # between 4 and 8 periods per day
    extra_classes = random.randint(1, 4)  # between 1 and 4 extra classes
    minutes_per_class = random.randint(30, 60)  # between 30 and 60 minutes per class
    days_per_week = 5  # standard school days per week
    extra_learning_ratio = random.choice([1 / 8, 1 / 10, 1 / 12, 1 / 16, 1 / 20])  # possible fractions

    # Additional variables for distractors
    vacation_days = random.randint(0, 2)  # number of vacation days in the week
    books_read = random.randint(0, 5)
    pet_age = random.randint(1, 10)

    # Construct the premises, with variables
    problem = [
        f"There are {periods_per_day_normal} periods in the day for a normal student but {name} has to take {extra_classes} extra classes.",
        f"Each class is {minutes_per_class} minutes long.",
        f"{name} goes to class for {days_per_week} days a week.",
        f"{name} then spends {int(extra_learning_ratio * 100)}% of {name}'s weekly minutes each on Saturday and Sunday as extra learning time."
    ]

    # Construct the question
    question = f"How many hours a week does {name} spend learning?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_activities = ["playing video games", "watching TV", "playing basketball", "painting"]
    irrelevant_infos = [
        f"{name} spent {random.randint(1, 5)} hours on {random.choice(irrelevant_activities)} a week.",
        f"Each class is {minutes_per_class + random.randint(10, 40)} minutes long for {name}'s brother.",
        f"{name}'s friend goes to class for {days_per_week + random.randint(0, 2)} days a week."
    ]
    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} has a pet dog who is {pet_age} years old.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Resolve pronouns in the problem
    problem = [p.replace(' He ', f' {name} ').replace(' he ', f' {name} ').replace('His', f"{name}'s").replace('his',
                                                                                                               f"{name}'s")
               for p in problem]

    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle sentences except the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    total_periods_per_day = periods_per_day_normal + extra_classes
    minutes_per_day = total_periods_per_day * minutes_per_class
    total_minutes_weekdays = minutes_per_day * days_per_week
    additional_minutes_per_day = extra_learning_ratio * total_minutes_weekdays
    total_additional_minutes = additional_minutes_per_day * 2  # Saturday and Sunday
    total_weekly_minutes = total_minutes_weekdays + total_additional_minutes
    answer = total_weekly_minutes / 60  # Convert minutes to hours

    # Return the problem and answer
    cot = [f"Calculate the total number of periods per day by adding {periods_per_day_normal} and {extra_classes}, which gives {total_periods_per_day}.", f"Calculate the total minutes per day by multiplying {total_periods_per_day} by {minutes_per_class}, resulting in {minutes_per_day}.", f"Calculate the total minutes for weekdays by multiplying {minutes_per_day} by {days_per_week}, which equals {total_minutes_weekdays}.", f"Calculate the additional minutes per day for extra learning by multiplying {extra_learning_ratio} by {total_minutes_weekdays}, resulting in {additional_minutes_per_day}.", f"Calculate the total additional minutes for the weekend by multiplying {additional_minutes_per_day} by 2, which gives {total_additional_minutes}.", f"Calculate the total weekly minutes by adding {total_minutes_weekdays} and {total_additional_minutes}, resulting in {total_weekly_minutes}.", f"Convert the total weekly minutes to hours by dividing {total_weekly_minutes} by 60, which gives the final answer of {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
