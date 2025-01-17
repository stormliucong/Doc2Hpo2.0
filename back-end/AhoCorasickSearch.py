from collections import deque 

class AhoCorasick:
    def __init__(self, hpo_dict):
        self.trie = {"children": {}, "fail": None, "output": []}
        terms = hpo_dict.keys()
        self.build_trie(terms)
        self.build_failure_links()

    def build_trie(self, terms):
        """Build the trie for the given terms."""
        for term in terms:
            node = self.trie
            for char in term:
                if char not in node["children"]:
                    node["children"][char] = {"children": {}, "fail": None, "output": []}
                node = node["children"][char]
            node["output"].append(term)

    def build_failure_links(self):
        """Build the failure links for the trie."""
        queue = deque()

        # Initialize root's children fail links to root
        for char, node in self.trie["children"].items():
            node["fail"] = self.trie
            queue.append(node)

        # BFS to set fail links
        while queue:
            current_node = queue.popleft()
            for char, next_node in current_node["children"].items():
                queue.append(next_node)
                fail_node = current_node["fail"]

                # Traverse fail links until we find a match or reach root
                while fail_node is not None and char not in fail_node["children"]:
                    fail_node = fail_node["fail"]

                # Set fail link to matched node or root
                next_node["fail"] = fail_node["children"][char] if fail_node else self.trie

                # Append outputs of fail node to the current node
                if next_node["fail"]:
                    next_node["output"].extend(next_node["fail"]["output"])

    def search(self, text):
        """Search for all terms in the given text."""
        try:
            node = self.trie
            intervals = []
            hpo_terms = []
            for i, char in enumerate(text):
                while node is not None and char not in node["children"]:
                    node = node["fail"]
                if node is None:
                    node = self.trie
                    continue
                node = node["children"][char]

                # Collect matches
                for term in node["output"]:
                    start = i - len(term) + 1
                    end = i + 1
                    intervals.append((start, end))
                    hpo_terms.append(term)
                    
            return intervals, hpo_terms   
        except Exception as e:
            raise ValueError("Failed to search for terms in the text using Acho-Corasick." + str(e))
        

# Example Usage:
if __name__ == "__main__":
    print("Aho-Corasick String Matching")
    from HpoFactory import HpoFactory
    from HpoLookup import HpoLookup
    hpo_F = HpoFactory()
    hpo_tree = hpo_F.build_hpo_tree()
    hpo_ancestors = hpo_F.get_hpo_ancestors(hpo_tree)
    hpo_levels = hpo_F.get_hpo_levels(hpo_tree)
    hpo_dict, hpo_name_dict, _ = hpo_F.build_hpo_dict(hpo_ancestors)
    hpo_dict = hpo_F.expand_hpo_dict(hpo_dict)
    with open('demo_patient_1.txt', 'r') as f:
        text = f.read()
    print(text)
    ac = AhoCorasick(hpo_dict) 
    intervals, hpo_terms = ac.search(text)
    print(f"Intervals: {intervals}, HPO Terms: {hpo_terms}")
    # matched_hpo = HpoLookup.add_hpo_attributes(text, intervals, hpo_dict, hpo_name_dict, hpo_levels)
    # print("Matched HPO:", matched_hpo)
