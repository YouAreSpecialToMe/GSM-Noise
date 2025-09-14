from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define name list
    names = ["Walter", "Alice", "Bob", "Carmen", "Diana", "Ethan", "Fiona", "George", "Hannah", "Isla"]

    # Randomly select a name
    name = random.choice(names)

    # Randomly generate amounts collected
    neighbor_amount = random.randint(100, 1000)      # Amount collected from neighbors
    online_fund_amount = random.randint(1000, 5000)  # Amount collected from online fund
    friend_amount = random.randint(100, 500)         # Amount collected from friend
    lawyer_multiplier = random.randint(2, 5)         # Multiplier offered by lawyer

    # Construct the premise content, breaking it down into sentences
    problem = [
        f"{name} is collecting money for charity.",
        f"First {name} collects ${neighbor_amount} from {name}'s neighbors.",
        f"Then {name} collects ${online_fund_amount} from a fund {name} set up online.",
        f"{name}'s lawyer offers to donate {lawyer_multiplier} times as much as everyone else donates.",
        f"{name} is going to tell him about {name}'s neighbors and the online fund until {name}'s friend gives {name} ${friend_amount} as well."
    ]

    # Construct the question
    question = f"How much is {name}'s lawyer going to contribute?"
    original_problem=problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    total_charity_goal = random.randint(5000, 10000)
    previous_charity_event_amount = random.randint(2000, 8000)
    irrelevant_infos = [
        f"The total goal for the charity is ${total_charity_goal}.",
        f"At a previous charity event, {name} collected ${previous_charity_event_amount}.",
    ]

    # Add out-topic irrelevant information
    ir_money = random.randint(1000, 5000)
    gender = random.choice(["boy", "girl"])
    out_topic_irrelevant_info = f"{name} is a {gender} who has more than ${ir_money} saved up."
    irrelevant_infos.append(out_topic_irrelevant_info)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume that these functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    problem_rest = problem[1:]
    if shuffle:
        random.shuffle(problem_rest)
    problem = [problem[0]] + problem_rest

    # Add the question
    problem.append(question)

    # Calculate the answer
    total_collected = neighbor_amount + online_fund_amount + friend_amount
    answer = lawyer_multiplier * total_collected

    # Return the problem and answer as a dictionary
    cot = [f"{name} collects a total of {neighbor_amount} from neighbors, {online_fund_amount} from an online fund, and {friend_amount} from a friend. Therefore, the total amount collected is {neighbor_amount} + {online_fund_amount} + {friend_amount}, which is {total_collected}.", f"{name}'s lawyer offers to donate {lawyer_multiplier} times the total collected amount. Therefore, the lawyer's contribution is {lawyer_multiplier} * {total_collected}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
