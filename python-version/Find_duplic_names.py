import os, sys

# יבוא פונקציה לזיהוי דמיון בין מחרוזות
from identify_similarities import similarity_sure


# הפונקצייה מסירה מספרים ממחרוזות ומאפשרת זיהוי קבצים כפולים לפי שם הקובץ
def ignoring_numbers(string):
    string = string.lstrip()
    for i, char in enumerate(string):
        if not char.isdigit() and not char.isspace():
            return string[i:]
    return ""
    
    
def main():
# פונקציה זו עוברת על קבוצת קבצים שבתיקיה ומפעילה עליהם את הפונקציה duplic_scan
    dir_path = str(sys.argv[1])
    if (dir_path != "") and (os.path.exists(dir_path)):
        print("\n>>" + sys.argv[1])

    len_item = 0
    len_dirs = sum(len(files) for _, _, files in os.walk(dir_path))
    files_list = []
    names_list = []
    dict_to_del = {}
    file_num = 0
    
    # מעבר על רשימת הקבצים והוספת השם שלהם ללא תוספות למשתנה
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # תצוגת אחוזים מתחלפת
            len_item += 1
            show_len = len_item * 100 // len_dirs
            print(str(show_len) + "% " + "הושלמו",end='\r')
            # בדיקה אם שם הקובץ הפנימי מכיל סיומות ספציפיות
            if not file.endswith((".mp3",".wma", ".wav")):
                continue
            # הפעלת פונקציה למיון קבצים דומים
            clear_name = ignoring_numbers(file.rsplit('.', 1)[0])
            
            # הוספת התוצאות לרשימה
            files_list.append((os.path.join(root, file), clear_name))
    
    # יצירת רשימת השמות הבסיסיים של הקבצים
    for file_item, name_item in files_list: names_list.append(name_item)
    
    # בדיקה אם שם מסויים קיים יותר מפעם אחת
    for file_item, name_item in files_list:
        if names_list.count(name_item) >= 2:
            file_num += 1
            dict_to_del.update({file_num: file_item})
            print_file_item = file_item.replace(dir_path + "\\", "")
            print(str(file_num) + ": " + print_file_item)
            
    if file_num >= 1:
        select_file = input("\nהכנס מספר רצוי בכדי למחוק קובץ\nניתן להכניס כמה ספרות בהפרדה של רווח ביניהם" + "\n>>>")
        select_file = select_file.split()
        try:
            for del_item in select_file:
                os.remove(dict_to_del[int(del_item)])
                print(dict_to_del[int(del_item)] + "  -- נמחק!")
        except Exception as e:
            print("עליך להכניס מספר בכדי למחוק קובץ מסוים!")
    else:
        print("לא נמצא דבר!")

if __name__ == '__main__':
    main()