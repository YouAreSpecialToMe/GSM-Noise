from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define capacity alternatives
    capacities = [100, 150, 200, 250, 300]
    capacity = random.choice(capacities)

    # Define city names
    cities = ['Chengli', 'Newtown', 'Springfield', 'Riverdale', 'Metropolis', 'Gotham']
    departure_city = random.choice(cities)

    # Define initial number of people
    init_people_options = [10, 20, 30, 40, 50]
    init_people = random.choice(init_people_options)

    # Define first stop people entering
    first_stop_people_options = [20, 30, 40, 50, 60]
    first_stop_people = random.choice(first_stop_people_options)

    # Second stop multiplier (fraction)
    second_stop_multiplier_options = [0.25, 0.5, 0.75, 1.0]
    second_stop_multiplier = random.choice(second_stop_multiplier_options)

    # Third stop multiplier (passengers multiplied by)
    third_stop_multiplier_options = [2, 3, 4]
    third_stop_multiplier = random.choice(third_stop_multiplier_options)

    # Additional variables for distractors
    bus_drivers = ['James', 'Maria', 'Li', 'Ahmed', 'Olga']
    bus_driver = random.choice(bus_drivers)

    # Construct the problem premises
    problem = [
        f"A bus has a capacity of {capacity} people.",
        f"When it departed {departure_city} city, it had {init_people} people.",
        f"On the first stop, {first_stop_people} people entered the bus.",
        f"On the second station, {int(second_stop_multiplier * 100)}% of the total number of people who entered the bus at the first station entered the bus.",
        f"The number of passengers on the bus multiplied by {third_stop_multiplier} at the third station."
    ]

    original_problem = problem.copy()

    # Construct irrelevant information
    irrelevant_infos = [
        f"On the first stop, {first_stop_people + random.randint(2, 15)} people entered another bus.",
        f"On the second stop, {random.uniform(0.1, 0.5) * 100:.0f}% of the people who entered the bus at the first station entered another bus.",
        f"The bus company owns {random.randint(10, 50)} buses in total.",
        f"The journey included a stop at {random.choice(cities)}."
    ]

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    question = f"Please calculate the total number of people required to fill the remaining spaces on the bus."
    original_problem.append(question)

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences + [question]

    # Compute the answer using the variables
    second_stop_people = first_stop_people * second_stop_multiplier
    total_passengers = init_people + first_stop_people + second_stop_people
    total_passengers *= third_stop_multiplier
    answer = capacity - total_passengers

    # Ensure the answer is not negative
    if answer < 0:
        answer = 0

    # Return the problem and the answer
    cot = [f"At the second station, {second_stop_multiplier} of the total number of people who entered the bus at the first station entered the bus, which is {first_stop_people} * {second_stop_multiplier}, resulting in {second_stop_people}.", f"The total number of passengers after the second station is {init_people} + {first_stop_people} + {second_stop_people}, which is {total_passengers}.", f"At the third station, the number of passengers on the bus multiplied by {third_stop_multiplier}, resulting in {total_passengers}.", f"The total number of people required to fill the remaining spaces on the bus is {capacity} - {total_passengers}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
