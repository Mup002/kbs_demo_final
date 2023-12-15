import mysql.connector
import re
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

    def getExcercise(self, id_regime):
        dbex =  mydb.cursor()
        dbex.execute("SELECT * FROM kbs_demo3.exercise;")
        rows = dbex.fetchall()
        lst = []
        for i in rows:
            if i[3] == id_regime:
                lst.append(i)
        return lst
    def getNutrition(self, id_regime):
        dbex =  mydb.cursor()
        dbex.execute("SELECT * FROM kbs_demo3.adive_nutrition")
        rows = dbex.fetchall()
        lst = []
        for i in rows:
            if i[3] == id_regime:
                lst.append(i)
        return lst

class Validate:
    def __init__(self) -> None:
        pass

    def validate_input_number_form(self,value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))
            check = valueGetRidOfSpace.isnumeric()
            if (check):
                return valueGetRidOfSpace
            else:
                print("-->Chatbot: Vui lòng nhập 1 số dương")
                value = input()

    def validate_phonenumber(self,value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))
            check = valueGetRidOfSpace.isnumeric()
            if (check):
                return valueGetRidOfSpace
            else:
                print("-->Chatbot: Vui lòng nhập 1 số điện thoại đúng định dạng")
                value = input()


    def validate_email(self, email):
        while (1):
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            if (re.fullmatch(regex, email)):
                # print("Chatbot:Tôi đã nhận được thông tin Email của bạn")
                return email

            else:
                print("-->Chatbot: Vui lòng nhập lại email")
                email = input()

    def validate_name(self, value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))

            check = valueGetRidOfSpace.isalpha()
            if (check):
                # print("Tôi đã nhận được thông tin Tên của bạn")
                return value
            else:
                print("-->Chatbot: Vui lòng nhập lại tên ! ")
                value = input()

    def validate_binary_answer(self, value):
        acceptance_answer_lst = ['1', 'y', 'yes', 'co', 'có']
        decline_answer_lst = ['0', 'n', 'no', 'khong', 'không']
        value = value+''
        while (1):
            if (value) in acceptance_answer_lst:
                return True
            elif value in decline_answer_lst:
                return False
            else:
                print(
                    "-->Chatbot: Câu trả lời không hợp lệ. Vui lòng nhập lại câu trả lời")
                value = input()

    def validate_height(self, value):
        while True:
            try:
                height = float(value)
                if 0 < height < 3:  # Assuming a reasonable range for height in meters
                    return height
                else:
                    print("-->Chatbot: Vui lòng nhập chiều cao hợp lệ (tính bằng mét)")
                    value = input()
            except ValueError:
                print("-->Chatbot: Vui lòng nhập chiều cao là một số.")
                value = input()

    def validate_weight(self, value):
        while True:
            try:
                weight = float(value)
                if 0 < weight:  # Assuming weight cannot be negative
                    return weight
                else:
                    print("-->Chatbot: Vui lòng nhập cân nặng hợp lệ (tính bằng kg)")
                    value = input()
            except ValueError:
                print("-->Chatbot: Vui lòng nhập cân nặng là một số.")
                value = input()


class Person:
    def __init__(self, name,  email, height, weight, bmi):
        self.name = name
        self.email = email
        self.height = height
        self.weight = weight
        self.bmi = bmi
    def __str__(self):
        return f"{self.name} - {self.email} - {self.height} - {self.weight} - {self.bmi}"