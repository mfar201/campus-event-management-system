from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    View,
)
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import (
    EventCategory,
    Event,
    JobCategory,
    #EventJobCategoryLinking,
    EventMember,
    EventImage,
    EventAgenda,
    UserProfile,

)
from .forms import EventForm, EventImageForm, EventAgendaForm, EventCreateMultiForm
from .decorators import admin_or_club_president_required, admin_or_club_president_required_cbv
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib import messages

# Event category list view
class EventCategoryListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = EventCategory
    template_name = 'events/event_category.html'
    context_object_name = 'event_category'


@admin_or_club_president_required_cbv
class EventCategoryCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = EventCategory
    fields = ['name', 'image']
    template_name = 'events/create_event_category.html'

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        return super().form_valid(form)

@admin_or_club_president_required_cbv
class EventCategoryUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = EventCategory
    fields = ['name', 'image']
    template_name = 'events/edit_event_category.html'

@admin_or_club_president_required_cbv
class EventCategoryDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model =  EventCategory
    template_name = 'events/event_category_delete.html'
    success_url = reverse_lazy('event-category-list')

@login_required(login_url='login')
@admin_or_club_president_required
def create_event(request):
    event_form = EventForm()
    event_image_form = EventImageForm()
    event_agenda_form = EventAgendaForm()
    catg = EventCategory.objects.all()
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        event_image_form = EventImageForm(request.POST, request.FILES)
        event_agenda_form = EventAgendaForm(request.POST)
        if event_form.is_valid() and event_image_form.is_valid() and event_agenda_form.is_valid():
            ef = event_form.save()
            created_updated(Event, request)
            event_image_form.save(commit=False)
            event_image_form.event_form = ef
            event_image_form.save()
            
            event_agenda_form.save(commit=False)
            event_agenda_form.event_form = ef
            event_agenda_form.save()
            return redirect('event-list')
    context = {
        'form': event_form,
        'form_1': event_image_form,
        'form_2': event_agenda_form,
        'ctg': catg,
    }
    return render(request, 'events/create.html', context)

@admin_or_club_president_required_cbv
class EventCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = EventCreateMultiForm
    template_name = 'events/create_event.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        evt = form['event'].save()
        event_image = form['event_image'].save(commit=False)
        event_image.event = evt
        event_image.save()

        event_agenda = form['event_agenda'].save(commit=False)
        event_agenda.event = evt
        event_agenda.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['ctg'] = EventCategory.objects.all()
        return context


class EventListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

@admin_or_club_president_required_cbv
class EventUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Event
    fields = ['category', 'name', 'description', 'scheduled_status', 'venue', 'start_date', 'end_date', 'maximum_attende', 'status']
    template_name = 'events/edit_event.html'


class EventDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

@admin_or_club_president_required_cbv
class EventDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Event
    template_name = 'events/delete_event.html'
    success_url = reverse_lazy('event-list')

@admin_or_club_president_required_cbv
class AddEventMemberCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = EventMember
    fields = ['event', 'user']
    template_name = 'events/add_event_member.html'

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        return super().form_valid(form)

@admin_or_club_president_required_cbv
class JoinEventListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = EventMember
    template_name = 'events/joinevent_list.html'
    context_object_name = 'eventmember'


class RemoveEventMemberDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = EventMember
    template_name = 'events/remove_event_member.html'
    success_url = reverse_lazy('join-event-list')

@admin_or_club_president_required_cbv
class UpdateEventStatusView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Event
    fields = ['status']
    template_name = 'events/update_event_status.html'


class CompleteEventList(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Event
    template_name = 'events/complete_event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(status='completed')

# @admin_or_club_president_required_cbv
# class CompleteEventUserList(LoginRequiredMixin, ListView):
#     login_url = 'login'
#     model = EventMember
#     template_name = 'events/complete_event_user_list.html'
#     context_object_name = 'completeuser'

#     def get_queryset(self):
#         return EventMember.objects.filter(attend_status='completed')



@login_required(login_url='login')
def search_event_category(request):
    if request.method == 'POST':
       data = request.POST['search']
       event_category = EventCategory.objects.filter(name__icontains=data)
       context = {
           'event_category': event_category
       }
       return render(request, 'events/event_category.html', context)
    return render(request, 'events/event_category.html')

@login_required(login_url='login')
def search_event(request):
    if request.method == 'POST':
       data = request.POST['search']
       events = Event.objects.filter(name__icontains=data)
       context = {
           'events': events
       }
       return render(request, 'events/event_list.html', context)
    return render(request, 'events/event_list.html')

class JoinEventView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        user_profile = request.user.userprofile

        if user_profile.role not in ['student', 'faculty']:
            messages.error(request, "Only students and faculty can join events.")
            return HttpResponseRedirect(reverse_lazy('event-list'))

        if EventMember.objects.filter(event=event, user=request.user).exists():
            messages.error(request, "You have already joined this event.")
        else:
            EventMember.objects.create(
                event=event,
                user=request.user,
                # attend_status='waiting',  # Initial status: waiting
                created_user=request.user,
                updated_user=request.user,
                # status='active'
            )
            messages.success(request, "You have successfully joined the event!")

        return HttpResponseRedirect(reverse_lazy('event-list'))