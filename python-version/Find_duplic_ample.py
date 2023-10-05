import os
import sys

# Constants
SUPPORTED_EXTENSIONS = (".mp3", ".wma", ".wav")

def read_binary_slice(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        return binary_data

def main():
    dir_path = str(sys.argv[1])
    if (dir_path != "") and (os.path.exists(dir_path)):
        print("\n>>" + sys.argv[1])

    len_dirs = sum(len(files) for _, _, files in os.walk(dir_path))
    files_list = []
    
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            len_item = len(files_list) + 1
            show_len = len_item * 100 // len_dirs
            print(f"{show_len}% הושלמו", end='\r')
            
            if not file.endswith(SUPPORTED_EXTENSIONS):
                continue
            
            id_file = read_binary_slice(os.path.join(root, file))
            files_list.append((os.path.join(root, file), id_file))
    
    id_list = [id_item for _, id_item in files_list]
    dict_to_del = {}
    
    for file_item, id_item in files_list:
        if id_list.count(id_item) >= 2:
            file_num = len(dict_to_del) + 1
            dict_to_del[file_num] = file_item
            print_file_item = file_item.replace(dir_path + "\\", "")
            print(f"{file_num}: {print_file_item}")
    
    if dict_to_del:
        select_file = input("\nהכנס מספר רצוי בכדי למחוק קובץ\nניתן להכניס כמה ספרות בהפרדה של רווח ביניהם" + "\n>>>")
        select_file = select_file.split()
        try:
            for del_item in select_file:
                os.remove(dict_to_del[int(del_item)])
                print(f"{dict_to_del[int(del_item)]}  -- נמחק!")
        except Exception as e:
            print("עליך להכניס מספר בכדי למחוק קובץ מסויים!")
    else:
        print("לא נמצא דבר!")

if __name__ == '__main__':
    main()
