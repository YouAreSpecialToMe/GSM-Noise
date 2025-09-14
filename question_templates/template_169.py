from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ["Daniel", "Alice", "Bob", "Cindy", "David", "Eva", "Frank", "Grace", "Helen", "Ivan",
             "Julia", "Kevin", "Linda", "Mike", "Nina", "Oscar", "Paula", "Quincy", "Rachel", "Steve",
             "Tracy", "Uma", "Victor", "Wendy", "Xander", "Yvonne", "Zach"]
    items = ['notebook', 'pen', 'calculator', 'geometry set', 'eraser', 'ruler', 'highlighter', 'backpack']
    base_prices = {
        'notebook': 1.50,
        'pen': 0.25,
        'calculator': 12.00,
        'geometry set': 10.00,
        'eraser': 0.75,
        'ruler': 1.00,
        'highlighter': 1.25,
        'backpack': 25.00,
    }
    base_quantities = {
        'notebook': 5,
        'pen': 2,
        'calculator': 1,
        'geometry set': 1,
        'eraser': 3,
        'ruler': 2,
        'highlighter': 4,
        'backpack': 1,
    }

    # Randomly select a name
    name = random.choice(names)

    # Randomly select items to be purchased
    num_items_to_buy = random.randint(3, 5)
    selected_items = random.sample(items, num_items_to_buy)

    # Initialize dictionaries for prices and quantities
    prices = {}
    quantities = {}

    # Discount percentage
    if name == 'Daniel':
        # Use original values to match the ground truth answer
        selected_items = ['notebook', 'pen', 'calculator', 'geometry set']
        prices = {item: base_prices[item] for item in selected_items}
        quantities = {item: base_quantities[item] for item in selected_items}
        discount = 10
    else:
        # Randomize prices and quantities
        for item in selected_items:
            fluctuation = base_prices[item] * round(random.uniform(0.05, 0.75), 2)
            prices[item] = round(random.uniform(base_prices[item] - fluctuation, base_prices[item] + fluctuation), 2)
            quantities[item] = random.randint(1, 10)
        discount = random.randint(0, 30)

    # Construct the premises
    problem = [f"A shop sells school supplies."]
    for item in selected_items:
        problem.append(f"One {item} is sold at ${prices[item]:.2f} each.")
    study_field = random.choice(['engineering', 'medical', 'law', 'business', 'art', 'computer science'])
    items_str = ', '.join(
        [f"{quantities[item]} {item}{'s' if quantities[item] > 1 else ''}" for item in selected_items])
    problem.append(f"{name} is a {study_field} student, and {name} wants to buy {items_str}.")
    problem.append(f"The shop gives a {discount}% discount on all the purchased items.")

    # Construct the question
    question = f"How much does {name} have to spend on all the items {name} wants to buy?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic and out-topic irrelevant information
    in_topic_irrelevant_infos = []
    irrelevant_items = items.copy()
    for tmp_item in selected_items:
        irrelevant_items.remove(tmp_item)
    irrelevant_selected_items = random.sample(irrelevant_items, 3)
    for irrelevant_item in irrelevant_selected_items:
        irrelevant_price = round(random.uniform(0.5, 2.5) * base_prices[irrelevant_item], 2)
        in_topic_irrelevant_infos.append(f"One {irrelevant_item} is sold at ${irrelevant_price:.2f} each.")

    out_topic_irrelevant_infos = [
        f"{name} enjoys {random.choice(['playing soccer', 'reading books', 'coding'])} during free time.",
    ]
    for info in in_topic_irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)
    for info in out_topic_irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Add symbol or grammar errors (assumed to be given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    problem_body = problem[1:]
    if shuffle:
        random.shuffle(problem_body)
    problem = [problem[0]] + problem_body

    # Add the question
    problem.append(question)

    # Calculate the answer
    total_cost = sum(prices[item] * quantities[item] for item in selected_items)
    total_cost_after_discount = total_cost * ((100 - discount) / 100)
    answer = round(total_cost_after_discount, 2)

    # Return the problem and answer
    cot = [f"Calculate the total cost by summing up the product of price and quantity for each item in {selected_items}. This gives us {total_cost}.", f"Apply the discount of {discount}% to the total cost. The total cost after discount is {total_cost} * ((100 - {discount}) / 100), which is {total_cost_after_discount}.", f"Round the total cost after discount to two decimal places to get the final answer, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
