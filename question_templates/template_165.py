from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and races
    names = ['Alex', 'Bailey', 'Casey', 'Dakota', 'Emerson', 'Finley', 'Morgan', 'Reese', 'Riley', 'Skyler', 'Taylor']
    races = ['100-meter race', '200-meter sprint', '400-meter dash', '800-meter run', '1500-meter run']

    # Randomly select a name and a race
    name = random.choice(names)
    race = random.choice(races)

    # Set starting position
    start_position = 1

    # Randomly generate movements
    fall_back_1 = random.randint(3, 10)
    move_ahead_1 = random.randint(1, fall_back_1 - 1)
    fell_behind_2 = random.randint(1, 5)
    max_jump_ahead = min(fell_behind_2 + move_ahead_1 - 1, 5)
    if max_jump_ahead < 1:
        max_jump_ahead = 1
    jumped_ahead_2 = random.randint(1, max_jump_ahead)

    # Ensure the final position is valid
    position = start_position + fall_back_1 - move_ahead_1 + fell_behind_2 - jumped_ahead_2
    while position < 1:
        fall_back_1 = random.randint(3, 10)
        move_ahead_1 = random.randint(1, fall_back_1 - 1)
        fell_behind_2 = random.randint(1, 5)
        max_jump_ahead = min(fell_behind_2 + move_ahead_1 - 1, 5)
        if max_jump_ahead < 1:
            max_jump_ahead = 1
        jumped_ahead_2 = random.randint(1, max_jump_ahead)
        position = start_position + fall_back_1 - move_ahead_1 + fell_behind_2 - jumped_ahead_2

    # Calculate the final answer
    # answer = start_position + fall_back_1 - move_ahead_1 + fell_behind_2 - jumped_ahead_2
    answer = position

    # Construct the problem statements
    problem = [
        f"{name} took part in a {race}.",
        f"{name} started off in {start_position}st place, but then fell back {fall_back_1} spots.",
        f"{name} then moved ahead {move_ahead_1} spots, before falling behind {fell_behind_2} spots.",
        f"Lastly, {name} jumped ahead {jumped_ahead_2} spots to finish the race."
    ]

    # Construct the question
    question = f"What place did {name} finish in?"

    original_problem = problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    in_topic_irrelevant = [
        f"{name}'s friend was {fall_back_1 + random.randint(1, 5)} spots ahead of {name} at the start."
        f"{name}'s friend then moved {move_ahead_1 + random.randint(1, 5)} spots, before falling behind {fell_behind_2 + random.randint(1, 5)} spots.",
        f"There were a total of {random.randint(30, 100)} runners in the race."
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant = [
        f"{name} had a breakfast of {random.choice(['pancakes', 'eggs', 'cereal'])} before the race.",
    ]

    # Combine irrelevant information
    irrelevant_infos = in_topic_irrelevant + out_topic_irrelevant

    # Add irrelevant information based on probability
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Add symbol or grammar errors (Assumed functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in problem
    ]

    # Shuffle the main sentences except the first one
    main_sentences = problem[1:]
    if shuffle:
        random.shuffle(main_sentences)
    problem = [problem[0]] + main_sentences

    # Add the question
    problem.append(question)

    # Return the problem and the answer
    cot = [f"{name} started in {start_position}st place.", f"{name} fell back {fall_back_1} spots, moving to position {start_position} + {fall_back_1}.", f"{name} then moved ahead {move_ahead_1} spots, moving to position {start_position} + {fall_back_1} - {move_ahead_1}.", f"{name} fell behind {fell_behind_2} spots, moving to position {start_position} + {fall_back_1} - {move_ahead_1} + {fell_behind_2}.", f"Lastly, {name} jumped ahead {jumped_ahead_2} spots, moving to position {start_position} + {fall_back_1} - {move_ahead_1} + {fell_behind_2} - {jumped_ahead_2}.", f"Therefore, {name} finished in position {position}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
