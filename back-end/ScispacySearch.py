import spacy
from scispacy.linking import EntityLinker
from scispacy.abbreviation import AbbreviationDetector
from scispacy.hyponym_detector import HyponymDetector




class ScispacySearch:
    def __init__(self):
        self.nlp = spacy.load("en_core_sci_sm")
        self.nlp.add_pipe("abbreviation_detector")
        self.nlp.add_pipe("hyponym_detector", last=True, config={"extended": False})
        self.nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "hpo"})
       

    def search(self, query):
        intervals = []
        linked_hpo_names = []
        doc = self.nlp(query)
        linker = self.nlp.get_pipe("scispacy_linker")
        linker.threshold = 0.8
        for entity in doc.ents:
            all_ents = entity._.kb_ents
            if len(entity._.kb_ents) > 0:
                umls_ent = entity._.kb_ents[0]
                intervals.append((entity.start_char, entity.end_char))
                linked_hpo_names.append(linker.kb.cui_to_entity[umls_ent[0]].canonical_name)
        
        return intervals, linked_hpo_names
                
            
             

# Example usage
if __name__ == "__main__":
    print("Scispacy Search")
    from HpoFactory import HpoFactory
    from HpoLookup import HpoLookup
    hpo_F = HpoFactory()
    hpo_tree = hpo_F.build_hpo_tree()
    hpo_ancestors = hpo_F.get_hpo_ancestors(hpo_tree)
    hpo_levels = hpo_F.get_hpo_levels(hpo_tree)
    hpo_dict, hpo_name_dict = hpo_F.build_hpo_dict(hpo_ancestors)
    hpo_dict = hpo_F.expand_hpo_dict(hpo_dict)
    with open('demo_patient_1.txt', 'r') as f:
        text = f.read()
    print(text)
    scispacy = ScispacySearch()
    intervals, linked_hpo_names = scispacy.search(text)
    print("Intervals:", intervals)
    print("Linked HPO Names:", linked_hpo_names)
    matched_hpo = HpoLookup.add_hpo_attributes(text, intervals, hpo_dict, hpo_name_dict, hpo_levels, linked_hpo_names)
    print("Matched HPO:", matched_hpo)