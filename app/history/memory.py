from typing import Dict, List

class ConversationMemory:
    def __init__(self)-> None:
        self.history: List[Dict[str,str]]= []

    def add(self, role: str, content: str)-> None:
        self.history.append(
            {
                "role":role,
                "content": content
            }
        )

    def reset(self):
        self.history=[]

    def get_context(self)-> str:
        return "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in self.history
        ])

    def to_list(self)-> List[Dict[str,str]]:
        return list(self.history)
    
    def load_from_list(self, items: List[Dict[str,str]]) -> None:
        self.history= list(items)