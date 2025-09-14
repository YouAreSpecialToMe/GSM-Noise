from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Variable options
    total_seniors_options = [30, 35, 40, 44, 50, 55, 60]
    frame_cost_options = [15, 20, 25, 30, 35]
    etching_cost_percentage_options = [10, 15, 20, 25, 30]
    number_of_pins_options = [1, 2, 3, 4, 5]
    pin_cost_options = [4, 5, 6, 7, 8, 9, 10]
    officer_fraction_options = [(1, 5), (1, 4), (1, 3), (1, 6), (1, 2)]
    cord_cost_options = [10, 12, 14, 16, 18, 20]
    mascots = ['Eagles', 'Tigers', 'Lions', 'Hawks']

    # Randomly select variable values
    total_seniors = random.choice(total_seniors_options)
    frame_cost = random.choice(frame_cost_options)
    etching_cost_percentage = random.choice(etching_cost_percentage_options)
    number_of_pins = random.choice(number_of_pins_options)
    pin_cost = random.choice(pin_cost_options)
    officer_fraction = random.choice(officer_fraction_options)
    cord_cost = random.choice(cord_cost_options)

    officer_fraction_numerator = officer_fraction[0]
    officer_fraction_denominator = officer_fraction[1]

    # Sentences with variables
    problem = [
        f"{total_seniors} seniors need to receive awards.",
        f"Each senior receives a picture frame that costs ${frame_cost}.",
        f"Each picture frame needs to be etched with the logo for an additional {etching_cost_percentage}% cost per frame.",
        f"{number_of_pins} of the seniors will also receive pins that are ${pin_cost}.",
        f"{officer_fraction_numerator}/{officer_fraction_denominator} of the seniors are officers and they will need to receive cords that are ${cord_cost} each."
    ]

    # Construct the question
    question = "How much will be spent on the senior gifts?"

    original_problem = problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    irrelevant_infos = [
        f"The senior awards ceremony will be held next week.",
        f"The event will cost ${random.randint(1000, 5000)} to organize."
        f"Each senior's wife receives a flower that costs ${frame_cost / 2 + 1}"
    ]

    # Out-topic irrelevant information
    irrelevant_infos.append(f"The school's mascot is the {random.choice(mascots)}.")
    irrelevant_infos.append(f"The principal has been with the school for {random.randint(5, 20)} years.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors to the problem (assumed functions)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle sentences except the first one
    problem_rest = problem[1:]
    if shuffle:
        random.shuffle(problem_rest)
    problem = [problem[0]] + problem_rest

    # Add the question
    problem.append(question)

    # Calculate the answer
    cost_per_frame = frame_cost * (1 + etching_cost_percentage / 100)
    total_frame_cost = total_seniors * cost_per_frame
    total_pin_cost = number_of_pins * pin_cost
    number_of_officers = total_seniors * officer_fraction_numerator / officer_fraction_denominator
    total_cord_cost = number_of_officers * cord_cost
    answer = total_frame_cost + total_pin_cost + total_cord_cost

    # Return the problem and answer
    cot = [
        f"Each picture frame costs {frame_cost} and needs to be etched with the logo for an additional {etching_cost_percentage}%, making the cost per frame {cost_per_frame}.",
        f"The total cost for all frames is {total_seniors} * {cost_per_frame}, which is {total_frame_cost}.",
        f"The total cost for pins is {number_of_pins} * {pin_cost}, which is {total_pin_cost}.",
        f"The number of officers is {total_seniors} * {officer_fraction_numerator} / {officer_fraction_denominator}, which is {number_of_officers}.",
        f"The total cost for cords is {number_of_officers} * {cord_cost}, which is {total_cord_cost}.",
        f"Therefore, the total amount spent on senior gifts is {total_frame_cost} + {total_pin_cost} + {total_cord_cost}, which is {answer}."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
