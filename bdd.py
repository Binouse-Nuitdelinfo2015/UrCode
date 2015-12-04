import sqlite3


def creaTables():
    print("coucou,")
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE utilisateur (idU INTEGER, nom text, prenom text, type text, PRIMARY KEY (idU))''')
    c.execute(
        '''CREATE TABLE note (idN INTEGER, fk_idU INTEGER, valeur INTEGER, FOREIGN KEY (fk_idU) REFERENCES utilisateur(idU) ON DELETE CASCADE, PRIMARY KEY (idN))''')
    c.execute(
        '''CREATE TABLE cata (idC INTEGER, appellation text, dateDebut text, dateFin text, lieu text, gravite INTEGER, PRIMARY KEY (idC))''')
    c.execute(
        '''CREATE TABLE actu (idDate text, fk_idC INTEGER, fk_idU INTEGER, information text, FOREIGN KEY (fk_idC) REFERENCES cata(idC)ON DELETE CASCADE, FOREIGN KEY (fk_idU) REFERENCES utilisateur(idU) ON DELETE CASCADE, PRIMARY KEY (idDate, fk_idC, fk_idU))''')

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    print("tu veux voir ma bite?")


def suprTables():
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    # supr table
    c.execute("DROP TABLE actu")
    c.execute("DROP TABLE cata")
    c.execute("DROP TABLE note")
    c.execute("DROP TABLE utilisateur")

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


def setUti(nom, prenom, typeU):
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute("insert into utilisateur(nom, prenom, type) values (?,?,?)", (nom, prenom, typeU))
    conn.commit()
    conn.close()


def setNote(fk_idU, valeur):
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute("insert into note(fk_idU, valeur) values (?,?)", (fk_idU, valeur))
    conn.commit()
    conn.close()


def setCata(appellation, dateDebut, dateFin, lieu, gravite):
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute("insert into cata(appellation, dateDebut, dateFin,lieu, gravite) values (?,?,?,?,?)",
              (appellation, dateDebut, dateFin, lieu, gravite))
    conn.commit()
    conn.close()


def setActu(pk_date, fk_idC, fk_idU, information):
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute("insert into Actu(fk_idC , fk_idU, information) values (?,?,?)", (fk_idC, fk_idU, information))
    conn.commit()
    conn.close()


def getUti():
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute("SELECT * FROM utilisateur")
    tout = c.fetchall()
    conn.close()
    return tout


def getNote():
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute("SELECT * FROM note")

    tout = c.fetchall()
    conn.close()
    return tout


def getCata():
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute("SELECT * FROM cata")

    tout = c.fetchall()
    conn.close()
    return tout


def getActu():
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute("SELECT * FROM actu")

    tout = c.fetchall()
    conn.close()
    return tout


def getUtiP(idU):
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute("SELECT * FROM utilisateur where idU=" + str(idU))
    tout = c.fetchall()
    conn.close()
    return tout


def getNoteP(idN):
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute("SELECT * FROM note where idN=" + str(idN))

    tout = c.fetchall()
    conn.close()
    return tout


def getCataP(idC):
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute("SELECT * FROM cata where idC=" + str(idC))

    tout = c.fetchall()
    conn.close()
    return tout


def getActuP(idA):
    conn = sqlite3.connect('example.db')

    c = conn.cursor()

    c.execute("SELECT * FROM actu where idDate=" + str(idA))

    tout = c.fetchall()
    conn.close()
    return tout


def creaTuples():
    setUti("chewbaca", "Chewi", "passant")
    setUti("C3PO", "6PO", "Famille")
    setUti("Empereur", "Palpatine", "Empereur")
    setUti("Solo", "Hans", "inutile")

    setNote(1, 10)
    setNote(1, 8)
    setNote(1, 7)
    setNote(1, 7)
    setNote(2, 10)
    setNote(3, 8)
    setNote(3, 10)
    setNote(4, 2)

    setCata("Caterine", "23/10/92", "25/10/92", "floridaison", 8)
    setCata("Caterine", "26/10/92", "30/10/92", "floridaison", 10)
    setCata("yannick", "22/10/92", "22/10/92", "paridaison", 2)
    setCata("daesh", "13/11/15", "13/11/15", "paris", 6)
    setCata("yeah", "32/02/64", "34/13/66", "nowere", 10)

    setActu("24/10/92", 1, 1, "whesh ya du vent")
    setActu("24/10/92", 1, 2, "whesh tavu")
    setActu("25/10/92", 1, 1, "whesh ya toujourduvent")
    setActu("05/11/93", 1, 3, "wesh trop pas du vent")

# ~ def main():
# ~ suprTables()
# ~ creaTables()
# ~ setUti("test","test1","inutile")
# ~ setUti("test2","test1","inutile")
# ~ for row in getUti():
# ~ print(row)
# ~ for row in getUtiP(1):
# ~ print(row)

# ~ main()
