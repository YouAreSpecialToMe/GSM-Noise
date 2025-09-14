from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and color lists
    names = ["Sally", "Bob", "Alice", "Carlos", "Daisy", "Ethan", "Fiona", "George", "Hannah", "Ian"]
    colors = ["red", "green", "yellow", "blue", "purple", "orange", "pink", "white", "black", "silver", "gold"]

    # Randomly select a name
    name = random.choice(names)

    # Randomly select colors, ensuring they are unique
    first_color = random.choice(colors)
    colors_remaining = [color for color in colors if color != first_color]
    second_color = random.choice(colors_remaining)
    colors_remaining.remove(second_color)
    third_color = random.choice(colors_remaining)

    # Assign starting balloon counts
    first_color_balloons = random.randint(10, 30)
    second_color_balloons = random.randint(5, 20)
    third_color_balloons = random.randint(5, 20)

    # Burst percentage for first_color balloons
    burst_percentage = random.choice([10, 20, 25, 33, 40, 50])

    # Release fraction for third_color balloons
    release_fraction_options = {'half': 0.5, 'one third': 1 / 3, 'one quarter': 0.25}
    release_fraction_name, release_fraction_value = random.choice(list(release_fraction_options.items()))

    # Found balloons and percentage added
    found_balloons = random.randint(5, 12)
    added_percentage = random.choice([50, 60, 66, 75, 80, 90, 100])

    # Prepare in-topic irrelevant information
    favorite_color = random.choice([color for color in colors if color not in [first_color, second_color, third_color]])
    distance_to_school = round(random.uniform(0.5, 5), 2)
    balloon_stores = ["The Balloon Emporium", "Balloon World", "Balloons R Us", "The Party Store",
                      "Inflate & Celebrate"]
    balloon_store = random.choice(balloon_stores)
    study_hours = random.randint(1, 5)

    # Construct the problem sentences
    problem = [
        f"As {name} walked to school, {name} was holding the strings to {first_color_balloons} {first_color} balloons, {second_color_balloons} {second_color} balloons, and {third_color_balloons} {third_color} balloons.",
        f"Suddenly, a gust of wind caused {burst_percentage}% of the {first_color} balloons to burst.",
        f"The shockingly loud sound startled {name}, and {name} accidentally released {release_fraction_name} of the {third_color} balloons.",
        f"But as {name} neared the school grounds, {name} found {found_balloons} blue balloons caught in a tree, and {name} added {added_percentage}% of them to {name}'s remaining clutch of balloons, which {name} carried into the school."
    ]

    # Construct the question
    question = f"What number of balloons did {name} finally carry into the school?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add irrelevant information based on probability
    irrelevant_colors = ["brown", "gray", "cyan", "lime", "magenta", "teal", "navy", "olive", "maroon"]
    irre_color1, irre_color2 = random.sample(irrelevant_colors, 2)
    irrelevant_infos = [
        f"The wind was caused {random.randint(10, 90)} percent of the {irre_color1} balloons to burst.",
        f"{random.randint(10, 30)} of the {irre_color2} balloons were released by {name}'s friend.",
        f"The number of {irre_color1} balloons found by {name}'s friend was {random.randint(1, 10)}.",
    ]

    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Replace variables in the problem with format {variable_name}
    # problem = [p.format(
    #     first_color_balloons='{first_color_balloons}',
    #     first_color='{first_color}',
    #     second_color_balloons='{second_color_balloons}',
    #     second_color='{second_color}',
    #     third_color_balloons='{third_color_balloons}',
    #     third_color='{third_color}',
    #     burst_percentage='{burst_percentage}',
    #     release_fraction_name='{release_fraction_name}',
    #     found_balloons='{found_balloons}',
    #     added_percentage='{added_percentage}',
    # ) for p in problem]

    # Apply symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the sentences except the first one
    first_sentence = problem[0]
    rest_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_sentences)
    problem = [first_sentence] + rest_sentences + [question]

    # Calculate the answer
    # answer = (first_color_balloons - (first_color_balloons * burst_percentage / 100)) + second_color_balloons + (third_color_balloons - (third_color_balloons * release_fraction_value)) + (found_balloons * added_percentage / 100)
    answer = (
            (first_color_balloons - (first_color_balloons * burst_percentage / 100)) +
            second_color_balloons +
            (third_color_balloons - (third_color_balloons * release_fraction_value)) +
            (found_balloons * added_percentage / 100)
    )
    answer = int(answer)

    # Return the problem and answer as a dictionary
    cot = [f"{name} initially has {first_color_balloons} balloons of the first color.", f"A gust of wind causes {burst_percentage}% of the first color balloons to burst, leaving {first_color_balloons - (first_color_balloons * burst_percentage / 100)}.", f"{name} also has {second_color_balloons} balloons of the second color.", f"{name} accidentally releases {release_fraction_value * 100}% of the third color balloons, leaving {third_color_balloons - (third_color_balloons * release_fraction_value)}.", f"{name} finds {found_balloons} blue balloons and adds {added_percentage}% of them, which is {(found_balloons * added_percentage / 100)}.", f"The total number of balloons {name} carries into the school is the sum of all remaining balloons: {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
