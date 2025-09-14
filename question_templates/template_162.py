from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ["Alice", "Bob", "Cindy", "David", "Erika", "Fiona", "George", "Hannah", "Ian", "Julia"]
    items = ["laptop", "bicycle", "smartphone", "guitar", "camera"]

    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)

    # Randomly generate relevant values
    item_cost = random.randint(400, 1000)  # Cost of the item
    discount = random.randint(50, 300)  # Discount for trading in old item
    job_pay = random.randint(50, 200)  # Money earned from part-time job
    mom_money = random.randint(20, 150)  # Money given by mom
    extra_needed = random.randint(10, 100)  # Extra money needed

    # Calculate purse_savings to make the problem consistent
    purse_savings = item_cost - discount - job_pay - mom_money - extra_needed

    # Adjust variables if necessary
    if purse_savings < 0:
        purse_savings = random.randint(0, 100)
        total_available = purse_savings + job_pay + mom_money
        total_needed = total_available + extra_needed
        item_cost = total_needed + discount

    # Recalculate the answer using the formula
    answer = item_cost - discount - job_pay - mom_money - extra_needed

    # Construct the premise content
    problem = [
        f"{name} is saving for a new {item}.",
        f"The {item} {name} wants costs ${item_cost}.",
        f"The sales assistant told {name} that if {name} traded in {name}'s old {item}, the price of the new one would be reduced by ${discount}.",
        f"{name} thinks this is a good deal and agrees to do it.",
        f"{name} already has some savings in {name}'s purse, and has also been paid ${job_pay} this week for {name}'s part-time job.",
        f"{name}'s mom agrees to give {name} ${mom_money} to help {name}.",
        f"If {name} now only needs an extra ${extra_needed} to buy the {item}, how much money does {name} have in {name}'s purse?"
    ]

    original_problem = problem.copy()

    # In-topic irrelevant information
    irrelevant_items = ["tablet", "watch", "earphones", "headphones", "speaker"]
    irrelevant_in_topic = [
        f"{name}'s old {item} costs ${item_cost - random.randint(50, 150)}.",
        f"{name}'s father agrees that {name}'s mom to give {name} ${mom_money} to help {name}.",
        f"{name} spent ${random.randint(10, 50)} on {random.choice(irrelevant_items)} last week.",
    ]

    # Out-topic irrelevant information
    hobbies = ["painting", "jogging", "reading books", "swimming", "playing soccer"]
    hobby = random.choice(hobbies)
    irrelevant_out_topic = f"{name} enjoys {hobby} during free time."

    irrelevant_infos = irrelevant_in_topic + [irrelevant_out_topic]

    # Add irrelevant information based on probability
    if random.random() < prob_irre:
        problem.append(random.choice(irrelevant_in_topic))
    if random.random() < prob_irre:
        problem.append(irrelevant_out_topic)

    # Add symbol or grammar errors. Assume that these functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    other_sentences = problem[1:-1]
    qustion = problem[-1]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences + [qustion]

    # Return problem and answer
    cot = [f"The cost of the {item} is {item_cost}.", f"The discount for trading in the old {item} is {discount}.", f"{name} has earned {job_pay} from the part-time job.", f"{name}'s mom gives {name} {mom_money}.", f"The extra money needed is {extra_needed}.", f"Therefore, the money in {name}'s purse is calculated as {item_cost} - {discount} - {job_pay} - {mom_money} - {extra_needed}, which is {purse_savings}.", f"Thus, the final answer is {purse_savings}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
