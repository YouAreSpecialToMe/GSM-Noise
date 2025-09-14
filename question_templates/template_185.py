from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names lists
    names = ["Alice", "Beth", "Carol", "Diana", "Emma", "Fiona", "Grace", "Hannah", "Isla", "Jennifer", "Katie", "Luna", "Mia", "Nora", "Olivia", "Paula", "Quinn", "Ruby", "Sophia", "Tina", "Uma", "Violet", "Wendy", "Xena", "Yara", "Zoe"]
    
    # Randomly select two different names
    name1, name2 = random.sample(names, 2)
    
    # Define item list
    items = ["signatures", "autographs", "photographs", "stickers", "postcards", "souvenirs"]
    item = random.choice(items)
    
    # Variables with original values to match ground truth answer
    weeks_passed = 5
    weeks_remaining = 3
    c1 = 20  # {name1}'s collection count
    c2 = 44  # {name2}'s collection count
    target = 100  # Target total collection
    
    # Construct the premise content
    problem = [
        f"{name1} and {name2} are sisters from Los Angeles who love collecting {item} from celebrities.",
        f"During their summer break from school, the sisters spend every afternoon collecting {item}.",
        f"After {weeks_passed} weeks, {name1} and {name2} compare their collections, counting up the number of {item} each sister has collected.",
        f"{name1} has {c1} {item} in her collection, and {name2} has {c2}.",
        f"The sisters have {weeks_remaining} more weeks of summer vacation, and they decide they want to reach {target} {item} between them by the end of the summer."
    ]
    
    # Construct the question
    question = f"How many {item} do the sisters need to collect to reach their goal?"
    original_problem = problem.copy()
    original_problem.append(question)
    # In-topic irrelevant information
    irrelevant_infos = [
        f"{name1} plans to attend a celebrity meet-and-greet next week.",
        f"{name2} just purchased a new album by her favorite singer.",
        f"{name1} and {name2} are planning a trip to Disneyland next month."
    ]

    # Out-topic irrelevant information
    irrelevant_out_info = [
        f"Their cousin is training for a marathon in the fall.",
        f"{name2} adopted a kitten named Bella recently."
    ]
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos + irrelevant_out_info:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Shuffle the order of sentences, except the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem
    
    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    answer = target - (c1 + c2)
    
    # Return problem and answer
    cot = [f"The total number of {item} collected by {name1} and {name2} is {c1} + {c2}.", f"Their goal is to collect {target} {item} in total.", f"The number of {item} they still need to collect is {target} - ({c1} + {c2}), which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
