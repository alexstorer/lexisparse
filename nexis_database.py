"""
Script makes an SQLite3 database from nexis files pre-processed by lexisparse

"""
import sqlite3
import os

def read_data(file):
    file_con = open(file, 'r')
    text = file_con.read()
    return(text)

def main():
    """docstring for main"""
    dir_files = os.path.join(os.getcwd(), ".lexisparse")

    conn = sqlite3.connect('Nexis Articles.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE articles (ID, Text)''')

    all_files = os.listdir(dir_files)
    txt_files = [f for f in all_files if ".txt" in f]

    for f in txt_files:
        file_path = os.path.join(dir_files, f)
        article_text = read_data(file_path)
        full_insert = [f, article_text]
        c.execute('INSERT INTO articles VALUES (?,?)',full_insert)
    
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()