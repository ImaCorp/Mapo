from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required


from gestione.models import Estructura, Staff, StaffPosicion, Encuesta, Capturista, EncuestaProc, ActivaEncuesta

@login_required
def index(request):
    if request.user.is_superuser or request.user.groups.filter(name='GestionAdmin').count():
        roots_staffpos = StaffPosicion.objects.filter(padre__isnull=True)
    else:
        roots_staffpos = StaffPosicion.objects.filter(staff__user_id=request.user.id) | StaffPosicion.objects.filter(capturista__user_id=request.user.id)

    context = {'roots_staffpos': roots_staffpos}
    return render(request, 'gestione/index.html', context)

@login_required
def encuesta(request, aenc_id):
    aenc = get_object_or_404(ActivaEncuesta, pk=aenc_id)
    return render(request, 'gestione/encuesta.html', {'aenc': aenc})

@login_required
def doencuesta(request, encproc_id, idcapt, idaenc):
    if encproc_id == 0:
        capt = Capturista.objects.get(pk=idcapt)
        idaenc = ActivaEncuesta.objects.get(pk=idaenc)
        enc = EncuestaProc.objects.ElQueSigue(capt, aenc)
    else:
        enc = get_object_or_404(EncuestaProc, pk=encproc_id)
    return render(request, 'gestione/doencuesta.html', {'enc': enc})

# @login_required
# def guarda_encuesta(request, enc_id):
#     enc = get_object_or_404(Encuesta, pk=enc_id)
#     return render(request, 'gestione/encuesta.html', {'enc': enc})

    # try:
    #     selected_choice = p.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the poll voting form.
    #     return render(request, 'polls/detail.html', {
    #         'poll': p,
    #         'error_message': "You didn't select a choice.",
    #     })
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))