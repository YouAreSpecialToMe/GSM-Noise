import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define the list of florist names and supplier names
    florist_names = ["Sandra", "Alice", "Cindy", "Diana", "Linda", "Rachel", "Yvonne", "Victoria", "Beth", "Julia", "Nina", "Hannah", "Wendy"]
    supplier_names = ["Fred", "Bob", "Ethan", "George", "Ivan", "Kevin", "Mike", "Oscar", "Peter", "Quincy", "Tom", "Xavier", "Zach"]

    # Randomly select a florist and a supplier, ensuring they are different
    florist_name = random.choice(florist_names)
    supplier_name = random.choice(supplier_names)
    
    # Define list of flowers
    flowers = [
        {"color": "red", "type": "roses"},
        {"color": "white", "type": "carnations"},
        {"color": "pink", "type": "calla lilies"},
        {"color": "yellow", "type": "tulips"},
        {"color": "blue", "type": "orchids"},
        {"color": "purple", "type": "lilacs"},
        {"color": "orange", "type": "dahlias"},
        {"color": "white", "type": "daisies"},
        {"color": "green", "type": "mums"},
        {"color": "red", "type": "anemones"}
    ]

    # Randomly select three different flowers
    selected_flowers = random.sample(flowers, 3)

    # Assign selected flowers to flower1, flower2, flower3
    flower1 = selected_flowers[0]  # Missing item
    flower2 = selected_flowers[1]
    flower3 = selected_flowers[2]

    # Get the full names of the flowers
    flower1_name = f"{flower1['color']} {flower1['type']}"
    flower2_name = f"{flower2['color']} {flower2['type']}"
    flower3_name = f"{flower3['color']} {flower3['type']}"

    # Set multipliers
    multiplier1 = random.randint(2, 9)
    multiplier2 = random.randint(2, 9)

    # Set number_flower3, ensuring it's divisible by multiplier2
    possible_numbers_flower3 = [i for i in range(50, 501) if i % multiplier2 == 0]
    number_flower3 = random.choice(possible_numbers_flower3)

    # Calculate number_flower2
    number_flower2 = number_flower3 / multiplier2
    number_flower2 = int(number_flower2)

    # Calculate number_flower1
    number_flower1 = multiplier1 * number_flower2

    # Choose a delivery time
    delivery_time = f"{random.randint(1, 11)} pm"

    # Construct the problem sentences
    problem = [
        f"{florist_name}, the florist around the corner, is very unhappy with {supplier_name}'s incomplete order delivery.",
        f"{florist_name} had ordered {multiplier1} times as many {flower1_name} as {flower2_name}.",
        f"{florist_name} also ordered {number_flower3} {flower3_name}, which were {multiplier2} times the number of {flower2_name}.",
        f"{florist_name} has threatened to switch suppliers if the missing {flower1_name} are not delivered by {delivery_time}."
    ]

    import copy
    original_problem = copy.deepcopy(problem)

    # Construct the question
    question = f"To keep {florist_name}'s business, how many {flower1_name} must {supplier_name} deliver by {delivery_time}?"

    # Construct in-topic irrelevant information
    other_flowers = [f for f in flowers if f not in selected_flowers]
    irrelevant_infos = [
        f"{supplier_name} had earlier delivered {random.randint(20,100)} {flower['color']} {flower['type']}, which {florist_name} was pleased with."
        for flower in random.sample(other_flowers, 2)
    ]

    # Construct out-topic irrelevant information
    hobbies = ["playing the guitar", "painting", "cycling", "hiking", "photography", "reading"]
    supplier_hobby = random.choice(hobbies)
    out_topic_irrelevant_info = f"In his free time, {supplier_name} enjoys {supplier_hobby}."
    irrelevant_infos.append(out_topic_irrelevant_info)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in problem
    ]

    # Shuffle the order of sentences, except for the first one
    intro_sentence = problem[0]
    problem_rest = problem[1:]
    if shuffle:
        random.shuffle(problem_rest)
    problem = [intro_sentence] + problem_rest

    # Append the question
    problem.append(question)
    original_problem.append(question)

    # Calculate the answer
    answer = number_flower1

    # Return the problem and answer
    cot = [f"The number of {flower2_name} is calculated by dividing {number_flower3} by {multiplier2}, which gives {number_flower2}.", f"The number of {flower1_name} is {multiplier1} times the number of {flower2_name}, which is {number_flower1}.", f"Therefore, the answer is {number_flower1}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}