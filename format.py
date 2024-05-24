import json
import os

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in '{file_path}': {e}")

def write_json_file(file_path, data):
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2)
            print(f"Data written to '{file_path}'.")
        except json.JSONDecodeError as e:
            print(f"Error encoding JSON for '{file_path}': {e}")

def main():
    file_count = 99998
    output_files_size = 10000
    drugs_filter = ["MDMA", "Mushrooms", "Cannabis", "LSD", "Salvia divinorum"]
    dataset = []
    files = [f for f in os.listdir("./Experiences") if f.endswith('.json')]
    for file in files:
        file_path = os.path.join("./Experiences/", file)
        data = read_json_file(file_path)
        if data == None: continue
        #write_json_file('./training_data/%i.json' %i, data)
        #exp = "The following is a drug experience of {author} who took {drug}, ".format(author = data["author"], drug = data["drug"])
        exp = "The following is a drug experience of someone who took "
        dose_filtered = {}
        if(data["drug"] not in drugs_filter): continue
        for dose in data.get("dosechart", []):
            try:
                dose['amount'] = float(dose['amount'])
            except (ValueError, TypeError):
                print("couldn't cast %s to float.", dose["amount"])
            substance = dose["substance"]
            if(substance not in dose_filtered):
                dose_filtered[substance] = [dose]
            else:
                for d in range(len(dose_filtered[substance])):
                    if(dose_filtered[substance][d]["units"] == dose["units"]):
                        if(type(dose_filtered[substance][d]["amount"]) == type(dose["amount"])):
                            dose_filtered[substance][d]["amount"] += dose["amount"]
                        else:
                            print("Type mismatch while merging doses.")
                    else:
                        dose_filtered[substance].append(dose)
        dose_filtered = list(dose_filtered.values())
        for i in range(len(dose_filtered)):
            for j in range(len(dose_filtered[i])):
                exp += "{amount} {units} of {substance} {method} in {form} form".format( amount = dose_filtered[i][j].get("amount", "?"), units = dose_filtered[i][j].get("units", "?"), method = dose_filtered[i][j].get("method", "?"), substance = dose_filtered[i][j].get("substance", "?"), form = dose_filtered[i][j].get("form", "?")[1:-2])  #last slice is to get rid of ()    
                if(i+1 == len(dose_filtered) and j+1 == len(dose_filtered[i])): 
                    exp += ":\n "
                else: 
                    if((i+1 == len(dose_filtered) and j+2 == len(dose_filtered[i])) or (i+2 == len(dose_filtered) and j+1 == len(dose_filtered[i]))): 
                        exp += " and "
                    else:
                        exp += ", "
        dataset.append({"text":(exp + ("".join(data["text"]).replace("End Body", "")))})
    write_json_file("training_data/output_top5.json", dataset)
if __name__ == '__main__':
	main()