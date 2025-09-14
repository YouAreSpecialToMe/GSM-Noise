from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name lists
    names = ['Alice', 'Bob', 'Cindy', 'David', 'Emma', 'Frank', 'Grace', 'Helen', 'Ian', 'Jane', 'Kevin', 'Laura']
    name1 = random.choice(names)
    names.remove(name1)
    name2 = random.choice(names)

    # Define item pairs (item1, item2)
    item_pairs = [
        ('sticker', 'button'),
        ('card', 'coin'),
        ('gem', 'stone'),
        ('flower', 'leaf'),
        ('marble', 'pebble'),
        ('shell', 'bead'),
        ('book', 'pencil'),
        ('ticket', 'token'),
        ('cup', 'plate'),
        ('note', 'stamp')
    ]
    item_pair = random.choice(item_pairs)
    item1 = item_pair[0]
    item2 = item_pair[1]
    item1_small = 'small ' + item1
    item1_large = 'large ' + item1
    item2_small = 'small ' + item2
    item2_large = 'large ' + item2

    # Randomly generate starting quantities and percentages
    small_item1_start = random.randint(10, 100)
    large_item1_start = random.randint(10, 100)
    trade_small_item1_percent = random.choice([70, 80, 90])
    trade_large_item1_for_large_item2_percent = random.choice([40, 50, 60])

    # Construct the premises
    problem = [
        f"{name1} and {name2} are trading {item1}s for {item2}s.",
        f"Each {item1_large} is worth a {item2_large} or three {item2_small}s.",
        f"A {item1_small} is worth one {item2_small}.",
        f"A {item2_large} is worth three {item1_small}s.",
        f"{name1} starts with {small_item1_start} {item1_small}s and {large_item1_start} {item1_large}s.",
        f"{name1} trades {trade_small_item1_percent}% of {name1}'s {item1_small}s for {item2_large}s.",
        f"{name1} trades {trade_large_item1_for_large_item2_percent}% of {name1}'s {item1_large}s for {item2_large}s and trades the rest of them for {item2_small}s."
    ]

    # Construct the question
    question = f"How many {item2}s does {name1} have by the end?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The {item2}s are made from rare materials collected by {name2}.",
        f"The exchange rate between {item1}s and {item2}s fluctuates every week."
    ]

    # Add out-of-topic irrelevant information
    hobbies = ['painting', 'playing guitar', 'dancing', 'hiking', 'writing poetry']
    hobby = random.choice(hobbies)
    irrelevant_infos.append(f"{name1} enjoys {hobby} in {name1}'s free time.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    # You do not have to generate these functions. Assume that they are given.
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

    # Calculate the answer

    # Compute number of small item1s traded
    small_item1_traded = int(small_item1_start * (trade_small_item1_percent / 100))

    # Number of large item2s obtained from trading small item1s
    large_item2_from_small_item1 = small_item1_traded // 3

    # Remaining small item1s are not traded further
    # Remaining small item1s = small_item1_start - small_item1_traded

    # Compute number of large item1s traded for large item2s
    large_item1_traded_for_large_item2 = int(large_item1_start * (trade_large_item1_for_large_item2_percent / 100))

    # Number of large item2s obtained from trading large item1s
    large_item2_from_large_item1 = large_item1_traded_for_large_item2  # Each large item1 is worth one large item2

    # Number of large item1s traded for small item2s
    large_item1_traded_for_small_item2 = large_item1_start - large_item1_traded_for_large_item2

    # Number of small item2s obtained from trading large item1s for small item2s
    small_item2_from_large_item1 = large_item1_traded_for_small_item2 * 3  # Each large item1 is worth three small item2s

    # Total item2s
    total_large_item2 = large_item2_from_small_item1 + large_item2_from_large_item1
    total_small_item2 = small_item2_from_large_item1

    # Total item2s as the sum of large and small item2s
    answer = total_large_item2 + total_small_item2

    # Return the problem and the answer
    cot = [f"{name1} trades {trade_small_item1_percent}% of {name1}'s {item1_small}s, which is {small_item1_traded} {item1_small}s.", f"These {small_item1_traded} {item1_small}s are traded for {item2_large}s, resulting in {large_item2_from_small_item1} {item2_large}s.", f"{name1} trades {trade_large_item1_for_large_item2_percent}% of {name1}'s {item1_large}s for {item2_large}s, which is {large_item1_traded_for_large_item2} {item1_large}s.", f"This results in {large_item2_from_large_item1} {item2_large}s.", f"The remaining {item1_large}s, {large_item1_traded_for_small_item2}, are traded for {item2_small}s, resulting in {small_item2_from_large_item1} {item2_small}s.", f"The total number of {item2_large}s is {large_item2_from_small_item1} + {large_item2_from_large_item1}, which is {total_large_item2}.", f"The total number of {item2_small}s is {small_item2_from_large_item1}.", f"Therefore, the total number of {item2}s is {total_large_item2} + {total_small_item2}, which is {answer}."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
