from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[32]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define name list
        names = ["Carlos", "Jim", "Carrey", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", "Kevin", "Laura", "Mike", "Nina", "Oscar", "Paula", "Quentin", "Rachel", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xavier", "Yvonne", "Zach"]
        
        # Randomly select 3 unique names
        selected_names = random.sample(names, 3)
        name1, name2, name3 = selected_names
        
        # Define item list
        items = ["seashells", "pebbles", "starfish", "sand dollars", "driftwood", "shells"]
        item_name = random.choice(items)
        
        # Randomly generate numeric variables
        while True:
            n_Jim_collected = random.randint(20, 50)  # Jim's collected amount
            n_Jim_Carlos_diff = random.randint(3, 10)  # Difference between Jim and Carlos
            n_Carlos_collected = n_Jim_collected - n_Jim_Carlos_diff  # Carlos's collected amount
            if n_Carlos_collected % 2 == 0 and n_Carlos_collected > 0:
                break  # Ensure Carlos's amount is positive and even
        n_Carrey_collected = n_Carlos_collected // 2  # Carrey's collected amount
        
        # Construct the premise content
        problem = [
            f"{name1}, {name2}, and {name3} were at the beach playing and they decided to gather some {item_name}.",
            f"{name2} collected {n_Jim_collected} {item_name}, which was {n_Jim_Carlos_diff} more than what {name1} collected.",
            f"{name1} collected twice as many as {name3}."
        ]
        original_problem=problem.copy()
        
        # Construct in-topic irrelevant information
        in_topic_irrelevant_infos = [
            f"They saw a dolphin jumping out of the water while collecting {item_name}.",
            f"The {item_name} were in various colors and sizes.",
            f"It was a sunny day with a gentle breeze at the beach."
        ]
        
        # Construct out-topic irrelevant information
        out_topic_irrelevant_infos = [
            f"{name1} is planning a trip to the mountains next week.",
            f"{name2} recently adopted a puppy.",
            f"{name3} won a prize in the school science fair."
        ]
        
        irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
        
        # Add irrelevant information based on probability
        for info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(info)
        
        # Add symbol or grammar errors
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error),
                prob_symbol_error
            )
            for p in problem
        ]
        
        # Compose the question
        question = f"They gathered all their {item_name} and divided them equally between themselves. How many did each person get?"
        original_problem.append(question)
        # Add the question
        
        
        # Shuffle the sentences (except the first one)
        first_sentence = problem[0]
        other_sentences = problem[1:]
        if shuffle:
            random.shuffle(other_sentences)
        problem = [first_sentence] + other_sentences
        
        problem.append(question)
        
        # Math formulas
        # n_Carlos_collected = n_Jim_collected - n_Jim_Carlos_diff
        # n_Carrey_collected = n_Carlos_collected // 2
        # total_collected = n_Jim_collected + n_Carlos_collected + n_Carrey_collected
        # answer = total_collected // 3
        
        total_collected = n_Jim_collected + n_Carlos_collected + n_Carrey_collected
        answer = total_collected // 3  # Final answer
        if answer%1==0:
            break
        
    # Return the problem and answer
    cot = [f"{name2} collected {n_Jim_collected} seashells, which was {n_Jim_Carlos_diff} more than what {name1} collected. Therefore, {name1} collected {n_Carlos_collected} seashells.", f"{name1} collected twice as many as {name3}, so {name3} collected {n_Carrey_collected} seashells.", f"The total number of seashells collected by {name1}, {name2}, and {name3} is {n_Jim_collected} + {n_Carlos_collected} + {n_Carrey_collected}, which is {total_collected}.", f"They divided the total seashells equally among themselves, so each person got {total_collected} // 3, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

