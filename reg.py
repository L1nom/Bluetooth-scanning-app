import winreg
import os

file_path = "\"" + os.path.abspath(os.path.abspath("gui.exe")) + "\"" + " \"%1\","

path = winreg.HKEY_CLASSES_ROOT
try:
    with winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT) as hkey:
        winreg.CreateKey(hkey, "zLocatify")
    with winreg.OpenKey(path, r"zLocatify\\", 0, winreg.KEY_ALL_ACCESS) as locatify:
        winreg.SetValueEx(locatify, "URL Protocol", 0, winreg.REG_SZ, "url protocol")
        winreg.CreateKey(locatify, "shell")
        with winreg.OpenKeyEx(path, r"zLocatify\\shell", 0, winreg.KEY_ALL_ACCESS) as shell:
            winreg.CreateKey(shell, "open")
            with winreg.OpenKeyEx(path, r"zLocatify\\shell\\open", 0, winreg.KEY_ALL_ACCESS) as open:
                winreg.CreateKey(open, "command")
                with winreg.OpenKeyEx(path, r"zLocatify\\shell\\open\\command", 0, winreg.KEY_ALL_ACCESS) as command:
                    # winreg.SetValueEx(command, None, 0, winreg.REG_SZ, "\"C:\Windows\System32\calc.exe\" \"%1\",")
                    winreg.SetValueEx(command, None, 0, winreg.REG_SZ, file_path)

except PermissionError:
    pass
