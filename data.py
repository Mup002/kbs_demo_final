import mysql.connector

from forward_demo1 import Rule

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password="1234",
    database = "kbs_demo3"
)

class QueryData:
    def __init__(self):
        self.resultRegime = []
        self.resultStatus = []
        self.resultfc = []
        self.resultbc = []
        self.resulttt = []

    def dataRegime(self):
        """ lay du lieu tu bang regime"""
        dbregime = mydb.cursor()
        dbregime.execute("SELECT * FROM kbs_demo3.exercise_regime;")
        regime = dbregime.fetchall()
        dirregime = {}
        for i in regime:
            dirregime['id_regime'] = i[0]
            self.resultRegime.append(dirregime)
            dirregime = {}
        return self.resultRegime

    def get_rules_type_1(self):
        dbinferences = mydb.cursor()
        dbinferences.execute("SELECT kbs_demo3.inferences.* FROM kbs_demo3.inferences JOIN kbs_demo3.rules ON inferences.id_rule = rules.id_rule WHERE kbs_demo3.rules.type = 1;")
        rows = dbinferences.fetchall()

        rules = []
        for row in rows:
            id_status = row[2]
            id_regime = row[1]
            id_rule = row[3]
            rule = Rule(id_rule, id_status, id_regime)
            rules.append(rule)

        return rules

    def dataStatus(self):
        dbstatus = mydb.cursor()
        dbstatus.execute("SELECT * FROM kbs_demo3.status;")
        status = dbstatus.fetchall()
        dirstatus = {}
        for i in status:
            dirstatus['id_status'] = i[0]
            dirstatus['status_name'] = i[1]
            self.resultStatus.append(dirstatus)
            dirstatus = {}
        return self.resultStatus
    def get_rules_type_0(self):
        dbinferences = mydb.cursor()
        dbinferences.execute("SELECT kbs_demo3.inferences.* FROM kbs_demo3.inferences JOIN kbs_demo3.rules ON inferences.id_rule = rules.id_rule WHERE kbs_demo3.rules.type = 0 order by inferences.id;")
        rows = dbinferences.fetchall()

        rules = []
        for row in rows:
            id_status = row[2]
            id_regime = row[1]
            id_rule = row[3]
            rule = Rule(id_rule, id_status, id_regime)
            rules.append(rule)

        return rules
    def getfc(self):
        dbfc = mydb.cursor()
        dbfc.execute(
            "select inferences.id, rules.id_rule, id_status, id_regime from kbs_demo3.inferences, kbs_demo3.rules where inferences.id_rule = rules.id_rule"

        )
        fc = dbfc.fetchall()
        s = []
        d = []
        for i in range(len(fc)):
            s.append(fc[i][2])
            d.append(fc[i][3])
        tt = s[0]
        regime = []
        dicfc = {}
        for i in range(len(s)):
            if s[i] == tt:
                regime.append(d[i])
            else:
                dicfc['status'] = tt
                dicfc['regime'] = regime
                tt = s[i]
                self.resultfc.append(dicfc)
                regime = []
                regime.append(d[i])
                dicfc ={}

    def getbc(self):
        dbbc = mydb.cursor()
        dbbc.execute("select inferences.id, rules.id_rule, id_status, id_regime from kbs_demo3.inferences, kbs_demo3.rules where inferences.id_rule = rules.id_rule order by id_regime")
        fc = dbbc.fetchall()
        rule = []
        s = []
        d = []
        for i in range(len(fc)):
            rule.append(fc[i][1])
            s.append(fc[i][2])
            d.append(fc[i][3])
        vtrule = rule[0]
        tt = []
        regime = None
        dicbc = {}
        for i in range(len(rule)):
            if rule[i] == vtrule:
                tt.append(s[i])
                regime = d[i]
            else:
                dicbc['rule'] = vtrule
                dicbc['regime'] = regime
                dicbc['status'] = tt
                vtrule = rule[i]
                self.resultbc.append(dicbc)
                regime =  d[i]
                tt = []
                tt.append(s[i])
                dicbc = {}
    def groupbc(self):
        p = []
        vt =  self.resultbc[0]['regime']
        temp = []
        for i in self.resultbc:
            t = []
            t.append(i['regime'])
            for j in i['status']:
                t.append(j)
            temp.append(t)
        return temp
    def groupfc(self):
        res = []
        for i in self.resultfc:
            for j in range(len(i['regime'])):
                res.append([i['regime'][j], i['status']])
        return res

class Person:
    def __init__(self, name, phoneNumber, email, height, weight, bmi):
        self.name = name
        self.phoneNumber = phoneNumber
        self.email = email
        self.height = height
        self.weight = weight
        self.bmi = bmi
    def __str__(self):
        return f"{self.name} - {self.phoneNumber} - {self.email} - {self.height} - {self.weight} - {self.bmi}"