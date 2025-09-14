import random
import math
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define possible values for variables
    names = ["Maddy", "Alex", "Sam", "Taylor", "Jordan", "Casey", "Jamie", "Riley", "Cameron", "Morgan"]
    relatives = ["brother", "sister", "cousin", "friend", "nephew", "niece", "grandchild"]
    events = ["soccer game", "basketball match", "swimming competition", "debate tournament", "dance recital", "school play"]
    
    name = random.choice(names)
    relative = random.choice(relatives)
    event = random.choice(events)
    
    team_members = random.randint(10, 20)
    coaches = random.randint(1, 5)
    guests_per_member = random.randint(1, 3)
    people_per_pizza = random.randint(2, 5)
    cost_per_pizza = random.randint(10, 20)
    
    coach_guests = random.randint(0, 2)
    sides = random.randint(1, 10)
    pet = random.choice(["dog", "cat", "parrot", "hamster"])
    pet_age = random.randint(1, 15)
    
    # Construct the premises
    problem = [
        f"{name} is buying pizza for {name}'s {relative}'s {event}.",
        f"There are {team_members} team members and {coaches} coaches.",
        f"Each team member brings {guests_per_member} guests.",
        f"A pizza will serve {people_per_pizza} people.",
        f"Each pizza costs ${cost_per_pizza}."
    ]

    import copy
    original_problem = copy.deepcopy(problem)
    
    # Construct the question
    question = f"How many dollars will {name} spend?"
    
    # Construct irrelevant information
    in_topic_irrelevant_infos = [
        # f"Each coach brings {coach_guests} guests.", # This is actually relevant
        # f"They also order {sides} sides of garlic bread." # This is actually relevant 
    ]
    
    out_topic_irrelevant_info = f"{name} has a pet {pet} that is {pet_age} years old."
    
    # Add irrelevant information based on probability
    for info in in_topic_irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)
    
    if random.random() < prob_irre:
        problem.append(out_topic_irrelevant_info)
    
    # Add symbol or grammar errors. Assume these functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences, except for the first one
    if len(problem) > 1:
        first_sentence = problem[0]
        rest = problem[1:]
        if shuffle:
            random.shuffle(rest)
        problem = [first_sentence] + rest
    
    # Add the question
    problem.append(question)
    original_problem.append(question)
    
    # Calculate the answer
    total_people = team_members + coaches + (team_members * guests_per_member)
    number_of_pizzas = math.ceil(total_people / people_per_pizza)
    answer = number_of_pizzas * cost_per_pizza
    
    # Return the problem and answer as a dictionary
    cot = [f"Calculate the total number of people by adding {team_members} team members, {coaches} coaches, and {team_members} * {guests_per_member} guests, which gives {total_people}.", f"Determine the number of pizzas needed by dividing {total_people} by {people_per_pizza} and rounding up, resulting in {number_of_pizzas} pizzas.", f"Calculate the total cost by multiplying {number_of_pizzas} by {cost_per_pizza}, which equals {answer} dollars."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': in_topic_irrelevant_infos + [out_topic_irrelevant_info]}