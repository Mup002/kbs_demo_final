class Rule:
    def __init__(self, id, status, regime):
        self.id = id
        self.status = status
        self.regime = regime

    def __repr__(self):
        return f"Rule({self.id}, {self.status}, {self.regime})"


class Inference:
    def __init__(self, rules, facts, file_name):
        self.rules = rules
        self.facts = facts
        self.inferences = []
        self.output = file_name
        self.kq1 = []
        self.kq2 = []
        self.kq3 = []
        self.kq4 = []


    def infer(self):
        # kq1 = []
        # kq2 = []
        # kq3 = []
        # kq4 = []
        for fact in self.facts:
            self.kq2.append(fact)
        for rule in self.rules:
            self.kq1.append(rule.id + ": IF " + rule.status + " THEN " + rule.regime )
        for rule in self.rules:
            for fact in self.facts:
                if fact == rule.status:
                    if rule.regime not in self.kq4:
                        self.kq4.append(rule.regime)
                        self.kq3.append(f"{rule.id} : {rule.status} -> {rule.regime} Được áp dụng")
                    else:
                        self.kq3.append(
                            f"{rule.id} : {rule.status} -> {rule.regime}  Không được áp dụng, vì đã nằm trong fact đã được cập nhật")
                else:
                    self.kq3.append(f"{rule.id} : {rule.status} -> {rule.regime}  Không được áp dụng, vì thiếu fact : {fact}")
        self.export_results()
        return self.kq4

    def export_results(self):
        with open(self.output, 'w', encoding='utf-8') as file:
            file.write('-----START-----\n')

            file.write("I. Tập luật suy diễn (rules):\n")
            for item in self.kq1:
                file.write(item + '\n')

            file.write('----------\n')

            file.write("\nII. Tập thể trạng người dùng (facts):\n")
            for item in self.kq2:
                file.write(item + '\n')

            file.write('----------\n')

            file.write("\nIII. Quá trình suy diễn tiến:\n")
            for item in self.kq3:
                file.write(item + '\n')

            file.write('----------\n')

            file.write("\nIV. Tập kết quả:\n")
            for item in self.kq4:
                file.write(item + '\n')

            file.write('-----END-----\n')

