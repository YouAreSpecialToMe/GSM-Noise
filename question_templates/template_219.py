from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
# Done
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define a list of possible names
    names = ["Kim", "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Jamie", "Riley", "Pat", "Drew"]

    # Randomly select a name
    name = random.choice(names)

    # Randomly generate usual sleep time and wake-up time
    sleep_time_hour = random.randint(9, 11)  # Usual sleep time between 9 p.m. and 11 p.m.
    wake_time_hour = random.randint(5, 8)    # Usual wake-up time between 5 a.m. and 8 a.m.



    # Randomly generate sleepwalking start and end times within the sleep period
    sleepwalking_start_hour = random.randint(1, 5)  # Between 1 a.m. and 5 a.m.
    sleepwalking_start_minute = random.randint(0, 59)
    sleepwalking_duration = random.randint(10, 30)  # Sleepwalking duration between 10 and 30 minutes
    sleepwalking_end_hour = sleepwalking_start_hour + (sleepwalking_start_minute + sleepwalking_duration) // 60
    sleepwalking_end_minute = (sleepwalking_start_minute + sleepwalking_duration) % 60

    # Randomly generate minutes woke up earlier than usual
    woke_up_earlier_minutes = random.randint(1, 15)

    # Additional variables for irrelevant information
    dream = random.choice(["flying", "falling", "being chased", "losing teeth", "taking an exam"])
    pet = random.choice(["cat", "dog", "hamster", "parrot", "rabbit"])
    hobby = random.choice(["painting", "playing the piano", "cycling", "hiking", "photography"])
    city = random.choice(["New York", "Paris", "Tokyo", "Sydney", "Rio de Janeiro"])
    age = random.randint(20, 50)

    # Construct the premise content, breaking it down into sentences
    problem = [
        f"{name} sleepwalks. To monitor {name}'s sleeping hours, {name} installs a camera in {name}'s room.",
        f"{name} usually goes to sleep at {sleep_time_hour} p.m. and wakes up at {wake_time_hour} a.m.",
        f"One day, after reviewing the cameras, {name} finds that {name} was sleepwalking from {sleepwalking_start_hour}:{sleepwalking_start_minute:02d} to {sleepwalking_end_hour}:{sleepwalking_end_minute:02d} a.m.",
        f"Also, that day {name} woke up {woke_up_earlier_minutes} minutes earlier than usual to go to the bathroom.",
    ]

    # Construct the question
    question = f"How many minutes did {name} sleep on {name}'s bed that day?"
    original_problem = problem.copy()
    original_problem.append(question)
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} had a dream about {dream} that night.",
        f"{name} usually sleeps with {name}'s pet {pet}.",
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} enjoys {hobby} during the weekends.")
    irrelevant_infos.append(f"{name} recently visited {city}.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (assumed to be given functions)
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

    # Add the question
    problem.append(question)

    # Calculate the answer
    # Total usual sleep minutes
    total_sleep_minutes = (12 - sleep_time_hour + wake_time_hour) * 60

    # Sleepwalking duration
    sleepwalking_duration_minutes = sleepwalking_duration

    # Total sleep time on bed
    answer = total_sleep_minutes - sleepwalking_duration_minutes - woke_up_earlier_minutes

    # Return premise and answer as a dictionary
    cot = [f"{name} usually sleeps from {sleep_time_hour} p.m. to {wake_time_hour} a.m., which is a total of (12 - {sleep_time_hour} + {wake_time_hour}) * 60 minutes, or {total_sleep_minutes} minutes.", f"On that day, {name} was sleepwalking for {sleepwalking_duration} minutes.", f"{name} also woke up {woke_up_earlier_minutes} minutes earlier than usual.", f"Therefore, the total sleep time on the bed is {total_sleep_minutes} - {sleepwalking_duration} - {woke_up_earlier_minutes}, which is equal to {answer} minutes."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
