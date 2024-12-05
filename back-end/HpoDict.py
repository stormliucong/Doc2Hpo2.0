from collections import deque, defaultdict 


class HpoDict:
    def __init__(self, hpo_file):
        self.hpo_file = hpo_file
    
    def build_hpo_dict(self):
        hpo_dict = defaultdict(str)
        with open(self.hpo_file, "r") as f:
            for line in f:
                hpo_name, hpo_code = line.strip().split("|")
                hpo_dict[hpo_name] = hpo_code
        hpo_dict = defaultdict(lambda: 'Not Found', hpo_dict)
        return hpo_dict