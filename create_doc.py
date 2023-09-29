from docx import Document
from docx.shared import Pt, RGBColor, Mm, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from jpg_replace import add_float_picture
import os

def save_document(dataset, user_id):
    doc = Document('new_resume.docx')
    all_tables = doc.tables

    for i, table in enumerate(all_tables):
        cell = table.cell(0,0)
        for j, row in enumerate(table.rows):
            if i == 0 and j == 1 :
                p = cell.paragraphs[0]
                # add_float_picture(p, f'./{dataset["profile_Photo"]}', width=Mm(60))
                add_float_picture(p, f'./userquest.jpg', width=Mm(60))
            for cell in row.cells:

                for word in cell.text.split():
                    if '_test' in word:
                        if word.split('_test')[0] in dataset:
                            cell.text = cell.text.replace(word, dataset[word.split('_test')[0]])
    doc.add_paragraph()

    # Создаем параграф и добавляем текст
    imgP = doc.add_paragraph()
    imgP_run = imgP.add_run('Pictures:')
    imgP_run.bold = True
    imgP_run.font.size = Pt(14)
    imgP_run.font.name = 'Arial'
    # os.remove(f'./{dataset["profile_Photo"]}') 
    # if 'covid_access' in dataset:
    #     doc.add_picture(f'./{dataset["COVID_Photo"]}', height = Mm(100))
    #     os.remove(f'./{dataset["COVID_Photo"]}') 

    # if 'Course_Photo' in dataset:
    #         doc.add_picture(f'./{dataset["Course_Photo"]}', height = Mm(100))
    #         os.remove(f'./{dataset["Course_Photo"]}') 

    # if 'tattoo_Photo' in dataset:
    #     doc.add_picture(f'./{dataset["tattoo_Photo"]}', height = Mm(100))
    #     os.remove(f'./{dataset["tattoo_Photo"]}') 

    doc.save(f'{dataset["full_name"]}_{user_id}.docx')
    doc.save('Check1.docx')


dataset = {'language': 'ru', 'desired_positions': 'info 1', 'full_name': 'info 2', 
           'profile_Photo': 'AgACAgIAAxkBAAIH4WUS2Y224qquSp1gc_rCkve4V7TWAAK90DEbvpqYSK2ETWHD0OT_AQADAgADdwADMAQ.jpg', 
           'date_of_birth': 'info 3', 'place_of_birth': 'info 4', 'married': 'N', 'have_any_children': 'N', 
           'height': 'info 5', 'weight': 'info 6', 'city_of_residence': 'info 7', 'current_location': 'info 8', 
           'nationality': 'info 9', 'nationality_country': 'info 10', 'haveP_': 'N', 'covid_access': 'Yes', 
           'COVID_Photo': 'AgACAgIAAxkBAAIH82US2bLh34iouz1SA48yOjzH9UAWAAK-0DEbvpqYSD_7xjd8eQZRAQADAgADeQADMAQ.jpg', 
           'phone_Number': 'info 11', 'messenger': 'info 12', 'email': 'info 13', 'instagram': 'info 14', 
           'Facebook': 'info 15', 'linkedIn': 'info 16', 'vkontakte': 'info 17', 'name_cousen': 'info 18', 
           'phone_Number_cousen': 'info 19', 'relative_cousen': 'info 20', 'father_name': 'info 21', 
           'mother_name': 'info 22', 'gatar': 'no', 'UAE': 'yes', 'Bahrain': 'no', 'Oman': 'yes', 
           'education_stepen': 'info 23', 'university_name': 'info 24', 'special_degree': 'info 25', 
           'year_of_Education': 'info 26', 'postgraduate_access': 'no', 'course_access': 'yes', 
           'сourse_name': 'info 27', 'course_date': 'info 28', 'Course_place': 'info 29', 
           'doc_course_access': 'yes', 'Course_Photo': 'AgACAgIAAxkBAAIIHWUS2fWSOI0uaQPpq-iSFpW000HSAALe0DEbvpqYSAclBDun5lnAAQADAgADbQADMAQ.jpg', 'tattoo_access': 'no', 'work_exp': 'info 30', 'work_name': 'info 31', 'work_place': 'info 32', 'work_position': 'info 33', 'work_responsibilities': 'info 34', 'other_work_access': 'no', 'now_work_access': 'yes', 'now_work_exp': 'info 35', 'now_work_name': 'info 36', 'now_work_place': 'info 37', 'now_work_position': 'info 38', 'now_work_responsibilities': 'info 39', 'hoste_program': 'info 40', 'finance_program': 'info 41', 'travel_program': 'info 42', 'graph_program': 'info 43', 'car_access': 'no', 'russian': 'Fluent', 'english': 'Upper Intermediate', 'other_lang_access': 'Yes', 'added_language': 'info 44', 'other_lang_level': 'Fluent', 'know_about_as': 'Friends','resume_creating_date':"26 September"}

save_document(dataset, 1231)
