from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and days
    names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Jamie", "Dakota", "Riley", "Cameron"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Assign a random name for the mechanic
    mechanic_name = random.choice(names)

    # Randomly select two different days
    day1 = random.choice(days)
    remaining_days = days.copy()
    remaining_days.remove(day1)
    day2 = random.choice(remaining_days)

    # Randomly assign rates for truck and car tire repairs
    truck_tire_rate = random.randint(50, 100)
    car_tire_rate = random.randint(30, 80)

    # Randomly assign the number of tires repaired on each day
    truck_tires_day1 = random.randint(0, 10)
    car_tires_day1 = random.randint(0, 10)
    truck_tires_day2 = random.randint(0, 10)
    car_tires_day2 = random.randint(0, 20)

    # Ensure at least one tire is repaired each day
    if truck_tires_day1 == 0 and car_tires_day1 == 0:
        truck_tires_day1 = random.randint(1, 10)
    if truck_tires_day2 == 0 and car_tires_day2 == 0:
        car_tires_day2 = random.randint(1, 20)

    # Compute revenues for each day
    revenue_day1 = (truck_tire_rate * truck_tires_day1) + (car_tire_rate * car_tires_day1)
    revenue_day2 = (truck_tire_rate * truck_tires_day2) + (car_tire_rate * car_tires_day2)

    # Ensure revenues are not equal
    while revenue_day1 == revenue_day2:
        truck_tires_day1 = random.randint(0, 10)
        car_tires_day1 = random.randint(0, 10)
        truck_tires_day2 = random.randint(0, 10)
        car_tires_day2 = random.randint(0, 20)
        revenue_day1 = (truck_tire_rate * truck_tires_day1) + (car_tire_rate * car_tires_day1)
        revenue_day2 = (truck_tire_rate * truck_tires_day2) + (car_tire_rate * car_tires_day2)

    # Construct the premises
    problem = [
        f"{mechanic_name} is a mechanic who charges different rates to repair the tires of trucks and cars.",
        f"For each truck tire that is repaired, {mechanic_name} will charge ${truck_tire_rate}.",
        f"For each car tire that is repaired, {mechanic_name} will charge ${car_tire_rate}.",
        f"On {day1}, {mechanic_name} repairs {truck_tires_day1} truck tires and {car_tires_day1} car tires.",
        f"On {day2}, {mechanic_name} repairs {truck_tires_day2} truck tires and {car_tires_day2} car tires."
    ]

    # Construct the question
    question = f"How much more revenue did {mechanic_name} earn on the day with higher revenue?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    remaining_days2 = days.copy()
    remaining_days2.remove(day1)
    remaining_days2.remove(day2)
    day3 = random.choice(remaining_days2)
    remaining_days2.remove(day3)
    day4 = random.choice(remaining_days2)
    irrelevant_infos = [
        f"{mechanic_name} recently bought a new tool set costing ${random.randint(200, 1000)}.",
        f"on {day3}, {mechanic_name} repaired 0 truck tire and 0 car tire.",
        f"on {day4}, {mechanic_name} repaired 0 truck tire and 0 car tire."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{mechanic_name} enjoys hiking during the weekends.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (Assume the functions are given)
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
    problem = [first_sentence] + other_sentences

    # Append the question
    problem.append(question)

    # Calculate the answer
    max_revenue = max(revenue_day1, revenue_day2)
    min_revenue = min(revenue_day1, revenue_day2)
    answer = max_revenue - min_revenue

    # Ensure that the derived answer matches the ground truth when using original variable values
    initial_values = {
        'truck_tire_rate': 60,
        'car_tire_rate': 40,
        'truck_tires_day1': 6,
        'car_tires_day1': 4,
        'truck_tires_day2': 0,
        'car_tires_day2': 12
    }
    revenue_day1_initial = (initial_values['truck_tire_rate'] * initial_values['truck_tires_day1']) + \
                           (initial_values['car_tire_rate'] * initial_values['car_tires_day1'])
    revenue_day2_initial = (initial_values['truck_tire_rate'] * initial_values['truck_tires_day2']) + \
                           (initial_values['car_tire_rate'] * initial_values['car_tires_day2'])
    max_revenue_initial = max(revenue_day1_initial, revenue_day2_initial)
    min_revenue_initial = min(revenue_day1_initial, revenue_day2_initial)
    ground_truth_answer = max_revenue_initial - min_revenue_initial

    assert ground_truth_answer == 40, "The ground truth answer does not match when using original values."

    # Return the problem and answer
    cot = [f"Calculate the revenue for the first day: {revenue_day1} = ({truck_tire_rate} * {truck_tires_day1}) + ({car_tire_rate} * {car_tires_day1}).", f"Calculate the revenue for the second day: {revenue_day2} = ({truck_tire_rate} * {truck_tires_day2}) + ({car_tire_rate} * {car_tires_day2}).", f"Determine the maximum revenue between the two days: {max_revenue} = max({revenue_day1}, {revenue_day2}).", f"Determine the minimum revenue between the two days: {min_revenue} = min({revenue_day1}, {revenue_day2}).", f"Calculate the difference in revenue between the day with higher revenue and the day with lower revenue: {answer} = {max_revenue} - {min_revenue}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}