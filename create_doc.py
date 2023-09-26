from docx import Document
from docx.shared import Pt, RGBColor, Mm, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
from translations import _


def save_document(dataset, user_id):
    # Create a new Document
    doc = Document()

    # Add Desired Positions
    paragraph = doc.add_paragraph()
    paragraph.add_run('Desired positions: ').bold = True
    paragraph.add_run(f'{dataset["desired_positions"]}.').font.color.rgb = RGBColor(255, 0, 0)
    for run in paragraph.runs:
        run.font.size = Pt(16)

    # Create a list of items
    items = [
        ('Full name:', f'{dataset["full_name"]}'),
        ('Date of birth:', f'{dataset["date_of_birth"]}'),
        ('Place of Birth:', f'{dataset["place_of_birth"]}'),
        ('Marital status:', f'{dataset["married"]}'),
        ('Children:', f'{dataset["have_any_children"]}'),
        ('Heigh (cm):', f'{dataset["height"]}'),
        ('Weight (kg):', f'{dataset["weight"]}'),

    ]

    # Create a table with three columns (two text columns and one image column)
    table = doc.add_table(0, len(items[0]) + 1)  # +1 for the image column
    table.style = 'Table Grid'

    # Set the width of the columns
    col_widths = [Pt(100)] * len(items[0]) + [Mm(50)]  # Adjust the widths as needed
    for i, width in enumerate(col_widths):
        table.columns[i].width = width

    # Fill in the table with data
    for row_data in items:
        row = table.add_row().cells
        for i, item in enumerate(row_data):
            row[i].text = str(item)

    # Add an image to the third column and merge the cells for the image
    from docx.shared import Inches
    cell = table.cell(6, len(items[0]))  # Cell in the third column, third row (0-based index)
    cell.vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER  # Center the image vertically
    p = cell.paragraphs[0]
    run = p.add_run()
    run.add_picture(f'./{dataset["profile_Photo"]}', width=Inches(1.5))  # Adjust the width as needed
    cell.merge(table.cell(0, len(items[0])))  # Merge cells for the image across five rows

    # Set the font size for the entire table
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(14)

    # Autofit the table
    table.autofit = True
    table.columns[0].width = Cm(3)  # Set the width of the first column to 5 cm


    # Create a list of items
    items2 = [
        ('City of residence:', f'{dataset["city_of_residence"]}'),
        ('Current location:', f'{dataset["current_location"]}'),
        ('Nationality:', f'{dataset["nationality"]}'),
        ('Citizenship:', f'{dataset["nationality_country"]}'),
        ('Do you have travel passport?', f'{dataset["haveP_"]}'),
        ('Have you received COVID vaccine?', f'{dataset["covid_access"]}'),
        ('Mobile number:', f'{dataset["phone_Number"]}'),
        ('Messenger: \nWhatsapp/Viber/Telegram', f'{dataset["messenger"]}'),
        ('E-mail addresses:', f'{dataset["email"]}'),
        ('Facebook page:', f'{dataset["Facebook"]}'),
        ('Instagram page:', f'{dataset["instagram"]}'),
        ('Linkedin page', f'{dataset["linkedIn"]}'),
        ('VKontakte page:', f'{dataset["vkontakte"]}'),
    ]
    table2 = doc.add_table(0, len(items2[0]))  # +1 for the image column
    table2.style = 'Table Grid'

    for row_data in items2:
        row = table2.add_row().cells
        for i, item2 in enumerate(row_data):
            row[i].text = str(item2)
    for row in table2.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(14)
    table2.autofit = True
    table2.columns[0].width = Cm(3)  
    table2.columns[1].width = Cm(10) 
    # **************************************************
    doc.add_paragraph()
    relatives = doc.add_paragraph().add_run('Relative’s contact details in case of emergency')
    relatives.font.size = Pt(16)
    relatives.bold = True

    items3 = [
        ('Name:', f'{dataset["name_cousen"]}'),
        ('Relationship:', f'{dataset["relative_cousen"]}'),
        ('Mobile number:', f'{dataset["phone_Number_cousen"]}'),
        ('Father’s name:', f'{dataset["father_name"]}'),
        ('Mother’s name:', f'{dataset["mother_name"]}'),
    ]

    table3 = doc.add_table(0, len(items3[0]))  # +1 for the image column
    table3.style = 'Table Grid'

    col_widths = [Pt(275)] * len(items3[0])  # Adjust the widths as needed
    col_widths2 = [Pt(370)] * len(items3[0])  # Adjust the widths as needed
    for i, width in enumerate(col_widths):
        table3.columns[0].width = width
    for i, width in enumerate(col_widths2):
        table3.columns[1].width = width


    for row_data in items3:
        row = table3.add_row().cells
        for i, item3 in enumerate(row_data):
            row[i].text = str(item3)
    for row in table3.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(14)

    # table3.autofit = True
    table3.columns[0].width = Cm(3)  

    # **************************************************
    # **************************************************
    doc.add_paragraph()
    relatives = doc.add_paragraph().add_run('Preferred countries to relocate and work:')
    relatives.font.size = Pt(16)
    relatives.bold = True

    items4 = [
        (f'{dataset["gatar"]}', f'{dataset["UAE"]}', 
         f'{dataset["Bahrain"]}', f'{dataset["Oman"]}') ]
    
    table4 = doc.add_table(1, len(items4[0]))
    table4.style = 'Table Grid'

    head_cells = table4.rows[0].cells
    for i, item in enumerate(['Qatar', 'UAE', 'Bahrain', 'Oman']):
        p = head_cells[i].paragraphs[0]
        p.add_run(item).bold = True

    for row in items4:
        # добавляем строку с ячейками к объекту таблицы
        cells = table4.add_row().cells
        for i, item4 in enumerate(row):
            # вставляем данные в ячейки
            cells[i].text = str(item4)

    for row in table4.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(14)
    # **************************************************
    # **************************************************
    doc.add_paragraph()
    education = doc.add_paragraph().add_run('Education:')
    education.font.size = Pt(16)
    education.bold = True

    items5 = [
        (f'{dataset["education_stepen"]}', f'{dataset["university_name"]}', f'{dataset["special_degree"]}', f'{dataset["year_of_Education"]}')
        
    ]
    if dataset["postgraduate_access"]=="yes":
        items5 = [
        (f'{dataset["education_stepen"]}', f'{dataset["university_name"]}', f'{dataset["special_degree"]}', f'{dataset["year_of_Education"]}'),
        (f'{dataset["postgraduate_degree"]}', f'{dataset["postgraduate_name"]}', f'{dataset["postgraduate_special"]}', f'{dataset["postgraduate_date"]}')
        ]



    table5 = doc.add_table(1, len(items5[0]))
    table5.style = 'Table Grid'

    head_cells = table5.rows[0].cells
    for i, item in enumerate(['Certificate/Degree', 'College/University', 
                            'Area of Specialization', 'Years started-completed']):
        p = head_cells[i].paragraphs[0]
        p.add_run(item).bold = True

    for row in items5:
        # добавляем строку с ячейками к объекту таблицы
        cells = table5.add_row().cells
        for i, item5 in enumerate(row):
            # вставляем данные в ячейки
            cells[i].text = str(item5)

    for row in table5.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(14)

    # **************************************************
    # **************************************************
    if dataset["course_access"]=="yes":
        doc.add_paragraph()
        course = doc.add_paragraph().add_run('Seminars/training attended/Short Courses taken:')
        course.font.size = Pt(16)
        course.bold = True

        items55 = [
            (f'{dataset["course_date"]}', f'{dataset["сourse_name"]}', f'{dataset["Course_place"]}')
        ]

        table55 = doc.add_table(1, len(items55[0]))
        table55.style = 'Table Grid'

        head_cells = table55.rows[0].cells
        for i, item in enumerate(['Year', 'Name', 'Place']):
            p = head_cells[i].paragraphs[0]
            p.add_run(item).bold = True

        for row in items55:
            # добавляем строку с ячейками к объекту таблицы
            cells = table55.add_row().cells
            for i, item5 in enumerate(row):
                # вставляем данные в ячейки
                cells[i].text = str(item5)

        for row in table55.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(14)

    # **************************************************
    # **************************************************
    doc.add_paragraph()
    education = doc.add_paragraph().add_run('Do you have any tattoos or piercing?')
    education.font.size = Pt(16)
    education.bold = True

    table6 = doc.add_table(1, 2)
    table6.style = 'Table Grid'
    for cell in table6.columns[0].cells:
        cell.width = Cm(5.2)
    for cell in table6.columns[1].cells:
        cell.width = Cm(10) 

    if dataset["tattoo_access"]=="yes":

        items6 = [
            ('discribe_tattoo', f'{dataset["tattoo_discribe"]}')
        ]
    else:
        items6 = [
            ('discribe_tattoo', 'No have tattoo')
        ]
    for i, row_data in enumerate(items6):
        row = table6.rows[i].cells
        for j, item in enumerate(row_data):
            row[j].text = str(item)
            
    for row in table6.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(14)


    # **************************************************
    # **************************************************
    doc.add_paragraph()
    experience = doc.add_paragraph().add_run('Work experience')
    experience.font.size = Pt(16)
    experience.bold = True

    items7 = [
        ('Company’s name, location:', f'{dataset["work_name"]} , {dataset["work_place"]}'),
        ('Position:', f'{dataset["work_position"]}'),
        ('Experience:', f'{dataset["work_exp"]}'),
        ('Responsibilities:', f'{dataset["work_responsibilities"]}'),
    ]
    if dataset["other_work_access"]=="yes" and dataset["now_work_access"]=="yes":
     items7 = [
        ('Company’s name, location:', f'{dataset["work_name"]} , {dataset["work_place"]}'),
        ('Position:', f'{dataset["work_position"]}'),
        ('Experience:', f'{dataset["work_exp"]}'),
        ('Responsibilities:', f'{dataset["work_responsibilities"]}'),

        ('Company’s name, location(Other):', f'{dataset["other_work_name"]} , {dataset["other_work_place"]}'),
            ('Position:', f'{dataset["other_work_position"]}'),
            ('Experience:', f'{dataset["other_work_exp"]}'),
            ('Responsibilities:', f'{dataset["other_work_responsibilities"]}'),

        ('Company’s name, location(Now):', f'{dataset["now_work_name"]} , {dataset["now_work_place"]}'),
            ('Position:', f'{dataset["now_work_position"]}'),
            ('Experience:', f'{dataset["now_work_exp"]}'),
            ('Responsibilities:', f'{dataset["now_work_responsibilities"]}'),
    ]   
    else:
        if dataset["other_work_access"]=="yes":
            items7 = [
                ('Company’s name, location:', f'{dataset["work_name"]} , {dataset["work_place"]}'),
                ('Position:', f'{dataset["work_position"]}'),
                ('Experience:', f'{dataset["work_exp"]}'),
                ('Responsibilities:', f'{dataset["work_responsibilities"]}'),

                ('Company’s name, location(Other):', f'{dataset["other_work_name"]} , {dataset["other_work_place"]}'),
                ('Position:', f'{dataset["other_work_position"]}'),
                ('Experience:', f'{dataset["other_work_exp"]}'),
                ('Responsibilities:', f'{dataset["other_work_responsibilities"]}'),
            ]

        if dataset["now_work_access"]=="yes":
            items7 = [
                ('Company’s name, location:', f'{dataset["work_name"]} , {dataset["work_place"]}'),
                ('Position:', f'{dataset["work_position"]}'),
                ('Experience:', f'{dataset["work_exp"]}'),
                ('Responsibilities:', f'{dataset["work_responsibilities"]}'),

                ('Company’s name, location(Now):', f'{dataset["now_work_name"]} , {dataset["now_work_place"]}'),
                ('Position:', f'{dataset["now_work_position"]}'),
                ('Experience:', f'{dataset["now_work_exp"]}'),
                ('Responsibilities:', f'{dataset["now_work_responsibilities"]}'),
            ]

    table7 = doc.add_table(0, len(items7[0]))
    table7.style = 'Table Grid'

    col_widths = [Pt(170)] * len(items[0])  # Adjust the widths as needed
    col_widths2 = [Pt(370)] * len(items[0])  # Adjust the widths as needed
    for i, width in enumerate(col_widths):
        table7.columns[0].width = width
    for i, width in enumerate(col_widths2):
        table7.columns[1].width = width

    for row_data in items7:
        row = table7.add_row().cells
        for i, item7 in enumerate(row_data):
            row[i].text = str(item7)
            
    for row in table7.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(14)

    # **************************************************
    # **************************************************
    doc.add_paragraph()
    programs  = doc.add_paragraph().add_run('Computer programs you work with:')
    programs .font.size = Pt(16)
    programs .bold = True

    items8 = [
        (f'{dataset["hoste_program"]}', f'{dataset["finance_program"]}', 
        f'{dataset["travel_program"]}', f'{dataset["graph_program"]}')
    ]
    table8 = doc.add_table(1, len(items4[0]))
    table8.style = 'Table Grid'

    head_cells = table8.rows[0].cells
    for i, item in enumerate(['Hospitality programs:', 'Finance programs:',
                            'Travel & booking programs:', 'Graphics & Design programs:']):
        p = head_cells[i].paragraphs[0]
        p.add_run(item).bold = True

    for row in items8:
        # добавляем строку с ячейками к объекту таблицы
        cells = table8.add_row().cells
        for i, item8 in enumerate(row):
            # вставляем данные в ячейки
            cells[i].text = str(item8)

    for row in table8.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(14)

    # **************************************************
    # **************************************************
    doc.add_paragraph()

    table9 = doc.add_table(rows=1, cols=4)
    table9.style = 'Table Grid'


    # Set the font size for the entire table to 14

    # Add data to the table
    if dataset["car_access"]=="yes":
        items9 = ['Driver license:', f'{dataset["car_access"]}', 'Category:', f'{dataset["car_category"]}']
    else:
        items9 = ['Driver license:', f'{dataset["car_access"]}', 'Category:', '']

    for i, cell in enumerate(table9.rows[0].cells):
        cell.text = items9[i]

    # Set the first and third columns to bold
    for i in [0, 2]:
        for paragraph in table9.cell(0, i).paragraphs:
            for run in paragraph.runs:
                run.bold = True

    # Adjust the column widths to approximate a total width of 15 cm
    column_widths = [Cm(3.81), Cm(3.81), Cm(3.81), Cm(3.81)]  # Adjust as needed
    for i, width in enumerate(column_widths):
        table9.columns[i].width = width
    for row in table9.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(14)


    # **************************************************
    # **************************************************
    doc.add_paragraph()
    experience = doc.add_paragraph().add_run('Languages Known:')
    experience.font.size = Pt(16)
    experience.bold = True


    items10 = [
        ('Russian:', f'{dataset["russian"]}'),
        ('English:', f'{dataset["english"]}')
        
    ]

    if dataset["other_lang_access"]=="Yes":
            items10 = [
                    ('Russian:', f'{dataset["russian"]}'),
                    ('English:', f'{dataset["english"]}'),
                    (f'{dataset["added_language"]}:', f'{dataset["other_lang_level"]}')
                    ]

    table10 = doc.add_table(0, len(items10[0]))
    table10.style = 'Table Grid'

    col_widths = [Pt(170)] * len(items[0])  # Adjust the widths as needed
    col_widths2 = [Pt(370)] * len(items[0])  # Adjust the widths as needed
    for i, width in enumerate(col_widths):
        table10.columns[0].width = width
    for i, width in enumerate(col_widths2):
        table10.columns[1].width = width

    for row_data in items10:
        row = table10.add_row().cells
        for i, item10 in enumerate(row_data):
            row[i].text = str(item10)
            
    for row in table10.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(14)

    # **************************************************
    # **************************************************
    # Create a table with two rows and one column
    doc.add_paragraph()
    table11 = doc.add_table(rows=2, cols=1)
    table11.style = 'Table Grid'

    # Add content to the first row (bold, font size 16)
    cell1 = table11.cell(0, 0)
    cell1.text = 'How did you know about us?'
    for paragraph in cell1.paragraphs:
        for run in paragraph.runs:
            run.bold = True
            run.font.size = Pt(16)
            run.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Add content to the second row (not bold, font size 14)
    cell2 = table11.cell(1, 0)
    cell2.text = f'{dataset["know_about_as"]}'
    for paragraph in cell2.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(14)
            run.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # **************************************************
    # **************************************************
    doc.add_paragraph()

    # Создаем параграф и добавляем текст
    dateP = doc.add_paragraph()
    date_run = dateP.add_run('Date: ')
    date_run.bold = True
    date_run.font.size = Pt(14)

    # Добавляем остальной текст
    dateP2 =dateP.add_run(f'{dataset["resume_creating_date"]}') 
    dateP2.font.size = Pt(14)
    dateP2.alignment = WD_ALIGN_PARAGRAPH.RIGHT



    # **************************************************
    # **************************************************
    doc.add_paragraph()

    # Создаем параграф и добавляем текст
    imgP = doc.add_paragraph()
    imgP_run = imgP.add_run('Pictures:')
    imgP_run.bold = True
    imgP_run.font.size = Pt(14)

    os.remove(f'./{dataset["profile_Photo"]}') 

    if dataset["covid_access"] == "Yes":
        doc.add_picture(f'./{dataset["COVID_Photo"]}', height = Mm(100))
        os.remove(f'./{dataset["COVID_Photo"]}') 


    if dataset["course_access"]=="yes":         
        if dataset["doc_course_access"]=="yes":
            doc.add_picture(f'./{dataset["Course_Photo"]}', height = Mm(100))
            os.remove(f'./{dataset["Course_Photo"]}') 

    

    if dataset["tattoo_access"]=="yes":
        doc.add_picture(f'./{dataset["tattoo_Photo"]}', height = Mm(100))
        os.remove(f'./{dataset["tattoo_Photo"]}') 

    
    # table11.columns[0].width = Cm(16)
    # Save the document
    doc.save(f'{dataset["full_name"]}_{user_id}.docx')
    return(_('Ваше резюме успешно отправлено!', dataset['language']))
