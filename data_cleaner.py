from fetcher import DataEntry
import glob
import shutil
import os.path

def check_entry(e: DataEntry):
    return e.end_year - e.start_year == len(e.data)

if __name__ == "__main__":
    
    to_delete = []
    counter = 0
    for fname in glob.glob('data2/*/*'):
        counter += 1
        with open(fname) as file:
            entry = DataEntry.from_json(file)
            if not check_entry(entry):
                to_delete.append(fname)  
    

    print(f"Purging {len(to_delete)} out of {counter}")
    for f in to_delete:
        os.remove(f)