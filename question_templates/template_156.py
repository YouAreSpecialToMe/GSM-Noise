from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define a list of diverse names
    names = ["Alice", "Bob", "Cindy", "David", "Ethan", "Fiona", "Gissela", "Gordy", "Gary", "Helen", "Ian", "Jenny",
             "Kevin", "Laura", "Mike", "Nina", "Oliver", "Paula", "Quincy", "Rachel", "Steve", "Tracy", "Uma", "Victor",
             "Wendy", "Xavier", "Yvonne", "Zach"]

    # Randomly select 3 unique names
    drivers = random.sample(names, 6)
    driver1 = drivers[0]
    driver2 = drivers[1]
    driver3 = drivers[2]
    irrelevant_driver1 = drivers[3]
    irrelevant_driver2 = drivers[4]
    irrelevant_driver3 = drivers[5]

    # Randomly assign capacities
    driver1_capacity = random.choice(range(1000, 5500, 500))  # 1000 to 5000, step 500
    driver2_capacity_increase = random.choice(range(100, 2500, 100))  # 100 to 2400, step 100

    # Ensure total capacity is enough so that driver3_capacity is positive
    min_total_capacity = 2 * driver1_capacity + driver2_capacity_increase + 500
    max_total_capacity = min_total_capacity + 5000

    while True:
        total_capacity = random.choice(range(min_total_capacity, max_total_capacity + 500, 500))
        driver3_capacity = total_capacity - driver1_capacity - (driver1_capacity + driver2_capacity_increase)
        if driver3_capacity > 0:
            break

    # Construct the premises
    problem = [
        f"{driver1}, {driver2}, and {driver3} are truck drivers.",
        f"{driver1} has a truck large enough to haul {driver1_capacity} pounds of gravel.",
        f"{driver2}'s truck can haul {driver2_capacity_increase} pounds more than {driver1}'s truck.",
        f"When {driver3} brings {driver3}'s truck and joins {driver1} and {driver2}, the three trucks combined can haul a total of {total_capacity} pounds of gravel."
    ]

    # Construct the question
    question = f"How many pounds of gravel can {driver3}'s truck carry?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Prepare in-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"{irrelevant_driver1} has a truck that can haul {driver1_capacity + random.randint(1, 10)} pounds of gravel.",
        f"{irrelevant_driver2}'s car can carry {driver2_capacity_increase + random.randint(5, 15)} pounds more than {driver1}'s truck.",
        f"{irrelevant_driver3}'s truck can haul a total pounds of the {driver1}'s and {irrelevant_driver1}'s trucks combined."
    ]

    # Prepare out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{driver1} is an excellent chess player who competes nationally.",
    ]

    all_irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Combine irrelevant information and randomly include it based on prob_irre
    irrelevant_infos = []
    for info in in_topic_irrelevant_infos + out_topic_irrelevant_infos:
        if random.random() < prob_irre:
            irrelevant_infos.append(info)

    # Add irrelevant infos to problem
    problem.extend(irrelevant_infos)

    # Apply symbol or grammar errors to problem sentences
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in problem
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
    # driver3_capacity = total_capacity - driver1_capacity - (driver1_capacity + driver2_capacity_increase)
    answer = driver3_capacity

    # Return problem and answer
    cot = [f"The total capacity of the three trucks is {total_capacity}.", f"{driver1}'s truck can haul {driver1_capacity} pounds of gravel.", f"{driver2}'s truck can haul {driver2_capacity_increase} pounds more than {driver1}'s truck, which is {driver1_capacity + driver2_capacity_increase}.", f"Therefore, {driver3}'s truck can carry {total_capacity} - {driver1_capacity} - ({driver1_capacity} + {driver2_capacity_increase}), which is {driver3_capacity}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': all_irrelevant_infos}
