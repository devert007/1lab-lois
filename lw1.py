"////////////////////////////////////////////////////////"
"// Лабораторная работа 1 по дисциплине ЛОИС //"
"// Выполнена студентами группы 321702 БГУИР Кислицын И.А., Олихвер В., Пучинская П.В.//"
"// Реализация прямого нечеткого логического вывода с использованием треугольной нормы произведения и нечеткой импликации Гогена//"
"// 15.10.2025 //"
"// Использованные источники: Голенков, В. В. Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие / В. В. Голенков. — БГУИР, 2011//"


import sys
class Fact:
    def __init__(self, name="", fuzzy_set=None):
        self.name = name
        self.fuzzy_set = fuzzy_set if fuzzy_set is not None else []

class Rule:
    def __init__(self, name1="", name2=""):
        self.name1 = name1
        self.name2 = name2

def is_valid_name(name):
    if not name:
        return False
    first_char = name[0]
    if not (('a' <= first_char <= 'z') or ('A' <= first_char <= 'Z')):
        return False
    
    for char in name[1:]:
        if not (('a' <= char <= 'z') or ('A' <= char <= 'Z') or ('0' <= char <= '9')):
            return False
    
    return True

def is_valid_fuzzy_value(value_str):
    try:
        value = float(value_str)
        return 0.0 <= value <= 1.0
    except ValueError:
        return False

def read_facts_and_rules(filename):
    facts = []
    rules = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден!")
        sys.exit(1)
    
    # Разделяем на две части по пустой строке
    parts = content.split('\n\n', 1)  # Разделяем по первой пустой строке
    
    if len(parts) == 1:
        # Если нет пустой строки, все считаем фактами
        fact_lines = [line.strip() for line in parts[0].split('\n') if line.strip()]
        rule_lines = []
        print("Ошибка: Правила не найдены или записаны не через пустую строку")
        sys.exit(1)
        
    else:
        fact_lines = [line.strip() for line in parts[0].split('\n') if line.strip()]
        rule_lines = [line.strip() for line in parts[1].split('\n') if line.strip()]
    
        
    if fact_lines==[]:
        print("Ошибка: Факты не найдены ")
        sys.exit(1)
        
    if rule_lines==[]:
        print("Ошибка: Правила не найдены или записаны не через пустую строку")
        sys.exit(1)
        
    for line in fact_lines:
        fact = parse_fact(line)
        if fact:
            facts.append(fact)
    
    for line in rule_lines:
        rule = parse_rule(line, facts)
        if rule:
            rules.append(rule)
    
    return facts, rules

def parse_fact(line):
    if '=' not in line:
        print(f"Ошибка: Отсутствует знак '=' в факте: '{line}'")
        sys.exit(1)
    
    if '{' not in line or '}' not in line:
        print(f"Ошибка: Отсутствуют фигурные скобки в факте: '{line}'")
        sys.exit(1)
    
    name_part = line.split('=')[0].strip()
    
    # Проверка имени факта
    if not is_valid_name(name_part):
        print(f"Ошибка: Некорректное имя факта '{name_part}'. Допустимы только латинские буквы и цифры, начинаться должно с буквы.")
        sys.exit(1)
    
    start = line.find('{') + 1
    end = line.find('}')
    
    if start >= end:
        print(f"Ошибка: Пустой или некорректный набор элементов в факте: '{line}'")
        sys.exit(1)
        
    content = line[start:end].strip()
    fuzzy_set = []
    
    # Проверка на пустой факт
    if not content.strip():
        print(f"Ошибка: Факт '{name_part}' не содержит элементов")
        sys.exit(1)
    
    i = 0
    while i < len(content):
        if content[i] == '<':
            end_pos = content.find('>', i)
            if end_pos == -1:
                print(f"Ошибка: Незакрытый кортеж в факте '{name_part}': '{content[i:]}'")
                sys.exit(1)
            
            element = content[i+1:end_pos].strip()
            
            # Проверка на пустой кортеж
            if not element:
                print(f"Ошибка: Пустой кортеж в факте '{name_part}'")
                sys.exit(1)
            
            # Разделяем на части по запятой
            comma_pos = element.find(',')
            if comma_pos == -1:
                print(f"Ошибка: Кортеж должен содержать запятую в факте '{name_part}': '{element}'")
                sys.exit(1)
            
            elem_name = element[:comma_pos].strip()
            value_str = element[comma_pos+1:].strip()
            
            # Проверка имени элемента
            if not is_valid_name(elem_name):
                print(f"Ошибка: Некорректное имя элемента '{elem_name}' в факте '{name_part}'. Допустимы только латинские буквы и цифры, начинаться должно с буквы.")
                sys.exit(1)
            
            # Проверка значения принадлежности
            if not is_valid_fuzzy_value(value_str):
                print(f"Ошибка: Некорректное значение принадлежности '{value_str}' в факте '{name_part}'. Должно быть действительным числом от 0 до 1.")
                sys.exit(1)
            
            try:
                value = float(value_str)
                fuzzy_set.append((elem_name, value))
            except ValueError:
                print(f"Ошибка: Невозможно преобразовать значение '{value_str}' в число в факте '{name_part}'")
                sys.exit(1)
            
            i = end_pos + 1
        else:
            # Проверка на посторонние символы (кроме пробелов, табуляций и запятых)
            if content[i] not in [' ', '\t', ',']:
                print(f"Ошибка: Посторонний символ '{content[i]}' в определении факта '{name_part}'")
                sys.exit(1)
            i += 1
    
  
    if not fuzzy_set:
        print(f"Ошибка: Факт '{name_part}' не содержит корректных элементов")
        sys.exit(1)
    
    return Fact(name_part, fuzzy_set)

def parse_rule(line, facts_list):
    if '~>' not in line:
        print(f"Ошибка: Правило записано некорректно, нечеткая импликация '~>' не найдена: '{line}'")
        return None
    
    parts = line.split('~>')
    if len(parts) != 2:
        print(f"Ошибка: Правило записано некорректно: '{line}'")
        return None
    
    name1 = parts[0].strip()
    name2 = parts[1].strip()
    
    if not is_valid_name(name1):
        print(f"Ошибка: Некорректное имя факта '{name1}' в правиле. Допустимы только латинские буквы и цифры, начинаться должно с буквы.")
        sys.exit(1)
    
    if not is_valid_name(name2):
        print(f"Ошибка: Некорректное имя факта '{name2}' в правиле. Допустимы только латинские буквы и цифры, начинаться должно с буквы.")
        sys.exit(1)
    
    # Проверка существования фактов, упомянутых в правиле
    fact1_exists = False
    fact2_exists = False
    for fact in facts_list:
        if fact.name == name1:
            fact1_exists = True
        if fact.name == name2:
            fact2_exists = True
    
    if not fact1_exists:
        print(f"Ошибка: Факт '{name1}', упомянутый в правиле, не определен: '{line}'")
        sys.exit(1)
    
    if not fact2_exists:
        print(f"Ошибка: Факт '{name2}', упомянутый в правиле, не определен: '{line}'")
        sys.exit(1)
    
    return Rule(name1, name2)

def can_apply_fact_to_rule(fact, rule, facts_list):
    
    first_fact_of_rule = None
    for f in facts_list:
        if f.name == rule.name1:
            first_fact_of_rule = f
            break
    
    # Если не нашли первый факт правила - нельзя применить правило
    if first_fact_of_rule is None:
        return False
    
    if len(fact.fuzzy_set) != len(first_fact_of_rule.fuzzy_set):
        return False
    
    for i in range(len(fact.fuzzy_set)):
        if fact.fuzzy_set[i][0] != first_fact_of_rule.fuzzy_set[i][0]:
            return False
    
    return True


class Implication:
    def __init__(self, rule_name, matrix, row_labels, col_labels):
        self.rule_name = rule_name
        self.matrix = matrix  
        self.row_labels = row_labels  
        self.col_labels = col_labels  

def calculate_implication(rule, facts_list):
    #Вычисляет матрицу импликации для правила
    first_fact = None
    second_fact = None
    
    for fact in facts_list:
        if fact.name == rule.name1:
            first_fact = fact
        if fact.name == rule.name2:
            second_fact = fact
    
    if first_fact is None or second_fact is None:
        return Implication(f"{rule.name1}->{rule.name2}", [], [], [])
    
    col_labels = [elem for elem in first_fact.fuzzy_set]
    row_labels = [elem for elem in second_fact.fuzzy_set]
    matrix = []
  
    for row_elem in second_fact.fuzzy_set:
        row_name, y_value = row_elem
        row = []
      
        for col_elem in first_fact.fuzzy_set:
            col_name, x_value = col_elem
            
        
            if x_value <= y_value:
                value = 1.0
            else:
                value = y_value/x_value if x_value != 0 else float('inf')
            
            if value>1.0:
                value=1.0
                
            row.append(value)
                 
        matrix.append(row)
    
    rule_name = f"{rule.name1}~>{rule.name2}"
    
    return Implication(rule_name, matrix, row_labels, col_labels)

def calculate_all_implications(rules, facts):
   
    implications = []
    
    for rule in rules:
        implication = calculate_implication(rule, facts)
        implications.append(implication)
    
    return implications

def print_implication(implication):
    print(f"\nИмпликация: {implication.rule_name}")
    
    if not implication.matrix:
        print("Пустая матрица нечеткой импликации, факт/ы для построения не были найдены")
        return
    

    print("     ", end="")
    for col_label in implication.col_labels:
        elem_name, value = col_label
        print(f"<{elem_name},{value}>".ljust(12), end="")
    print()
    
    for i, row_label in enumerate(implication.row_labels):
        elem_name, value = row_label
        print(f"<{elem_name},{value}>: ", end="")
        for value in implication.matrix[i]:
            print(f"{value:8.2f}", end="")
        print()

def apply_goguen_t_norm(fact, implication):
    result = []
 
    if not implication.matrix or len(fact.fuzzy_set) != len(implication.col_labels):
        return result
    
    fact_dict = {elem[0]: elem[1] for elem in fact.fuzzy_set}
    
    for row_index in range(len(implication.matrix)):
        row_values = []
        
        for col_index in range(len(implication.matrix[0])):
            
            col_label = implication.col_labels[col_index] 
            fact_value = fact_dict.get(col_label[0])
            implication_value = implication.matrix[row_index][col_index]
            t_norm_value = fact_value * implication_value
            
            row_values.append(t_norm_value)
        max_value = max(row_values) if row_values else 0.0
        row_label = implication.row_labels[row_index]
        result.append((row_label[0], max_value))
    
    return result


def fuzzy_set_equal_exact(res, facts_list):
    res_set = set((elem, float(val)) for elem, val in res)
    equal_fact = ''
    
    for  fact in facts_list:
        fact_set = set((elem, float(val)) for elem, val in fact.fuzzy_set)
        if res_set == fact_set:
            return True, fact.name
            
    
    return False, 0

def format_res(fuzzy_set):
    
    
    elements = []
    for elem_name, value in fuzzy_set:
        elements.append(f"<{elem_name}, {value}>")
    
    return "{" + ", ".join(elements) + "}"

if __name__ == "__main__":
    try:
        facts, rules = read_facts_and_rules(input("Enter file name: "))
        
        # Вычисляем все импликации
        implications = calculate_all_implications(rules, facts)
      
        for implication in implications:
            print_implication(implication)
            
        new_facts_calc = 0
        
        for fact in facts:
            for j, rule in enumerate(rules):
                if can_apply_fact_to_rule(fact, rule, facts):
                    res = apply_goguen_t_norm(fact, implications[j])
                    flag, index = fuzzy_set_equal_exact(res, facts)
                    new_facts_calc += 1
                    if flag:
                        print("{",fact.name,",",implications[j].rule_name,"}"," |~ ","I",new_facts_calc, "=",format_res(res), "=", index)
                    else:
                        facts.append(Fact("I"+str(new_facts_calc), res))
                        print("{",fact.name,",",implications[j].rule_name,"}"," |~ ","I",new_facts_calc, "=",format_res(res))
                        
    except SystemExit:
        pass
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)