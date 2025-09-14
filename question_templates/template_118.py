from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible variable values
    names = ["Tom", "Jerry", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
    locations = ["Europe", "Asia", "Africa", "South America", "Australia"]
    genders = {"Tom": "male", "Jerry": "male", "Bob": "male", "Charlie": "male", "Frank": "male",
               "Alice": "female", "Diana": "female", "Eve": "female"}

    # Randomly select a name and location
    name = random.choice(names)
    location = random.choice(locations)
    gender = genders[name]
    if gender == "male":
        pronoun = "him"
    else:
        pronoun = "her"

    # Randomly generate variables
    trip_duration = 14  # Total days of the trip
    first_period_days = random.randint(2, 5)
    first_period_distance_per_day = random.randint(100, 500)
    second_period_days = random.randint(1, 3)
    second_period_percentage = random.randint(10, 50)
    third_period_days = 1  # Not traveling at all
    third_day_traveled = 0  # Distance on the non-traveling day
    total_days_so_far = first_period_days + second_period_days + third_period_days
    fourth_period_days = trip_duration - total_days_so_far
    fourth_period_distance_per_day = random.randint(200, 500)

    # Construct premises
    problem = [
        f"{name} went on a two-week-long trip through {location}.",
        f"In the first {first_period_days} days, {name} traveled {first_period_distance_per_day} kilometers every day.",
        f"Over the next {second_period_days} days, {name} totaled only {second_period_percentage}% of the distance traveled over the first {first_period_days} days.",
        f"On the next day, {name} wasn't traveling at all.",
        f"During the second week, {name} made {fourth_period_distance_per_day} kilometers every day."
    ]

    # Construct the question
    question = f"How many kilometers in total did {name} make during {pronoun} two-week-long trip?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Construct in-topic irrelevant information
    friend_names = [n for n in names if n != name]
    friend_name = random.choice(friend_names)
    souvenir_price = random.randint(20, 100)
    in_topic_irrelevant_infos = [
        f"{name}'s friend {friend_name} joined {pronoun} for a few days during the trip.",
        f"{name} used to travel {first_period_distance_per_day + random.randint(2, 10)} kilometers every day."
        f"On the next day, {name}'s friend {friend_name} continued to travel {second_period_percentage - random.randint(1, second_period_percentage)}% of the distance traveled over the first {first_period_days + random.randint(1, 10)} days."
    ]

    # Construct out-topic irrelevant information
    hobbies = ["playing guitar", "reading books", "swimming", "cooking", "photography"]
    hobby = random.choice(hobbies)
    out_topic_irrelevant_info = f"{name} is a {gender} who enjoys {hobby} in {pronoun} free time."

    # Combine irrelevant information
    irrelevant_infos = in_topic_irrelevant_infos + [out_topic_irrelevant_info]

    # Randomly add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    # Assume these functions are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(prem, prob_grammar_error),
            prob_symbol_error
        ) for prem in problem
    ]

    # Shuffle the order of sentences, except for the first one
    main_premise = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [main_premise] + rest_of_problem

    # Append the question
    problem.append(question)

    # Calculate the answer
    first_period_distance = first_period_days * first_period_distance_per_day
    second_period_total_distance = (second_period_percentage / 100) * first_period_distance
    third_day_distance = third_day_traveled
    fourth_period_distance = fourth_period_days * fourth_period_distance_per_day
    total_distance = first_period_distance + second_period_total_distance + third_day_distance + fourth_period_distance
    answer = total_distance

    # Return the problem and the answer
    cot = [f"During the first {first_period_days} days, {name} traveled {first_period_distance_per_day} kilometers each day, totaling {first_period_distance}.", f"Over the next {second_period_days} days, {name} traveled {second_period_percentage}% of the distance from the first period, which is {second_period_total_distance}.", f"On the next day, {name} did not travel, so the distance for that day is {third_day_distance}.", f"During the second week, {name} traveled {fourth_period_distance_per_day} kilometers each day for {fourth_period_days} days, totaling {fourth_period_distance}.", f"Adding all these distances together gives the total distance: {first_period_distance} + {second_period_total_distance} + {third_day_distance} + {fourth_period_distance} = {total_distance}.", f"Therefore, the total distance traveled by {name} during the trip is {answer} kilometers."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
