import os

# renvoie le chemin absolu du repertoire courant
basedir = os.path.abspath(os.path.dirname(__file__))

print (basedir)


# renvoie le chemin absolu du repertoire contenant le repertoire courant
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print (BASE_DIR)

path_db=os.path.join(basedir, 'app.db')
print (path_db)