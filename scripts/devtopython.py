#!/usr/bin/python3
'''
NOTLAR
- gsettings komutu ile set etme
# print('dbus-launch gsettings set apps.gsettings-ornekuygulama  normalcertler \"' + str(normalcertler) + '\"')
'''
import gi
from gi.repository import Gio
import os.path
import subprocess
import datetime
from datetime import date
import sys
import re

G_ID = "apps.gsettings-ornekuygulama"
F_PATH = "/usr/share/glib-2.0/schemas/" + G_ID + ".gschema.xml"
mico = Gio.Settings.new(G_ID)

# Check if mico gsettings is exist / it should be compiled as "glib-compile-schemas /usr/share/glib-2.0/schemas/"
if not os.path.isfile(F_PATH): 
    print("GSettings Miço XML is not found!")
    exit

#Bash command execution
def execute_it(cmd):
    output = subprocess.check_output(["bash","-c", cmd])
    return output.decode("utf-8")

#Return certificate fingerprint
def get_fingerp(path):
    cmd = "openssl x509 -noout -fingerprint -sha1 -inform pem -in " + path
    return execute_it(cmd)[17:-1]

# get_certinfo function's returned date format doesnt satisfy needs. It formats them.
def format_date(str):
    if int(str[4:6])<10:
        day = "0" + str[5:6]
    else:
        day = str[4:6]
    raw_date = str[:3] + " " + day + " " + str[7:]
    raw_date = datetime.datetime.strptime(raw_date, "%b %d %Y")
    return raw_date.strftime('%Y-%m-%d')[0:10]

def get_today():
    return date.today().strftime('%Y-%m-%d')[0:10]

#Check if cerfication is valid according to dates from get_certinfo function.
def validate_cert(start, end):
    today = get_today()
    start = format_date(start)
    end = format_date(end)
    if(start<=today<end):
        return "VALID"
    return "INVALID"

#Normal cert info
def get_certinfo(path):
    cmd = "openssl x509 -text -noout -in " + path
    output = execute_it(cmd)
    start, end, issuer = "", "", ""
    for line in output.split("\n"):
        if "Issuer:" in line:
            m = re.search('CN = (.+?)(,|$)', line)
            issuer = m.group(1)
        elif "Not Before:" in line:
            start = line[24:30] + " " + line[40:44]
        elif "Not After :" in line:
            end = line[24:30] + " " + line[40:44]
    return issuer, validate_cert(start, end), start, end, get_fingerp(path), path

#This function adds new value into normalcertler key.
def add_normalcert(path):
    crt1 = get_certinfo(path)
    normalcertler = get_normalcerts()
    normalcertler.append(str(crt1))
    mico.set_strv("normalcertler", normalcertler)

def add_normalcert(path):
    crt1 = get_certinfo(path)
    normalcertler = get_normalcerts()
    normalcertler.append(str(crt1))
    mico.set_strv("normalcertler", normalcertler)

#This function returns instant normalcertler values.
def get_normalcerts():
    return mico.get_strv("normalcertler")

def print_normalcerts():
    normalcertler = get_normalcerts()
    print("<style>table {border-collapse: collapse;width: 100%;}td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}[data-status='VALID'] {color: green;}[data-status='INVALID'] {color: red;}</style>")
    print("<table><tr><th>CN</th><th>Validity</th><th>Start</th><th>End</th><th>Fingerprint</th><th>Path</th></tr>")
    for cert in normalcertler:
        cer = cert.split(",")
        print("<tr>")
        print("<td>" + cer[0][2:-1] + "</td><td data-status=" + cer[1][2:-1] + "> " + cer[1][2:-1] + " </td><td> " +cer[2][2:-1] + " </td><td> " +cer[3][2:-1] + " </td><td> " +cer[4][2:-1] + " </td><td> " +cer[5][2:-2] + "</td> " )
        print("</tr>")
    print("</table>")

#################################

'''#Example normalcert addition manually
cert_path = "/home/liman/KokCA3.crt"
add_normalcert(cert_path)'''

if len(sys.argv) > 1:
    fonksiyon_adi = sys.argv[1]
    fonksiyon_degeri = sys.argv[2]
    if fonksiyon_adi == "add_normalcert":
        add_normalcert(fonksiyon_degeri)

print_normalcerts()



