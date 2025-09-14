from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible station names and item names
    station_names = ["pediatrics ward", "emergency unit", "cardiology department", "ICU", "nurses' station"]
    item_names = ["bandages", "syringes", "gloves", "masks", "IV bags", "thermometers"]

    # Randomly select a station and an item
    station_name = random.choice(station_names)
    item_name = random.choice(item_names)

    # Initialize variables
    for _ in range(100):
        # Randomly generate pack size
        pack_size = random.choice([20, 30, 40, 50, 60, 80, 100])

        # Randomly generate day1_used
        day1_used = random.randint(20, max(pack_size - 10, 20))

        # Randomly generate day1_ordered_packs
        day1_ordered_packs = random.randint(1, 3)

        # Randomly generate day2_used_diff
        day2_used_diff = random.randint(5, min(15, day1_used - 5))
        day2_used = day1_used - day2_used_diff

        # Randomly generate day3_ordered_packs
        day3_ordered_packs = random.randint(1, 3)

        # Randomly generate day3_used_packs
        day3_used_packs = random.choice([0.25, 0.5, 0.75, 1.0])
        day3_used = day3_used_packs * pack_size

        # Randomly generate ending_inventory
        ending_inventory = random.randint(50, 150)

        # Calculate total ordered and total used
        total_ordered = (day1_ordered_packs + day3_ordered_packs) * pack_size
        total_used = day1_used + day2_used + day3_used

        # Calculate initial_inventory
        initial_inventory = ending_inventory + total_used - total_ordered

        if initial_inventory >= 0 and initial_inventory == int(initial_inventory):
            break

    # Construct the problem sentences
    problem = [
        f"A {station_name} orders {item_name} in bulk packs of {pack_size}.",
        f"On the first day, the nurses used {day1_used} {item_name} and ordered {day1_ordered_packs} bulk pack{'s' if day1_ordered_packs > 1 else ''} of {item_name}.",
        f"On the second day, they used {day2_used_diff} fewer {item_name}.",
        f"On the third day, they ordered {day3_ordered_packs} bulk pack{'s' if day3_ordered_packs > 1 else ''} of {item_name} and only used {day3_used_packs} pack{'s' if day3_used_packs != 1 else ''}.",
        f"They had {ending_inventory} {item_name} left at the end of the third day."
    ]

    # Construct the question
    question = f"How many {item_name} did they start with on the first day?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"They plan to use more {item_name} the following week.",
        f"On the fourth day, they used {ending_inventory - random.randint(0,ending_inventory)} {item_name}.",
        f"On the fifth day, they ordered {random.randint(1, 3)} bulk pack{'s' if day3_ordered_packs > 1 else ''} of {item_name}."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"The hospital cafeteria serves over {random.randint(100, 500)} meals per day.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Assume introduce_symbol_error and introduce_grammar_error functions are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except the first one
    rest = problem[1:]
    if shuffle:
        random.shuffle(rest)
    problem = [problem[0]] + rest

    # Add the question
    problem.append(question)

    # Calculate the answer
    answer = initial_inventory

    # Return the problem and the answer
    cot = [f"On the second day, the nurses used {day2_used_diff} fewer {item_name} than the first day, so they used {day1_used} - {day2_used_diff}, which is {day2_used}.", f"On the third day, they used {day3_used_packs} packs of {item_name}, which is {day3_used_packs} * {pack_size}, resulting in {day3_used}.", f"The total number of {item_name} ordered is ({day1_ordered_packs} + {day3_ordered_packs}) * {pack_size}, which is {total_ordered}.", f"The total number of {item_name} used is {day1_used} + {day2_used} + {day3_used}, which is {total_used}.", f"The initial inventory of {item_name} is calculated as {ending_inventory} + {total_used} - {total_ordered}, which is {initial_inventory}.", f"Therefore, the number of {item_name} they started with on the first day is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}