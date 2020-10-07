from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import re
import logging
import os

http = "https://files.pushshift.io/reddit/comments/"
endpoints = ["RC_2016-05.bz2","RC_2016-06.bz2","RC_2016-07.bz2",
             "RC_2016-08.bz2","RC_2016-09.bz2","RC_2016-10.bz2",
             "RC_2016-11.bz2","RC_2016-12.bz2","RC_2017-01.bz2",
             "RC_2017-02.bz2","RC_2017-03.bz2","RC_2017-04.bz2",
             "RC_2017-05.bz2","RC_2017-06.bz2","RC_2017-07.bz2",
             "RC_2017-08.bz2","RC_2017-09.bz2","RC_2017-10.bz2",
             "RC_2017-11.bz2","RC_2017-12.xz","RC_2018-01.xz",
             "RC_2018-02.xz","RC_2018-03.xz","RC_2018-04.xz",
             "RC_2018-05.xz","RC_2018-06.xz","RC_2018-07.xz",
             "RC_2018-08.xz","RC_2018-09.xz","RC_2018-10.xz",
             "RC_2018-11.zst","RC_2018-12.zst","RC_2019-01.zst",
             "RC_2019-02.zst","RC_2019-03.zst","RC_2019-04.zst",
             "RC_2019-05.zst"
        ]

for endpoint in endpoints[:]: 
    os.system("wget " + http + endpoint)
    file_name,file_extension = os.path.splitext(endpoint)
    #use different command to unzip based on file extension
    if file_extension == ".bz2":
        os.system("bunzip2 " + endpoint) 
    elif file_extension == ".xz":
        os.system("unxz " + endpoint)
    elif file_extension ==".zst":
        os.system("unzstd " + endpoint)
    #remove zipped file
    os.system(f"rm {endpoint}")
    os.system(f"grep -E 'news|funny|Conservative|The_Donald|politics|esist|Science|gaming' {file_name} > holder_file")  
    os.system(f"mongoimport --db reddit_comments --collection All_Data --type json --file holder_file") 
    client = MongoClient()
    print("Succesfully wrote to db")
    #remove the unzipped file after we have written to the mongodb
    os.system(f"rm {file_name}")
    os.system(f"rm holder_file")
