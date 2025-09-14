from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define possible names
    names = ["Greg", "James", "Luke", "Ethan", "Liam", "Noah", "Oliver", "Mason", "Logan", "Lucas", "Emma", "Olivia",
             "Ava", "Isabella", "Sophia"]

    # Define items
    items = ["flavored jello", "chocolate pudding", "fruit snacks", "mini cupcakes", "cookies", "candy bars"]

    # Define possible box weights (ounces)
    box_weights = [1, 2, 3, 4, 5]

    # Define possible cups per box
    cups_per_box_options = [5, 10, 15, 20]

    # Number of kids
    num_kids_options = list(range(10, 50))

    # Cups per kid
    cups_per_kid_options = list(range(1, 6))

    # Price per box
    prices = [0.99, 1.25, 1.50, 2.00, 2.50]

    # Original variable values
    original_name = "Greg"
    original_item = "flavored jello"
    original_box_weight = 3
    original_cups_per_box = 10
    original_num_kids = 30
    original_cups_per_kid = 4
    original_price = 1.25

    # Randomly assign variables
    name = random.choice(names)
    item = random.choice(items)
    box_weight = random.choice(box_weights)
    cups_per_box = random.choice(cups_per_box_options)
    num_kids = random.choice(num_kids_options)
    cups_per_kid = random.choice(cups_per_kid_options)
    price = random.choice(prices)

    # Build the problem sentences using variable names
    problem = [
        f"A {box_weight}-ounce box of {item} makes {cups_per_box} small {item} cups.",
        f"{name} wants to make small {item} cups for his son's outdoor birthday party.",
        f"There will be {num_kids} kids and he wants to have enough so that each kid can have {cups_per_kid} {item} cups.",
        f"{item.capitalize()} is currently on sale for ${price}.",
    ]

    # Construct the question
    question = f"How much will he spend on {item}?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_items = ["gummy bears", "chips", "popcorn", "soda", "ice cream", "cake"]
    irrelevant_item = random.choice(irrelevant_items)
    in_topic_irrelevant_infos = [
        f"A {box_weight}-ounce box of {irrelevant_item} makes {cups_per_box + random.randint(1, 5)} small {irrelevant_item} cups.",
        f"{name}'s friend wants to make small {irrelevant_item} cups for his daughter's outdoor birthday party.",
        f"{irrelevant_item.capitalize()} is currently on sale for ${price + random.choice([0.25, 0.50, 0.75, 1.00])}.",
    ]

    # Add out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{name} just bought a new car last week.",
    ]

    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Randomly add irrelevant information based on probability
    for info in in_topic_irrelevant_infos + out_topic_irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the sentences
    if shuffle:
        random.shuffle(problem)

    # Append the question
    problem.append(question)

    # Compute the answer using the variables
    total_cups_needed = num_kids * cups_per_kid
    boxes_needed = -(-total_cups_needed // cups_per_box)  # Ceiling division
    total_cost = round(boxes_needed * price, 2)

    # Ensure that the derived answer matches the ground truth answer with original values
    # original_total_cups_needed = original_num_kids * original_cups_per_kid
    # original_boxes_needed = -(-original_total_cups_needed // original_cups_per_box)
    # original_total_cost = round(original_boxes_needed * original_price, 2)
    # assert original_total_cost == 15, "Derived answer does not match the ground truth answer."

    # Return the problem and the answer
    cot = [f"Calculate the total number of {item} cups needed by multiplying the number of kids, {num_kids}, by the number of cups each kid will have, {cups_per_kid}. This gives {total_cups_needed}.", f"Determine the number of boxes needed by dividing {total_cups_needed} by the number of cups each box makes, {cups_per_box}, and rounding up to the nearest whole number. This results in {boxes_needed} boxes.", f"Calculate the total cost by multiplying the number of boxes needed, {boxes_needed}, by the price per box, {price}, and rounding to two decimal places. This gives a total cost of {total_cost}."]
    
    return {"cot": cot, 'problem': problem, 'answer': total_cost, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
