from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Step 1: Define lists of possible alternative values for variables
    names = ['Tom', 'Alice', 'Bob', 'Cindy', 'David', 'Emma', 'Frank', 'Grace']
    initial_trees_values = list(range(30, 70))  # Initial trees from 30 to 70
    trees_planted_per_year_values = list(range(5, 15))  # Trees planted per year from 5 to 15
    trees_chopped_per_year_values = list(range(1, 5))  # Trees chopped down per year from 1 to 5
    years_values = list(range(5, 15))  # Number of years from 5 to 15
    death_percentages = list(range(10, 50, 5))  # Death percentages from 10% to 45%

    # Randomly assign variables from lists
    name = random.choice(names)
    initial_trees = random.choice(initial_trees_values)
    trees_planted_per_year = random.choice(trees_planted_per_year_values)
    trees_chopped_per_year = random.choice(trees_chopped_per_year_values)
    years = random.choice(years_values)
    death_percentage = random.choice(death_percentages)

    # Step 2: Break problem into premises and question with variables replaced by {variable_name}
    problem_sentences = [
        f"{name} plants {trees_planted_per_year} trees each year.",
        f"Every year, {name} also chops down {trees_chopped_per_year} trees.",
        f"{name} starts with {initial_trees} trees.",
        f"After {years} years, {death_percentage}% of the trees die."
    ]

    question_sentence = "How many trees does {name} have left?"

    original_problem = problem_sentences.copy()
    original_problem.append(question_sentence)

    # Step 3: Construct in-topic and out-topic irrelevant information
    plantable_objects = [
        "tomatoes", "peppers", "carrots", "onions", "potatoes",
        "beans", "peas", "corn", "cucumbers", "lettuce",
        "spinach", "radishes", "squash", "zucchini", "broccoli",
        "cabbage", "eggplant", "beets", "strawberries", "blueberries",
        "raspberries", "melons", "watermelons", "basil", "parsley",
        "cilantro", "mint", "rosemary", "thyme", "sage",
        "oregano", "dill", "chives", "marigolds", "nasturtiums",
        "sunflowers", "daffodils", "tulips", "roses", "lavender",
        "geraniums", "lilacs", "hydrangeas", "grapes", "clematis",
        "honeysuckle", "sweet potatoes", "kale", "swiss chard",
        "arugula", "garlic", "leeks", "pumpkins", "okra"
    ]
    plant = random.choice(plantable_objects)
    in_topic_irrelevant_infos = [
        f"{name} plants {trees_planted_per_year} {plant} each year.",
        f"Every year, {name} also chops down {trees_chopped_per_year + random.randint(1, 6)} {plant}.",
        f"Each tree that {name} plants absorbs a lot of CO2."
    ]
    out_topic_irrelevant_infos = [
        f"{name} bought a new car last month.",
    ]

    irrelevant_infos = []
    for ir_info in in_topic_irrelevant_infos + out_topic_irrelevant_infos:
        if random.random() < prob_irre:
            irrelevant_infos.append(ir_info)

    # Combine problem sentences and irrelevant infos
    problem = problem_sentences + irrelevant_infos

    all_irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    # Step 4: Format the sentences with variable values
    # problem = [sentence.format(
    #     name=name,
    #     trees_planted_per_year=trees_planted_per_year,
    #     trees_chopped_per_year=trees_chopped_per_year,
    #     initial_trees=initial_trees,
    #     years=years,
    #     death_percentage=death_percentage
    # ) for sentence in problem]
    #
    # question = question_sentence.format(name=name)

    # Step 5: Introduce symbol or grammar errors
    problem = [introduce_symbol_error(introduce_grammar_error(p, prob_grammar_error), prob_symbol_error) for p in
               problem]

    # Shuffle the problem sentences
    if shuffle:
        random.shuffle(problem)

    # Append the question
    problem.append(question_sentence)

    # Step 6: Calculate the answer using the math formula
    net_trees_per_year = trees_planted_per_year - trees_chopped_per_year
    total_trees_after_years = initial_trees + net_trees_per_year * years
    surviving_trees = total_trees_after_years * (100 - death_percentage) / 100
    answer = surviving_trees

    # Return the problem and the answer
    cot = [f"{name} plants {trees_planted_per_year} trees and chops down {trees_chopped_per_year} trees each year, resulting in a net increase of {net_trees_per_year} trees per year.", f"After {years} years, the total number of trees is {initial_trees} + {net_trees_per_year} * {years}, which equals {total_trees_after_years}.", f"After accounting for the {death_percentage}% of trees that die, the number of surviving trees is {total_trees_after_years} * (100 - {death_percentage}) / 100, which equals {surviving_trees}.", f"Therefore, the final answer is {surviving_trees}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': all_irrelevant_infos}
