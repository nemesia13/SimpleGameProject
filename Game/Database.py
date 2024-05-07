import sqlite3

#this files is used to update/remove/modify and keep track of the contents of the Database

connection = sqlite3.connect("oppari_game.db") #has to be Game/ in VSCode

#send SQL commands to DB with cursor
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS highscore (id INTEGER PRIMARY KEY UNIQUE, name TEXT, score INTEGER, unique (id, name))")
cursor.execute("CREATE TABLE IF NOT EXISTS obstacles (id INTEGER PRIMARY KEY UNIQUE, img_path TEXT, character TEXT, type TEXT, unique (id, type))")

cursor.execute("CREATE TABLE IF NOT EXISTS suitPlayer(id INTEGER PRIMARY KEY UNIQUE, img_path TEXT, description TEXT, unique (description, id))")
cursor.execute("CREATE TABLE IF NOT EXISTS bunnyPlayer(id INTEGER PRIMARY KEY UNIQUE, img_path TEXT, description TEXT, unique (description, id))")
cursor.execute("CREATE TABLE IF NOT EXISTS clownPlayer(id INTEGER PRIMARY KEY UNIQUE, img_path TEXT, description TEXT, unique (description, id))")


#add suitPlayer's different moves to database
cursor.execute("INSERT OR REPLACE INTO suitPlayer VALUES (1, 'graphics/suitPlayer/suit_climb_left01.png', 'climb_left01')")
cursor.execute("INSERT OR REPLACE INTO suitPlayer VALUES (2, 'graphics/suitPlayer/suit_climb_left02.png', 'climb_left02')") #left
cursor.execute("INSERT OR REPLACE INTO suitPlayer VALUES (3, 'graphics/suitPlayer/suit_climb_middle01.png', 'climb_middle01')")
cursor.execute("INSERT OR REPLACE INTO suitPlayer VALUES (4, 'graphics/suitPlayer/suit_climb_middle02.png', 'climb_middle02')")#middle
cursor.execute("INSERT OR REPLACE INTO suitPlayer VALUES (5, 'graphics/suitPlayer/suit_climb_right01.png', 'climb_right01')")
cursor.execute("INSERT OR REPLACE INTO suitPlayer VALUES (6, 'graphics/suitPlayer/suit_climb_right02.png', 'climb_right02')")#right
#fall
cursor.execute("INSERT OR REPLACE INTO suitPlayer VALUES (7, 'graphics/suitPlayer/suit_fall_left01.png', 'fall_left01')")
cursor.execute("INSERT OR REPLACE INTO suitPlayer VALUES (8, 'graphics/suitPlayer/suit_fall_left02.png', 'fall_left02')")
cursor.execute("INSERT OR REPLACE INTO suitPlayer VALUES (9, 'graphics/suitPlayer/suit_fall_right01.png', 'fall_right01')")
cursor.execute("INSERT OR REPLACE INTO suitPlayer VALUES (10, 'graphics/suitPlayer/suit_fall_right02.png', 'fall_right02')")
cursor.execute("INSERT OR REPLACE INTO suitPlayer VALUES (11, 'graphics/suitPlayer/gameOver_suit.png', 'game_over')")

#add bunnyPlayer's different moves to database
cursor.execute("INSERT OR REPLACE INTO bunnyPlayer VALUES (1, 'graphics/bunnyPlayer/bunny_climb_left01.png', 'climb_left01')")
cursor.execute("INSERT OR REPLACE INTO bunnyPlayer VALUES (2, 'graphics/bunnyPlayer/bunny_climb_left02.png', 'climb_left02')")
cursor.execute("INSERT OR REPLACE INTO bunnyPlayer VALUES (3, 'graphics/bunnyPlayer/bunny_climb_middle01.png', 'climb_middle01')")
cursor.execute("INSERT OR REPLACE INTO bunnyPlayer VALUES (4, 'graphics/bunnyPlayer/bunny_climb_middle02.png', 'climb_middle02')")
cursor.execute("INSERT OR REPLACE INTO bunnyPlayer VALUES (5, 'graphics/bunnyPlayer/bunny_climb_right01.png', 'climb_right01')")
cursor.execute("INSERT OR REPLACE INTO bunnyPlayer VALUES (6, 'graphics/bunnyPlayer/bunny_climb_right02.png', 'climb_right02')")
#fall
cursor.execute("INSERT OR REPLACE INTO bunnyPlayer VALUES (7, 'graphics/bunnyPlayer/bunny_fall_left01.png', 'fall_left01')")
cursor.execute("INSERT OR REPLACE INTO bunnyPlayer VALUES (8, 'graphics/bunnyPlayer/bunny_fall_left02.png', 'fall_left02')")
cursor.execute("INSERT OR REPLACE INTO bunnyPlayer VALUES (9, 'graphics/bunnyPlayer/bunny_fall_right01.png', 'fall_right01')")
cursor.execute("INSERT OR REPLACE INTO bunnyPlayer VALUES (10, 'graphics/bunnyPlayer/bunny_fall_right02.png', 'fall_right02')")
cursor.execute("INSERT OR REPLACE INTO bunnyPlayer VALUES (11, 'graphics/bunnyPlayer/gameOver_bunny.png', 'game_over')")

#add clownPlayer's different moves to database
cursor.execute("INSERT OR REPLACE INTO clownPlayer VALUES (1, 'graphics/clownPlayer/clown_climb_left01.png', 'climb_left01')")
cursor.execute("INSERT OR REPLACE INTO clownPlayer VALUES (2, 'graphics/clownPlayer/clown_climb_left02.png', 'climb_left02')")
cursor.execute("INSERT OR REPLACE INTO clownPlayer VALUES (3, 'graphics/clownPlayer/clown_climb_middle01.png', 'climb_middle01')")
cursor.execute("INSERT OR REPLACE INTO clownPlayer VALUES (4, 'graphics/clownPlayer/clown_climb_middle02.png', 'climb_middle02')")
cursor.execute("INSERT OR REPLACE INTO clownPlayer VALUES (5, 'graphics/clownPlayer/clown_climb_right01.png', 'climb_right01')")
cursor.execute("INSERT OR REPLACE INTO clownPlayer VALUES (6, 'graphics/clownPlayer/clown_climb_right02.png', 'climb_right02')")
#fall
cursor.execute("INSERT OR REPLACE INTO clownPlayer VALUES (7, 'graphics/clownPlayer/clown_fall_left01.png', 'fall_left01')")
cursor.execute("INSERT OR REPLACE INTO clownPlayer VALUES (8, 'graphics/clownPlayer/clown_fall_left02.png', 'fall_left02')")
cursor.execute("INSERT OR REPLACE INTO clownPlayer VALUES (9, 'graphics/clownPlayer/clown_fall_right01.png', 'fall_right01')")
cursor.execute("INSERT OR REPLACE INTO clownPlayer VALUES (10, 'graphics/clownPlayer/clown_fall_right02.png', 'fall_right02')")
cursor.execute("INSERT OR REPLACE INTO clownPlayer VALUES (11, 'graphics/clownPlayer/gameOver_clown.png', 'game_over')")

#add obstacles into the obstacles table
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (1,'graphics/obstacles/flower011.png', 'suitPlayer', 'type_011' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (2,'graphics/obstacles/flower012.png', 'suitPlayer', 'type_012' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (3,'graphics/obstacles/flower021.png', 'suitPlayer', 'type_021' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (4,'graphics/obstacles/flower022.png', 'suitPlayer', 'type_022' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (5,'graphics/obstacles/flower031.png', 'suitPlayer', 'type_031' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (6,'graphics/obstacles/flower032.png', 'suitPlayer', 'type_032' )") #suitPlayers obstacles

cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (7,'graphics/obstacles/pie011.png', 'clownPlayer', 'type_011' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (8,'graphics/obstacles/pie012.png', 'clownPlayer', 'type_012' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (9,'graphics/obstacles/pie021.png', 'clownPlayer', 'type_021' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (10,'graphics/obstacles/pie022.png', 'clownPlayer', 'type_022' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (11,'graphics/obstacles/pie031.png', 'clownPlayer', 'type_031' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (12,'graphics/obstacles/pie032.png', 'clownPlayer', 'type_032' )") #clownPlayers obstacles

cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (13,'graphics/obstacles/vege011.png', 'bunnyPlayer', 'type_011' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (14,'graphics/obstacles/vege012.png', 'bunnyPlayer', 'type_012' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (15,'graphics/obstacles/vege021.png', 'bunnyPlayer', 'type_021' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (16,'graphics/obstacles/vege022.png', 'bunnyPlayer', 'type_022' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (17,'graphics/obstacles/vege031.png', 'bunnyPlayer', 'type_031' )")
cursor.execute("INSERT OR REPLACE INTO obstacles VALUES (18,'graphics/obstacles/vege032.png', 'bunnyPlayer', 'type_032' )") #bunnyPlayers obstacles

#deletes all the rows from a table
#cursor.execute("DELETE FROM highscore")

#commit changes to DB
connection.commit()

cursor.execute("SELECT COUNT(*) FROM highscore")
result = cursor.fetchone()
row_count = result[0]
print(row_count)

cursor.execute("SELECT score FROM highscore ORDER BY score DESC")
result = cursor.fetchall()
cursor.execute("SELECT name FROM highscore ORDER BY score DESC")
names = cursor.fetchall()

for (re, na) in zip(result,names):
    print(str(re[0])+" "+str(na[0]))

connection.close()



