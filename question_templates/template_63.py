import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define possible names
    names = ['Sheila', 'Paul', 'Greg', 'Sarah', 'Emily', 'John', 'Mike', 'Linda', 'Karen', 'David', 'Rachel', 'Peter', 'Anna', 'Tom', 'Nicole']

    # Randomly select a name
    name = random.choice(names)

    # Define possible initial charges
    initial_charges = [85.00, 100.00, 120.00, 75.00, 90.00, 110.00, 95.00, 80.00]
    initial_charge = random.choice(initial_charges)

    # Define returned items and their costs
    returned_items = [('item', 15.00), ('shirt', 12.00), ('pair of shoes', 25.00), ('hat', 10.00), ('book', 8.00), ('dress',18.00)]
    returned_item, returned_item_cost = random.choice(returned_items)

    # Define possible purchased items after returning
    purchased_items_options = [
        [('frying pan', 20, 20.00), ('set of towels', 10, 30.00)],
        [('blender', 25, 40.00), ('coffee maker', 15, 50.00)],
        [('vacuum cleaner', 30, 100.00), ('laptop case', 5, 45.00)],
        [('camera', 20, 200.00), ('tripod', 15, 60.00)],
        [('watch', 10, 150.00), ('sunglasses', 30, 80.00)],
        [('smartphone',15, 600.00), ('headphones', 25, 120.00)],
        [('microwave oven',20, 150.00), ('slow cooker', 15, 80.00)]
    ]

    purchased_items = random.choice(purchased_items_options)
    purchased_item1_name, purchased_item1_discount, purchased_item1_price = purchased_items[0]
    purchased_item2_name, purchased_item2_discount, purchased_item2_price = purchased_items[1]

    # Construct problem sentences with variables
    problem = [
        f"{name} charged ${initial_charge:.2f} worth of merchandise on {name}'s credit card.",
        f"{name} ended up returning one {returned_item} that cost ${returned_item_cost:.2f}.",
        f"After {name} returned the {returned_item}, {name} bought a {purchased_item1_name} that was on sale for {purchased_item1_discount}% off ${purchased_item1_price:.2f} and a {purchased_item2_name} that was {purchased_item2_discount}% off ${purchased_item2_price:.2f}.",
        f"{name} put both of these purchases on {name}'s credit card."
    ]

    import copy
    original_problem = copy.deepcopy(problem)

    # Construct the question
    question = f"What is the new balance on {name}'s credit card?"

    # In-topic irrelevant information
    in_topic_irrelevant = [
        f"The credit card has a limit of ${random.randint(1000, 5000)}.",
        f"{name} had previously paid off a balance of ${random.randint(50, 200)}.",
        f"The store was having a clearance sale with discounts up to {random.randint(30, 50)}%.",
        f"The interest rate on the credit card is {random.randint(15, 25)}%."
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant = [
        f"{name} went to the gym earlier that day.",
        f"{name} is planning a vacation next month.",
        f"{name} has a pet dog named Buddy.",
        f"It was raining on that day.",
        f"{name} enjoys painting in their free time.",
        f"The stock market went up by {random.randint(1,5)}% that day."
    ]

    # Combine the irrelevant information
    irrelevant_infos = in_topic_irrelevant + out_topic_irrelevant

    # Randomly add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    # Assume introduce_symbol_error and introduce_grammar_error are given
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

    # Add the question
    problem.append(question)
    original_problem.append(question)

    # Calculate the answer
    # Calculate the discounted prices
    purchased_item1_cost = purchased_item1_price * (100 - purchased_item1_discount) / 100
    purchased_item2_cost = purchased_item2_price * (100 - purchased_item2_discount) / 100

    # New balance equals initial_charge - returned_item_cost + purchased_item1_cost + purchased_item2_cost
    answer = initial_charge - returned_item_cost + purchased_item1_cost + purchased_item2_cost

    # Return problem and answer
    cot = [f"Calculate the cost of the {purchased_item1_name} after discount: {purchased_item1_price} * (100 - {purchased_item1_discount}) / 100 = {purchased_item1_cost}.", f"Calculate the cost of the {purchased_item2_name} after discount: {purchased_item2_price} * (100 - {purchased_item2_discount}) / 100 = {purchased_item2_cost}.", f"The new balance on {name}'s credit card is calculated as: {initial_charge} - {returned_item_cost} + {purchased_item1_cost} + {purchased_item2_cost} = {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}