from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from competitions.models import Competition, Entrie
import io 
import xlsxwriter
from django.http import HttpResponse


@staff_member_required
def staff_portal(request):
    competions = Competition.objects.filter(state="awaiting")
    context = {"competions": competions}
    return render(request, "staff/staffportal.html", context=context)

@staff_member_required
def get_comp_excel(request, competition_id):
    comp = Competition.objects.filter(pk=competition_id)
    if comp.exists():
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        row = 0
        for entry in comp[0].entries.all():
            if entry.valid_entry:
                for i in range(entry.number_of_tickets_purchased):
                    worksheet.write(row, 0, row + 1 )
                    worksheet.write(row, 1, entry.user.email)
                    row += 1

        worksheet.write(row, 0, "End of file")
        workbook.close()

        # create a response
        response = HttpResponse(content_type='application/vnd.ms-excel')

        # tell the browser what the file is named
        response['Content-Disposition'] = 'attachment;filename="'+ competition_id + '.xlsx"'

        # put the spreadsheet data into the response
        response.write(output.getvalue())

        # return the response
        return response
