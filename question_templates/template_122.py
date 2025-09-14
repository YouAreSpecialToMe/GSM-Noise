from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ["James", "Olivia", "Li Wei", "Santiago", "Fatima", "Aiko", "Mikhail", "Zara", "Amir", "Sophia"]
    items = ["plane", "yacht", "helicopter", "sports car", "motorboat", "RV"]

    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)

    # Randomly generate values
    plane_cost = random.randint(100000, 1000000)
    hanger_rent = random.randint(1000, 20000)
    months = 12  # First year

    # Construct the premises
    problem = [
        f"{name} buys a {item}.",
        f"The {item} cost ${plane_cost}.",
        f"{name} pays ${hanger_rent} a month to rent a hanger to keep it in.",
        f"{name} also spends twice as much as that on fuel per month."
    ]

    # Construct the question
    question = f"How much did it cost {name} to get and maintain the {item} for the first year?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The {item} was manufactured in {random.randint(1990, 2021)} and cost ${plane_cost + random.randint(10, 100)} at that time.",
        f"{name} took lessons that cost ${random.randint(100, 500)} per hour.",
        f"The hanger is located {random.randint(10, 100)} miles from {name}'s home."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(
        f"{name} has a pet {random.choice(['dog', 'cat', 'parrot'])} named {random.choice(['Buddy', 'Max', 'Bella', 'Charlie'])}.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume these functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    remaining_sentences = problem[1:]
    if shuffle:
        random.shuffle(remaining_sentences)
    problem = [first_sentence] + remaining_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    fuel_cost = hanger_rent * 2
    total_maintenance_cost = (hanger_rent + fuel_cost) * months
    answer = plane_cost + total_maintenance_cost

    # Return problem and answer
    cot = [f"{name} spends twice as much as the hanger rent on fuel per month, so the fuel cost is {hanger_rent} * 2, which is {fuel_cost}.", f"The total maintenance cost for the first year is ({hanger_rent} + {fuel_cost}) * {months}, which is {total_maintenance_cost}.", f"The total cost to get and maintain the {item} for the first year is {plane_cost} + {total_maintenance_cost}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
