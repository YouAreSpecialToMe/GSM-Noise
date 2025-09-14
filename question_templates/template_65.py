import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of names
    names = ['Alice', 'Bob', 'Carlos', 'Diana', 'Eva', 'Frank', 'Grace', 'Helen', 'Ivan', 'Julia', 'Mark', 'Nina', 'Oscar', 'Paula', 'Quincy', 'Rachel', 'Sam', 'Tina', 'Uma', 'Victor', 'Wendy', 'Xavier', 'Yvonne', 'Zach']

    # Define occupations
    occupations = ['copy-editor', 'translator', 'proofreader', 'editor', 'writer', 'journalist']

    # Randomly select a name and occupation
    name = random.choice(names)
    occupation = random.choice(occupations)

    # Publishers
    publishers = ['Publisher A', 'Publisher B']

    # Randomly generate numeric variables
    total_sentences = random.randint(500, 2000)
    total_sentences -= total_sentences % 50  # Round to nearest multiple of 50

    rate_publisher_A = random.randint(1, 10)  # Cents per sentence
    rate_multiplier = random.randint(2, 5)    # Multiplier for Publisher B's rate
    rate_publisher_B = rate_publisher_A * rate_multiplier

    # Construct the premise content
    problem = [
        f"{name} is a {occupation}.",
        f"{name} edits an equal number of sentences each week for two different publishers, who each pay {name} a different rate per sentence.",
        f"Publisher B pays {name} {rate_multiplier} times what Publisher A pays.",
        f"{name} edits a total number of {total_sentences} sentences each week, and Publisher A pays {name} {rate_publisher_A} cents per sentence."
    ]

    import copy
    original_problem = copy.deepcopy(problem)

    # Construct the question
    question = f"How much does {name} make in a week, in cents?"

    # Add in-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"{name} also writes articles for a local newspaper.",
        f"{name} is considering taking up an additional job as a freelance {occupation}.",
        f"The publishers sometimes give {name} bonuses for exceptional work."
    ]

    # Add out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{name} enjoys hiking and recently climbed {random.randint(1,10)} mountains.",
        f"{name} has a collection of {random.randint(5,20)} vintage cars.",
        f"{name} is training for a marathon."
    ]

    # Randomly add irrelevant information
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

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

    # Add the question
    problem.append(question)
    original_problem.append(question)

    # Calculate the answer
    sentences_per_publisher = total_sentences / 2
    earning_publisher_A = sentences_per_publisher * rate_publisher_A
    earning_publisher_B = sentences_per_publisher * rate_publisher_B
    answer = earning_publisher_A + earning_publisher_B

    # Return the problem and the answer
    cot = [f"{name} edits a total of {total_sentences} sentences each week, so each publisher gets {total_sentences} / 2, which is {sentences_per_publisher} sentences.", f"Publisher A pays {rate_publisher_A} cents per sentence, so {name} earns {sentences_per_publisher} * {rate_publisher_A}, which is {earning_publisher_A} cents from Publisher A.", f"Publisher B pays {rate_multiplier} times what Publisher A pays, so the rate is {rate_publisher_A} * {rate_multiplier}, which is {rate_publisher_B} cents per sentence.", f"{name} earns {sentences_per_publisher} * {rate_publisher_B}, which is {earning_publisher_B} cents from Publisher B.", f"Therefore, the total earnings in a week are {earning_publisher_A} + {earning_publisher_B}, which is {answer} cents."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}