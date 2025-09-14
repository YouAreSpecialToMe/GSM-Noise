import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define possible names
    names = ["Morgan", "Alex", "Taylor", "Jordan", "Casey", "Riley", "Hayden", "Jamie", "Cameron", "Quinn"]
    name = random.choice(names)
    
    # Budget amount
    budget_amount = random.randint(50, 200)
    budget_amount = (budget_amount // 5) * 5  # Round to nearest $5
    
    # Activity costs
    per_person_golf_cost = random.randint(3, 10)
    arcade_token_cost = random.randint(2, 10)
    go_kart_cost_per_ride = random.randint(5, 20)
    go_kart_rides = random.randint(1, 3)
    
    # In-topic irrelevant variables
    cake_cost = random.randint(10, 50)
    number_of_holes = random.choice([9, 18])
    number_of_games = random.randint(20, 100)
    
    # Out-topic irrelevant variables
    pet_animals = ["dog", "cat", "parrot", "rabbit"]
    pet_names = ["Buddy", "Max", "Charlie", "Bella", "Lucy"]
    pet_animal = random.choice(pet_animals)
    pet_name = random.choice(pet_names)
    
    # Construct the premise sentences
    problem = [
        f"{name}'s dad said that {name} had ${budget_amount} budgeted for {name}'s birthday party.",
        f"{name} wants to make sure {name} and {name}'s friends all get to play one round of mini-golf, have ${arcade_token_cost} in arcade tokens, and get to ride the go-karts {go_kart_rides} times.",
        f"A round of mini-golf is ${per_person_golf_cost}.",
        f"The go-karts cost ${go_kart_cost_per_ride} a ride.",
    ]

    import copy
    original_problem = copy.deepcopy(problem)
    
    # Construct irrelevant information
    irrelevant_infos = [
        f"{name} also wants to buy a birthday cake that costs ${cake_cost}.",
        f"The mini-golf course has {number_of_holes} holes.",
        f"The arcade has over {number_of_games} different games.",
        f"{name} has a pet {pet_animal} named {pet_name}."
    ]
    
    # Add irrelevant information based on probability
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)
    
    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences, except for the first one
    problem_first_sentence = problem[0]
    problem_rest = problem[1:]
    if shuffle:
        random.shuffle(problem_rest)
    problem = [problem_first_sentence] + problem_rest
    
    # Add the question
    question = f"How many friends can {name} invite?"
    problem.append(question)
    original_problem.append(question)
    
    # Calculate the answer
    total_cost_per_person = per_person_golf_cost + arcade_token_cost + go_kart_cost_per_ride * go_kart_rides
    number_of_people = budget_amount // total_cost_per_person
    number_of_friends = max(number_of_people - 1, 0)
    
    answer = number_of_friends
    
    # Return the problem and answer as a dictionary
    cot = [f"Calculate the total cost per person by adding the cost of mini-golf, arcade tokens, and go-kart rides: {per_person_golf_cost} + {arcade_token_cost} + {go_kart_cost_per_ride} * {go_kart_rides} = {total_cost_per_person}.", f"Determine the number of people that can be accommodated within the budget by dividing the budget by the total cost per person: {budget_amount} // {total_cost_per_person} = {number_of_people}.", f"Calculate the number of friends {name} can invite by subtracting 1 from the number of people: max({number_of_people} - 1, 0) = {number_of_friends}.", f"Therefore, the final answer is {number_of_friends}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}