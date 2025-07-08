import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

'''
networkx
    •   Create undirected or directed graphs
	•	Add nodes and edges dynamically
	•	Assign and retrieve attributes like weights (e.g. compatibility scores)
	•	Perform graph algorithms: shortest path, clustering, centrality, etc.
	•	Easy integration with matplotlib for visualizing graphs
'''

'''
    - weight (% of total)
    - type (complementary = opposite, similar = same)

    - store users in json? 
        dictionary user name to dict of answers

'''
# 1. Survey schema
# 2. User responses (1–5 scale)

# 3. Matching function

def compare_multi_select(set1, set2):
    if not set1 and not set2:
        return 100.0  # both skipped, consider them a match
    if not set1 or not set2:
        return 0.0  # one skipped, no match
    overlap = len(set1 & set2)
    total = len(set1 | set2)
    return round((overlap / total) * 100, 2)

def directional_match(userA, userB, field):
    a_self = set(userA.get(f"{field}_self", []))
    a_expect = set(userA.get(f"{field}_expected", []))
    b_self = set(userB.get(f"{field}_self", []))
    b_expect = set(userB.get(f"{field}_expected", []))

    if not a_self or not b_self or not a_expect or not b_expect:
        return 0.0  # fallback for incomplete data

    # A's self satisfies B's expectations
    a_to_b = len(a_self & b_expect) / max(len(b_expect), 1)
    # B's self satisfies A's expectations
    b_to_a = len(b_self & a_expect) / max(len(a_expect), 1)

    return round(((a_to_b + b_to_a) / 2) * 100, 2)

def calculate_match_score(u1, u2, schema):
    actual = 0
    total = 0

    for q_id, meta in schema.items():
        q_type = meta['type']
        weight = meta['weight']

        # Handle multi-select questions
        if q_type == 'multi-select':
            score = compare_multi_select(set(u1[q_id]), set(u2[q_id]))
            max_score = 100
        # Handle similar-type questions
        elif q_type == 'similar':
            score = 5 - abs(u1[q_id] - u2[q_id])
            max_score = 5
        # Handle complementary-type questions
        elif q_type == 'complementary':
            score = abs(u1[q_id] - u2[q_id])
            max_score = 5
        # Handle mode-type questions
        elif q_type == 'mode':
            score = directional_match(u1, u2, q_id)
            max_score = 100
        else:
            continue  # unsupported type

        actual += score * weight
        total += max_score * weight

    return round((actual / total) * 100, 2) if total else 0.0

'''
-survey answers on 1-5 scale
-actual v total points possible (100)
-normalized
'''

# 4. Build graph
G = nx.Graph()

# Add nodes (usernames)
for user in users:
    G.add_node(user)

# Add edges if score >= 50%
for u1, u2 in combinations(users.keys(), 2):
    score = calculate_match_score(users[u1], users[u2], survey_schema)
    if score >= 50:
        G.add_edge(u1, u2, weight=score)

# 5. Print matches
print("Matches over 50% compatibility:")
for u, v, data in G.edges(data=True):
    print(f"{u} ↔ {v}: {data['weight']}%")

# 6. Visualize (optional)
'''
pos = nx.spring_layout(G, seed=42)
edge_labels = nx.get_edge_attributes(G, 'weight')

nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("User Compatibility Graph (≥ 50%)")
plt.show()
'''
