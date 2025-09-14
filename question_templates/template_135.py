from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and product lists
    names = ["Tanya", "Alex", "Jordan", "Casey", "Morgan", "Taylor", "Riley", "Jamie", "Cameron"]
    products = ['salt scrub', 'body butter', 'lip balm', 'facial mask', 'hair conditioner']
    
    # Randomly select a name and a product
    name = random.choice(names)
    product = random.choice(products)
    
    # Define ingredients
    ingredients = ['salt', 'oil', 'fragrance', 'citrus zest', 'sugar']
    
    # Define total volume
    total_volume = random.randint(8, 20)  # Ounces
    
    # Construct the premises with variable placeholders
    problem = [
        f"{name} makes a {product} from {', '.join(ingredients)}.",
        f"{name} makes enough to fill a {total_volume}-ounce jar each time.",
        f"{name} uses the same amount of citrus zest as fragrance and the same amount of salt as sugar.",
        f"{name} uses twice as much oil as salt and twice as much salt as zest."
    ]
    
    # Construct the question
    question = f"How many ounces of oil does {name} use?"

    original_problem = problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The {product} is very popular among {name}'s friends.",
        f"{name} spends 2 hours to make each batch of {product}.",
        f"She sells each jar of {product} for $15."
    ]
    
    # Add out-topic irrelevant information
    out_topic_irrelevant_info = [
        f"In her free time, {name} enjoys hiking and photography."
    ]
    
    # Combine and add irrelevant information based on probability
    all_irrelevant_infos = irrelevant_infos + out_topic_irrelevant_info
    for info in all_irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)
    
    # Add symbol or grammar errors (assuming the functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error), 
            prob_symbol_error
        ) for sentence in problem
    ]
    
    # Shuffle the problem sentences (except for the first one)
    middle = problem[1:]
    if shuffle:
        random.shuffle(middle)
    problem = [problem[0]] + middle
    
    # Add the question at the end
    problem.append(question)
    
    # Calculate the answer
    z = total_volume / 10  # Amount of zest and fragrance
    salt = 2 * z
    oil = 2 * salt  # Amount of oil
    answer = oil  # Answer in ounces

    cot = [f"{name} uses the same amount of citrus zest as fragrance, and the total volume is divided equally among the ingredients. Therefore, the amount of zest is {total_volume} / 10, which is {z}.", f"Since {name} uses twice as much salt as zest, the amount of salt is 2 * {z}, which is {salt}.", f"{name} uses twice as much oil as salt, so the amount of oil is 2 * {salt}, which is {oil}.", f"Therefore, the final answer is the amount of oil, which is {oil} ounces."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': all_irrelevant_infos}
