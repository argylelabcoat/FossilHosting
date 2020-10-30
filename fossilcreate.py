import os
import sys
import shlex
import subprocess
import requests
import random
import string
import getpass


def get_random_string(length):

    letters = string.ascii_lowercase

    result_str = ''.join(random.choice(letters) for i in range(length))

    return result_str

fossil = "bin/fossil"

defaultuser=getpass.getuser()
defaultpassword=get_random_string(16)

print("Using this password this run: ", defaultpassword)


def joinLoginGroup(targetRepo, groupRepo):
    cmd = f"{fossil} login-group join -R {targetRepo}  {groupRepo} -name default"
    cmdlist = shlex.split(cmd)
    subprocess.call(cmdlist, stdout=sys.stdout)


def initInternal():
    if not os.path.exists("internal"):
        os.mkdir("internal")

    if not os.path.exists("internal/user"):
        os.mkdir("internal/user")

    if not os.path.exists("internal/primary.fossil"):
        cmd = f"{fossil} new internal/primary.fossil"
        cmdlist = shlex.split(cmd)
        subprocess.call(cmdlist)

        cmd = f"{fossil} user password {defaultuser} {defaultpassword} -R internal/primary.fossil"
        cmdlist = shlex.split(cmd)
        subprocess.call(cmdlist, stdout=sys.stdout)


    if not os.path.exists("internal/template.fossil"):
        cmd = f"{fossil} new internal/template.fossil"
        cmdlist = shlex.split(cmd)
        subprocess.call(cmdlist)

        joinLoginGroup("internal/template.fossil", "internal/primary.fossil")


def authenticate(username, password, reponame):
    url = f"http://localhost:8080/{reponame}/json/login"
    print(url)
    authr = requests.get(url,
                         params={"name":username, "password":password})
    print(authr.status_code, authr.text)
    authj = authr.json()
    cookiename = authj["payload"]["loginCookieName"]
    cookie = authr.cookies.get(cookiename)
    authtoken = authj["payload"]["authToken"]
    print(authtoken, cookiename, cookie)
    return authtoken
    

def whoami(authtoken, reponame):
    url = f"http://localhost:8080/{reponame}/json/whoami"
    print(url)
    whoamireq = requests.get(url,
                         params={"authToken":authtoken})
    print(whoamireq.status_code, whoamireq.text)
    whoamij = whoamireq.json()
    print(whoamij, authtoken )
    pass


def verifyUser(username):
    pass


def getUserRepoFilename(username, reponame):
    return f"_{username}_{reponame}.fossil"


def addUserRepo(username, reponame):
    filename = getUserRepoFilename(username, reponame)
    repoPath = os.path.join("internal", filename)
    if not os.path.exists(repoPath):
        cmd = f"{fossil} new --template internal/template.fossil {repoPath}"
        cmdlist = shlex.split(cmd)
        subprocess.call(cmdlist)
        joinLoginGroup(f"{repoPath}", "internal/primary.fossil")



def removeUserRepo(username, reponame):
    filename = getUserRepoFilename(username, reponame)
    repoPath = os.path.join("internal", filename)
    if os.path.exists(repoPath):
        os.remove(repoPath)


ext=".fossil"
initInternal()
addUserRepo(defaultuser, "demo")
authtoken = authenticate(defaultuser, defaultpassword,"primary")
print()
whoami(authtoken, "primary")
print()
whoami(authtoken, "template")
print()
fname = getUserRepoFilename(defaultuser, "demo")
fname = fname[:len(fname)-len(ext)]
print(fname)
whoami(authtoken, fname)
