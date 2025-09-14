from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define the lists for names and items
    names = ["Maria", "Sophia", "Emma", "Isabella", "Olivia", "Ava"]
    mom_names = ["Mrs. Johnson", "Mrs. Smith", "Mrs. Davis", "Mrs. Brown", "Mrs. Garcia"]
    activities = ["water balloon fight", "paintball game", "snowball fight", "pillow fight", "mud fight"]

    # Randomly select names and activity
    name = random.choice(names)
    mom_name = random.choice(mom_names)
    activity = random.choice(activities)

    # Randomly generate numeric values
    friends = random.randint(2, 6)  # Number of friends
    initial_balloons = random.randint(1, 5)  # Initial balloons given to each friend
    self_balloons = random.randint(1, 5)  # Balloons the main person has
    mom_balloons = random.randint(2, 5)  # Balloons mom gives to each person

    # Irrelevant numerical values
    extra_friends = random.randint(1, 3)  # Number of friends who couldn't come
    balloons_leftover = random.randint(1, 10)  # Balloons left over after the game
    day = random.choice(["Saturday", "Sunday", "Friday"])
    weather = random.choice(["sunny", "rainy", "cloudy"])

    # Construct the premise content
    problem = [
        f"{name} invited {friends} of her friends over for a {activity} in the backyard.",
        f"At the start of the game, {name} gave each of her friends {initial_balloons} water balloons.",
        f"{name} had {self_balloons} water balloons for herself.",
        f"Then {name}'s mom, {mom_name}, came out and gave each person {mom_balloons} more balloons."
    ]

    # Construct the question
    question = f"How many total balloons did the girls have?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{extra_friends} of {name}'s friends bring snacks.",
        f"There were {balloons_leftover} water balloons left over after the {activity}."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"It was a {weather} {day} when they had the {activity}.")

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
    total_people = friends + 1  # Including the main person
    total_balloons = (friends * initial_balloons) + self_balloons + (total_people * mom_balloons)
    answer = total_balloons

    # Return the problem and answer
    cot = [f"The total number of people, including {name}, is {friends} + 1, which is {total_people}.", f"{name} gave each of her {friends} friends {initial_balloons} water balloons, and she had {self_balloons} for herself.", f"Then, {name}'s mom gave each of the {total_people} people {mom_balloons} more balloons.", f"The total number of balloons is ({friends} * {initial_balloons}) + {self_balloons} + ({total_people} * {mom_balloons}), which is {total_balloons}.", f"Therefore, the total number of balloons the girls had is {total_balloons}, which is the final answer."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
