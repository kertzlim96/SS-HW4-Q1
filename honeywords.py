import hashlib
import random

wordlist = []
with open("10k-most-common.txt",'r') as f:
    for i in f:
        wordlist.append(i.rstrip())
        
#################################
#  Generate honeywords functions
#################################
def md5_hash(pw):
    hashed = hashlib.md5(pw.encode()).hexdigest() 
    return hashed
def choose_rand_pw(wordlist):
    # returns a random word from list
    no = random.randrange(len(wordlist)) 
    return wordlist[no]
def generate_honeywords(real_password,wordlist):
    honeyword_list = []
    honeyhash_list = []
    no_honeyword = 10  # no to generate, including real password
    index = random.randrange(no_honeyword) # index of real password in honeyword_list[index]
    for i in range(no_honeyword): 
        if i == index:
            hashed = md5_hash(real_password)
            honeyword_list.append(real_password)
            honeyhash_list.append(hashed)
        else:
            pw = choose_rand_pw(wordlist)
            hashed = md5_hash(pw)
            honeyword_list.append(pw)
            honeyhash_list.append(hashed)

    return index, honeyword_list, honeyhash_list

#################################
#  Authenticate
#################################
def authenticate_pw(pw_hashlist,index, password):
    hashed_pw = md5_hash(password)
    # case 1: Real password
    if hashed_pw in pw_hashlist and pw_hashlist[index] == hashed_pw:
        print("Authenticate success")
    
    # case 2: Honeyword
    elif hashed_pw in pw_hashlist and pw_hashlist[index] != hashed_pw:
        print("Honeyword, ALERT")
        
    # case 3: Wrong password
    else:
        print("Login fail")


#################################
#  CSV database
#################################

def gen_and_add_new_user_db(user,real_password,wordlist):
    # generates the honeywords
    index, honeyword_list, honeyhash_list= generate_honeywords(real_password,wordlist)
    
    # add the hashes into the hash_db.csv
    csv_entry = str(user) 
    for i in range(len(honeyhash_list)):
        csv_entry = csv_entry+","+str(honeyhash_list[i])
    with open("Hash_db.csv",'a') as f:
        f.writelines(csv_entry)
        f.write("\n")
    
    # add the plaintext passwords, just for testing, so know plaintext
    csv_entry = str(user) 
    for i in range(len(honeyword_list)):
        csv_entry = csv_entry+","+str(honeyword_list[i])
    with open("pass_db.csv",'a') as f:
        f.writelines(csv_entry)
        f.write("\n")
        
    # add index of correct hash, but put in seperate file which must be secured
    csv_entry = str(user) +","+str(index)
    with open("index_db.csv",'a') as f:
        f.writelines(csv_entry)
        f.write("\n")

def read_db():
    USER = []
    HASH = []
    INDEX = []
    with open("Hash_db.csv",'r') as f:
        for i in f:
            temp = i.split(',')
            temp[-1] = temp[-1].rstrip()
            USER.append(temp[0])
            HASH.append(temp[1:])
    with open("index_db.csv",'r') as f:
        for i in f:
            temp = i.split(',')
            INDEX.append(temp[1].rstrip())
    return USER, INDEX, HASH
