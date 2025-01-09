import json
import glob
import pandas as pd

# Load the generated clinical notes
file_list = glob.glob("./simulated_pt_description/*.json")
row = []
for file in file_list:
    with open(file, "r") as f:
        uuid = file.split("/")[-1].split(".")[0]
        json_data = json.load(f)
        hpo_terms_str = ";".join(json_data["hpo_terms"])
        hpo_id_str = ";".join(json_data["hpo_ids"])
        text = json_data["response"]
        row.append([uuid, hpo_terms_str, hpo_id_str, text])
df = pd.DataFrame(row, columns=["uuid", "hpo_terms", "hpo_ids", "text"])
df.to_csv("mygpt_worksheet.csv", index=False)