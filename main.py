import json
from difflib import get_close_matches

#load knowledge base

def load_knowledge(filepath:str ) -> dict:
    with open(filepath,'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge(filepath:str, data:dict):
    with open(filepath,'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question:str, questions:list[str]) -> str|None:
    matches: list = get_close_matches(user_question, questions, n=2,cutoff=0.6)
    return matches[0] if matches else None

def get_answer (question:str, knowledge:dict)-> str | None:
    for q in knowledge["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None
        
def chatbot():
    knowledge_base: dict = load_knowledge('knowledge.json') 
    while True:
        user_input:str = input('You: ')
        if user_input.lower() == 'quit':
            break

        best_match:str | None = find_best_match(user_input,[q["question"]for q in knowledge_base["questions"]])

        if best_match:
            answer:str = get_answer(best_match,knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer, Can you teach me ?')
            new_answer:str = input('Type answer or "skip" to skip: ')
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer":new_answer})
                save_knowledge('knowledge.json',knowledge_base)
                print('Thank you I learned something new!')

if __name__ == '__main__':
    chatbot()

