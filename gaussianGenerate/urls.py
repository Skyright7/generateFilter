
from django.urls import path

from .views import doGenerate,doClip,taskResult

urlpatterns = [
    path('gaussianGenerate/', doGenerate, name='doGenerate'),
    path('clipFilter/', doClip, name='doClip'),
    path('task_result/',taskResult, name='taskResult')
]