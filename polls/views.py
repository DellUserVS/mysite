from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Choice, Question

def index(request):
    # Filter and return first 5 latest Questions
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    # Context of 'polls/index.html'
    context = {
        "title": "Home page",
        "latest_question_list": latest_question_list
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # Raise 'ErrorType: Http404' if object does not exist
    question = get_object_or_404(Question, pk=question_id)
    
    title = "Question %s details" % question_id

    # Context of 'polls/detail.html'
    context = {
        "title": title,
        "question": question
    }
    
    return render(request, 'polls/detail.html', context)

def results(request, question_id):
    response = "You're looking at the results of question %s"
    question = get_object_or_404(Question, pk=question_id)

    # Context of 'polls/results.html'
    context = {
        "title": "Results of question %s" % question_id,
        "question": question
    }
    
    return render(request, "polls/results.html", context)

def vote(request, question_id):
    # Get the question object. If Question object does not exist raise 'ErrorType: Http404'
    question = get_object_or_404(Question, pk=question_id)

    # Return a 'ErrorType: KeyError' if USER did not enter choice text
    try:
        # Get the selected choice
        selected_choice = question.choice_set.get(pk=request.POST["choice"])

    except (KeyError, Choice.DoesNotExist):
        # Context of 'polls/detail.html'
        context = {
            "title": "Vote on question %s" % question_id,
            "question": question,
            "error_message": error_message
        }

        return render(request, "polls/detail.html", context)
    
    else:
        # If USER votes on a CHOICE, instruct the database to increase VOTES by 1
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

