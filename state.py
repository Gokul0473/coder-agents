from dataclasses import dataclass

@dataclass
class State:
    task: str = ""
    plan: list = None
    current_code: str = ""
    test_results: dict = None
    status: str = "pending"
