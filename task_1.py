# scyqy1 20318224 Qi YOU
# === WARNING ===
# Do not import any additional modules
# ===============
from csv import reader
import sqlite3

def task1_solution():
    conn = sqlite3.connect('iMusic.db')
    #Establish a connection to the target file
    conn.row_factory = sqlite3.Row
    #Maybe optional?
    cur = conn.cursor()
    #Create a "cursor" -> "pointer?"
    #SEQUENCE MATTERS!
    with open('TrackPrices.csv') as TP:
        csv_read = reader(TP)
        #Read the file loaded as "TP"
        title = next(csv_read)
        #Grab 1st line as the title
        if title != None:
            #For Assumption cases only. In TrackPrices.csv it won't happen. But I'd love to keep it for safety.
            for row in csv_read:
                cur.execute("UPDATE Track SET UnitPrice = :P WHERE TrackId = :ID;", {"P": row[1], "ID": row[0]})
                #Funfact: "row" is a list. "P", "ID" were treated as elements in a row.

    conn.commit()
    #Commit & Apply the changes.
    conn.close()
    #Close the connection.

if __name__ == '__main__':
    task1_solution()

#Status: Completed!