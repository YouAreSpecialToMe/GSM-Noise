from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define list of names
    names = ["Alex", "Maria", "Kai", "Liam", "Sophia", "Emma", "Noah", "Oliver", "Ava", "Isabella", 'James']

    # Randomly select a name
    name = random.choice(names)

    # Randomly generate lake distance
    lake_distance = random.randint(5, 100)  # in miles

    # Randomly generate swimming speeds
    initial_speed = round(random.uniform(1, 5), 2)  # in miles per hour

    # Randomly generate initial swimming percentage
    initial_percent = random.randint(20, 80)  # in percent
    num_times_swam = random.randint(1, 10)  # number of times swam

    # Randomly generate rest fraction and calculate percentage
    rest_fraction = round(random.uniform(0.25, 0.75), 2)  # as fraction of swimming time
    rest_percent = round(rest_fraction * 100, 2)  # as percentage

    # Randomly generate final speed fraction and calculate percentage
    final_speed_fraction = round(random.uniform(0.4, 0.9), 2)  # fraction of initial speed
    final_speed_percent = round(final_speed_fraction * 100, 2)  # as percentage

    # Uncomment below lines to use original values and match the ground truth answer
    # name = "James"
    # lake_distance = 20
    # initial_speed = 2
    # initial_percent = 60
    # rest_fraction = 0.5
    # rest_percent = 50.0
    # final_speed_fraction = 0.5
    # final_speed_percent = 50.0

    # Construct the premise content
    problem = [
        f"{name} loves to go swimming and has to swim across a {lake_distance}-mile lake.",
        f"{name} can swim at a pace of {initial_speed} miles per hour.",
        f"{name} swims {initial_percent}% of the distance.",
        f"After that, {name} stops on an island and rests for {rest_percent}% as long as the swimming time.",
        f"{name} then finishes the remaining distance while going at {final_speed_percent}% of the speed."
    ]

    # Construct the question
    question = f"How long did it take {name} to get across the lake?"
    original_problem = problem.copy()

    original_problem.append(question)

    # Add in-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"The lake is known for its beautiful scenery.",
        f"{name} is training for an upcoming swimming competition.",
        f"The weather was perfect for swimming that day.",
        f"{name} had swimed in this lake {num_times_swam} times before."
    ]

    # Add out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{name} has a pet dog named Buddy.",
        f"{name}'s favorite hobby is painting.",
        f"{name} recently bought a new car.",
        f"{name} enjoys reading mystery novels."
    ]

    # Combine irrelevant information
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (Assuming functions are given)
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
    initial_distance = lake_distance * (initial_percent / 100)
    time_initial = initial_distance / initial_speed
    rest_time = time_initial * rest_fraction
    remaining_distance = lake_distance - initial_distance
    final_speed = initial_speed * final_speed_fraction
    time_final = remaining_distance / final_speed
    answer = time_initial + rest_time + time_final

    # Return the problem and answer
    cot = [f"{name} swims {initial_percent}% of the {lake_distance}-mile lake, which is {lake_distance} * ({initial_percent} / 100) = {initial_distance} miles.", f"The time taken to swim this initial distance is {initial_distance} / {initial_speed} = {time_initial} hours.", f"{name} rests for {rest_fraction} of the swimming time, which is {time_initial} * {rest_fraction} = {rest_time} hours.", f"The remaining distance to swim is {lake_distance} - {initial_distance} = {remaining_distance} miles.", f"The speed for the remaining distance is {initial_speed} * {final_speed_fraction} = {final_speed} miles per hour.", f"The time taken to swim the remaining distance is {remaining_distance} / {final_speed} = {time_final} hours.", f"Therefore, the total time taken to get across the lake is {time_initial} + {rest_time} + {time_final} = {answer} hours."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
