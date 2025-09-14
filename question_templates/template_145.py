from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible alternative values
    names = ["Dean", "Alice", "Bob", "Charlie", "Grace", "Helen", "Ian", "Jenna", "Kevin", "Laura"]
    toy_stores = ["toy store", "bookstore", "game shop", "pet shop", "candy store"]
    toy1_list = ["toy car", "rubber duck", "action figure", "yo-yo", "marble"]
    toy2_list = ["teddy bear", "doll", "puzzle", "kite", "stuffed animal"]
    toy3_list = ["ball", "frisbee", "jump rope", "skipping rope", "hula hoop"]
    toy4_list = ["board game", "card game", "jigsaw puzzle", "video game", "building blocks"]

    # Randomly assign variables
    name = random.choice(names)
    mother = f"{name}'s mother"
    toy_store = random.choice(toy_stores)
    toy1 = random.choice(toy1_list)
    toy2 = random.choice(toy2_list)
    money_given = random.randint(20, 50)  # Starting amount of money
    num_toy1 = random.randint(2, 10)
    num_toy2 = random.randint(2, 10)
    cost_toy1 = random.randint(1, 5)
    cost_toy2 = random.randint(1, 5)
    extra_money = random.randint(5, 20)

    # Irrelevant variables
    toy3 = random.choice(toy3_list)
    toy4 = random.choice(toy4_list)
    friend_name = random.choice(["Sam", "Alex", "Jordan", "Taylor", "Morgan", "Riley"])
    friend_age = random.randint(5, 15)
    year_established = random.randint(1950, 2023)
    store_owner = random.choice(["Mr. Smith", "Mrs. Johnson", "Ms. Lee", "Dr. Brown"])

    # Break the problem into sentences with variable placeholders
    problem = [
        f"{mother} gave {name} ${money_given} to go to the {toy_store}.",
        f"{name} bought {num_toy1} {toy1}s and {num_toy2} {toy2}s.",
        f"Each {toy1} cost ${cost_toy1} and each {toy2} cost ${cost_toy2}.",
        f"{mother} then feels generous and decides to give {name} an extra ${extra_money}.",
    ]

    # Construct the question
    question = f"How much money does {name} have left?"

    original_problem = problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    irrelevant_infos = [
        f"Each {toy3} costs ${random.randint(1, 5)} and each {toy4} costs ${random.randint(1, 5)}.",
        f"{friend_name} bought {random.randint(1, 5)} {toy3}s and {random.randint(1, 5)} {toy4}s.",
        f"{friend_name} bought {random.randint(1, 5)} {toy1}s and {random.randint(1, 5)} {toy2}s.",
    ]

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (assume functions are provided)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences except for the first one
    first_sentence = problem[0]
    rest_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_sentences)
    problem = [first_sentence] + rest_sentences

    # Add the question at the end
    problem.append(question)

    # Calculate the answer
    total_spent = num_toy1 * cost_toy1 + num_toy2 * cost_toy2
    money_left = money_given - total_spent + extra_money
    answer = money_left

    # Return the problem and the answer
    cot = [f"{name} bought {num_toy1} {toy1}s and {num_toy2} {toy2}s. Each {toy1} costs {cost_toy1} and each {toy2} costs {cost_toy2}. Therefore, the total spent is {num_toy1} * {cost_toy1} + {num_toy2} * {cost_toy2}, which is {total_spent}.", f"{mother} gave {name} ${money_given} initially. After spending {total_spent}, {name} has {money_given} - {total_spent} left.", f"{mother} then gives {name} an extra ${extra_money}. Therefore, the total money left is {money_given} - {total_spent} + {extra_money}, which is {money_left}.", f"Thus, the final answer is {money_left}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
