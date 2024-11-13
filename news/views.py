from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import OuterRef, Exists, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from notifications.signals import notify

from .forms import NewsCreationForm, NewsCommentCreationForm
from .models import News, NewsComment
from players.models import Player
from clubs.models import Club
from news.models import NewsLike


class PublicNewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 2
    extra_context = {
        'title': 'Новости',
    }

    def get_queryset(self):
        """Mark news if the user has already liked the news"""

        news = News.objects.filter(is_open=News.OPEN.YES, is_published=News.PUBLISHED.YES).\
            select_related('club', 'author').prefetch_related('newscomment_news', 'newslike_news')
        user_id = self.request.user.pk
        news = news.annotate(liker=Exists(NewsLike.objects.filter(news_id=OuterRef('pk'), liker_id=user_id)))
        return news


def get_news_index_page(request: HttpRequest) -> HttpResponse:
    first_news = News.objects.filter(is_open=News.OPEN.YES, is_published=News.PUBLISHED.YES).exclude(cover=''). \
        order_by('-created_at').first()
    news = News.objects.filter(is_open=News.OPEN.YES, is_published=News.PUBLISHED.YES).exclude(cover=''). \
               order_by('-created_at')[1:3]
    context = {
        'title': 'Главная',
        'news': news,
        'first_news': first_news,
    }
    return render(request, 'news/index.html', context)


class PublicNewsDetailView(DetailView):
    """Making page oof the news with corresponding comments and form for the comments"""

    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_queryset(self):
        news_pk = self.kwargs.get('pk')
        return News.objects.select_related('club', 'author').prefetch_related('newscomment_news', 'newslike_news'). \
            filter(pk=news_pk, is_open=News.OPEN.YES, is_published=News.PUBLISHED.YES)

    def get_object(self, queryset=None):
        """Checking if the user has seen the news in the session"""

        news_id = self.kwargs.get('news_id')
        viewed_news_set = set(self.request.session.get('viewed_news', []))
        if news_id not in viewed_news_set:
            news = super().get_object(queryset)
            news.views_count += 1
            news.save()
            viewed_news_set.add(news_id)
            self.request.session['viewed_news'] = list(viewed_news_set)
        else:
            news = super().get_object(queryset)

        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = NewsCommentCreationForm()
        context['form'] = form

        # Checking if the user is authenticated and has already liked
        if self.request.user.is_authenticated:
            context['news'].liker = True if NewsLike.objects.filter(liker=self.request.user,
                                                                    news=context['news']).exists() else False

        # Pagination's settings
        comments = NewsComment.objects.filter(news=context['news']).select_related('commenter').order_by('created_at')
        paginator = Paginator(comments, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        context['title'] = context['news'].name

        return context

    def post(self, request, *args, **kwargs):
        # Handle form submission for posting comments
        form = NewsCommentCreationForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.commenter = request.user
            new_comment.news = self.get_object()
            new_comment.save()
        # Redirect to the same page after comment submission
        return redirect(request.META.get('HTTP_REFERER'))


def get_rules(request: HttpRequest) -> HttpResponse:
    return render(request, 'news/rules.html', {})


def about_us(request: HttpRequest) -> HttpResponse:
    return render(request, 'news/about_us.html', {})


class NewsCreationView(LoginRequiredMixin, CreateView):
    """Creating news"""

    model = News
    form_class = NewsCreationForm
    template_name = 'news/create_news.html'
    login_url = reverse_lazy('players:login')
    success_url = reverse_lazy('news:index')
    extra_context = {
        'title': 'Добавление новости',
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        # Получаем текущего пользователя его клуб, если он был выбран
        user = self.request.user
        form.instance.author = user
        club = form.cleaned_data.get('club', None)

        # Если клуб выбран и пользователь является владельцем клуба, публикуем новость незамедлительно
        if club and club.owner == user:
            form.instance.is_published = News.PUBLISHED.YES
            message = f'В клубе "{club}" опубликована новость "{form.cleaned_data.get("name")}"'
            notify.send(sender=self.request.user, recipient=club.members.all(), verb=message, target=form.instance)
        elif club:
            message = f'В клубе "{club}" предложили новость "{form.cleaned_data.get("name")}"'
            notify.send(sender=self.request.user, recipient=club.owner, verb=message, target=form.instance)
        else:
            message = f'Предложена новость "{form.cleaned_data.get("name")}"'
            admin = Player.objects.get(username='admin')
            notify.send(sender=self.request.user, recipient=admin, verb=message, target=form.instance)
        return super().form_valid(form)


class UpdateNewsView(LoginRequiredMixin, UpdateView):
    """For changing news.
    Only author or club's owner of the club can modify news"""

    model = News
    fields = ['name', 'club', 'is_open', 'keywords', 'content', 'cover']
    template_name = 'news/edit_news.html'
    login_url = reverse_lazy('players:login')
    success_url = reverse_lazy('news:index')
    extra_context = {
        'title': 'Редактирование новости',
    }

    def get_queryset(self):
        """Making SQL query better"""
        return super().get_queryset().select_related('author', 'club')

    def dispatch(self, request, *args, **kwargs):
        """Checking if the user is author of the news or club owner where the news published.
        If it is not redirect will happen. If it is everything will be ok"""

        self.news = self.get_object()
        club_owner = self.news.club.owner if self.news.club else None

        if request.user != self.news.author and request.user != club_owner:
            return redirect('news:index')

        return super().dispatch(request, *args, **kwargs)


def like_news(request: HttpRequest, news_pk: int) -> JsonResponse:
    """Changing user's like state and updating after that numbers of like of the news"""

    response_data = {}
    if request.GET:
        news = get_object_or_404(News, pk=news_pk)
        like, created = NewsLike.objects.get_or_create(liker=request.user, news=news)

        if not created:
            like.delete()
            response_data['delete_like'] = 1
        else:
            response_data['delete_like'] = 0

        response_data['news_like_count'] = NewsLike.objects.filter(news=news).count()

    return JsonResponse(response_data)
