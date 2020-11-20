import os

def remove_first(dir):
    files_in_directory = os.listdir(dir)
    filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
    for file in filtered_files:
        path_to_file = os.path.join(dir, file)

        file1 = open(path_to_file, 'r') 

        Lines = file1.read().splitlines()
        file1.close()
        file1 = open(path_to_file, 'w') 
        count = 0
        val = 0
        for line in Lines: 
            if count != 0:
                file1.write(line)
                file1.write("\n")

            if count == 20:    
                val = line
            count = count +1

        file1.write(val)
        file1.close()

if __name__ == '__main__':
    #remove_first('baseline/')            
    remove_first('tree/')            
