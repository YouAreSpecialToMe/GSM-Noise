from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible variables
    farmer_names = ['Alex', 'Jordan', 'Taylor', 'Casey', 'Riley', 'Chris']
    field_items = ['hay', 'straw', 'wheat', 'corn', 'barley']
    truck_driver_names = ['Sam', 'Morgan', 'Robin', 'Drew', 'Jamie', 'Pat']

    # Randomly select names and items
    farmer_name = random.choice(farmer_names)
    field_item = random.choice(field_items)
    truck_driver_name = random.choice(truck_driver_names)

    # Define the default values
    default_farmer_rate = 5  # Bales made per hour by the farmer
    default_truck_rate = 3   # Bales picked up per hour by the truck
    default_working_hours = 6  # Working hours per day

    # Generate alternative values including the original values
    farmer_rate_options = [i for i in range(4, 11) if i != default_farmer_rate]
    farmer_rate = random.choice(farmer_rate_options + [default_farmer_rate])

    truck_rate_options = [i for i in range(2, 9) if i != default_truck_rate]
    truck_rate = random.choice(truck_rate_options + [default_truck_rate])

    working_hours_options = [i for i in range(5, 9) if i != default_working_hours]
    working_hours = random.choice(working_hours_options + [default_working_hours])

    # Construct premises, replacing values with variable names
    problem = [
        f"{farmer_name} is baling {field_item} in their field.",
        f"Each hour {farmer_name} makes {farmer_rate} bales.",
        f"At the same time, a truck driven by {truck_driver_name} is picking the {field_item} bales up.",
        f"Each hour the truck driven by {truck_driver_name} picks up {truck_rate} bales of {field_item}.",
        f"If {farmer_name} and {truck_driver_name} put in a {working_hours} hour day,"
    ]

    # Construct the question
    question = f"How many bales of {field_item} are left in the field?"
    original_problem = problem.copy()

    original_problem.append(question)

    # In-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"The field is {random.randint(10, 100)} acres.",
        f"The weather was {random.choice(['sunny', 'rainy', 'cloudy', 'windy'])} that day.",
        f"{farmer_name} started working at {random.randint(5, 9)} AM."
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{farmer_name} has a pet {random.choice(['dog', 'cat', 'parrot'])} named {random.choice(['Buddy', 'Max', 'Charlie'])}.",
        f"In their free time, {farmer_name} likes to play {random.choice(['guitar', 'chess', 'basketball'])}."
    ]

    # Combine irrelevant information
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Randomly add irrelevant information based on probability
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Introduce symbol or grammar errors (assumed to be given functions)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences except for the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question at the end
    problem.append(question)

    # Calculate the answer using the variables
    total_bales_made = farmer_rate * working_hours
    total_bales_picked = truck_rate * working_hours
    answer = total_bales_made - total_bales_picked

    # Return the problem and the answer
    cot = [f"{farmer_name} makes {farmer_rate} bales of {field_item} each hour. Over {working_hours} hours, the total bales made are {farmer_rate} * {working_hours}, which is {total_bales_made}.", f"The truck driven by {truck_driver_name} picks up {truck_rate} bales of {field_item} each hour. Over {working_hours} hours, the total bales picked up are {truck_rate} * {working_hours}, which is {total_bales_picked}.", f"The number of bales left in the field is the total bales made minus the total bales picked up, which is {total_bales_made} - {total_bales_picked}, resulting in {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
