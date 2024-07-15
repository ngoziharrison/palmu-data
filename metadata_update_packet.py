import pandas as pd
import os

df = pd.read_csv("merritt-updates/palmu_metadata_delivery1-merrit-update.csv")

path = "/Users/ngoziharrison/Documents/palmu-data/merritt-updates/ingest-process"

txt_template = """erc: 
what:{title} | {alt_title} ; {collection}
who: no data
where: {ark}
where: {link}"""

for index, row in df.iterrows():
    folder = row["where"]
    print(folder)
    os.makedirs(os.path.join(path, folder), exist_ok = True)

    with open(path + "/" + folder + "/mrt-erc.txt", "w") as file:
        file.write(txt_template.format(title = row[5], alt_title = row[6], ark = row[1], collection = row[2], link = row[4]))

