from django.http import HttpResponseNotFound
from django.utils.deprecation import MiddlewareMixin


class BlockGitAccessMiddleware(MiddlewareMixin):
    """
    安全中间件：阻止对.git路径的所有访问
    这是最直接有效的保护方法，确保在Django层面拦截所有.git相关的请求
    """
    def process_request(self, request):
        # 检查请求路径是否包含.git
        if '.git' in request.path:
            # 返回404错误，完全隐藏资源存在
            return HttpResponseNotFound('Not Found')
        
        # 继续处理其他请求
        return None