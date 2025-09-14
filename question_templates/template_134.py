from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ["Chad", "Beth", "Alex", "Taylor", "Jordan", "Morgan"]
    items = ["build-your-own burrito", "custom sandwich", "personal pizza", "pasta bowl", "salad"]

    # Randomly select a name and a menu item
    name = random.choice(names)
    item = random.choice(items)

    # Randomly generate prices and quantities within reasonable ranges
    base_price = round(random.uniform(5.0, 10.0), 2)  # Base price between $5.00 and $10.00
    extra_meat_price = round(random.uniform(1.0, 3.0), 2)
    extra_cheese_price = round(random.uniform(0.5, 2.0), 2)
    avocado_price = round(random.uniform(0.5, 2.0), 2)
    sauce_price = round(random.uniform(0.1, 0.5), 2)
    num_sauces = random.randint(1, 5)
    upgrade_price = round(random.uniform(2.0, 5.0), 2)
    gift_card_value = round(random.uniform(0.0, 10.0), 2)

    # Other irrelevant items
    dessert_price = round(random.uniform(1.0, 5.0), 2)
    tip_percentage = random.randint(0, 20)
    friend_name = random.choice([n for n in names if n != name])

    # Construct the premise, replacing values with variable names
    problem = [
        f"{name} ordered a {item} for lunch.",
        f"The base {item} is ${base_price}.",
        f"{name} adds extra meat for ${extra_meat_price}, extra cheese for ${extra_cheese_price}, avocado for ${avocado_price}, and {num_sauces} sauces for ${sauce_price} each.",
        f"{name} decides to upgrade the meal for an extra ${upgrade_price} which will add chips and a drink.",
        f"{name} left a {tip_percentage}% tip for the server.",
        f"{name} has a gift card for ${gift_card_value} that {name} uses at checkout."
    ]

    # Construct the question
    question = f"How much does {name} still owe?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} considered adding a dessert for ${dessert_price} but decided not to.",
        f"The chips cost ${round(upgrade_price * 0.5, 2)} and the drink costs ${round(upgrade_price * 0.5, 2)}.",
        f"{friend_name} joined {name} for lunch but paid separately."
    ]

    # Add out-topic irrelevant information
    irrelevant_out_topic = f"{name} has to go back to work in an hour."
    irrelevant_infos.append(irrelevant_out_topic)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (Assume functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except the first one
    problem_first = problem[0]
    problem_rest = problem[1:]
    if shuffle:
        random.shuffle(problem_rest)
    problem = [problem_first] + problem_rest

    # Add the question at the end
    problem.append(question)

    # Calculate the answer
    total_cost = (base_price + extra_meat_price + extra_cheese_price + avocado_price + (
                sauce_price * num_sauces) + upgrade_price) * (1 + tip_percentage / 100)
    final_cost = total_cost - gift_card_value
    final_cost = round(final_cost, 2)
    answer = final_cost

    # Return the problem and answer
    cot = [f"Calculate the total cost by adding {base_price}, {extra_meat_price}, {extra_cheese_price}, {avocado_price}, and the cost of {num_sauces} sauces at {sauce_price} each, plus {upgrade_price}.", f"Apply the tip percentage of {tip_percentage}% to the total cost.", f"Subtract the {gift_card_value} from the total cost to get the final cost.", f"Round the final cost to two decimal places to get the amount {name} still owes, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
