import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and fish type lists
    names = ["Bob", "Alice", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah"]
    fish_types = ["orange", "white", "red", "blue", "yellow", "black"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly select two different fish types
    fish_type1, fish_type2 = random.sample(fish_types, 2)
    
    # Randomly select initial numbers of fish
    initial_num_fish_type1 = random.randint(1, 5)
    initial_num_fish_type2 = random.randint(1, 5)
    initial_total_fish = initial_num_fish_type1 + initial_num_fish_type2
    
    # Randomly select total number of fish bought from store
    num_bought = random.randint(10, 30)
    
    # Randomly select K (ratio of types in final count)
    K = random.choice([2, 3])
    
    # Try to compute num_fish_type2_bought
    N = K * initial_num_fish_type2 - (initial_num_fish_type1 + num_bought)
    denominator = - (K + 1)
    if denominator == 0 or N % denominator != 0:
        return generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error)
    num_fish_type2_bought = N // denominator
    if num_fish_type2_bought < 0 or num_fish_type2_bought > num_bought:
        return generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error)
    num_fish_type1_bought = num_bought - num_fish_type2_bought
    if num_fish_type1_bought < 0:
        return generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error)
    
    # Construct the premise content
    problem = [
        f"{name} had {initial_total_fish} fish in {name}'s ornamental fish pond.",
        f"{initial_num_fish_type1} were {fish_type1}, and {initial_num_fish_type2} were {fish_type2}.",
        f"{name} decided {name} wanted to get some more, so {name} went to the pet store.",
        f"{name} had a sales assistant at the pet shop dip out {num_bought} fish out of a mixed tank of both {fish_type1} and {fish_type2} fish.",
        f"When {name} got them home and added them to {name}'s pond, {name} found that {name} now had {K} times as many {fish_type1} fish as {fish_type2} fish."
    ]

    import copy
    original_problem = copy.deepcopy(problem)
    
    # Construct the question
    question = f"How many {fish_type2} fish did {name} buy at the store?"
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The pet store had a special offer on {fish_type1} fish.",
        f"{name} also bought fish food costing ${random.randint(5, 20)}.",
        f"There were {random.randint(50, 100)} different species of fish at the pet store."
    ]
    
    # Add out-topic irrelevant information
    out_topic_irrelevant_info = f"{name} drove a {random.choice(['red', 'blue', 'green', 'black'])} car to the store."
    irrelevant_infos.append(out_topic_irrelevant_info)
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest = problem[1:]
    if shuffle:
        random.shuffle(rest)
    problem = [first_sentence] + rest
    
    # Add symbol or grammar errors. Assume the functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]
    
    # Add the question
    problem.append(question)
    original_problem.append(question)

    # Calculate the answer
    answer = num_fish_type2_bought
    
    # Return problem and answer as a dictionary
    cot = [f"Calculate N as {K} times {initial_num_fish_type2} minus the sum of {initial_num_fish_type1} and {num_bought}, which is {N}.", f"Calculate the denominator as negative of ({K} + 1), which is {denominator}.", f"Determine the number of {fish_type2} fish bought by dividing {N} by {denominator}, resulting in {num_fish_type2_bought}.", f"Calculate the number of {fish_type1} fish bought by subtracting {num_fish_type2_bought} from {num_bought}, resulting in {num_fish_type1_bought}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}