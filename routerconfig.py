import paramiko
import time
import config
from auth import Authentication


def connectSsh(self,usr,pwd):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(
        str(self),
        username=usr,
        password=pwd,
        look_for_keys=False,
        allow_agent=False)
    return conn


circuit = ""
incir = inpir = outcir = outpir = linein = lineout = ""


class RouterConfig:

    def config_router(self, auth):
        authres = Authentication.login(auth)
        if authres == 'success':
            print(self)
            conn = connectSsh(self['IP'],self['USR'],self['PWD'])

            output = ""
            GE = ""
            stdin, stdout, stderr = conn.exec_command("display interface description | include " + self['CIRCUIT'])
            stdout = stdout.readlines()
            conn.close()

            for line in stdout:
                if 'GE' in line:
                    GE = (line.split(" ")[0])[2:7]
                    print(GE)

            conn = connectSsh(self['IP'],self['USR'],self['PWD'])
            stdin, stdout, stderr = conn.exec_command("display current-configuration interface GigabitEthernet " + GE)
            stdout = stdout.readlines()
            conn.close()

            for line in stdout:
                if 'user-queue' in line:
                    if 'inbound' in line:
                        incir = line.split(" ")[3]
                        inpir = line.split(" ")[5]
                        print(line)

                    if 'outbound' in line:
                        outcir = line.split(" ")[3]
                        outpir = line.split(" ")[5]
                        print(line)
            if incir == inpir == outcir == outpir:
                conn = connectSsh(self['IP'],self['USR'],self['PWD'])
                remote_conn = conn.invoke_shell()
                remote_conn.send("system-view \n")
                remote_conn.send("interface GigabitEthernet " + GE + " \n")
                remote_conn.send("undo user-queue inbound \n")
                remote_conn.send("undo user-queue outbound \n")
                remote_conn.send("user-queue cir " + self['SPEED'] + " pir " + self['SPEED'] + " flow-queue 201 inbound \n")
                remote_conn.send(
                    "user-queue cir " + self['SPEED'] + " pir " + self['SPEED'] + " flow-queue 201 outbound \n")
                remote_conn.send("display this \n")
                time.sleep(2)
                output = remote_conn.recv(1000)
                print(output.decode("utf-8"))
                responsedata = {"message": output.decode("utf-8")}
                return responsedata

            else:
                print("invalid inbound Outbound values")
                responsedata = {"message": "invalid inbound Outbound values"}
                return responsedata
        else:
            responsedata = {"message": authres}
            return responsedata
