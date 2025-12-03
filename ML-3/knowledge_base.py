from py2neo import Graph, Node, Relationship

class KnowledgeBase:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="1234"):
        self.graph = Graph(uri, auth=(user, password))

    def clear(self):
        self.graph.delete_all()

    def init_ontology(self):
        passenger_flow = Node("Concept", name="Пассажиропоток")
        time_of_day = Node("Concept", name="Время суток")
        elevator = Node("Concept", name="Управление лифтом")

        self.graph.create(passenger_flow | time_of_day | elevator)

        terms = {
            "Пассажиропоток": ["Низкий", "Средний", "Высокий"],
            "Время суток": ["Ночь", "Утро", "День", "Вечер"],
            "Управление лифтом": ["Мало активных", "Норма активных", "Много активных"]
        }

        for concept, term_list in terms.items():
            concept_node = self.graph.nodes.match("Concept", name=concept).first()
            for term_name in term_list:
                term = Node("Term", name=term_name)
                rel = Relationship(term, "BELONGS_TO", concept_node)
                self.graph.create(term | rel)

        rules = [
            ("Высокий", "Утро", "Много активных"),
            ("Средний", "День", "Норма активных"),
            ("Низкий", "Ночь", "Мало активных"),
            ("Высокий", "Вечер", "Много активных"),
            ("Низкий", "День", "Норма активных")
        ]

        for flow, time, action in rules:
            self.add_rule(flow, time, action)

    def add_rule(self, flow, time, action):
        rule = Node("Rule", flow=flow, time=time, action=action)
        self.graph.create(rule)

    def get_rules(self):
        rules_data = self.graph.nodes.match("Rule")
        return [
            {"flow": r["flow"], "time": r["time"], "action": r["action"]}
            for r in rules_data
        ]
