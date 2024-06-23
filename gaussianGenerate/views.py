from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import taskResultList
import json
from .generateScript import generate_script
from .clipScript import do_clip
from django.shortcuts import get_object_or_404

@csrf_exempt
@require_http_methods(["POST"])
def doGenerate(request):
    try:
        print(request.body)
        data = json.loads(request.body)
        taskId = data['taskId']
        dataPath = data['dataPath']
        numBasePeps = data['numBasePeps']
        numPepsPerBase = data['numPepsPerBase']
        minLength = data['minLength']
        maxLength = data['maxLength']
        sampleVariancesDown = data['sampleVariancesDown']
        sampleVariancesUp = data['sampleVariancesUp']
        sampleVariancesStep = data['sampleVariancesStep']
        out_file_path = generate_script(taskId, dataPath, numBasePeps, numPepsPerBase, minLength, maxLength,
                                        sampleVariancesDown, sampleVariancesUp, sampleVariancesStep)
        base_dir = '/home/student/disk2T/lgy/generateFilter'
        relative_path = out_file_path
        # 去掉开头的"./"
        if out_file_path.startswith('./'):
            relative_path = out_file_path[2:]
        generateOutPath = base_dir + '/' + relative_path
        outputPath = generateOutPath
        outputPreviewPath = outputPath
        newTask = taskResultList.objects.create(taskId=taskId,outputPath=outputPath,outputPreviewPath=outputPreviewPath)
        return JsonResponse({'successful': 1, 'message': f'generate task id:{newTask.taskId} successful running'})
    except Exception as e:
        return JsonResponse({'e':e,'successful': 0, 'message': 'running failed'})


@csrf_exempt
@require_http_methods(["POST"])
def doClip(request):
    try:
        data = json.loads(request.body)
        taskId = data['taskId']
        peptidesPath = data['peptidesPath']
        targetSeq = data['targetSeq']
        pepsPerTarget = data['pepsPerTarget']
        out_file_path = do_clip(targetSeq,taskId, peptidesPath,pepsPerTarget)
        base_dir = '/home/student/disk2T/lgy/generateFilter'
        relative_path = out_file_path
        # 去掉开头的"./"
        if out_file_path.startswith('./'):
            relative_path = out_file_path[2:]
        generateOutPath = base_dir + '/' + relative_path
        outputPath = generateOutPath
        outputPreviewPath = outputPath
        newTask = taskResultList.objects.create(taskId=taskId, outputPath=outputPath,
                                                outputPreviewPath=outputPreviewPath)
        return JsonResponse({'successful': 1, 'message': f'clipFilter task id:{newTask.taskId} successful running'})
    except Exception as e:
        print(e)
        return JsonResponse({'successful': 0, 'message': 'running failed'})

@csrf_exempt
@require_http_methods(["POST"])
def taskResult(request):
    try:
        data = json.loads(request.body)
        taskId = data['taskId']
        taskOut = get_object_or_404(taskResultList,pk=taskId)
        data = {'outputPath':taskOut.outputPath,
                'outputPreviewPath':taskOut.outputPreviewPath,
                'successful': 1,
                'message': f'task id:{taskOut.taskId} successful fetching'
        }
        return JsonResponse(data)

    except Exception as e:
        print(e)
        return JsonResponse({'successful': 0, 'message': 'request failed'})
