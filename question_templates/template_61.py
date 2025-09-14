import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):

    # Define lists of names and relatives
    names = ["Alex", "Charlie", "Jordan", "Taylor", "Sam", "Morgan", "Pat", "Jamie", "Lee", "Casey"]
    relatives = ["niece", "nephew", "son", "daughter", "cousin", "grandchild", "godchild"]

    # Randomly select a name and a relative
    name = random.choice(names)
    relative = random.choice(relatives)

    # Define toys and their quantities
    # Toy1: building blocks
    toy1_name = "bag of building blocks"
    number_blocks = random.randint(20,50) # between 20 and 50

    # Toy2: stuffed animals
    toy2_name = "bin of stuffed animals"
    number_stuffed_animals = random.randint(5,15)

    # Toy3: stacking rings
    toy3_name = "tower of stacking rings"
    number_rings = random.randint(5,15)

    # Toy4: various options
    toy4_options = [("tube of bouncy balls", "bouncy balls"),
                    ("box of crayons", "crayons"),
                    ("set of puzzle pieces", "puzzle pieces"),
                    ("pack of toy cars", "toy cars"),
                    ("bundle of action figures", "action figures")]
    toy4_choice = random.choice(toy4_options)
    toy4_name = toy4_choice[0]
    toy4_item_name = toy4_choice[1]

    # Calculate total number of toys, total known toys (without toy4)
    total_known_toys = number_blocks + number_stuffed_animals + number_rings
    # Randomly decide on total number of toys
    total_toys = total_known_toys + random.randint(10,30) # Randomly add between 10 and 30 toys

    # Compute the number of items in toy4
    number_toy4_items = total_toys - total_known_toys

    # Construct the premise content, replacing values with variable names in format {variable_name}
    problem_sentences = [
        f"When {name} watches {name}'s {relative}, {name} gets out a variety of toys for {relative}.",
        f"The {toy1_name} has {number_blocks} blocks in it.",
        f"The {toy2_name} has {number_stuffed_animals} stuffed animals inside.",
        f"The {toy3_name} has {number_rings} multicolored rings on it.",
        f"{name} recently bought a {toy4_name}, bringing {name}'s total number of toys for {relative} up to {total_toys}."
    ]

    import copy
    original_problem = copy.deepcopy(problem_sentences)

    # Resolve pronouns (e.g., use {name} instead of 'she' or 'his/her')
    # In this problem, pronouns are already avoided by using the name

    # Construct the question
    question = f"How many {toy4_item_name} came in the {toy4_name}?"

    # Add in-topic irrelevant information
    irrelevant_infos_in_topic = [
        f"{name} keeps the toys in a large toy chest.",
        f"{name} also has a collection of educational books for {relative}.",
        f"The {toy1_name} was a gift from {name}'s {random.choice(['friend', 'sibling', 'parent'])}."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos_out_topic = [
        f"{name} works as a {random.choice(['engineer', 'teacher', 'artist', 'doctor'])}.",
        f"In {name}'s free time, {name} enjoys hiking and photography.",
        f"{name} has a pet {random.choice(['dog', 'cat', 'parrot', 'rabbit'])} named {random.choice(['Buddy', 'Mittens', 'Coco', 'Max'])}."
    ]

    # Combine irrelevant informations
    irrelevant_infos = irrelevant_infos_in_topic + irrelevant_infos_out_topic

    # Decide whether to add irrelevant information based on prob_irre
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem_sentences.append(info)

    # Add symbol or grammar errors (assuming we have introduce_symbol_error and introduce_grammar_error functions)
    problem_sentences = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in problem_sentences
    ]
    # Shuffle the order of sentences, except perhaps the first one
    first_sentence = problem_sentences[0]
    other_sentences = problem_sentences[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem_sentences = [first_sentence] + other_sentences

    # Append the question
    problem_sentences.append(question)
    original_problem.append(question)

    # Calculate the answer
    answer = number_toy4_items

    # Replace variables in the problem sentences
    # problem_sentences = [
    #     sentence.format(
    #         number_blocks=number_blocks,
    #         number_stuffed_animals=number_stuffed_animals,
    #         number_rings=number_rings,
    #         total_toys=total_toys
    #     ) for sentence in problem_sentences
    # ]

    # Return the problem and the answer as a dictionary
    cot = [f"Calculate the total number of known toys by adding {number_blocks}, {number_stuffed_animals}, and {number_rings}, which gives {total_known_toys}.", f"Subtract the total known toys {total_known_toys} from the total number of toys {total_toys} to find the number of {toy4_item_name} in the {toy4_name}, which is {number_toy4_items}.", f"Therefore, the final answer is {number_toy4_items}."]
    
    return {"cot": cot, 'problem': problem_sentences, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}