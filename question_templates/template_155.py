from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and items
    names = ["Julia", "David", "Alex", "Emma", "Liam", "Sophia", "Daniel", "Olivia", "Michael", "Emily"]
    items = ["boat", "kayak", "canoe", "dinghy", "sailboat"]

    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)

    # Randomly generate variables
    water_amount = random.randint(1, 5)  # liters per interval
    distance_interval = random.choice([5, 10, 15, 20])  # feet
    time_amount = random.randint(10, 30)  # seconds
    time_distance = random.choice([10, 20, 30, 40, 50])  # feet

    # Calculate speed (feet per second)
    speed = time_distance / time_amount  # ft/sec

    # Now, pick total_time_to_shore such that total_distance is reasonable
    total_time_to_shore = random.randrange(30, 121, 10)  # seconds

    # Calculate total_distance
    total_distance = speed * total_time_to_shore

    # Adjust total_distance to be multiple of distance_interval
    total_distance = distance_interval * int(total_distance / distance_interval)

    # Recalculate total_time_to_shore
    total_time_to_shore = total_distance / speed

    # Calculate number of intervals
    num_intervals = total_distance / distance_interval

    # Construct the problem sentences
    problem = [
        f"{name}'s {item} sprang a leak while {name} was out on the lake.",
        f"The {item} was taking on {water_amount} liters of water for every {distance_interval} feet {name} rowed back towards shore.",
        f"It took {name} {time_amount} seconds to row {time_distance} feet.",
        f"The shore was {int(total_time_to_shore)} seconds away."
    ]

    # Construct the question
    question = f"How much water had the {item} taken on by the time {name} reached shore?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_items = ["bottle", "bowl", "bucket", "glass", "jug"]
    irelevant_item = random.choice(irrelevant_items)
    irrelevant_infos = [
        f"The {irelevant_item} was filled on {random.randint(1,5)} liters of water for every {distance_interval} feet {name} rowed back towards shore.",
        f"The {irelevant_item} can be totally filled with {random.randint(30,70)} liters of water.",
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} had just celebrated a birthday the day before.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume functions are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except the first one
    first_sentence = problem[0]
    remaining_sentences = problem[1:]
    if shuffle:
        random.shuffle(remaining_sentences)
    problem = [first_sentence] + remaining_sentences + [question]

    # Calculate the answer
    total_water = num_intervals * water_amount
    answer = total_water

    # Return problem and answer as a dictionary
    cot = [f"Calculate the speed by dividing {time_distance} by {time_amount}, which gives {speed} feet per second.", f"Calculate the total distance to shore by multiplying {speed} by {total_time_to_shore}, resulting in {total_distance} feet.", f"Adjust the total distance to be a multiple of {distance_interval}, resulting in {total_distance}.", f"Recalculate the total time to shore by dividing {total_distance} by {speed}, which gives {total_time_to_shore} seconds.", f"Determine the number of intervals by dividing {total_distance} by {distance_interval}, resulting in {num_intervals}.", f"Calculate the total water taken on by multiplying {num_intervals} by {water_amount}, which gives {total_water} liters.", f"Therefore, the final answer is {total_water} liters."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}