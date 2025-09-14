import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):

    # Define names, professions, and topics
    names = ["Meredith", "Sophia", "Liam", "Olivia", "Ethan", "Ava", "Noah", "Emma", "Isabella", "Mason"]
    professions = ["freelance blogger", "content writer", "journalist", "editor", "novelist", "copywriter", "technical writer"]
    topics = ["health topics", "technology trends", "travel experiences", "financial advice", "culinary recipes", "fashion insights", "environmental issues"]

    # Randomly select a name, profession, and topic
    name = random.choice(names)
    profession = random.choice(professions)
    topic = random.choice(topics)

    # Randomly generate variables with ranges that ensure consistency
    article_time = random.randint(2, 6)
    articles_monday = random.randint(3, 8)
    fractions = [(1,articles_monday), (2,articles_monday)]
    numerator, denominator = random.choice(fractions)
    times_more_tuesday = numerator / denominator
    multiplier_wednesday = random.choice([2, 3, 4])

    # Compute articles written on each day
    articles_tuesday = int(articles_monday * (1 + times_more_tuesday))
    articles_wednesday = int(articles_tuesday * multiplier_wednesday)
    total_articles = articles_monday + articles_tuesday + articles_wednesday
    total_hours = total_articles * article_time

    # Prepare variables for insertion
    # variable_values = {
    #     'name': name,
    #     'profession': profession,
    #     'topic': topic,
    #     'article_time': article_time,
    #     'articles_monday': articles_monday,
    #     'numerator': numerator,
    #     'denominator': denominator,
    #     'multiplier_wednesday': multiplier_wednesday
    # }

    # Construct the problem sentences
    problem = []
    problem.append(f"{name} is a {profession} who writes about {topic}.")
    problem.append(f"A blog article takes an average of {article_time} hours to research and write about.")
    problem.append(f"Last week, {name} wrote {articles_monday} articles on Monday and {numerator}/{denominator} times more articles on Tuesday than on Monday.")
    problem.append(f"On Wednesday, {name} wrote {multiplier_wednesday} times the number of articles {name} wrote on Tuesday.")

    import copy
    original_problem = copy.deepcopy(problem)

    # In-topic irrelevant information
    irrelevant_infos_in_topic = [
        f"{name} also spends time promoting articles on social media.",
        f"{name} attends workshops on {topic} occasionally.",
        f"{name} earns income based on the number of articles written."
    ]

    # Out-topic irrelevant information
    irrelevant_infos_out_topic = [
        f"{name} enjoys hiking during weekends.",
        f"{name} recently adopted a pet named Buddy.",
        f"{name} is planning a vacation to Japan next month."
    ]

    # Add irrelevant information based on probability
    problem_with_irrelevant = problem.copy()
    for info in irrelevant_infos_in_topic:
        if random.random() < prob_irre:
            problem_with_irrelevant.append(info)
    for info in irrelevant_infos_out_topic:
        if random.random() < prob_irre:
            problem_with_irrelevant.append(info)

    # Add symbol or grammar errors
    problem_with_errors = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in problem_with_irrelevant
    ]

    # Shuffle the order of sentences, except the first one
    first_sentence = problem_with_errors[0]
    other_sentences = problem_with_errors[1:]
    if shuffle:
        random.shuffle(other_sentences)
    final_problem = [first_sentence] + other_sentences

    # Add the question at the end
    question = f"Calculate the total number of hours {name} spent writing articles in the three days."
    final_problem.append(question)

    original_problem.append(question)

    # Compute the answer
    answer = total_hours

    # Return problem and answer
    cot = [f"{name} wrote {articles_monday} articles on Monday.", f"On Tuesday, {name} wrote {numerator}/{denominator} times more articles than on Monday, which is {articles_tuesday}.", f"On Wednesday, {name} wrote {multiplier_wednesday} times the number of articles written on Tuesday, which is {articles_wednesday}.", f"The total number of articles written over the three days is {articles_monday} + {articles_tuesday} + {articles_wednesday}, which is {total_articles}.", f"Each article takes {article_time} hours to write, so the total hours spent is {total_articles} * {article_time}, which is {total_hours}.", f"Therefore, the total number of hours spent writing articles is {answer}."]
    
    return {"cot": cot, 'problem': final_problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos_in_topic + irrelevant_infos_out_topic}