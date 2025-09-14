import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ["Stephen", "Emily", "Michael", "Sophia", "Daniel", "Olivia", "James", "Emma"]
    items = ["groceries", "electronics", "clothes", "furniture", "books", "toys", "appliances", "gardening supplies"]
    
    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)
    
    # Randomly generate order-related values
    final_bill = round(random.uniform(20.00, 100.00), 2)  # Base final bill in dollars
    delivery_fee_percentage = random.randint(5, 30)  # Percentage fee added by vendor
    delivery_fee_flat = round(random.uniform(1.00, 10.00), 2)  # Flat delivery fee in dollars
    tip = round(random.uniform(0.00, 10.00), 2)  # Tip in dollars
    
    # Original values for ground truth answer
    original_name = "Stephen"
    original_item = "groceries"
    original_final_bill = 40.00
    original_delivery_fee_percentage = 25
    original_delivery_fee_flat = 3.00
    original_tip = 4.00
    
    # Construct the premise, replacing values with variable names
    problem = [
        f"{name} placed an online order for {item}.",
        f"{name}'s final bill came to ${final_bill}.",
        f"Because this was through a delivery vendor, they tacked on a {delivery_fee_percentage}% fee to {name}'s final total and charged {name} ${delivery_fee_flat} in delivery fees.",
        f"{name} also added a ${tip} tip."
    ]

    import copy
    original_problem = copy.deepcopy(problem)
    
    # Construct the question
    question = f"After the extra fees, what was the final price of {name}'s {item}?"
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The {item} store is having a big sale next week.",
        f"{name} used a coupon code for future purchases."
    ]
    
    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} is planning a vacation to Europe next month.")
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors (Assuming functions are given)
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
    answer = round(final_bill + (delivery_fee_percentage / 100 * final_bill) + delivery_fee_flat + tip, 2)
    
    # Ensure the derived answer matches the ground truth when using original values
    original_answer = round(
        original_final_bill +
        (original_delivery_fee_percentage / 100 * original_final_bill) +
        original_delivery_fee_flat +
        original_tip, 2
    )
    
    # Return premise and answer as a dictionary
    cot = [f"Calculate the delivery fee by multiplying {final_bill} by {delivery_fee_percentage}/100.", f"Add the calculated delivery fee to {final_bill}.", f"Add the flat delivery fee of {delivery_fee_flat} to the total.", f"Add the tip of {tip} to the total.", f"The final price of {name}'s {item} after all extra fees is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}