from grammar_error import introduce_grammar_error, introduce_symbol_error

import random


# Done
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ['Gary', 'Alice', 'Luis', 'Zhang Wei', 'Amina', 'Omar', 'Priya', 'Artem', 'Nkechi', 'Miguel']
    items = ['boat', 'car', 'motorcycle', 'piano', 'antique vase', 'computer', 'camera', 'bicycle', 'sculpture',
             'diamond ring']
    hobbies = ['painting', 'cycling', 'reading', 'swimming', 'hiking', 'photography', 'gardening', 'cooking', 'dancing']

    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)

    # Randomly generate initial_value and depreciation rates
    initial_value = random.randint(1000, 20000) // 100 * 100  # Multiple of 100
    depreciation_rate_year1 = random.randint(10, 50)
    depreciation_rate_year2 = random.randint(10, 50)
    depreciation_rate_year3 = random.randint(10, 50)
    selling_price = initial_value * random.uniform(0, 1)  # Multiple of 100

    # Construct the premise content, replacing values with variable names
    problem = [
        f"{name} bought a {item} for ${initial_value}.",
        f"Over the first year the {item} depreciated {depreciation_rate_year1}%.",
        f"Over the second year the {item} depreciated another {depreciation_rate_year2}%.",
        f"Over the third year the {item} depreciated {depreciation_rate_year3}%.",
    ]

    # Construct the question
    question = f"How much is the {item} worth after the three years?"
    original_problem = problem.copy()
    original_problem.append(question)
    # Construct in-topic irrelevant information
    maintenance_cost = random.randint(100, 1000) // 10 * 10

    in_topic_irrelevant_infos = [
        f"The {item} requires a yearly maintenance cost of ${maintenance_cost}."
        f"{name} managed to sell {item} in the third year with a price of ${selling_price}."
    ]
    # Construct out-topic irrelevant information
    hobby = random.choice(hobbies)
    out_topic_irrelevant_info = f"{name} enjoys hobbies such as {hobby}."

    # Add irrelevant information based on probability
    irrelevant_infos = in_topic_irrelevant_infos + [out_topic_irrelevant_info]
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (assumed given functions)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_sentences)
    problem = [first_sentence] + rest_sentences

    # Add the question
    problem.append(question)

    # Provide the math formula to calculate the answer
    # answer = initial_value * (1 - depreciation_rate_year1/100) * (1 - depreciation_rate_year2/100) * (1 - depreciation_rate_year3/100)
    answer = initial_value * (1 - depreciation_rate_year1 / 100) * (1 - depreciation_rate_year2 / 100) * (
                1 - depreciation_rate_year3 / 100)

    # # Ensure the derived answer matches the ground truth when using original variable values
    # test_initial_value = 9000
    # test_depreciation_rate_year1 = 30
    # test_depreciation_rate_year2 = 30
    # test_depreciation_rate_year3 = 20
    # test_answer = test_initial_value * (1 - test_depreciation_rate_year1/100) * (1 - test_depreciation_rate_year2/100) * (1 - test_depreciation_rate_year3/100)
    # assert round(test_answer, 2) == 3528, f"Test answer {test_answer} does not match the ground truth 3528"

    # Return premise and answer as a dictionary
    cot = [f"The initial value of the {item} is {initial_value}.",
           f"After the first year, the {item} depreciates by {depreciation_rate_year1}%, so its value becomes {initial_value} * (1 - {depreciation_rate_year1}/100).",
           f"After the second year, the {item} depreciates by another {depreciation_rate_year2}%, so its value becomes {initial_value} * (1 - {depreciation_rate_year1}/100) * (1 - {depreciation_rate_year2}/100).",
           f"After the third year, the {item} depreciates by {depreciation_rate_year3}%, so its value becomes {initial_value} * (1 - {depreciation_rate_year1}/100) * (1 - {depreciation_rate_year2}/100) * (1 - {depreciation_rate_year3}/100).",
           f"Therefore, the final answer is {answer}."]

    return {"cot": cot, 'problem': problem, 'answer': round(answer, 2), 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
