from django.contrib import admin

# Register your models here.
from .models import Contact, Feedback, Cement, Oil, Withdraw
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

    # Heading
    heading = Paragraph(" RK Financial Cement Order Report", heading_style)

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

    # Build the PDF
    elements = [heading, table]
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
        subject = 'RK Financial New Cement Order Report'
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

    # Heading
    heading = Paragraph(" RK Financial Oil Order Report", heading_style)

    # Define data for the table
    data = [
        ["Field", "Value"],
        ["Order ID", str(oil.id)],
        ["Person Name", oil.name],
        ["Person Mobile number", oil.mobile],
        ["Personal EmailID",oil.email],
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

    # Build the PDF
    elements = [heading, table]
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
        subject = 'RK Financial New Oil Order Report'
        message = 'A new oil order has been placed. Please find the report attached.'
        from_email = settings.DEFAULT_FROM_EMAIL
        # from_email = "jadhavatul161093@gmail.com"
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
    heading = Paragraph("RK Financial Withdraw Slip", heading_style)

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
        subject = 'RK Financial Withdraw Amount Slip'
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
