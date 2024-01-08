from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import TemplateView, ListView, FormView, CreateView

from django.urls import reverse_lazy

from .forms import StrategyPostForm, CommentCreateForm ,ContactForm

from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required

from .models import StrategyPost, Comment, LikeForPost

from django.views.generic import DetailView

from django.views.generic import DeleteView

from django.http import JsonResponse

from django.contrib import messages

from django.core.mail import EmailMessage


class ContextMixin:
    """
    get_context_data()で受け取ったキーワード引数をテンプレート・コンテキストとして渡す
    """
    extra_context = None

    def get_context_data(self, **kwargs):
        kwargs.setdefault('view', self) # key:'view'が無い時、value:selfを追加
        if self.extra_context is not None:
            kwargs.update(self.extra_context) # extra_contextがある時、kwargsに上書き
        return kwargs


class IndexView(ListView):

    template_name ='index.html'

    queryset = StrategyPost.objects.order_by('-posted_at')

    paginate_by = 3


@method_decorator(login_required, name='dispatch')
class CreateStrategyView(CreateView):

    form_class = StrategyPostForm

    template_name = "post_strategy.html"

    success_url = reverse_lazy('strategy:post_done')

    def form_valid(self, form):

        postdata = form.save(commit=False)

        postdata.user = self.request.user

        postdata.save()

        return super().form_valid(form)
    
class PostSuccessView(TemplateView):

    template_name = 'post_success.html'

class DetailView(DetailView):

    template_name ='detail.html'

    model = StrategyPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(StrategyPost, pk=self.kwargs['pk'])
        detail = StrategyPost.objects.filter(pk=self.kwargs['pk']).order_by("-id").first()
        context['comments'] =Comment.objects.filter(target=detail.id)



        like_for_post_count = self.object.likeforpost_set.count()
        context['like_for_post_count'] = like_for_post_count
        if self.object.likeforpost_set.filter(user=self.request.user).exists():
            context['is_user_liked_for_post'] = True
        else:
            context['is_user_liked_for_post'] = False

        return context




class StrategyDeleteView(DeleteView):


    model = StrategyPost

    template_name ='strategy_delete.html'

    success_url = reverse_lazy('strategy:index')

    def delete(self, request, *args, **kwargs):
        
        return super().delete(request, *args, **kwargs)
    

    
        
class MypageView(ListView):


    template_name ='mypage.html'

    paginate_by = 3

    def get_queryset(self):

        queryset = StrategyPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        
        return queryset
    


class CommentCreate(CreateView):
    """コメント投稿ページのビュー"""
    template_name = 'comment_form.html'
    model = Comment
    form_class = CommentCreateForm
 
    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(StrategyPost, pk=post_pk)
        comment = form.save(commit=False)
        comment.target = post
        comment.save()

        return redirect('strategy:strategy_detail', pk=post_pk)
    

 
def like_for_post(request):
    post_pk = request.POST.get('post_pk')
    context = {
        'user': f'{request.user.last_name} {request.user.first_name}',
    }
    post = get_object_or_404(StrategyPost, pk=post_pk)
    like = LikeForPost.objects.filter(target=post, user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(target=post, user=request.user)
        context['method'] = 'create'

    context['like_for_post_count'] = post.likeforpost_set.count()

    return JsonResponse(context)

class ContactView(FormView):

    template_name ='contact.html'

    form_class = ContactForm

    success_url = reverse_lazy('strategy:contact')

    def form_valid(self, form):

        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']

        subject = 'お問い合わせ: {}'.format(title)

        message = \
        '送信者名 : {0}\nメールアドレス : {1}\n\n タイトル : {2}\n\n メッセージ :\n{3}' \
        .format(name, email ,title, message)

        from_email = 'masaori09040911@gmail.com'

        to_list = ['masaori09040911@gmail.com']

        message = EmailMessage(subject=subject,
                               body=message,
                               from_email=from_email,
                               to=to_list,
                               )

        message.send()

        messages.success(
            self.request, 'お問い合わせは正常に送信されました。')
        

        return super().form_valid(form)
