from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
import math
# Done
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible values
    names = ["Carlos", "Alexandra", "Jamal", "Ling", "Svetlana", "Mohammed", "Fatima", "Diego", "Yuki", "Chen"]
    tree_types = ["lemon tree", "apple tree", "orange tree", "pear tree", "peach tree", "cherry tree", "mango tree", "olive tree"]

    # Randomly select values
    name = random.choice(names)
    tree_type = random.choice(tree_types)
    plant_cost = random.randint(50, 150)  # Planting cost between $50 and $150
    fruits_per_year = random.randint(5, 20)  # Number of fruits per year
    selling_price = round(random.uniform(1.0, 2.0), 2)  # Selling price per fruit between $1.00 and $2.00
    annual_cost = random.randint(1, 5)  # Cost per year to water and feed

    # Irrelevant information variables
    lifespan = random.randint(10, 50)  # Lifespan of the tree in years
    instrument = random.choice(['guitar', 'piano', 'violin', 'flute', 'drums', 'saxophone'])

    # Construct the premise content
    problem_sentences = [
        f"{name} is planting a {tree_type}.",
        f"The tree will cost ${plant_cost} to plant.",
        f"Each year it will grow {fruits_per_year} fruits, which {name} can sell for ${selling_price} each.",
        f"It costs ${annual_cost} a year to water and feed the tree."
    ]

    # Construct the question
    question = f"How many years will it take before {name} starts earning money on the {tree_type}?"
    original_problem = problem_sentences.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    irrelevant_infos = [
        f"The {tree_type} can live for up to {lifespan} years."
    ]

    # Out-topic irrelevant information
    irrelevant_infos.append(f"{name} enjoys playing the {instrument} in their spare time.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem_sentences.append(irrelevant_info)

    # Add symbol or grammar errors
    problem_sentences = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem_sentences
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem_sentences[0]
    other_sentences = problem_sentences[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    net_gain_per_year = (fruits_per_year * selling_price) - annual_cost

    # To prevent division by zero or negative net gain
    if net_gain_per_year <= 0:
        answer = None  # Indicates it will never be profitable
    else:
        division = plant_cost / net_gain_per_year
        years_needed = math.ceil(division)
        answer = years_needed

    # Return problem and answer as dictionary
    cot = [f"Each year, the {tree_type} produces {fruits_per_year} fruits, which {name} can sell for {selling_price} each. The annual cost to maintain the tree is {annual_cost}.", f"The net gain per year is calculated as ({fruits_per_year} * {selling_price}) - {annual_cost}, which is {net_gain_per_year}.", f"To find out how many years it will take to cover the initial planting cost of {plant_cost}, divide {plant_cost} by {net_gain_per_year}, resulting in {division}.", f"Since the number of years must be a whole number, round up {division} to the nearest whole number, which is {years_needed}.", f"Therefore, the answer is {years_needed} years."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
