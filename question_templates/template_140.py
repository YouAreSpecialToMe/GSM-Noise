from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible values
    names = ["Sasha", "Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Jamie", "Avery", "Parker"]
    boards_dimensions = ["2 x 4 x 10", "2 x 6 x 12", "4 x 4 x 8", "1 x 6 x 10", "2 x 8 x 12", "1 x 4 x 8", "2 x 2 x 10"]
    price_increase_percentages = [10, 20, 25, 50, 75, 100]

    # Randomly select values
    name = random.choice(names)
    price_increase_percentage = random.choice(price_increase_percentages)

    # Board type 1
    qty_board1 = random.randint(5, 20)
    cost_board1 = random.randint(5, 20)
    dimensions_board1 = random.choice(boards_dimensions)

    # Board type 2
    qty_board2 = random.randint(2, 10)
    cost_board2 = random.randint(10, 30)
    dimensions_board2 = random.choice(boards_dimensions)

    # Personalized variables for irrelevant info
    hobby = random.choice(["painting", "cycling", "photography", "gardening", "cooking", "hiking"])
    age = random.randint(20, 60)
    city = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia"])

    # Construct the premises with variables
    problem = [
        f"{name} notices that prices for lumber have gone up {price_increase_percentage}% in the last few months after {name} bought some lumber.",
        f"Since {name} has leftovers, {name} decides to sell them.",
        f"{name} has leftover {qty_board1} {dimensions_board1} boards that cost {name} ${cost_board1} each.",
        f"{name} also has {qty_board2} {dimensions_board2} boards {name} bought for ${cost_board2} each."
    ]

    # Construct the question
    question = f"If {name} sells them all, how much profit does {name} make?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Construct in-topic irrelevant information
    irrelvant_names = ["Quinn", "Skylar", "Harper", "Emerson", "Finley", "Cameron", "Rowan", "Charlie", "Sage", "Reese"]
    irrelevant_name = random.choice(irrelvant_names)
    irrelevant_infos = [
        f"{name}'s friend {irrelevant_name} has leftover {qty_board1 + random.randint(1, 5)} {dimensions_board1} boards that cost {irrelevant_name} ${cost_board1 + random.randint(1, 5)} each.",
        f"{name} sold {qty_board2 + random.randint(3, 10)} {dimensions_board2} boards cost {name} ${cost_board2 - random.randint(2, 10)} each to a construction company in {city} last year.",
    ]

    # Construct out-topic irrelevant information
    out_topic_irrelevant_info = f"In {name}'s free time, {name} enjoys {hobby}."
    irrelevant_infos.append(out_topic_irrelevant_info)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume the functions introduce_symbol_error and introduce_grammar_error are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    problem_body = problem[1:]
    if shuffle:
        random.shuffle(problem_body)
    problem = [problem[0]] + problem_body

    # Add the question
    problem.append(question)

    # Calculate the answer
    # Total cost
    total_cost = qty_board1 * cost_board1 + qty_board2 * cost_board2

    # Selling price per board
    selling_price_board1 = cost_board1 * (1 + price_increase_percentage / 100)
    selling_price_board2 = cost_board2 * (1 + price_increase_percentage / 100)

    # Total revenue
    total_revenue = qty_board1 * selling_price_board1 + qty_board2 * selling_price_board2

    # Profit
    answer = total_revenue - total_cost

    # Return problem and answer
    cot = [f"Calculate the total cost of the boards: {qty_board1} * {cost_board1} + {qty_board2} * {cost_board2}, which is {total_cost}.", f"Calculate the selling price for each type of board. For the first type: {cost_board1} * (1 + {price_increase_percentage} / 100), which is {selling_price_board1}.", f"For the second type: {cost_board2} * (1 + {price_increase_percentage} / 100), which is {selling_price_board2}.", f"Calculate the total revenue from selling all boards: {qty_board1} * {selling_price_board1} + {qty_board2} * {selling_price_board2}, which is {total_revenue}.", f"The profit is the total revenue minus the total cost: {total_revenue} - {total_cost}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
