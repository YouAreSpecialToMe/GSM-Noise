import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible values
    names = ["Tim", "Jim", "Sam", "Dan", "Ben", "Ron", "Max", "Eli", "Leo", "Kai"]
    base_lengths = [4, 5, 6, 7, 8]
    heights = [10, 12, 15, 18, 20]
    bean_volumes = [0.10, 0.12, 0.15, 0.18, 0.20]
    packing_efficiencies = [0.70, 0.75, 0.80, 0.85, 0.90]
    estimated_red_percents = [0.25, 0.30, 0.35]
    actual_red_beans_list = [700, 800, 900, 1000]
    
    # Original variables for ground truth answer
    original_name = "Tim"
    original_base_length = 6
    original_height = 15
    original_bean_volume = 0.15
    original_packing_efficiency = 0.80
    original_estimated_red_percent = 0.30
    original_actual_red_beans = 900
    
    # Randomly assign variables
    name = random.choice(names)
    base_length = random.choice(base_lengths)
    height = random.choice(heights)
    bean_volume = random.choice(bean_volumes)
    packing_efficiency = random.choice(packing_efficiencies)
    estimated_red_percent = random.choice(estimated_red_percents)
    actual_red_beans = random.choice(actual_red_beans_list)
    
    # Construct the problem premises
    problem = [
        f"{name} enters a competition and has to try and guess the number of red jelly beans in a jar.",
        f"The jar has a square base and is {base_length} inches by {base_length} inches and {height} inches tall.",
        f"{name} knows that a jelly bean is {bean_volume} cubic inches.",
        f"{name} also knows that they get about {packing_efficiency*100}% efficiency in packing.",
        f"{name} estimates {estimated_red_percent*100}% of the jelly beans are red.",
        f"The true number of red jelly beans in the container is {actual_red_beans}."
    ]
    
    import copy
    original_problem = copy.deepcopy(problem)

    # Construct the question
    question = "How far off was his guess?"
    
    # Add in-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"The jar is made of recycled glass.",
        f"The jelly beans come in various flavors.",
        f"The competition is held every year during the summer festival."
    ]
    
    # Add out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{name} enjoys playing basketball in his free time.",
        f"{name} has a pet dog named Buddy.",
        f"{name} is studying computer science at university."
    ]
    
    # Combine irrelevant information
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    
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
    problem_body = problem[1:]
    if shuffle:
        random.shuffle(problem_body)
    problem = [problem[0]] + problem_body
    
    # Add the question
    problem.append(question)
    original_problem.append(question)

    # Calculate the answer
    # Compute the jar volume
    jar_volume = base_length * base_length * height
    effective_volume = jar_volume * packing_efficiency
    total_jelly_beans = effective_volume / bean_volume
    estimated_red_beans = total_jelly_beans * estimated_red_percent
    difference = abs(actual_red_beans - estimated_red_beans)
    answer = difference
    
    # Ensure the answer matches ground truth when using original values
    if (name == original_name and
        base_length == original_base_length and
        height == original_height and
        bean_volume == original_bean_volume and
        packing_efficiency == original_packing_efficiency and
        estimated_red_percent == original_estimated_red_percent and
        actual_red_beans == original_actual_red_beans):
        
        # Re-calculate using original values to ensure correctness
        jar_volume = original_base_length * original_base_length * original_height
        effective_volume = jar_volume * original_packing_efficiency
        total_jelly_beans = effective_volume / original_bean_volume
        estimated_red_beans = total_jelly_beans * original_estimated_red_percent
        difference = abs(original_actual_red_beans - estimated_red_beans)
        answer = difference  # This should be 36
    
    # Return the problem and the answer
    cot = [f"Calculate the volume of the jar by multiplying {base_length} by {base_length} and then by {height}, resulting in {jar_volume}.", f"Determine the effective volume by multiplying {jar_volume} by {packing_efficiency}, which gives {effective_volume}.", f"Calculate the total number of jelly beans by dividing {effective_volume} by {bean_volume}, resulting in {total_jelly_beans}.", f"Estimate the number of red jelly beans by multiplying {total_jelly_beans} by {estimated_red_percent}, which gives {estimated_red_beans}.", f"Find the difference between the actual number of red jelly beans, {actual_red_beans}, and the estimated number, {estimated_red_beans}, resulting in {difference}.", f"The final answer, representing how far off the guess was, is {difference}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}