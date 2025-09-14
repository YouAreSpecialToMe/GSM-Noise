import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name lists
    titles = ["Mrs.", "Mr.", "Dr.", "Ms.", "Miss", "Prof."]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    first_names = ["Alex", "Taylor", "Jordan", "Morgan", "Casey", "Riley", "Jamie", "Cameron", "Peyton", "Devin"]

    # Randomly choose a title and a name
    title = random.choice(titles)
    if title in ["Dr.", "Prof."]:
        name = f"{title} {random.choice(first_names)} {random.choice(last_names)}"
    else:
        name = f"{title} {random.choice(last_names)}"

    # Randomly generate financial values
    budget = random.randint(300000, 1000000)  # Budget between $300,000 and $1,000,000
    budget = (budget // 1000) * 1000  # Round to nearest thousand

    selling_price = random.randint(int(budget * 0.7), int(budget * 0.95))
    selling_price = (selling_price // 1000) * 1000  # Round to nearest thousand

    brokerage_percent = random.randint(1, 10)  # Between 1% and 10%
    transfer_fee_percent = random.randint(5, 20)  # Between 5% and 20%

    # Ensure the total price exceeds the budget
    brokerage_fee = selling_price * brokerage_percent / 100
    transfer_fee = selling_price * transfer_fee_percent / 100
    total_price = selling_price + brokerage_fee + transfer_fee
    difference = total_price - budget

    while difference <= 0:
        budget = random.randint(300000, 1000000)
        budget = (budget // 1000) * 1000
        selling_price = random.randint(int(budget * 0.97), int(budget * 0.98))
        selling_price = (selling_price // 1000) * 1000
        brokerage_percent = random.randint(1, 10)
        transfer_fee_percent = random.randint(5, 20)
        brokerage_fee = selling_price * brokerage_percent / 100
        transfer_fee = selling_price * transfer_fee_percent / 100
        total_price = selling_price + brokerage_fee + transfer_fee
        difference = total_price - budget

    # Construct the premise content
    problem = [
        f"{name} is looking for a house that will not go beyond {name}'s ${budget} budget.",
        f"{name} saw a property that has a selling price of ${selling_price}.",
        f"On top of that, the buyer has to pay a brokerage fee which is {brokerage_percent}% of the selling price, and also the transfer fee that is {transfer_fee_percent}% of the selling price."
    ]

    import copy
    original_problem = copy.deepcopy(problem)

    # Construct the question
    question = f"How much more is the total price of the house than {name}'s budget?"

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The house has {random.randint(2, 5)} bedrooms and a large backyard.",
        f"The seller originally purchased the house for ${random.randint(200000, selling_price)}."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} enjoys hiking and photography during weekends.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    to_shuffle = problem[1:]
    if shuffle:
        random.shuffle(to_shuffle)
    problem = [problem[0]] + to_shuffle

    # Add the question
    problem.append(question)
    original_problem.append(question)

    # Calculate the answer using the variables
    brokerage_fee = selling_price * brokerage_percent / 100
    transfer_fee = selling_price * transfer_fee_percent / 100
    total_price = selling_price + brokerage_fee + transfer_fee
    answer = total_price - budget

    # Return premise and answer as a dictionary
    cot = [f"Calculate the brokerage fee as {selling_price} * {brokerage_percent} / 100, which is {brokerage_fee}.", f"Calculate the transfer fee as {selling_price} * {transfer_fee_percent} / 100, which is {transfer_fee}.", f"The total price of the house is {selling_price} + {brokerage_fee} + {transfer_fee}, which is {total_price}.", f"The difference between the total price and {name}'s budget is {total_price} - {budget}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}