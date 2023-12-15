import time
from data import *
from data import  QueryData
from forward_demo1 import Inference
from backward_demo1 import Inference2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# bien khoi tao
person = Person(None,  None, None, None, None)
list_status_of_person = []
bmi_of_person = None;
db = QueryData()
db.dataRegime()
db.dataStatus()
validate =  Validate()
# luat_tien = db.groupfc()
#welcome_question
def welcome_question():
    print("-->Chatbot: Xin chào, tôi là chatbot tư vấn chế độ dinh dưỡng và chế độ luyện tập cho người muốn giảm cân")
    print("-->Chatbot: Để nhận tư vấn chính xác , hãy để lại cho tôi 1 số thông tin")

    print("-->Chatbot: hãy nhập tên")
    person.name = validate.validate_name(input())
    print(f'--> Người dùng: Tên tôi là, {person.name}')

    # print("-->Chatbot : hãy nhập số điện thoại")
    # person.phoneNumber = validate.validate_phonenumber(input())
    # print(f'-->Người dùng: Số điện thoại của tôi là, {person.phoneNumber}')

    print("-->Chatbot : hãy nhập email")
    person.email = validate.validate_email(input())
    print(f'-->Người dùng: Email của tôi là, {person.email}')

    print("-->Chatbot : hãy nhập cân nặng (ví dụ 90kg -> nhập 90)")
    person.weight = validate.validate_weight(input())
    print(f'-->Người dùng: Cân nặng của tôi là, {person.weight}')

    print("-->Chatbot : hãy nhập chiều cao (ví dụ 165cm -> nhập 1.65)")
    person.height = validate.validate_height(input())
    print(f'-->Người dùng: Chiều cao của tôi là, {person.height}')

    print(f'-->Chat : hãy chờ tôi tính chỉ số BMI của cơ thể bạn')
    person.bmi = float(person.weight) / (float(person.height) ** 2)
    if 18.5 <= person.bmi < 24.9 :
        list_status_of_person.append(db.resultStatus[1])
    else:
        list_status_of_person.append(db.resultStatus[0])
    time.sleep(5)
    print(f'-->Chatbot : Đây là chỉ số BMI hiện tại của cơ thể bạn, {person.bmi}')

    print(person)
    return person

# first_question
def first_question(list_status_of_person, person):
    FirstLstQuestion = [db.resultStatus[2],
                db.resultStatus[3],
                db.resultStatus[4]
                ]
    CheckLst = []
    # for i in FirstLstQuestion:
    #     CheckLst.append(i["id_status"])
    while(1):
        count = 1
        if(len(CheckLst) != 0):
            break
        if(len(CheckLst) == 0):
            print(f'-->Chatbot : {person.name} hãy cho tôi biết về mức độ hoạt động thường ngày của bạn')
            for i in FirstLstQuestion:
                print(f'{count}. {i["status_name"]} \n')
                count += 1
            answer = validate.validate_input_number_form(input())
            print(f'-->{person.name}: Câu trả lời của tôi là {answer}')

            if(int(answer) <=0 or int(answer) >= 4):
                print(f'-->Chat bot: Vui lòng nhập số từ 1 đến 3')
                continue
            else:
                CheckLst.append(FirstLstQuestion[int(answer)-1]["id_status"])
                list_status_of_person.append(db.resultStatus[int(answer)+1])
    return list_status_of_person

# 2th question
def second_question(list_status_of_person, person):
    SecondLstQuestion = [db.resultStatus[5],
                         db.resultStatus[6],
                         db.resultStatus[7]
                         ]
    CheckLst = []
    while(1):
        count = 1
        if(len(CheckLst) != 0):
            break
        if(len(CheckLst) == 0):
            print(f'-->Chatbot : {person.name} , bạn muốn mức độ các bài tập trong chế độ tập luyện như nào?')
            for i in SecondLstQuestion:
                print(f'{count}. {i["status_name"]}\n')
                count += 1
            answer = validate.validate_input_number_form(input())
            print(f'-->{person.name}: Câu trả lời của tôi là {answer}')

            if (int(answer) <= 0 or int(answer) >= 4):
                print(f'-->Chat bot: Vui lòng nhập số từ 1 đến 3')
                continue
            else:
                CheckLst.append(SecondLstQuestion[int(answer)-1]["id_status"])
                list_status_of_person.append(db.resultStatus[int(answer) + 4])
    return list_status_of_person

## 3th question
def third_question(list_status_of_person, person):
    ThirdLstQuestion = [db.resultStatus[8],
                        db.resultStatus[9]
                        ]
    CheckLst = []
    while(1):
        count = 1
        if(len(CheckLst) != 0):
            break
        if(len(CheckLst) == 0):
            print(f'-->Chatbot : {person.name} , bạn muốn tốc độ giảm cân sẽ diễn ra như nào?')
            for i in ThirdLstQuestion:
                print(f'{count}. {i["status_name"]}\n')
                count += 1
            answer = validate.validate_input_number_form(input())
            print(f'-->{person.name}: Câu trả lời của tôi là {answer}')

            if (int(answer) <= 0 or int(answer) >= 3):
                print(f'-->Chat bot: Vui lòng nhập số từ 1 đến 2')
                continue
            else:
                CheckLst.append(ThirdLstQuestion[int(answer)-1]["id_status"])
                list_status_of_person.append(db.resultStatus[int(answer) + 7])
    return list_status_of_person
## thực hiện suy diễn tiến
def forward_chaining_1(list_status_of_person_id):
    list_kq = []
    infe1 = Inference(db.get_rules_type_1(), list_status_of_person_id, "output_results_forward_1.txt")
    inferences = infe1.infer()
    for inference in inferences:
        list_kq.append(inference)
    return list_kq

## 1 số câu hỏi phụ trợ suy diễn lùi
def support_question(list_status_of_person, person):
    SupportQuestion = [db.resultStatus[10],
                       db.resultStatus[11]
                       ]

    print(f'-->Chatbot : {person.name} , bạn có {SupportQuestion[0]["status_name"]} không?')
    print(f'{1}. {"Có"}\n')
    print(f'{0}. {"Không"}\n')
    answer1 = validate.validate_input_number_form(input())
    print(f"answer: {answer1}")
    if answer1 == 1:
        list_status_of_person.append(db.resultStatus[10])

    print(f'-->Chatbot : {person.name} , bạn có {SupportQuestion[1]["status_name"]} không?')
    print(f'{1}. {"Có"}\n')
    print(f'{0}. {"Không"}\n')
    answer2 = validate.validate_input_number_form(input())
    print(f"answer: {answer2}")
    if answer2 == 1:
        list_status_of_person.append(db.resultStatus[11])

    return list_status_of_person

## thực hiện suy diễn lùi
def backward_chaining_1(list_status_of_person_id, forward_1):
    infe2 = Inference2(db.get_rules_type_0(),list_status_of_person_id,forward_1,"output_results_backward_1.txt")
    inference = infe2.infer()
    kq = inference
    return kq

## Gửi thông tin qua email
def send_email(subject, body, to_email):
    # Thông tin tài khoản email của bạn
    sender_email = "buiminhvu.b20dccn741@gmail.com"
    sender_password = "jlqn hlcz ylsc nlra"

    # email = 'buiminhvu.b20dccn741@gmail.com'
    # password = 'jlqn hlcz ylsc nlra'
    # Tạo đối tượng MIMEMultipart
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # Thêm nội dung email
    message.attach(MIMEText(body, "plain"))

    # Kết nối đến máy chủ SMTP của bạn (ví dụ: Gmail)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        # Bắt đầu phiên kết nối
        server.starttls()

        # Đăng nhập vào tài khoản email
        server.login(sender_email, sender_password)

        # Gửi email
        server.sendmail(sender_email, to_email, message.as_string())


person = welcome_question()
list_status_of_person = first_question(list_status_of_person,person)
print([i['id_status'] for i in list_status_of_person])
list_status_of_person = second_question(list_status_of_person,person)
print([i['id_status'] for i in list_status_of_person])
list_status_of_person = third_question(list_status_of_person, person)
print([i['id_status'] for i in list_status_of_person])

list_status_of_person_id = [i['id_status'] for i in list_status_of_person]
list_status_of_person_id = list(set(list_status_of_person_id))

print(f'-->Chatbot: Đây là những dự đoán sơ bộ của chúng tôi')
print(forward_chaining_1(list_status_of_person_id))
print("\n")
print(f'-->Chatbot: Tiếp theo tôi sẽ hỏi tiếp 1 số câu hỏi nữa để đưa ra phương pháp tập luyện tối ưu nhất cho bạn.')

list_status_of_person = support_question(list_status_of_person,person)
print([i['id_status'] for i in list_status_of_person])

list_status_of_person_id = [i['id_status'] for i in list_status_of_person]
list_status_of_person_id = list(set(list_status_of_person_id))

print(f'-->Chatbot: Chế độ tập luyện phù nhất cho bạn:')

id_regime = backward_chaining_1(list_status_of_person_id, forward_chaining_1(list_status_of_person_id))
print(backward_chaining_1(list_status_of_person_id, forward_chaining_1(list_status_of_person_id)))
# id_regime = 'D02'
print(f'-->Chatbot : Đây là chế độ tập luyện dành cho {person.name} trong 1 tuần tới:')
for i in db.getExcercise(id_regime):
    print(i[1] + " : " + i[2])

print(f'-->Chatbot : Việc tập luyện dành cho sẽ kết hợp chế độ dinh dưỡng nhưu sau:')
for i in db.getNutrition(id_regime):
    print(i[1])

# Lấy thông tin về bài tập từ db
exercise_info = "\n".join([f"{i[1]}: {i[2]}" for i in db.getExcercise(id_regime)])

# Lấy thông tin về dinh dưỡng từ db
nutrition_info = "\n".join([i[1] for i in db.getNutrition(id_regime)])

subject = "Test Email"
body = f"""
***Xin chào {person.name}
***Tôi là chatbot tư vấn dinh dưỡng và tập luyện cho người giảm cân
***Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi
***Đây là nhưng tư vấn cho bạn:
Bài tập:
{exercise_info}

Chế độ dinh dưỡng:
{nutrition_info}
"""
recipient_email = f"{person.email}"
send_email(subject, body, recipient_email)

