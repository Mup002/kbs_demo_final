class Rule:
    def __init__(self, id, status, regime):
        self.id = id
        self.status = status
        self.regime = regime

    def __repr__(self):
        return f"Rule({self.id}, {self.status}, {self.regime})"

class Inference2:
    def __init__(self, rules, facts, goals, file_name):
        self.rules = rules
        self.facts = facts
        self.goals = goals
        self.inferences = []
        self.output = file_name
        self.road = 0
        self.true_rule = ""
        self.true_id_rule = ""
        self.kq1 = []
        self.kq2 = []
        self.kq3 = []
        self.kq4 = []
        self.kq5 = []
        self.kq6 = []
    def infer(self):
        current_rule = "R1"
        list_fact = ""
        current_regime = 'D01'
        count = 0
        for fact in self.facts:
            self.kq2.append(fact)
        for goal in self.goals:
            self.kq3.append(goal)
        for rule in self.rules:
            if current_rule == rule.id:
                if len(list_fact) == 0:
                    list_fact += str(rule.status)
                else:
                    list_fact += " + " + str(rule.status)
            else:
                self.kq1.append(current_rule + ": " + list_fact + " -> " + current_regime)

                current_rule = rule.id
                current_regime = rule.regime
                list_fact = ""
                list_fact += str(rule.status)
            count += 1
            if count == len(self.rules):
                self.kq1.append(rule.id + ": " + list_fact + " -> " + rule.regime)
            # self.kq1.append(rule.id)
        for rule in self.kq1:
            true_rule = None
            rule_name = rule.split(":")[0]
            list_count = []
            string = rule.split(":")[1]
            regime_name = string.split("->")[1].strip()
            stringList = string.split("->")[0]
            list = stringList.split('+')
            max_value = 0
            for goal in self.kq3:
                if str(goal) == str(regime_name):
                    count = 0

                    self.kq4.append(f"Mục tiêu {regime_name}. Tìm thấy luật {rule}. Các mục tiêu cần chứng minh là {list}")

                    for fact in list:
                        if fact.strip() in self.kq2:
                            self.kq4.append(
                                f"- Mục tiêu {fact} được tìm thấy . Done")
                            count += 1
                        else:
                            self.kq4.append(
                                f"- Mục tiêu {fact} không được tìm thấy . Failed")

                    if count > int(self.road):
                        self.road = count
                        self.true_rule = goal
                        self.true_id_rule = rule.split(":")[0]
                    # self.kq6.append(count)
                    # self.road = max(list_count)
            # self.road = max_value
            # self.road = max(self.kq6)
            # self.kq6.append(true_rule)

        self.export_results()
        return self.true_rule
    def export_results(self):
        with open(self.output, 'w', encoding='utf-8') as file:
            file.write('-----START-----\n')

            file.write("I. Tập luật suy diễn:\n")
            for item in self.kq1:
                file.write(item + '\n')

            file.write('----------\n')

            file.write("\nII. Tập thể trạng người dùng:\n")
            for item in self.kq2:
                file.write(item + '\n')

            file.write('----------\n')

            file.write("\nIII. Tập mục tiêu:\n")
            for item in self.kq3:
                file.write(item + '\n')

            file.write('----------\n')

            file.write("\nIV. Quá trình suy diễn tiến:\n")
            for item in self.kq4:
                file.write(item + '\n')

            file.write('----------\n')

            file.write("\nV. Tập kết quả:\n")
            file.write(self.true_rule)
            file.write("\n")
            file.write(self.true_id_rule + "\n")
            # for item in self.kq5:
            #     file.write(item + '\n')

            file.write('-----END-----\n')
