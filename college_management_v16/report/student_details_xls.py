from odoo import models
import base64
import io

class StudentdetailsXLS(models.AbstractModel):
    _name = 'report.college_management.report_student_detail_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Student Details')
        format1 = workbook.add_format({'font_size':12, 'align':'center','bold': True})
        format2 = workbook.add_format({'font_size':12,'align':'center'})
        format3 = workbook.add_format({'bold':True,'align':'center','bg_color':'yellow'})

        print("\n\n\nLines",lines)
        row = 3
        col = 3
        sheet.set_column('D:D',12)

        for student in lines:  
            row += 1    
            sheet.merge_range(row,col,row,col + 1,'ID CARD',format3)

            row += 1   
            if student.image:
                student_image = io.BytesIO(base64.b64decode(student.image)) 
                sheet.insert_image(row, col, "image.png", {'image_data': student_image, 'x_scale': 0.05, 'y_scale': 0.05})


                row += 6

            
            sheet.write(row,col,'Name',format1)
            sheet.write(row,col + 1,student.name,format2)
            row += 1
            sheet.write(row,col,'Age',format1)
            sheet.write(row,col + 1,student.age,format2)
            row += 1
            sheet.write(row,col,'Gender',format1)
            sheet.write(row,col + 1,student.gender,format2)

            row += 2