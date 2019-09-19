# since only exam results are published, I'm can actually calculate an approximation of overall averages.

import PyPDF2

all_pdfs = ['/Users/michalina/Downloads/exam_results/ECO00001I Marks 2017-18.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00002I Marks 2017-18.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00003I Marks 2017-18.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00004I Marks 2017-18.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00006I Marks 2017-18.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00008I Introduction to Accountancy Marks 1718.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00009I Cost Benefit Analysis Marks 1718.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00012I Dynamic Modelling for Economists Marks 1718.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00015I Marks 2017-18.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00016I Marks 2017-18.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00017I Marks 2017-18.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00019I Econometric Theory 1 Marks 1718.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00021I Marks 2017-18.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00024I Marks 2017-18.pdf',
            '/Users/michalina/Downloads/exam_results/ECO00027I Marks 2017-18.pdf']

second_year_modules_weights = {'ECO00001I': 20, 'ECO00002I': 20, 'ECO00003I': 20, 'ECO00004I': 20, 'ECO00008I': 10,
                               'ECO00019I': 10, 'ECO00021I': 10, 'ECO00024I': 20, 'ECO00027I': 10, 'ECO00012I': 10,
                               'ECO00015I': 10, 'ECO00009I': 10, 'ECO00017I': 10, 'ECO00006I': 20, 'ECO00016I': 10}


def read_pdf(file_path):
    """
    takes a path to a PDF file as input and returns a list of strings
    with all the text from this PDF split by newline
    """
    result = ''
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pages_number = pdf_reader.numPages
        for page in range(pages_number):
            single_page = pdf_reader.getPage(page)
            result = result + single_page.extractText()
    return result.splitlines()


def get_module_name(split_string):
    # make sure to consider the case when it would return None (name not found)
    """
    loops though a split list of strings to find the module name and returns it
    """
    for i in split_string:
        if "ECO" in i:
            name_line = i.split()
            if len(name_line) > 1:
                return name_line[-1]
            else:
                return name_line[0]


def get_next_student(split_string):
    """
    returns student ID and corresponding grade
    """
    for i in split_string:
        if i[0] == "Y" and len(i) == 8:
            grade_location = split_string.index(i) + 1
            return i, split_string[grade_location], grade_location


def should_we_include(grade):
    """
    checks whether output of get_next_student, particularly grade is ok and can be
    included in the all_grades dictionary. People with grade 0 are NOT included,
    as uni also does not count them when calculating percentiles
    """
    for char in grade:
        if not char.isdigit():
            return False
    if grade == "0":
        return False
    return True


def get_from_one_pdf(split_string, grades_dictionary):
    """
    deals with all students in one pdf and adds their grades to all_grades
    grades are stored in a dictionary with student IDs as keys and lists of tuples as values,
    each tuple will contain module grade and module name
    """
    module_name = get_module_name(split_string)
    while True:
        try:
            student_id, grade, end = get_next_student(split_string)
            split_string = split_string[end:]
            if should_we_include(grade):
                if student_id not in grades_dictionary:
                    grades_dictionary[student_id] = [(grade, module_name)]
                else:
                    grades_dictionary[student_id].append((grade, module_name))
            else:
                continue
        except TypeError:
            print("PDF has been read")
            return grades_dictionary


def get_all_grades(list_of_pdfs):
    all_grades = {}
    for pdf in list_of_pdfs:
        pdf_string = read_pdf(pdf)
        all_grades = get_from_one_pdf(pdf_string, all_grades)
    return all_grades


def check_weights_sum(all_grades, student, modules_weights):
    weights_sum = 0
    for module in all_grades[student]:
        weights_sum += modules_weights[module[1]]
    if weights_sum == 120:
        return True
    else:
        return False


def calculate_averages(all_grades, modules_weights):
    all_averages = []
    wrong_weights = []
    for student in all_grades:
        if check_weights_sum(all_grades, student, modules_weights):
            modules_sum = 0
            for module in all_grades[student]:
                modules_sum += (int(module[0]) * modules_weights[module[1]])
            average = modules_sum / 120
            all_averages.append(("%.2f" % average, student))
        else:
            wrong_weights.append(student)
    # it might have been that student got 0 from some subjects or does a joint degree
    print("Weights don't add up to 120 for students {}.".format(wrong_weights))
    print("Average has been calculated for {} students.".format(len(all_averages)))
    return all_averages


def gruta_grades(list_of_pdfs, list_of_weights):
    all_grades = get_all_grades(list_of_pdfs)
    all_averages = calculate_averages(all_grades, list_of_weights)
    sorted_averages = sorted(all_averages, reverse=True)
    for student in sorted_averages:
        print(student)


gruta_grades(all_pdfs, second_year_modules_weights)