# Part 3: Semantic Network
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

g = nx.DiGraph()

# (from, to, relation)
relations = [
    ("Student", "Person", "is_a"),
    ("Professor", "Person", "is_a"),
    ("Person", "Name", "has"),
    ("Student", "Roll_No", "has"),
    ("Professor", "Employee_ID", "has"),
    ("Asha", "Student", "instance_of"),
    ("Ravi", "Student", "instance_of"),
    ("Dr_Rao", "Professor", "instance_of"),
    ("Dr_Rao", "AI_Course", "teaches"),
    ("Asha", "AI_Course", "enrolled_in"),
    ("Ravi", "AI_Course", "enrolled_in"),
    ("AI_Course", "CSE_Dept", "offered_by"),
    ("Dr_Rao", "CSE_Dept", "works_in"),
]

for a, b, rel in relations:
    g.add_edge(a, b, relation=rel)

print("Nodes:", g.number_of_nodes())
print("Edges:", g.number_of_edges())
print()
for a, b, data in g.edges(data=True):
    print(a, "--", data["relation"], "-->", b)


def get_properties(node):
    # go up the is_a / instance_of links and collect every "has" property
    props = []
    to_visit = [node]
    while len(to_visit) > 0:
        current = to_visit.pop()
        for _, nxt, data in g.out_edges(current, data=True):
            if data["relation"] == "has":
                props.append(nxt + " (from " + current + ")")
            elif data["relation"] in ("is_a", "instance_of"):
                to_visit.append(nxt)
    return props


print("\nProperties of Asha (inheritance):")
for p in get_properties("Asha"):
    print(" ", p)

# fixed positions so the graph is readable
pos = {
    "Person": (4, 5), "Name": (6.5, 5),
    "Student": (1.5, 3.5), "Professor": (6.5, 3.5),
    "Roll_No": (0, 5), "Employee_ID": (8, 5),
    "Asha": (0, 2), "Ravi": (2.5, 2), "Dr_Rao": (6.5, 2),
    "AI_Course": (4, 0.5), "CSE_Dept": (6.5, 0.5),
}

os.makedirs("outputs", exist_ok=True)
plt.figure(figsize=(13, 8))
nx.draw(g, pos, with_labels=True, node_color="lightblue", node_size=3600,
        font_size=9, edgecolors="black")
nx.draw_networkx_edge_labels(g, pos, edge_labels=nx.get_edge_attributes(g, "relation"),
                             font_size=8, font_color="darkred", label_pos=0.4)
plt.title("University Semantic Network")
plt.savefig("outputs/semantic_network.png", dpi=120, bbox_inches="tight")
print("\nSaved outputs/semantic_network.png")