from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and item lists
    names = ["Lucy", "Alice", "Beth", "Cindy", "Diana", "Eve", "Olivia", "Will", "Sam", "Alex"]
    items = ["apples", "oranges", "pears", "bananas", "peaches"]

    # Randomly select a name and an item
    name = random.choice(names)
    item_name = random.choice(items)

    # Randomly generate values
    price_per_item = random.randint(1, 10)  # Price per item in dollars
    money_got_monday = random.randint(20, 100)  # Money got from selling items picked on Monday
    items_picked_tuesday = random.randint(5, 20)  # Items picked on Tuesday

    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"{name} sells {item_name} from {name}'s orchard at ${price_per_item} per piece.",
        f"On Monday, {name} sold all the {item_name} picked.",
        f"On Tuesday, {name} picked {items_picked_tuesday} {item_name}.",
        f"On Wednesday, {name} picked double the number of {item_name} {name} did the previous day.",
        f"{name} got ${money_got_monday} from selling the {item_name} picked on Monday."
    ]

    question = f"How many {item_name} did {name} pick over the three days?"
    original_problem = problem.copy()
    original_problem.append(question)


    # Replace the variable placeholders with their values
    # problem = [sentence.format(
    #     name=name,
    #     item_name=item_name,
    #     price_per_item=price_per_item,
    #     items_picked_tuesday=items_picked_tuesday,
    #     money_got_monday=money_got_monday
    # ) for sentence in problem]

    # In-topic irrelevant information
    in_topic_irrelevant_infos = [
        "{name} also sells {other_item} at the local market.".format(
            name=name,
            other_item=random.choice([item for item in items if item != item_name])
        ),
        "{name} plans to plant more {item_name} trees next year.".format(
            name=name, item_name=item_name
        ),
        "On Sunday, {name} took a day off from picking {item_name}.".format(
            name=name, item_name=item_name
        ),
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant_infos = [
        "{name} enjoys painting landscapes in {pronoun} free time.".format(
            name=name,
            pronoun='his' if name in ["Will", "Sam", "Alex"] else 'her'
        ),
        "{name} adopted a puppy last weekend.".format(name=name),
        "{name} is saving up to buy a new car.".format(name=name),
    ]

    # Add irrelevant information based on probability
    irrelevant_infos = []
    for info in in_topic_irrelevant_infos + out_topic_irrelevant_infos:
        if random.random() < prob_irre:
            irrelevant_infos.append(info)

    # Combine all sentences
    all_sentences = problem[:-1] + irrelevant_infos + [problem[-1]]

    # Apply symbol or grammar errors
    # Assume functions introduce_symbol_error and introduce_grammar_error are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in all_sentences
    ]
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem + [question]

    # Calculate the answer
    items_sold_monday = money_got_monday / price_per_item
    items_picked_wednesday = 2 * items_picked_tuesday
    total_items_picked = items_sold_monday + items_picked_tuesday + items_picked_wednesday
    answer = total_items_picked

    # Return the problem and answer
    cot = [f"{name} sold all the {item_name} picked on Monday for ${money_got_monday}. Since each {item_name} costs ${price_per_item}, the number of {item_name} sold on Monday is {money_got_monday} / {price_per_item}, which is {items_sold_monday}.", f"On Tuesday, {name} picked {items_picked_tuesday} {item_name}.", f"On Wednesday, {name} picked double the number of {item_name} picked on Tuesday, which is 2 * {items_picked_tuesday}, resulting in {items_picked_wednesday} {item_name}.", f"The total number of {item_name} picked over the three days is {items_sold_monday} + {items_picked_tuesday} + {items_picked_wednesday}, which is {total_items_picked}.", f"Therefore, the final answer is {total_items_picked}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
