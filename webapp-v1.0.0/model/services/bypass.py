import jwt
import bcrypt
from infrastructure import database
from model import device
#Database configuration
#databaseOBJ=database.postgresDatabase(user=os.environ['DBUSER'], password=os.environ['DBPASSWORD'], host=os.environ['DBHOST'], dbname=os.environ['DBNAME'])
databaseOBJ=database.postgresDatabase(host='localhost')


def login(self: device.iotDevice):
    password = self.get_password()
    token = jwt.encode({"tag": str(self.get_tag())}, "secret", algorithm="HS256")
    tag = token.split('.')
    tag = tag[1]
    credentials = databaseOBJ.readRaw("select password from devices where tag='" + tag+ "';")
    if credentials != []:
        if bcrypt.checkpw(password.encode(), credentials[0][0].encode()):
            self.set_logged(True)
            self.set_tag(tag)
            return True
        else:
            self.set_logged(False)
            return False
    else:
        self.set_logged(False)
        return False
            
