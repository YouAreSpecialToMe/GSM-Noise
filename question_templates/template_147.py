from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define company names and fruits
    company_names = [
        "FreshFruit Co.", "Fruitopia", "Healthy Harvest",
        "Nature's Bounty", "Fruitful Ventures", "Orchard Express"
    ]
    fruit_types = [
        "apples", "bananas", "oranges", "pears",
        "kiwis", "grapes", "peaches", "plums"
    ]

    # Randomly select a company name
    company_name = random.choice(company_names)

    # Randomly select three different fruits
    fruits = random.sample(fruit_types, 3)
    fruit1, fruit2, fruit3 = fruits[0], fruits[1], fruits[2]

    # Define singular forms of the fruit names
    def singular(fruit):
        return fruit[:-1] if fruit.endswith('s') else fruit

    fruit1_singular = singular(fruit1)
    fruit2_singular = singular(fruit2)
    fruit3_singular = singular(fruit3)

    # Randomly generate quantities per crate
    fruit1_qty = random.randint(1, 20)
    fruit2_qty = random.randint(1, 20)
    fruit3_qty = random.randint(1, 20)

    # Randomly generate base price for fruit2
    fruit2_price = round(random.uniform(0.1, 2.0), 2)  # Price per unit of fruit2 in dollars

    # Randomly generate price ratios
    fruit1_price_ratio = random.randint(2, 5)  # fruit1 costs fruit1_price_ratio times as much as fruit2
    fruit3_price_ratio = random.randint(2, 5)  # fruit3 costs fruit3_price_ratio times as much as fruit1

    # Calculate prices for fruit1 and fruit3
    fruit1_price = round(fruit2_price * fruit1_price_ratio, 2)
    fruit3_price = round(fruit1_price * fruit3_price_ratio, 2)

    # # Prepare variables dictionary
    # variables = {
    #     'company_name': company_name,
    #     'fruit1_qty': fruit1_qty,
    #     'fruit2_qty': fruit2_qty,
    #     'fruit3_qty': fruit3_qty,
    #     'fruit1': fruit1,
    #     'fruit2': fruit2,
    #     'fruit3': fruit3,
    #     'fruit1_singular': fruit1_singular,
    #     'fruit2_singular': fruit2_singular,
    #     'fruit3_singular': fruit3_singular,
    #     'fruit1_price': fruit1_price,
    #     'fruit2_price': fruit2_price,
    #     'fruit1_price_ratio': fruit1_price_ratio,
    #     'fruit3_price_ratio': fruit3_price_ratio,
    # }

    # Construct the problem templates with variable placeholders
    problem_templates = [
        f"{company_name} is in the business of selling fresh fruit.",
        f"One crate of such fruit consists of {fruit1_qty} {fruit1}, {fruit2_qty} {fruit2}, and {fruit3_qty} {fruit3}.",
        f"The price for such a crate depends on the price of its individual fruits.",
        f"One {fruit2_singular} costs ${fruit2_price} and one {fruit1_singular} costs {fruit1_price_ratio} times as much.",
        f"{fruit3_singular.capitalize()}s are the most expensive and cost {fruit3_price_ratio} times as much as a {fruit1_singular} per piece."
    ]

    # Construct the question
    question = "What would be the price for such a crate of fruit?"

    original_problem = problem_templates.copy()
    original_problem.append(question)

    # Construct irrelevant information
    irrelevant_fruits = ["mangoes", "cherries", "blueberries", "strawberries", "watermelons", "pineapples",
                         "pomegranates", "lemons", "limes"]
    irrelevant_fruit = random.choice(irrelevant_fruits)
    irrelevant_fruits.remove(irrelevant_fruit)
    irrelevant_fruit2 = random.choice(irrelevant_fruits)
    irrelevant_fruits.remove(irrelevant_fruit2)
    irrelevant_fruit3 = random.choice(irrelevant_fruits)
    irrelevant_infos = [
        f"One {irrelevant_fruit} costs ${random.uniform(0.1, 2.0):.2f}.",
        f"One {irrelevant_fruit2} costs ${random.uniform(0.1, 2.0):.2f}.",
        f"{irrelevant_fruit3.capitalize()}s are expensive and cost ${random.uniform(0.1, 2.0):.2f} per piece.",
    ]

    # Out-topic irrelevant information
    out_topic_info = f"{company_name} is planning to launch a new line of fruit juices next summer."
    irrelevant_infos.append(out_topic_info)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem_templates.append(irrelevant_info)

    # Add symbol or grammar errors (assumed functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem_templates
    ]

    # Shuffle the sentences except the first one
    main_sentences = problem_templates[1:]
    if shuffle:
        random.shuffle(main_sentences)
    problem = [problem_templates[0]] + main_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    total_price = (
            fruit1_qty * fruit1_price +
            fruit2_qty * fruit2_price +
            fruit3_qty * fruit3_price
    )
    answer = round(total_price, 2)

    # Return the problem and answer
    cot = [f"Calculate the total price for {fruit1_qty} units of the first fruit at {fruit1_price} each, {fruit2_qty} units of the second fruit at {fruit2_price} each, and {fruit3_qty} units of the third fruit at {fruit3_price} each.", f"The total price is {fruit1_qty} * {fruit1_price} + {fruit2_qty} * {fruit2_price} + {fruit3_qty} * {fruit3_price}, which is {total_price}.", f"Round the total price to two decimal places to get the final answer, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
