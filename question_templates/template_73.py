import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define possible values for variables
    order_quantities = [i * 10 for i in range(20, 81)]  # From 200 to 800
    total_workers = 5  # Keeping it at 5 for the structure of the problem
    shift_hours_list = [8, 9, 10, 11, 12]
    group1_workers = 2
    group1_rates_list = [i for i in range(5, 11)]  # From 5 to 10 toys/hour
    group2_workers = 2
    group2_rates_list = [i for i in range(3, 7)]  # From 3 to 6 toys/hour
    remaining_toys_list = [i * 10 for i in range(1, 6)]  # 10, 20, 30, 40, 50

    # Randomly assign the variables
    order_quantity = random.choice(order_quantities)
    shift_hours = random.choice(shift_hours_list)
    group1_rate = random.choice(group1_rates_list)
    group2_rate = random.choice(group2_rates_list)
    remaining_toys = random.choice(remaining_toys_list)

    # Create irrelevant information variables
    extra_worker_rate = random.randint(2, 10)
    extra_order = random.randint(50, 200)
    break_time = random.randint(30, 60)
    city_population = random.randint(100000, 1000000)

    # Construct the premise content
    problem = [
        f"A toy manufacturer receives an order for {order_quantity} toys.",
        f"{total_workers} workers are available to work on the order.",
        f"{group1_workers} of the workers produce {group1_rate} toys an hour, and another {group2_workers} workers produce {group2_rate} toys an hour.",
        f"They all work on the order during their {shift_hours}-hour shift, and by the end of their shift the manufacturer still needs another {remaining_toys} toys to be able to ship the order.",
    ]

    import copy
    original_problem = copy.deepcopy(problem)

    # Add in-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"There was an extra worker who produced {extra_worker_rate} toys per hour but was assigned to a different project.",
        # f"The workers took a {break_time}-minute break during their shift.",
        f"The manufacturer previously had an order of {extra_order} toys last month."
    ]

    # Add out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"The factory is located in a city with a population of {city_population}.",
        f"The CEO of the company likes to play golf on weekends."
    ]

    # Combine irrelevant information
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    def introduce_grammar_error(text, prob):
        return text  # Assume function is given

    def introduce_symbol_error(text, prob):
        return text  # Assume function is given

    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the problem except the first sentence
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question
    question = f"How many toys per hour does the fifth worker produce?"
    problem.append(question)
    original_problem.append(question)

    # Calculate the answer
    total_known_production = (
        group1_workers * group1_rate + group2_workers * group2_rate
    ) * shift_hours
    required_total_production = order_quantity - remaining_toys
    answer = (required_total_production - total_known_production) / shift_hours

    # Return premise and answer as a dictionary
    cot = [f"Calculate the total production of the known workers: ({group1_workers} * {group1_rate} + {group2_workers} * {group2_rate}) * {shift_hours}, which is {total_known_production}.", f"Determine the required total production by subtracting the remaining toys from the order quantity: {order_quantity} - {remaining_toys}, which is {required_total_production}.", f"Calculate the production rate of the fifth worker: ({required_total_production} - {total_known_production}) / {shift_hours}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}