from django.shortcuts import render
from django.conf import settings  # 引入 settings 以获取 GRADIO_URL

def embed_gradio_view(request):
    gradio_url = settings.GRADIO_URL  # 通过 settings 获取 URL
    return render(request, 'embed_gradio.html', {'gradio_url': gradio_url})
