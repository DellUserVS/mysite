from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

# using <django.views.generic> for [IndexView, DetailView, ResultsView] for 'shortcut'

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = "latest_question_list"
    http_web_page_title = "Home Page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.http_web_page_title
        return context
    
    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    http_web_page_title = "Question details"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.http_web_page_title
        return context

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    http_web_page_title = "Results Page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.http_web_page_title
        return context

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

