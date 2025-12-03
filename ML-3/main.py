# main.py
from knowledge_base import KnowledgeBase
from fuzzy_controller import FuzzyController
from simulator import ElevatorSimulator

def main():
    kb = KnowledgeBase(password="12345678")
    kb.clear()
    kb.init_ontology()

    controller = FuzzyController(kb)

    sim = ElevatorSimulator(controller)
    sim.run()

if __name__ == "__main__":
    main()
