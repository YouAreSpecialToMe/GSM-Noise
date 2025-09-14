from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible values
    names = ["Alex", "Beth", "Carlos", "Diana", "Eve", "Frank", "Grace", "Henry", "Billy"]
    items = ["DVDs", "books", "magazines", "CDs", "video games"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Randomly select values
    name = random.choice(names)
    item = random.choice(items)
    day = random.choice(days)

    # Numeric variables with original values to match the ground truth answer
    total_customers = 8
    group1_customers = 3
    group1_items_per_customer = 1
    group2_customers = 2
    group2_items_per_customer = 2
    group3_customers = 3
    group3_items_per_customer = 0

    # Randomize variables for variability while ensuring the total customers add up
    total_customers = random.randint(6, 15)
    group1_customers = random.randint(1, total_customers - 2)
    remaining_customers = total_customers - group1_customers
    group2_customers = random.randint(1, remaining_customers - 1)
    group3_customers = total_customers - group1_customers - group2_customers

    group1_items_per_customer = random.randint(1, 3)
    group2_items_per_customer = random.randint(1, 5)
    group3_items_per_customer = 0

    # Construct the premises
    problem = [
        f"{name} sells {item}.",
        f"{name} has {total_customers} customers on {day}.",
        f"{name}'s first {group1_customers} customers buy {group1_items_per_customer} {item.lower()} each.",
        f"{name}'s next {group2_customers} customers buy {group2_items_per_customer} {item.lower()} each.",
        f"{name}'s last {group3_customers} customers don't buy any {item.lower()}.",
    ]

    # Construct the question
    question = f"How many {item.lower()} did {name} sell on {day}?"

    original_problem = problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    items2 = ["smartphones", "laptops", "headphones", "tablets", "smartwatches"]
    in_topic_irrelevant_infos = [
        f"{name}'s first {group1_customers} customers buy {group1_items_per_customer} {random.choice(items2).lower()} each.",
        f"{name}'s next {group2_customers} customers buy {group2_items_per_customer} {random.choice(items2).lower()} each.",
        f"{name}'s last {group3_customers} customers don't buy any {random.choice(items2).lower()}."
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{name}'s favorite color is {random.choice(['red', 'blue', 'green', 'yellow', 'purple'])}.",
    ]

    # Add irrelevant information based on probability
    all_irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    for info in all_irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Add symbol or grammar errors (assume these functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        )
        for p in problem
    ]

    # Shuffle the premises except for the first one
    body_premises = problem[1:]
    if shuffle:
        random.shuffle(body_premises)
    problem = [problem[0]] + body_premises + [question]

    # Calculate the answer
    answer = (
        group1_customers * group1_items_per_customer +
        group2_customers * group2_items_per_customer +
        group3_customers * group3_items_per_customer
    )

    # Return the problem and the answer
    cot = [f"{name} has {group1_customers} customers who each buy {group1_items_per_customer} {item.lower()}, totaling {group1_customers * group1_items_per_customer} {item.lower()}.", f"{name} has {group2_customers} customers who each buy {group2_items_per_customer} {item.lower()}, totaling {group2_customers * group2_items_per_customer} {item.lower()}.", f"{name} has {group3_customers} customers who do not buy any {item.lower()}, contributing 0 to the total.", f"Therefore, the total number of {item.lower()} sold is {group1_customers * group1_items_per_customer} + {group2_customers * group2_items_per_customer} + 0, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': all_irrelevant_infos}