from .views import UploadGradePDF

urlpatterns += [
    path('project/<int:project_id>/upload-grade/', UploadGradePDF.as_view(), name='upload_grade_pdf'),
] 