from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and items
    names = ["Ethan", "Olivia", "Liam", "Sophia", "Noah", "Ava", "Mason", "Mia", "Lucas", "Isabella", "Toby"]
    items = ["book", "novel", "magazine", "report", "article", "document"]

    # Randomly select a name and item
    name = random.choice(names)
    item = random.choice(items)

    # Define possible values
    pages_options = [45, random.randint(20, 100)]
    words_per_page_options = [200, random.randint(150, 500)]
    reading_rate_options = [300, random.randint(100, 500)]
    time_until_event_options = [60, random.randint(30, 120)]
    time_to_destination_options = [10, random.randint(5, 30)]

    # Randomly assign variables
    pages = random.choice(pages_options)
    words_per_page = random.choice(words_per_page_options)
    reading_rate = random.choice(reading_rate_options)
    time_until_event = random.choice(time_until_event_options)
    time_to_destination = random.choice(time_to_destination_options)

    # Construct the premises
    problem = [
        f"{name} is reading a {item} that is {pages} pages long.",
        f"It averages {words_per_page} words per page.",
        f"{name} can read at a rate of {reading_rate} words per minute.",
        f"{name} has to be at the airport in {time_until_event} minutes and plans to leave as soon as {name} finishes the {item}.",
        f"It takes {time_to_destination} minutes to get to the airport."
    ]

    original_problem = problem.copy()

    # Construct in-topic irrelevant information
    in_topic_irrelevant = [
        f"The {item} was read by {name}'s sister in {words_per_page * reading_rate + random.randint(100, 400)} minutes",
        f"The pages are {random.randint(3, 10)} tree sticks long",
        f"{name}'s brother can read {item} a rate of {reading_rate + 4} words per minute."
    ]

    # Construct out-topic irrelevant information
    out_topic_irrelevant = [
        f"{name} has a dog named Max.",
        f"{name} won a prize in a cooking contest last month.",
    ]

    irrelevant_infos = in_topic_irrelevant + out_topic_irrelevant

    # Add irrelevant information based on given probabilities
    for sentence in in_topic_irrelevant:
        if random.random() < prob_irre:
            problem.append(sentence)

    for sentence in out_topic_irrelevant:
        if random.random() < prob_irre:
            problem.append(sentence)

    # Shuffle the problem sentences except the first one
    first_sentence = problem[0]
    rest_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_sentences)
    problem = [first_sentence] + rest_sentences

    # Add the question
    question = f"How many minutes early will {name} be?"
    problem.append(question)
    original_problem.append(question)

    # Apply grammar and symbol errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Compute the answer using the variables
    total_words = pages * words_per_page
    reading_time = total_words / reading_rate
    total_time = reading_time + time_to_destination
    minutes_early = time_until_event - total_time
    answer = minutes_early

    # Return the problem and the answer
    cot = [f"Calculate the total number of words in the {item} by multiplying the number of {pages} by the {words_per_page}, which gives {total_words}.", f"Determine the {reading_time} by dividing the {total_words} by the {reading_rate}.", f"Add the {reading_time} to the {time_to_destination} to get the {total_time}.", f"Subtract the {total_time} from the {time_until_event} to find out how many minutes early {name} will be, which is {minutes_early}.", f"Therefore, the final answer is {minutes_early}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
