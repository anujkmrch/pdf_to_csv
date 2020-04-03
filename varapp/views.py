import os
from django.conf import settings
from django.http import Http404
from varapp.models import *
from django.utils.http import urlencode
import string
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from varapp.forms import DocumentForm
from django.urls import reverse
from django.contrib import messages
from varapp.document_processor import process_document

from django.db.models import Prefetch


def index(request):
    "method to display for"

    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = DocumentForm(request.POST, request.FILES)

        # check whether it's valid:
        if form.is_valid():
            f = request.FILES['pdf_file']

            title = request.POST['title']
            year = request.POST['year']

            file_name = ''.join(random.choice(string.ascii_lowercase)
                                for i in range(10))
            pdf_file_path = f'media/pdf/{file_name}.pdf'
            csv_file_path = f'media/csv/{file_name}.csv'
            with open(pdf_file_path, 'wb') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

            enteries = process_document(pdf_file_path, csv_file_path)

            csv = Csv(slug=file_name)
            csv.save()

            for entity in enteries:
                csv.journal_set.create(
                    npa_key=entity['npa_key'],
                    npa_val=entity['npa_val']
                )

            url = reverse('processed_pdf', kwargs={
                'file_processing_code': f'{file_name}'})

            query_kwargs = {'title': title, 'year': year}

            if query_kwargs:
                url = u'%s?%s' % (url, urlencode(query_kwargs))

            return HttpResponseRedirect(url)
        else:
            err = form.errors
            return redirect(reverse('homepage'))

    form = DocumentForm()
    return render(request, 'index.html', {'document_form': form})


def process_pdf(request, file_processing_code):
    title = request.GET.get('title')
    year = request.GET.get('year')
    key = title.replace(' ', '-').lower()+'-'+year

    csv = Csv.objects.prefetch_related('journal_set').get(
        slug=file_processing_code)

    entry = csv.journal_set.filter(npa_key=key).get()

    # SELECT csv.slug as csv_slug from varapp_csv as csv join varapp_entry as vent
    # on vent.csv_id=csv.id  WHERE csv.slug=file_processing_code
    #

    # print(entry, entry.csv.slug)
    # return HttpResponse('process')
    return render(request, 'download.html', context={'csv': csv, 'entry': entry, 'key': title})


def download(request, file_processing_code):
    path = f'csv/{file_processing_code}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    raise Http404
