from django.urls import path

from .views import (
    EventCategoryListView,
    EventCategoryCreateView,
    EventCategoryUpdateView,
    EventCategoryDeleteView,
    EventCreateView,
    EventListView,
    EventUpdateView,
    EventDetailView,
    EventDeleteView,
    AddEventMemberCreateView,
    JoinEventListView,
    RemoveEventMemberDeleteView,
    UpdateEventStatusView,
    CompleteEventList,
    #CompleteEventUserList,
    search_event_category,
    search_event,
    create_event,
    JoinEventView,
)

urlpatterns = [
    path('category-list/', EventCategoryListView.as_view(), name='event-category-list'),
    path('create-category/', EventCategoryCreateView.as_view(), name='create-event-category'),
    path('category/<int:pk>/edit/', EventCategoryUpdateView.as_view(), name='edit-event-category'),
    path('category/<int:pk>/delete/', EventCategoryDeleteView.as_view(), name='delete-event-category'),
    path('event-create/', EventCreateView.as_view(), name='event-create'),
    path('event-list/', EventListView.as_view(), name='event-list'),
    path('event/<int:pk>/edit/', EventUpdateView.as_view(), name='event-edit'),
    path('detail/<int:pk>', EventDetailView.as_view(), name='event-detail'),
    path('delete/<int:pk>', EventDeleteView.as_view(), name='event-delete'),
    path('add-event-member/', AddEventMemberCreateView.as_view(), name='add-event-member'),
    path('join-event-list/', JoinEventListView.as_view(), name='join-event-list'),
    path('event-member/<int:pk>/remove/', RemoveEventMemberDeleteView.as_view(), name='remove-event-member'),
    path('update-status/<int:pk>/event/', UpdateEventStatusView.as_view(), name='update-event-status'),
    path('complete-event/', CompleteEventList.as_view(), name='complete-event'),
    #path('complete-event-user/', CompleteEventUserList.as_view(), name='complete-event-user'),
    path('search_category/', search_event_category, name='search-event-category'),
    path('search_event/', search_event, name='search-event'),
    path('create/', create_event, name='create'),
    path('event/<int:pk>/join/', JoinEventView.as_view(), name='join-event'),
]