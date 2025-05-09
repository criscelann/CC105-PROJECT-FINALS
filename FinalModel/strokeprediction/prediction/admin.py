# # yourapp/admin.py
# from django.contrib import admin
# from django.urls import path
# from django.template.response import TemplateResponse

# class MyAdminSite(admin.AdminSite):
#     site_header = 'Stroke Prediction Admin'

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('dashboard/', self.admin_view(self.dashboard_view))
#         ]
#         return custom_urls + urls

#     def dashboard_view(self, request):
#         context = dict(
#             self.each_context(request),
#             title='Dashboard',
#             total_patients=Patient.objects.count(),
#         )
#         return TemplateResponse(request, "admin/dashboard.html", context)

# # Replace the default admin site
# admin_site = MyAdminSite(name='myadmin')

# from .models import Patient
# admin_site.register(Patient)
