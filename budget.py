class Category:
    
    def __init__(self, name_category):
        self.name_category = name_category
        self.total = 0.0
        self.ledger = []
        self.total_withdraw = 0.0

    def __repr__(self):
        text_object = ('*')*int(((30 - len(self.name_category))/2)) + self.name_category + ('*')*int(((30 - len(self.name_category))/2)) + '\n'

        for x in self.ledger:
            spaces = 30 - (len(x['description'][:23]) + len("%.2f"%x['amount']))
            text_object += x['description'][:23] +spaces*' '+ ("%.2f"%x['amount']) + '\n'

        return text_object + "Total: "+ ("%.2f"%self.total)

    def deposit(self, amount, description = ''):
        self.total += amount
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description = ''):
        
        if self.check_funds(amount):
            self.total -= amount
            self.total_withdraw += amount
            self.ledger.append({"amount": -amount, "description": description})
            
        return self.check_funds(amount)

    def get_balance(self):
        return self.total

    def transfer(self, amount, instance):
        if self.check_funds(amount):
            self.withdraw(amount, 'Transfer to '+instance.name_category)
            instance.deposit(amount, 'Transfer from '+self.name_category)
        return self.check_funds(amount)

    def check_funds(self, amount):
        if amount > self.total:
            return False
        return True

def create_spend_chart(categories):
    sum_withdraws = 0.0
    text_to_show = "Percentage spent by category\n"
    aux_percent = []
    aux_len_caracteres = 0
    aux_text = "   "

    for cat in categories:
        sum_withdraws += cat.total_withdraw
        if len(cat.name_category) > aux_len_caracteres:
            aux_len_caracteres = len(cat.name_category)

    for cat in categories:
        aux_percent.append(
            int(((cat.total_withdraw / sum_withdraws) * 100 // 10)) * 10)

    #print(aux_percent)

    #draw chart
    for x in range(100, -1, -10):
        if len(str(x)) == 3:
            text_to_show += str(x) + "|"
        if len(str(x)) == 2:
            text_to_show += " " + str(x) + "|"
        if len(str(x)) == 1:
            text_to_show += "  " + str(x) + "|"
        for n in aux_percent:
            text_to_show += " o " if x == n or x < n else "   "

        text_to_show += " \n"
    text_to_show += "    " + (len(categories) * 3 + 1) * "-" + "\n"

    #columns categories
    for i in range(aux_len_caracteres):
        for column in categories:
            if i < len(column.name_category):
                aux_text += "  " + column.name_category[i]
            else:
                aux_text += "   "
        aux_text += "  \n   "

    text_to_show += aux_text[:-5]+" "

    return text_to_show