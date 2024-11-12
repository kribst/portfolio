import random
from django.http import FileResponse
from django.conf import settings
import os
from django.shortcuts import render, get_object_or_404
from .models import Work, WorkImage, CV, WorkDescription
from django.http import HttpResponse




# Create your views here.
def index(request):
    works = Work.objects.all()

    # Sélectionner aléatoirement 4 travaux
    if works.count() > 4:
        selected_works = random.sample(list(works), 4)
    else:
        selected_works = list(works)

    context = {
        'selected_works': selected_works,  # Passer les travaux sélectionnés à la vue index.html
    }
    return render(request, 'index.html', context=context)


def work_details(request, work_id):
    # Récupérer le travail par son ID
    work = get_object_or_404(Work, id=work_id)

    # Récupérer uniquement les images liées au travail spécifique
    work_images = WorkImage.objects.filter(product=work)

    # Récupérer les descriptions du travail
    works_element = WorkDescription.objects.filter(work=work)

    context = {
        'work': work,  # Passer les détails du travail au contexte
        'work_images': work_images,  # Passer les images au template
        'works_element': works_element,
    }
    return render(request, 'work_details.html', context)


def work(request):
    works = Work.objects.all()
    context = {
        'works': works,  # Passer les détails du travail au contexte
    }
    return render(request, 'work.html', context)


def Services(request):
    return render(request, 'services.html')



def download_cv(request):
    cv = CV.objects.first()
    if cv:
        response = HttpResponse(cv.file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={cv.file.name}'
        return response
    return HttpResponse("Aucun CV disponible.")
