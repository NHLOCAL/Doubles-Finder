# -*- coding: utf-8 -*-
import os
import sys

def duplic_scan(myfile):
# פונקציה זו עוברת על הקוד הבינארי של הקובץ ושומרת מדגם שלו למשתנה
    break_num = 0
    id_file = "id:"
    with open(myfile, 'rb') as input_file:
        for line in input_file:
            break_num += 1
            if ((break_num > 145) and (break_num < 1985)) or ((break_num > 2778) and (break_num < 4900)):
                continue
            line_to_str = str(line)
            id_file += line_to_str[7:83:19]
            if 5530 == break_num:
                break
            
    return id_file


def duplic_files(dir_path):
# פונקציה זו עוברת על קבוצת קבצים שבתיקיה ומפעילה עליהם את הפונקציה duplic_scan
    len_item = 0
    len_dirs = sum(len(files) for _, _, files in os.walk(dir_path))
    files_list = []
    files_dict = {}
    dict_to_del = {}
    
    # מעבר על רשימת הקבצים והוספת דגימה של הקידוד שלהם למשתנה
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # תצוגת אחוזים מתחלפת
            len_item += 1
            show_len = len_item * 100 // len_dirs
            print(str(show_len) + "% " + "הושלמו",end='\r')
            # בדיקה אם שם הקובץ הפנימי מכיל סיומות ספציפיות
            if not file.endswith((".mp3",".wma", ".wav")):
                continue
            my_file = duplic_scan(os.path.join(root,file))
            files_dict[file] = my_file
            files_list.append(my_file)
        
    dict_list = files_dict.items()
    file_num = 0
    
    for item in dict_list:
        if files_list.count(item[1]) == 2:
            file_num += 1
            dict_to_del[file_num] = item[0]
            print(str(file_num) + ": " + item[0])
            
    if file_num >= 1:
        select_file = input("\nהכנס מספר רצוי בכדי למחוק קובץ\nניתן להכניס כמה ספרות בהפרדה של רווח ביניהם" + "\n>>>")
        select_file = select_file.split()
        try:
            for del_item in select_file:
                os.remove(dir_path + "\\" + dict_to_del[int(del_item)])
                print(dict_to_del[int(del_item)] + "  -- נמחק!")
        except:
            print("עליך להכניס מספר בכדי למחוק קובץ מסוים!")
    else:
        print("לא נמצא דבר!")
            
def main():
    dir_path = str(sys.argv[1])
    if (dir_path != "") and (os.path.exists(dir_path)):
        print("\n>>" + sys.argv[1])
        duplic_files(dir_path)

if __name__ == '__main__':
    main()