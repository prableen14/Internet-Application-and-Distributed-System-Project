from django.views import View
from django.shortcuts import redirect, render
from cryptoApp.forms import ArticleForm
from cryptoApp.models import Article
from django.views.generic.detail import DetailView


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'cryptoApp/create_article.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            # Redirect to the view displaying all articles
            return redirect('article_list')
        return render(request, 'cryptoApp/create_article.html', {'form': form})


class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve all articles from the database
        articles = Article.objects.all()
        return render(
            request, 'cryptoApp/article_list.html', {'articles': articles}
        )


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'cryptoApp/article_detail.html'
    context_object_name = 'article'
