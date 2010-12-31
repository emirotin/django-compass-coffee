from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from models import *

def polls_index(request):
    return render_to_response('dcc/index.html',
                              context_instance=RequestContext(request))
    

def poll_create(request):
    if request.method == 'GET':
        return render_to_response('dcc/create.html',
                                  context_instance=RequestContext(request))
    else:
        question = request.POST['question']
        poll = Poll(question=question)
        poll.save()
        total_answers = int(request.POST['total_answers'])
        for i in range(1, total_answers + 1):
            answer = request.POST['answer_{0}'.format(i)].strip()
            if not answer: 
                continue
            pa = PollAnswer(answer=answer, poll=poll)
            pa.save()
        return HttpResponseRedirect(reverse('dcc.views.poll_view', args=(poll.pk, )))
        

def poll_view(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('dcc/poll.html', {'poll': poll},
                              context_instance=RequestContext(request))
    

def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('dcc.views.poll_view', args=(poll.pk, )))
    answer_id = request.POST['answer']
    answer = get_object_or_404(PollAnswer, pk=answer_id)
    ra = RegisteredAnswer(answer=answer)
    ra.save()
    return HttpResponseRedirect(reverse('dcc.views.poll_results', args=(poll.pk, )))

def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    answers = []
    total = 0
    for answer in poll.pollanswer_set.all():
        count = RegisteredAnswer.objects.filter(answer=answer).count()
        answers.append([answer.answer, count])
        total += count
    for a in answers:
        a.append(a[1] * 100.0 / total)
        
    return render_to_response('dcc/results.html', {'poll': poll, 'results': answers, 'total': total},
                              context_instance=RequestContext(request))