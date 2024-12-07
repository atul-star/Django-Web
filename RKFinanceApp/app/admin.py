from django.contrib import admin

# Register your models here.
from .models import Contact, Feedback, Cement, Oil, Withdraw
from django.urls import path
from django.http import HttpResponse
from django.utils.html import format_html
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Client, Transaction
# from django.contrib import admin

# Customize site header and title
admin.site.site_header = 'आर के इंटरप्राईज'
admin.site.site_title = 'आर के इंटरप्राईज'

# admin.site.register(Contact)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.fields]  # Display all fields
    list_filter = ['id','name', 'email','mobile']  # Add filtering options for field1 and field2
    search_fields = ['name']  # Enable searching within field1 and field2
    ordering = ('id',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Feedback._meta.fields]  # Display all fields
    list_filter = ['id','name', 'email','mobile','is_satisfy','feedback','created_at']  # Add filtering options for field1 and field2
    search_fields = ['name']  # Enable searching within field1 and field2
    ordering = ('id',)



# @admin.register(Cement)
# class CementAdmin(admin.ModelAdmin):
#
#     list_display = [field.name for field in Cement._meta.fields]  # Display all fields
#     list_filter = ['id','name', 'email','mobile','quantity']  # Add filtering options for field1 and field2
#     search_fields = ['name']  # Enable searching within field1 and field2
#     ordering = ('id',)
#
#
# def get_queryset(self, request):
#         qs = super(CementAdmin, self).get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(user=request.user)


from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib import messages

def generate_pdf_for_cement(oil):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Styles for heading and table
    styles = getSampleStyleSheet()
    heading_style = ParagraphStyle(
        'Heading1',
        parent=styles['Title'],
        fontSize=18,
        alignment=1,  # Centered
        spaceAfter=12
    )
    normal_style = styles['Normal']
    # Heading
    heading = Paragraph(" R K ENTERPRISE  Cement Order Report", heading_style)

    # Define data for the table
    data = [
        ["Field", "Value"],
        ["Order ID", str(oil.id)],
        ["Person Name", oil.name],
        ["Person Mobile number", oil.mobile],
        ["Personal EmailID",oil.email],
        # ["Oil Type", str(oil.name)],
        ["Cement Quantity(bags)", str(oil.quantity)],
        # Add more fields as needed
    ]

    # Create table with data
    table = Table(data, colWidths=[2 * inch, 4 * inch])  # Adjust column widths if needed

    # Define table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ])

    table.setStyle(style)
    large_spacer = Paragraph("<br/><br/><br/><br/><br/><br/><br/><br/>", normal_style)
    # Signature text
    client_signature = Paragraph("Client Signature:", normal_style)
    authority = Paragraph("Authority:", normal_style)

    # Create a table for signatures with proper alignment
    signatures_data = [
        [client_signature, authority]
    ]
    signatures_table = Table(signatures_data, colWidths=[3 * inch, 3 * inch])
    signatures_style = TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ])
    signatures_table.setStyle(signatures_style)
    # Create spacers for spacing between table, signature, and authority sections
    space_after_table = Spacer(1, 0.5 * inch)  # Adjust the height as needed for spacing
    space_between_signatures = Spacer(1, 0.75 * inch)  # Adjust the height as needed for spacing

    # Build the PDF
    elements = [heading, table,space_after_table,large_spacer,signatures_table,space_between_signatures]
    doc.build(elements)

    buffer.seek(0)
    return buffer

class CementAdmin(admin.ModelAdmin):

    def response_add(self, request, obj, post_url_continue=None):
        # response = super().response_add(request, obj, post_url_continue)
        # # Add a success message after the object is added
        # messages.success(request, "Order Placed Successfully")
        # return  response

        response = super().response_add(request, obj, post_url_continue)
        # Add a success message after the object is added
        messages.success(request, "Order Placed Successfully")

        # Generate PDF
        pdf_buffer = generate_pdf_for_cement(obj)

        # Email details
        subject = 'R K ENTERPRISE New Cement Order Report'
        message = 'A new Cement order has been placed. Please find the report attached.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.ADMIN_EMAIL]  # Ensure you set this in your settings.py


        # Create email
        email = EmailMessage(
            subject,
            message,
            from_email,
            recipient_list
        )
        email.attach('cement_order_report.pdf', pdf_buffer.getvalue(), 'application/pdf')
        email.send()

        return response

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Allow only superusers and users in 'My User' group to add Cement instances
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='My Users').exists():
            return qs.none()  # No access to view or change instances
        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='My Users').exists():
            return False
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='My Users').exists():
            return False
        return super().has_view_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:  # New object
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Cement, CementAdmin)





# class OilAdmin(admin.ModelAdmin):
#
#     def response_add(self, request, obj, post_url_continue=None):
#         response = super().response_add(request, obj, post_url_continue)
#         # Add a success message after the object is added
#         messages.success(request, "Order Placed Successfully")
#         return  response
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         # Allow only superusers and users in 'My User' group to add Cement instances
#         if request.user.is_superuser:
#             return qs
#         if request.user.groups.filter(name='My Users').exists():
#             return qs.none()  # No access to view or change instances
#         return qs
#
#     def has_change_permission(self, request, obj=None):
#         if request.user.is_superuser:
#             return True
#         if request.user.groups.filter(name='My Users').exists():
#             return False
#         return super().has_change_permission(request, obj)
#
#     def has_view_permission(self, request, obj=None):
#         if request.user.is_superuser:
#             return True
#         if request.user.groups.filter(name='My Users').exists():
#             return False
#         return super().has_view_permission(request, obj)
#
#     def has_delete_permission(self, request, obj=None):
#         return self.has_change_permission(request, obj)
#
#     def save_model(self, request, obj, form, change):
#         if not change:  # New object
#             obj.user = request.user
#         super().save_model(request, obj, form, change)
#
#
# admin.site.register(Oil, OilAdmin)


# utils.py

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# def generate_pdf(oil):
#     buffer = BytesIO()
#     c = canvas.Canvas(buffer, pagesize=letter)
#     width, height = letter
#
#     # Write some text
#     c.drawString(100, height - 100, f"Oil Order Report")
#     c.drawString(100, height - 120, f"Order ID: {oil.id}")
#     c.drawString(100, height - 140, f"Oil Name: {oil.name}")
#     c.drawString(100, height - 160, f"Quantity: {oil.quantity}")
#     # Add more data as needed
#
#     c.showPage()
#     c.save()
#
#     buffer.seek(0)
#     return buffer


# utils.py

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch



def generate_pdf_for_oil(oil):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Styles for heading and table
    styles = getSampleStyleSheet()
    heading_style = ParagraphStyle(
        'Heading1',
        parent=styles['Title'],
        fontSize=18,
        alignment=1,  # Centered
        spaceAfter=12
    )
    normal_style = styles['Normal']


    # Heading
    heading = Paragraph("R K ENTERPRISE Oil Order Report", heading_style)

    # Define data for the table
    data = [
        ["Field", "Value"],
        ["Order ID", str(oil.id)],
        ["Person Name", oil.name],
        ["Person Mobile number", oil.mobile],
        ["Personal EmailID", oil.email],
        ["Oil Type", str(oil.fuel_type)],
        ["Oil Quantity(ltrs)", str(oil.quantity)],
        # Add more fields as needed
    ]

    # Create table with data
    table = Table(data, colWidths=[2 * inch, 4 * inch])  # Adjust column widths if needed

    # Define table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ])

    table.setStyle(style)
    table.setStyle(style)
    large_spacer = Paragraph("<br/><br/><br/><br/><br/><br/><br/><br/>", normal_style)
    # Signature text
    client_signature = Paragraph("Client Signature:", normal_style)
    authority = Paragraph("Authority:", normal_style)

    # Create a table for signatures with proper alignment
    signatures_data = [
        [client_signature, authority]
    ]
    signatures_table = Table(signatures_data, colWidths=[3 * inch, 3 * inch])
    signatures_style = TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ])
    signatures_table.setStyle(signatures_style)
    # Create spacers for spacing between table, signature, and authority sections
    space_after_table = Spacer(1, 0.5 * inch)  # Adjust the height as needed for spacing
    space_between_signatures = Spacer(1, 0.75 * inch)  # Adjust the height as needed for spacing

    # Build the PDF
    elements = [heading, table, space_after_table, large_spacer, signatures_table, space_between_signatures]
    doc.build(elements)

    buffer.seek(0)
    return buffer


from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import admin, messages
# from .models import Oil
# from .utils import generate_pdf


class OilAdmin(admin.ModelAdmin):

    def response_add(self, request, obj, post_url_continue=None):
        response = super().response_add(request, obj, post_url_continue)
        # Add a success message after the object is added
        messages.success(request, "Order Placed Successfully")

        # Generate PDF
        pdf_buffer = generate_pdf_for_oil(obj)

        # Email details
        subject = 'R K ENTERPRISE  New Oil Order Report'
        message = 'A new oil order has been placed. Please find the report attached.'
        from_email = settings.DEFAULT_FROM_EMAIL

        recipient_list = [settings.ADMIN_EMAIL]  # Ensure you set this in your settings.py
        # recipient_list = ["jadhavatul1610@gmail.com"]  # Ensure you set this in your settings.py

        # Create email
        email = EmailMessage(
            subject,
            message,
            from_email,
            recipient_list
        )
        email.attach('oil_order_report.pdf', pdf_buffer.getvalue(), 'application/pdf')
        email.send()

        return response

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='My Users').exists():
            return qs.none()
        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='My Users').exists():
            return False
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='My Users').exists():
            return False
        return super().has_view_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:  # New object
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Oil, OilAdmin)





def generate_pdf_for_withdraw(obj):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Styles for heading and table
    styles = getSampleStyleSheet()
    heading_style = ParagraphStyle(
        'Heading1',
        parent=styles['Title'],
        fontSize=18,
        alignment=1,  # Centered
        spaceAfter=12
    )
    normal_style = styles['Normal']

    # Heading
    heading = Paragraph("R K ENTERPRISE Withdraw Slip", heading_style)

    # Define data for the table
    data = [
        ["Field", "Value"],
        ["Name", str(obj.name)],
        ["Date", obj.date],
        ["Withdraw Amount", obj.amount],
        # Add more fields as needed
    ]

    # Create table with data
    table = Table(data, colWidths=[2 * inch, 4 * inch])  # Adjust column widths if needed

    # Define table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ])
    table.setStyle(style)
    large_spacer = Paragraph("<br/><br/><br/><br/><br/><br/><br/><br/>", normal_style)
    # Signature text
    client_signature = Paragraph("Client Signature:", normal_style)
    authority = Paragraph("Authority:", normal_style)

    # Create a table for signatures with proper alignment
    signatures_data = [
        [client_signature, authority]
    ]
    signatures_table = Table(signatures_data, colWidths=[3 * inch, 3 * inch])
    signatures_style = TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ])
    signatures_table.setStyle(signatures_style)

    # Create spacers for spacing between table, signature, and authority sections
    space_after_table = Spacer(1, 0.5 * inch)  # Adjust the height as needed for spacing
    space_between_signatures = Spacer(1, 0.75 * inch)  # Adjust the height as needed for spacing

    # Build the PDF
    elements = [
        heading,
        table,
        space_after_table,
        large_spacer,# Space between the table and the signature section
        signatures_table,
        space_between_signatures  # Space between signature and authority
    ]
    doc.build(elements)

    buffer.seek(0)
    return buffer
class WithdrawAdmin(admin.ModelAdmin):

    def response_add(self, request, obj, post_url_continue=None):
        response = super().response_add(request, obj, post_url_continue)
        # Add a success message after the object is added
        messages.success(request, "Please get your pdf from Rameshwar for Withdrawal")

        # Generate PDF
        pdf_buffer = generate_pdf_for_withdraw(obj)

        # Email details
        subject = 'R K ENTERPRISE Withdraw Amount Slip'
        message = 'Please find the Withdraw Slip attached.'
        from_email = settings.DEFAULT_FROM_EMAIL

        recipient_list = [settings.ADMIN_EMAIL]  # Ensure you set this in your settings.py


        # Create email
        email = EmailMessage(
            subject,
            message,
            from_email,
            recipient_list
        )
        email.attach('withdraw_slip.pdf', pdf_buffer.getvalue(), 'application/pdf')
        email.send()

        return response

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='My Users').exists():
            return qs.none()
        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='My Users').exists():
            return False
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='My Users').exists():
            return False
        return super().has_view_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:  # New object
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Withdraw,WithdrawAdmin)





class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'download_pdf_button')

    def download_pdf_button(self, obj):
        """
        Render a button in the admin list view to download a PDF.
        """
        return format_html(
            '<a class="button" href="{}">Download PDF</a>',
            f"{obj.id}/download-pdf/"
        )
    download_pdf_button.short_description = "Actions"

    def get_urls(self):
        """
        Add custom URL for downloading PDFs.
        """
        urls = super().get_urls()
        custom_urls = [
            path('<int:client_id>/download-pdf/', self.admin_site.admin_view(self.download_pdf), name='client-download-pdf'),
        ]
        return custom_urls + urls


    def draw_centered_header(self, p, client, width, height):
        """
        Draw the header section centered on the page with different colors for each item.
        Also adds a green line under the report title.
        """
        # Business Name (Blue)
        p.setFont("Helvetica-Bold", 16)
        text = "R.K. ENTERPRISES"
        text_width = p.stringWidth(text, "Helvetica-Bold", 16)
        p.setFillColor(colors.burlywood)  # Set color to brown
        p.drawString((width - text_width) / 2, height - 50, text)

        # Address and Phone (Green)
        p.setFont("Helvetica", 10)
        address_text = "At Post Taroda Ta Umarkhed, Yavatmal    ✆ : 7666341953"
        address_width = p.stringWidth(address_text, "Helvetica", 10)
        p.setFillColor(colors.green)  # Set color to green
        p.drawString((width - address_width) / 2, height - 70, address_text)

        # Report Title (Red)
        p.setFont("Helvetica-Bold", 25)
        title_text = "All Transaction Report"
        title_width = p.stringWidth(title_text, "Helvetica-Bold", 25)
        p.setFillColor(colors.red)  # Set color to red
        p.drawString((width - title_width) / 2, height - 100, title_text)

        # Draw green line under the title
        p.setStrokeColor(colors.green)  # Set the line color to green
        p.setLineWidth(5)
        p.line((width - title_width) / 2, height - 105, (width + title_width) / 2, height - 105)

        # Client Name and Phone (Black)
        p.setFont("Helvetica", 12)
        client_text = f"Name   :  {client.name}      ✆ : {client.phone_number}"
        client_width = p.stringWidth(client_text, "Helvetica", 12)
        p.setFillColor(colors.yellowgreen)  # Set color to black
        p.drawString((width - client_width) / 2, height - 120, client_text)


    def download_pdf(self, request, client_id):
        """
        Generate a PDF with dynamic remaining balance calculation for the "Cls Balance" column.
        """
        client = Client.objects.get(pk=client_id)
        transactions = client.transactions.all().order_by('date')

        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{client.name}_transactions.pdf"'

        # Initialize ReportLab canvas
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # Constants
        header_height = 180  # Adjusted to accommodate styled header
        row_height = 18  # Row height in table
        rows_per_page = 5  # Number of rows per page
        page_number = 1  # Starting page number

        # Total calculations
        total_credit = 0
        total_debit = 0
        running_balance = 0  # Start with an initial balance of 0

        # Loop through transactions, chunked by rows_per_page
        for start_idx in range(0, len(transactions), rows_per_page):
            # Check if it's the first page
            is_first_page = page_number == 1

            # Set a light blue background for the page
            p.setFillColor(colors.aliceblue)
            p.rect(0, 0, width, height, stroke=0, fill=1)

            # Draw the styled header
            self.draw_styled_header(p, client, width, height, is_first_page)

            # Calculate Y-position for the table start
            y_position = height - header_height - 80  # Space between header and table

            # Prepare table data for the current page
            table_data = [["No", "Date", "Remarks", "Credit (In)", "Debit (Out)", "Cls Balance"]]

            # Transactions for the current page
            page_transactions = transactions[start_idx:start_idx + rows_per_page]
            for idx, transaction in enumerate(page_transactions, start=start_idx + 1):
                # Update running balance
                running_balance += transaction.credit - transaction.debit
                self.running_balance=running_balance
                # Append row data
                table_data.append([
                    str(idx),
                    transaction.date.strftime("%d/%m/%Y\n%I:%M %p"),
                    transaction.remarks,
                    f"{transaction.credit:,.2f}" if transaction.credit > 0 else "-",
                    f"{transaction.debit:,.2f}" if transaction.debit > 0 else "-",
                    f"{running_balance:,.2f}",  # Use the dynamically calculated balance
                ])
                total_credit += transaction.credit
                total_debit += transaction.debit

            # Define column widths dynamically
            total_width = width - 100  # Leave padding on both sides
            col_widths = [
                total_width * 0.05,  # "No"
                total_width * 0.2,  # "Date"
                total_width * 0.25,  # "Remarks"
                total_width * 0.15,  # "Credit (In)"
                total_width * 0.15,  # "Debit (Out)"
                total_width * 0.2  # "Cls Balance"
            ]

            # Create and style table
            table = Table(table_data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.blue),  # Header text color in blue
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Row font
                ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Table borders
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding for header
                ('TOPPADDING', (0, 1), (-1, -1), 6),  # Padding for rows
                ('TEXTCOLOR', (4, 1), (4, -1), colors.red),  # Debit column values in red
            ]))

            # Draw table
            table.wrapOn(p, width, height)
            table.drawOn(p, 50, y_position - len(page_transactions) * row_height)

            # Draw footer (with page number)
            self.draw_styled_footer(p, page_number, width, height)

            # Increment page number
            page_number += 1

            # Add new page if there are more transactions
            if start_idx + rows_per_page < len(transactions):
                p.showPage()  # Create a new page

        # p.drawString(100, 300, f"Total Balance: {running_balance:,.2f}")
        p.setFont("Helvetica-Bold", 12)  # Set the font to bold
        p.setFillColor(colors.red)  # Set text color to red
        p.drawString(100, 300, f"Total Balance: {running_balance:,.2f}")  # Draw text in PDF

        # Save PDF
        p.save()
        return response

    def draw_styled_header(self, p, client, width, height, is_first_page):
        """
        Draw the styled header matching the provided PDF reference.
        """
        # Business Name
        p.setFont("Helvetica-Bold", 20)
        p.setFillColor(colors.burlywood)
        p.drawString((width - p.stringWidth("R.K. ENTERPRISES", "Helvetica-Bold", 20)) / 2, height - 50,
                     "R.K. ENTERPRISES")

        # Address and Phone Number
        p.setFont("Helvetica", 12)
        p.setFillColor(colors.darkviolet)
        address = "At Post Taroda Tq: Umarkhed, Dist: Yavatmal    ✆ : 7666341953"
        p.drawString((width - p.stringWidth(address, "Helvetica", 12)) / 2, height - 70, address)

        # Report Title (only on the first page)
        if is_first_page:
            p.setFont("Helvetica-Bold", 25)
            p.setFillColor(colors.lime)
            p.drawString((width - p.stringWidth("All Transaction Report", "Helvetica-Bold", 25)) / 2, height - 100,
                         "All Transaction Report")

            # Client Info
            p.setFont("Helvetica", 12)
            p.setFillColor(colors.hotpink)
            client_info = f"Name   :  {client.name}      ✆ : {client.phone_number}"

            p.drawString(50, height - 130, client_info)
    def draw_styled_footer(self, p, page_number, width, height):
        """
        Draw the styled footer with centered page number.
        """

        p.setFont("Helvetica", 10)
        p.setFillColor(colors.black)
        p.drawCentredString(width / 2, 50, f"Page No. {page_number}")


class TransactionAdmin(admin.ModelAdmin):
    # list_display = ('name', 'phone_number', 'download_pdf_button')
    list_display = (
        "client",
        "date",
        "remarks",
        "credit",
        "debit",
    )
    search_fields = ("client__name", "remarks", "date")  # Enable search functionality
    list_filter = ("client", "date")  # Enable filtering
    readonly_fields = ("date",)  # Set date to read-only


admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Client, ClientAdmin)