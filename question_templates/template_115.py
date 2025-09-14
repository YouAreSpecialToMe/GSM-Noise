from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and item lists
    company_names = ["DairyCo", "Farm Fresh", "Healthy Harvest", "Organic Valley", "Pure Milk Inc", "Green Pastures"]
    buyer_names = ["Mr. Marcellus", "Mrs. Smith", "Dr. Johnson", "Ms. Lee", "Prof. Brown", "Captain Davis"]
    products = ["milk in jars", "orange juice", "almond milk", "soy milk", "goat milk", "chocolate milk"]
    fractions = [(1, 2), (1, 3), (2, 5), (3, 4)]  # Numerator, Denominator

    # Randomly select names, product, fraction
    company_name = random.choice(company_names)
    buyer_name = random.choice(buyer_names)
    product = random.choice(products)
    fraction_numerator, fraction_denominator = random.choice(fractions)
    expired_fraction = fraction_numerator / fraction_denominator

    # Randomly generate numeric values
    amount_sold = random.randint(1000, 10000) // 1000 * 1000  # Round to nearest 1000
    cost_per_unit = round(random.uniform(1.0, 10.0), 1)

    # Construct the premise content
    problem = [
        f"{company_name} sold {amount_sold} gallons of {product} to {buyer_name}'s store at the cost of ${cost_per_unit} per gallon.",
        f"However, {buyer_name} later realized {fraction_numerator}/{fraction_denominator} of the amount of {product} he purchased had passed the expiry date and could not be sold.",
        f"{buyer_name} returned the sour {product} to {company_name} and ordered a refund."
    ]

    # Construct the question
    question = f"Calculate how much he got in refunds."

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    in_topic_irrelevant_infos = [
        # f"{company_name} also sells cheese and yogurt.",
        f"The {company_name} sold {buyer_name} {amount_sold * 2 - 4} gallons of oil."
        f"The {product} was packaged in eco-friendly jars.",
        f"{buyer_name} had also purchased 500 gallons of ice cream from {company_name} earlier."
    ]

    # Add out-topic irrelevant information
    out_topic_irrelevant_infos = [
        # f"{buyer_name} recently went on vacation.",
        # f"{company_name} is planning to expand to Europe.",
        f"On the same day, {buyer_name} bought a new car."
    ]

    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    random.shuffle(irrelevant_infos)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors, assume the functions are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences

    problem.append(question)

    # Calculate the answer
    answer = amount_sold * expired_fraction * cost_per_unit

    # Return premise and answer as a dictionary
    cot = [f"The fraction of the {product} that expired is {fraction_numerator}/{fraction_denominator}, which is {expired_fraction}.", f"The total amount of expired {product} is {amount_sold} * {expired_fraction}.", f"The refund amount is the total expired {product} multiplied by the cost per unit, which is {amount_sold} * {expired_fraction} * {cost_per_unit}.", f"Therefore, the refund amount is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
