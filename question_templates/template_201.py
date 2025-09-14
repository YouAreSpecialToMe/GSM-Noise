from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
from itertools import combinations


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define possible values for variables
    names = ["Sam", "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Sydney", "Chris"]
    products = ["bread", "cakes", "pies", "cookies", "pastries", "sandwiches", "bagels", "muffins"]
    target_sales_list = [80, 100, 120, 150, 200]
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    weekend_days = ["Saturday", "Sunday"]

    # Randomly select variables
    name = random.choice(names)
    product = random.choice(products)
    target_sales = random.choice(target_sales_list)

    # Randomly select 2 days to be closed
    closed_days = random.sample(week_days, 2)
    open_week_days = [day for day in week_days if day not in closed_days]

    # Randomly assign sales numbers for open days
    sales_per_day = {}
    for day in open_week_days:
        sales_per_day[day] = random.randint(10, 30)

    # Assign weekend sales
    weekend_sales = random.randint(10, 50)

    # Construct the premises with variable placeholders
    problem_sentences = [
        "{name} sells {product}.",
        "{name} has a target of selling {target_sales} crates of {product} in a week.",
        "One week {name} was closed on {closed_day1} and {closed_day2}.",
        "Over the weekend {name} sold {weekend_sales} crates.",
    ]
    for day in open_week_days:
        problem_sentences.append(f"On {day} {name} sold {{{{sales_{day}}}}} crates.")
    problem_sentences.append("By how many crates was {name} off from {name}'s target for the week?")
    original_problem = problem_sentences.copy()

    # Construct in-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"{name} has been experimenting with new recipes for {product}.",
        f"{name}'s shop won an award for best {product} in town.",
        f"Each crate of {product} is sold to retailers for $20.",
        f"{name} is planning to open a new branch next year.",
    ]

    # Possible animals and hobbies
    animals = ["dog", "cat", "parrot", "rabbit"]
    hobbies = ["painting", "cycling", "playing guitar", "photography"]

    # Construct out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{name} recently adopted a pet {random.choice(animals)}.",
        f"{name}'s favorite hobby is {random.choice(hobbies)}.",
    ]

    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem_sentences.append(irrelevant_info)

    # Replace variable placeholders with actual variable values
    closed_day1, closed_day2 = closed_days[0], closed_days[1]
    variables = {
        'name': name,
        'product': product,
        'target_sales': target_sales,
        'closed_day1': closed_day1,
        'closed_day2': closed_day2,
        'weekend_sales': weekend_sales,
    }
    # Add sales per day variables
    for day in open_week_days:
        variables[f'sales_{day}'] = sales_per_day[day]

    # Fill in the problem sentences with variable values
    problem_sentences = [sentence.format(**variables) for sentence in problem_sentences]
    original_problem = [sentence.format(**variables) for sentence in original_problem]

    # Add symbol or grammar errors. Assume the functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in problem_sentences
    ]

    # Shuffle the sentences except the first one and the last one
    first_sentence = problem[0]
    rest_of_problem = problem[1:-1]
    last_sentence = problem[-1]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem + [last_sentence]

    # Calculate the answer using variables
    total_sales = weekend_sales + sum(sales_per_day.values())
    answer = target_sales - total_sales

    # Construct the corrected chain-of-thought (cot)
    # List the sales per day in the cot
    sales_details = " + ".join(
        [f"{sales_per_day[day]} (on {day})" for day in open_week_days] + [f"{weekend_sales} (over the weekend)"])
    total_sales_expression = " + ".join([str(sales_per_day[day]) for day in open_week_days] + [str(weekend_sales)])

    cot = [
        f"{name} was open on {', '.join(open_week_days)} and the weekend.",
        f"The sales on these days were: {sales_details}.",
        f"Total sales = {total_sales_expression} = {total_sales} crates.",
        f"Difference from target = {target_sales} (target sales) - {total_sales} (total sales) = {answer} crates.",
    ]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}