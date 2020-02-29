from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)

from .models import Post
from django.contrib.auth.models import User

# graph
import pandas as pd
import numpy as np
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.express as px
import plotly.graph_objects as go

import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_for_files = os.path.join(base_dir, 'staticfiles/')


def home(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about_med_scan.html', {'title': 'About'})

def pricing(request):
    return render(request, 'pricing.html', {'title': 'Price'})

class PostListView(ListView):
    model = Post # create model
    # <app>/<model>_<viewtype>.html
    template_name = 'home.html' # last changes
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView): #post of the filtered user
    model = Post
    template_name = 'user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self): # check if user exists
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView): # not working?
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView): # LoginRequiredMixin - for only logged user
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # overwrite save with author of the post
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('post-create')
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # UserPassesTestMixin - only use post
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self): # check test condition that currect user is author of the post
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    # def get_success_url(self):
    #     return reverse('post-detail')

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
# plots
def show_plotly(request):

    data_f = pd.read_csv(root_for_files + 'ready_build_graph.csv')
    df_temp = data_f.groupby(['Location']).sum().reset_index(drop=False)

    fig = px.scatter(df_temp, x=df_temp['RainToday'],
                                y=df_temp['Location'],
                            size=df_temp['Rainfall'],
                            color=df_temp['RainToday'],
                            height=800
                )

    lat = data_f.groupby('Location').mean().Latitude
    lon = data_f.groupby('Location').mean().Longitude
    z = data_f.groupby('Location').mean()['Rainfall']

    fig_2 = go.Figure(go.Densitymapbox(lat=lat,
                                       lon=lon,
                                       z=z,
                                       radius=30))

    fig_2.update_layout(mapbox_style="open-street-map",
                        mapbox_center_lon=133.7751312,
                        mapbox_center_lat=-25.2743988)

    fig_2 = plot(fig_2, output_type='div', include_plotlyjs=False, show_link=False, link_text="")

    fig = plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")

    return render(request, "graph.html", context={'fig': fig, 'fig_2':fig_2})


def show_plotly_future(request):

    temp = pd.read_csv(root_for_files + 'temp.csv')

    fig = px.scatter_mapbox(temp, lat='Latitude', lon='Longitude', hover_name="Location",
                    color='probability', color_continuous_scale=["yellow", "blue"],
                    zoom=3, opacity=0.5)

    fig.update_layout(mapbox_style="open-street-map", height=400)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    fig = plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")

    return render(request, "predict_results.html", context={'fig': fig})
