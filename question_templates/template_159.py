from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define possible names
    names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Jamie", "Riley", "Drew"]
    hobbies = ["playing basketball", "reading books", "painting", "cooking gourmet meals", "hiking", "writing poetry"]

    # Randomly select a name and a hobby
    name = random.choice(names)
    hobby = random.choice(hobbies)

    # Randomly generate values for the problem
    lines_song = random.randint(40, 100)  # Lines in the solo song

    # First scene variables
    multipliers_scene1 = [2, 3, 4]
    multiplier_scene1 = random.choice(multipliers_scene1)
    fractions_scene1 = [(1, 2), (1, 3), (1, 4)]
    numerator_scene1, denominator_scene1 = random.choice(fractions_scene1)
    fraction_his_scene1 = numerator_scene1 / denominator_scene1

    # Second scene variables
    increment_scene2 = random.randint(5, 10)  # Extra lines compared to the song
    fractions_scene2 = [(3, 4), (4, 5), (2, 3)]
    numerator_scene2, denominator_scene2 = random.choice(fractions_scene2)
    fraction_his_scene2 = numerator_scene2 / denominator_scene2

    # Calculate lines for each scene
    total_lines_scene1 = multiplier_scene1 * lines_song
    his_lines_scene1 = total_lines_scene1 * fraction_his_scene1

    total_lines_scene2 = lines_song + increment_scene2
    his_lines_scene2 = total_lines_scene2 * fraction_his_scene2

    # Total lines to memorize
    total_lines_to_memorize = his_lines_scene1 + his_lines_scene2 + lines_song

    # Construct the problem sentences
    problem = [
        f"{name} is practicing for {name}'s role in a theater production.",
        f"{name} has to memorize {name}'s lines for two scenes and the lyrics to one solo song.",
        f"{name}'s solo song has {lines_song} lines in the lyrics.",
        f"The first scene has {multiplier_scene1} times the number of lines, but only {numerator_scene1}/{denominator_scene1} of them are {name}'s lines.",
        f"The second scene has {increment_scene2} more lines than the song, and {numerator_scene2}/{denominator_scene2} of them are {name}'s.",
    ]

    # Construct the question
    question = f"How many lines does {name} have to memorize?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"{name}'s friend has to memorize {random.randint(20, 50)} more lines than {name}.",
        f"{name}'s line in the first scene is {random.randint(2, 4)} times more than {name}'s friend's line in the second scene.",
        f"{name}'s line in the solo sang is {random.randint(2, 4)} times less than {name}'s friend's line in the first scene.",
    ]

    # Add out-topic irrelevant information
    out_topic_irrelevant_info = f"In {name}'s free time, {name} enjoys {hobby}."

    # Add irrelevant information based on probability
    irrelevant_infos = in_topic_irrelevant_infos + [out_topic_irrelevant_info]

    all_irrelevant_infos = in_topic_irrelevant_infos + [out_topic_irrelevant_info]
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Add symbol or grammar errors. Assume the functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences

    # Add the question at the end
    problem.append(question)

    # Calculate the answer
    answer = his_lines_scene1 + his_lines_scene2 + lines_song

    # Return the problem and answer as a dictionary
    cot = [f"The first scene has {multiplier_scene1} times the number of lines as the solo song, which means it has {total_lines_scene1} lines.", f"Out of these, {numerator_scene1}/{denominator_scene1} are {name}'s lines, which is {his_lines_scene1}.", f"The second scene has {increment_scene2} more lines than the solo song, making it {total_lines_scene2} lines long.", f"Out of these, {numerator_scene2}/{denominator_scene2} are {name}'s lines, which is {his_lines_scene2}.", f"Adding the lines from the solo song, {lines_song}, the total number of lines {name} has to memorize is {total_lines_to_memorize}.", f"Therefore, the final answer is {total_lines_to_memorize}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
