from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define lists of names and items
    names = ["Krissa", "Alice", "Beth", "Cindy", "Diana", "Ella", "Fiona", "Gina", "Hannah"]
    items = ["field trip shirts", "graduation hats", "team jerseys", "class sweaters", "camp T-shirts"]

    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)

    # Number needing extra small
    es_num = random.randint(5, 20)

    # Multiplier for small size students
    small_factor = random.choice([2, 3])
    small_num = small_factor * es_num

    # Subtractor for medium size
    max_subtractor = small_num - 2
    if max_subtractor < 2:
        subtractor = 2
    else:
        subtractor = random.randint(2, min(6, max_subtractor))
    medium_num = small_num - subtractor
    if medium_num < 2:
        medium_num = 2  # Ensure at least 2 students need medium

    # Ensure medium_num is even
    if medium_num % 2 != 0:
        medium_num -= 1  # Adjust to make even
        if medium_num < 2:
            medium_num = 2

    large_num = medium_num // 2

    # Random addend for extra-large size
    addend = random.randint(4, 8)
    extra_large_num = large_num + addend

    # Now, construct the premise sentences
    problem = [
        f"{name} needs to order {item} for her preschool students.",
        f"{es_num} students need size extra-small.",
        f"{small_factor} times as many students need size small as extra small.",
        f"{subtractor} less than the number of size small students need size medium.",
        f"Half as many students need size large as size medium.",
        f"{addend} more students need size extra-large than large."
    ]

    # Construct the question
    question = f"Altogether, how many {item} did {name} order?"

    original_problem = problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    irrelevant_items = ["school uniforms", "club hoodies", "sports caps", "band jackets", "debate team blazers"]
    irelevant_item = random.choice(irrelevant_items)
    irrelevant_infos = [
        f"{name} also needs to order {random.randint(2, 10)} extra {irelevant_item}s for the teachers.",
        f"{es_num + random.randint(1, 20)} students need size extra-small for the {irelevant_item}.",
        f"{small_factor + random.randint(1, 5)} times as many students need size small as extra small for the {irelevant_item}.",
    ]

    # Out-topic irrelevant information
    hobbies = ["painting", "swimming", "dancing", "singing", "reading"]
    out_topic_irrelevant_info = f"{name}'s favorite hobby is {random.choice(hobbies)}."
    irrelevant_infos.append(out_topic_irrelevant_info)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    # You can assume these functions are given: introduce_symbol_error and introduce_grammar_error
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except the first one
    main_sentences = problem[1:]
    if shuffle:
        random.shuffle(main_sentences)
    problem = [problem[0]] + main_sentences

    # Add the question at the end
    problem.append(question)

    # Calculate the answer
    answer = es_num + small_num + medium_num + large_num + extra_large_num

    # Return the problem sentences and the answer
    cot = [f"{small_factor} times as many students need size small as extra small, so the number of small size students is {small_factor} * {es_num}, which is {small_num}.", f"{subtractor} less than the number of size small students need size medium, so the number of medium size students is {small_num} - {subtractor}, which is {medium_num}.", f"Half as many students need size large as size medium, so the number of large size students is {medium_num} // 2, which is {large_num}.", f"{addend} more students need size extra-large than large, so the number of extra-large size students is {large_num} + {addend}, which is {extra_large_num}.", f"Altogether, the total number of shirts ordered is {es_num} + {small_num} + {medium_num} + {large_num} + {extra_large_num}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
