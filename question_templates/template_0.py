from grammar_error import introduce_grammar_error, introduce_symbol_error
import random
import json


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Initialize story and irrelevant information lists
    stories = []
    irrelative_informations = []

    # Define name and item lists
    names = ["Alice", "Beth", "Cindy", "Diana", "Carmen", "Bob"]
    items = ['antique desk', 'Van Gogh painting', 'ancient Japanese samurai sword']

    # Randomly select a name and an auction item
    name = random.choice(names)
    item = random.choice(items)

    # Randomly generate auction-related values
    begin_money = random.randint(100, 1000)  # Starting bid
    raise_money = random.randint(20, 100)  # Amount by which bids increase each time
    people = random.randint(3, 20)  # Number of other bidders
    ticket_money = random.randint(5, 100)  # Auction ticket cost

    discount = random.randint(0, 100)  # Discount percentage on the final cost
    item_money = random.randint(500, 1000)  # Cost of the auction item for the owner
    year = random.randint(1951, 2024)  # Year the auction house was built
    auction_money = random.randint(1000, 10000)  # Cost to build the auction house

    # Construct the story content, breaking it down into sentence level
    story_1 = f"{name} goes to an auction to win the {item}."
    story_1 = introduce_grammar_error(story_1, prob_grammar_error)
    story_1 = introduce_symbol_error(story_1, prob_symbol_error)
    stories.append(story_1)

    story_2 = f"{name} accepts the opening bid of ${begin_money} and continues bidding until {name} wins."
    story_2 = introduce_grammar_error(story_2, prob_grammar_error)
    story_2 = introduce_symbol_error(story_2, prob_symbol_error)
    stories.append(story_2)

    story_3 = f"The bids on the {item} rise by ${raise_money} each time and {people} other people each bid once."
    story_3 = introduce_grammar_error(story_3, prob_grammar_error)
    story_3 = introduce_symbol_error(story_3, prob_symbol_error)
    stories.append(story_3)

    story_4 = f"{name} bids after each of the {people} other people and eventually wins."
    story_4 = introduce_grammar_error(story_4, prob_grammar_error)
    story_4 = introduce_symbol_error(story_4, prob_symbol_error)
    stories.append(story_4)

    story_5 = f"The auction gives {name} a {discount}% discount on the final cost."
    story_5 = introduce_grammar_error(story_5, prob_grammar_error)
    story_5 = introduce_symbol_error(story_5, prob_symbol_error)
    stories.append(story_5)

    # Add in-topic irrelevant information
    irrelative_info_1 = f"The {item} originally cost ${item_money} for the auction owner to acquire."
    irrelative_info_1 = introduce_grammar_error(irrelative_info_1, prob_grammar_error)
    irrelative_info_1 = introduce_symbol_error(irrelative_info_1, prob_symbol_error)
    irrelative_informations.append(irrelative_info_1)

    irrelative_info_2 = f"The auction house was established in {year} and cost ${auction_money} to build."
    irrelative_info_2 = introduce_grammar_error(irrelative_info_2, prob_grammar_error)
    irrelative_info_2 = introduce_symbol_error(irrelative_info_2, prob_symbol_error)
    irrelative_informations.append(irrelative_info_2)

    # Add out-topic irrelevant information
    all_genders = ['boy', 'girl']
    gender = random.choice(all_genders)
    ir_money = random.randint(1000, 5000)
    irrelative_info_3 = f"{name} is a {gender} who has more than ${ir_money} saved up."
    irrelative_info_3 = introduce_grammar_error(irrelative_info_3, prob_grammar_error)
    irrelative_info_3 = introduce_symbol_error(irrelative_info_3, prob_symbol_error)
    irrelative_informations.append(irrelative_info_3)

    original_problem = stories.copy()

    # Add irrelevant information based on probability
    for irrelative_information in irrelative_informations:
        if random.random() < prob_irre:
            stories.append(irrelative_information)

    # stories = [
    #     introduce_symbol_error(
    #         introduce_grammar_error(p, prob_grammar_error),
    #         prob_symbol_error
    #     ) for p in stories
    # ]

    # Shuffle the order of sentences, except for the first one
    first_story = stories[0]
    rest_stories = stories[1:]
    if shuffle:
        random.shuffle(rest_stories)
    stories = [first_story] + rest_stories

    # Add the question
    question = f"How much money, in dollars, does the {item} cost {name}?"
    stories.append(question)
    original_problem.append(question)

    # Calculate the answer
    ans = (begin_money + raise_money * people * 2) * ((100 - discount) / 100)

    # Return story and answer as a dictionary
    cot = [
        f"{name} bids after each of the {people} people. This means the total number of bids is {people} * 2, which is {people * 2}.",
        f"Therefore, the final bid amount is {begin_money} + ({raise_money} * {people}), which is {ans}."]

    return {"cot": cot, 'problem': stories, 'answer': ans, 'original_problem': original_problem,
            'irrelevant_infos': irrelative_informations}
