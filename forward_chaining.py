class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.flag1 = False
        self.flag2 =  False

    def follows(self, facts):
        for fact in self.left:
            if fact not in facts:
                return fact
        return None
    def __str__(self):
        return ",".join(self.left) + "->" + self.right
class ForwardChaining:
    def __init__(self, rule, fact, goal, file_name):
        self.iteration  = 0
        self.output = ""
        self.output_file_name = None

        self.output += "Part 1. Dữ liệu (Luật)\n"
        rules = self.read_rule(rule)
        facts = self.read_facts(fact)
        self.print_data(rules, facts, goal)

        self.output += "Part 2. Suy dien\n"
        self.result, self.road, self.facts = self.forward_chaining(rules,facts, goal)

        self.output += "Part 3. Kết quả\n"
        self.print_results(self.result, self.road, goal, self.facts)

        self.write_output(file_name)

    def forward_chaining(self, rules, facts, goal):
        ir = len(facts)
        iteration = 0
        road = []

        while 1:
            rule_applied = False
            iteration += 1
            self.output += "%i".rjust(4, " ") % iteration + " INTERATION\n"

            for rule in rules:
                self.output += "    R%i:%s " % ((rules.index(rule) + 1), str(rule))

                if rule.flag1:
                    self.output += "bỏ qua , vì flag1 đã được cập nhập.\n"
                    continue
                if rule.flag2:
                    self.output += "bỏ qua , vì flag2 đã được cập nhật.\n"
                    continue
                if rule.right in facts:
                    self.output += "không áp dụng , vì %s nằm trong số các facts. Cập nhật flags. \n"
                    rule.flag2 = True
                    continue
                missing = rule.follows(facts)
                if missing in None:
                    rule_applied = True
                    rule.flag1 = True
                    facts.append(rule.right)
                    road.append("R" + str(rules.index(rule) + 1))
                    self.output += "được áp dụng . Cập nhật flag1. Facts %s suy ra %s. \n" % (
                        ", ".join(facts[:ir]), ", ".join(facts[ir:])
                    )
                    break
                else:
                    self.output += "Không được áp dụng, vì thiếu fact: %s\n" % missing
            self.output += "\n"

            if not rule_applied:
                return False, road, facts
        return True, road, facts
    def read_rule(self, rule):
        new_rule = []
        for i in rule:
            right = i[0]
            left = i[1:]
            new_rule.append(Rule(left,right))
        return new_rule
    def read_facts(self,line):
        ad = []
        for i in line:
            ad.append(i)
        return ad
    def print_data(self, rules, facts, goal):
        self.output += "  1) Productions\n"
        for rule in rules:
            self.output += "    R%i: %s\n" % (rules.index(rule) + 1, str(rule))
        self.output += "\n  2) Facts %s.\n" % ", ".join(facts)
        # self.output += "\n  2) Facts %s.\n" % ", ".join(map(str, facts))

        self.output += "\n  3) Goal %s\n\n" % goal

    def print_results(self, result, road, goal, facts):

        if result:
            if len(road) == 0:
                self.output += "  1) Kết quả là : %s .\n" % ", ".join(facts)
                self.output += "  2) Empty road.\n"
            else:
                self.output += "  1) Kết quả là : %s .\n" % ", ".join(facts)
                self.output += "  2) Road: %s.\n" % ", ".join(road)
        else:
            self.output += "  1) Kết quả là : %s .\n" % ", ".join(facts)
            self.output += "  2) Đường đi suy diễn được là:%s" % ", ".join(road)  # new

    def write_output(self, file_name):
        self.output_file_name = "FC_OUTPUT_%s.txt" % file_name.replace("/", ".")
        file = open(self.output_file_name, "w", encoding='utf8')
        file.write(self.output)