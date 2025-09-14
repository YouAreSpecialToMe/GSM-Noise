from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names
    names = ["Steve", "Tim", "Mike", "John", "Alex", "Ryan", "Chris", "Emily", "Sarah", "Jessica", "Rachel", "Megan",
             "Hannah", "Sam", "Taylor", "Jordan"]

    name1, name2 = random.sample(names, 2)

    # Define transport modes
    transport_modes = ["bike", "skateboard", "rollerblades", "scooter", "running", "walking"]
    transport1 = random.choice(transport_modes)
    transport_modes2 = [mode for mode in transport_modes if mode != transport1]
    transport2 = random.choice(transport_modes2)

    # Define distances
    distance2 = random.randint(1, 10)  # miles
    distance1 = random.randint(distance2 + 1, distance2 + 7)  # Ensure distance1 > distance2

    # Initialize variables
    # Speeds in ft/min
    speed1 = random.randint(300, 600) * 5.28
    speed2 = random.randint(200, 800) * 5.28
    # Compute times
    distance1_ft = distance1 * 5280
    distance2_ft = distance2 * 5280
    t1 = distance1_ft / speed1  # time in minutes
    t2 = distance2_ft / speed2  # time in minutes

    # Round times to closest integer
    delta_t = abs(t2 - t1)

    # Construct the premise content
    problem = [
        f"{name1} and {name2} decide to see who can get home from school the fastest.",
        f"{name1} lives further away than {name2}, so {name1} is allowed to ride {name1}'s {transport1}.",
        f"{name1} lives {distance1} miles from the school and can {transport1} at {speed1} feet per minute.",
        f"{name2} lives {distance2} miles away from the school.",
        f"{name2} can {transport2} at {speed2} feet per minute."
    ]

    question = f"How long will the winner be waiting at their house before the loser finishes the race?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Construct in-topic irrelevant information
    irrelevant_names = ["Liam", "Noah", "Oliver", "James", "William", "Benjamin", "Elijah", "Lucas", "Mason", "Logan",
                        "Alexander", "Ethan", "Jacob", "Michael", "Daniel", "Henry"]
    irrelevant_name1, irrelevant_name2 = random.sample(irrelevant_names, 2)
    irrelevant_infos = [
        f"{irrelevant_name1} lives {random.randint(1, 5)} miles away from the school.",
        f"{irrelevant_name2} lives further away than {name1}.",
        f"{irrelevant_name1} can {random.choice(transport_modes)} at {random.randint(200, 600)} feet per minute.",
    ]

    # Construct out-topic irrelevant information
    irrelevant_out_topic = [
        f"{name1} has a pet {random.choice(['dog', 'cat', 'parrot'])} named {random.choice(['Buddy', 'Milo', 'Oscar'])}.",
    ]

    all_irrelevant_infos = irrelevant_infos + irrelevant_out_topic

    # Randomly add irrelevant information
    for irrelevant_info in irrelevant_infos + irrelevant_out_topic:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume the functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences + [question]

    # Calculate times and the answer
    # t1 = (distance1 * 5280) / speed1
    # t2 = (distance2 * 5280) / speed2
    # answer = t2 - t1

    answer = delta_t
    # answer = int(round(answer))

    # Return problem and answer
    cot = [f"Convert {name1}'s distance from miles to feet: {distance1} miles * 5280 = {distance1_ft} feet.", f"Convert {name2}'s distance from miles to feet: {distance2} miles * 5280 = {distance2_ft} feet.", f"Calculate the time it takes for {name1} to get home: {distance1_ft} feet / {speed1} feet per minute = {t1} minutes.", f"Calculate the time it takes for {name2} to get home: {distance2_ft} feet / {speed2} feet per minute = {t2} minutes.", f"The difference in time, or how long the winner waits, is the absolute difference between {t1} and {t2}, which is {delta_t} minutes."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': all_irrelevant_infos}
