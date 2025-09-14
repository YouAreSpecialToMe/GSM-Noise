from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
import math

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define lists of organization types and activities
    org_types = ["charity group", "school club", "community center", "youth organization", "non-profit"]
    activities = ["yard sale", "bake sale", "fundraising event", "auction", "book fair"]

    # Randomly select organization type and activity
    org = random.choice(org_types)
    activity = random.choice(activities)

    # Randomly select numbers within reasonable ranges
    people = random.randint(5, 20)  # Number of people donating
    boxes_per_person = random.randint(2, 10)  # Number of boxes each
    boxes_already = random.randint(5, 20)  # Boxes they already have
    boxes_per_table = random.randint(1, 5)  # Boxes per table
    tables_already_have = random.randint(5, 20)  # Number of tables they already have

    # Other irrelevant info variables
    total_members = random.randint(20, 100)
    event_duration = random.randint(2, 8)  # Event duration in hours
    money_goal = random.randint(500, 5000)  # Fundraising goal in dollars
    ticket_price = random.randint(1, 20)  # Price of event ticket
    raised_last_year = random.randint(1000, 10000)
    person_name = random.choice(["John", "Mary", "Susan", "Peter", "Alex", "Emily"])

    # Break problem into sentences, using variable names in curly braces
    problem = [
        f"A {org} decides to do a {activity}.",
        f"{people} people donate {boxes_per_person} boxes of stuff each.",
        f"They also have {boxes_already} boxes of stuff already.",
        f"They can fit {boxes_per_table} boxes worth of stuff per table.",
    ]
    question= f"If they already own {tables_already_have} tables, how many new tables do they need?"
    original_problem=problem.copy()
    original_problem.append(question)
    
    # Construct in-topic irrelevant information
    irrelevant_infos = [
        f"The {org} has {total_members} members.",
        f"The {activity} will last {event_duration} hours.",
        f"Their fundraising goal is ${money_goal}.",
        f"They are selling tickets at ${ticket_price} each.",
        f"Last year, they raised ${raised_last_year}.",
        f"{person_name} is responsible for organizing the {activity}.",
        f"The weather forecast predicts sunny skies for the day of the {activity}.",
        f"The {activity} will take place at the local park."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{person_name} is learning to play the piano.")
    irrelevant_infos.append(f"The local football team won their last game.")

    # Add irrelevant information based on probability
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Shuffle some sentences except for the first one
    problem_start = problem[0]
    problem_rest = problem[1:]
    if shuffle:
        random.shuffle(problem_rest)
    problem = [problem_start] + problem_rest+[question]

    # Add grammar and symbol errors (assumed functions)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]

    # Calculate the answer
    total_boxes = people * boxes_per_person + boxes_already
    total_tables_needed = math.ceil(total_boxes / boxes_per_table)
    answer = max(0, total_tables_needed - tables_already_have)

    # Return problem and answer
    cot = [f"Calculate the total number of boxes by multiplying the number of {people} by the {boxes_per_person} each donates and adding the {boxes_already} they already have, resulting in {total_boxes}.", f"Determine the total number of tables needed by dividing {total_boxes} by {boxes_per_table} and rounding up to the nearest whole number, which gives {total_tables_needed}.", f"Subtract the {tables_already_have} from {total_tables_needed} to find out how many new tables are needed, ensuring the result is not negative, resulting in {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
