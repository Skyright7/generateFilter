
from django.urls import path

from .views import doGenerate,doClip,taskResult

urlpatterns = [
    path('api/gaussianGenerate/', doGenerate, name='doGenerate'),
    path('api/clipFilter/', doClip, name='doClip'),
    path('task_result/',taskResult, name='taskResult')
]