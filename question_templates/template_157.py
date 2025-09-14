from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists for pirate crew names, islands, treasure items, pirate names
    pirate_crews = ["Blackbeard's Crew", "Captain Kidd's Band", "Redbeard's Pirates", "The Jolly Rogers",
                    "Silver's Company", "Calico Jack's Fleet"]
    islands = ["Isle of Tortuga", "Skull Island", "Dead Man's Cay", "Cutthroat Cove", "Isla de Muerta",
               "Treasure Island"]
    treasure_items = ["treasure chest full of gold", "sarcophagus filled with jewels", "ancient relic", "lost map",
                      "golden compass", "enchanted sword"]
    pirate_names = ["Captain Jack", "Captain Hook", "Captain Flint", "Captain Morgan", "Captain Sparrow",
                    "Captain Davy"]

    # Randomly select pirate crew and island
    pirate_crew = random.choice(pirate_crews)
    island = random.choice(islands)
    treasure_item = random.choice(treasure_items)
    pirate_name = random.choice(pirate_names)

    # Assign original variables to maintain the ground truth answer
    holes_day1 = random.randint(10, 30)  # Number of holes dug on the first day
    holes_day2 = random.randint(5, 35)  # Number of holes dug on the second day
    holes_day3 = random.randint(7, 33)  # Number of holes dug on the third day
    holes_filled = random.randint(10, 20)  # Number of holes filled on the third day
    multiplier = random.randint(10,
                                50)  # The island had four times as many holes by then as it did at the end of the first day

    # Calculate total holes at the end of the first day
    H1 = holes_day1
    # Calculate holes at the end of the third day after filling in holes
    H3 = H1 + holes_day2 + holes_day3 - holes_filled
    # Calculate total holes needed by the fourth day
    H_total = multiplier * H1
    # Calculate holes dug on the fourth day
    holes_day4 = H_total - H3
    # The final answer
    answer = holes_day4

    # Construct the premise content
    problem = [
        f"A pirate crew named {pirate_crew} is digging for buried treasure on the island {island} marked X on a map.",
        f"They dug {holes_day1} holes the first day, {holes_day2} holes the second day, and {holes_day3} holes the third day.",
        f"They stopped digging early on the third day to fill in {holes_filled} holes the pirates kept falling in.",
        f"On the fourth day of digging, they unearthed a {treasure_item}.",
        f"The island had {multiplier} times as many holes by then as it did at the end of the first day."
    ]

    # Construct the question
    question = "How many holes did the pirates dig on the fourth day before finding the treasure?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"On the fifth day, the pirates dug {random.randint(5, 15)} more holes than they did on the first day.",
        f"On the fifth day, the pirates filled in {random.randint(1, 5)} more holes than they did on the third day.",
        f"On the sixth day, the pirates tried to dig {random.randint(5, 15)} holes but found nothing."
    ]

    # Add out-topic irrelevant information
    out_topic_irrelevant_info = "Meanwhile, in a distant kingdom, a dragon was spotted flying over the mountains."
    irrelevant_infos.append(out_topic_irrelevant_info)

    # Randomly add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (assumed functions)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    problem_body = problem[1:]
    if shuffle:
        random.shuffle(problem_body)
    problem = [problem[0]] + problem_body

    # Add the question
    problem.append(question)

    # Return the problem and answer
    cot = [f"The number of holes dug on the first day is {holes_day1}, so {H1} = {holes_day1}.", f"By the end of the third day, the total number of holes is {H1} + {holes_day2} + {holes_day3} - {holes_filled}, which is {H3}.", f"The island had {multiplier} times as many holes by then as it did at the end of the first day, so the total number of holes needed is {multiplier} * {H1}, which is {H_total}.", f"The number of holes dug on the fourth day is {H_total} - {H3}, which is {holes_day4}.", f"Therefore, the final answer is {holes_day4}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
