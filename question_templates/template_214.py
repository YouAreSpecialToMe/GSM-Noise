from grammar_error import introduce_grammar_error, introduce_symbol_error

import random


# Done
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and relationships
    names = ['Alice', 'Bob', 'Carlos', 'Diana', 'Ellen', 'Fiona', 'George', 'Hannah']
    main_name = random.choice(names)
    names.remove(main_name)
    sibling_relation = random.choice(['brother', 'sister', 'cousin'])
    friend_relation = 'friend'

    # Variables with possible alternative values
    total_sodas = random.randint(10, 100)  # Total number of sodas in the case
    shaken_sodas = random.randint(2, total_sodas // 2)  # Number of sodas shaken
    unshaken_sodas = total_sodas - shaken_sodas

    # Main person takes unshaken sodas
    main_name_sodas_taken = random.randint(1, round(unshaken_sodas / 2) - 1)
    unshaken_sodas -= main_name_sodas_taken

    # Sibling takes shaken and unshaken sodas
    shaken_sodas_taken_by_sibling = random.randint(1, round(unshaken_sodas / 2) - 1)
    shaken_sodas -= shaken_sodas_taken_by_sibling

    unshaken_sodas_taken_by_sibling = random.randint(1, unshaken_sodas - 1)
    unshaken_sodas -= unshaken_sodas_taken_by_sibling

    # Remaining sodas
    total_remaining_sodas = shaken_sodas + unshaken_sodas

    # Compute the answer using the formula
    answer = (shaken_sodas / total_remaining_sodas) * 100 if total_remaining_sodas > 0 else 0

    # Construct the premises
    problem = [
        f"{main_name} decided to play a prank on {main_name}'s {friend_relation}.",
        f"{main_name} got a case of {total_sodas} sodas and shook {shaken_sodas + shaken_sodas_taken_by_sibling} of them up.",
        f"Then {main_name} took {main_name_sodas_taken} unshaken soda for {main_name}self and left.",
        f"{main_name}'s {sibling_relation} stopped by and took {shaken_sodas_taken_by_sibling} of the shaken sodas and {unshaken_sodas_taken_by_sibling} of the unshaken sodas, then {main_name}'s {friend_relation} came along."
    ]
    question = f"What is the likelihood, expressed as a percentage, that {main_name}'s {friend_relation} gets sprayed with soda from a shaken can?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Construct in-topic and out-topic irrelevant information
    irrelevant_infos = [
        f"The sodas were part of a limited edition release.",
        f"{main_name} had been planning the prank for weeks.",
        f"The weather was unusually warm that day.",
        f"{main_name} loves to collect vintage soda cans.",
        f"{main_name} and {main_name}'s {sibling_relation} both drink one bottle of water.",
    ]

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        )
        for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences

    # Construct the question

    problem.append(question)

    # Return the problem and answer
    cot = [
        f"Initially, there are {total_sodas} sodas, out of which {shaken_sodas} are shaken. Therefore, the number of unshaken sodas is {total_sodas} - {shaken_sodas}, which is {unshaken_sodas}.",
        f"{main_name} takes {main_name_sodas_taken} unshaken sodas, leaving {unshaken_sodas} - {main_name_sodas_taken} unshaken sodas.",
        f"The sibling takes {shaken_sodas_taken_by_sibling} shaken sodas, leaving {shaken_sodas} - {shaken_sodas_taken_by_sibling} shaken sodas.",
        f"The sibling also takes {unshaken_sodas_taken_by_sibling} unshaken sodas, leaving {unshaken_sodas} - {unshaken_sodas_taken_by_sibling} unshaken sodas.",
        f"The total remaining sodas are the sum of the remaining shaken and unshaken sodas, which is {shaken_sodas} + {unshaken_sodas}, giving {total_remaining_sodas}.",
        f"The likelihood that {main_name}'s friend gets sprayed with soda from a shaken can is calculated as ({shaken_sodas} / {total_remaining_sodas}) * 100, which results in {answer} percent."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
