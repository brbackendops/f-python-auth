
from django.http import JsonResponse
from django.conf import settings

# redis
from django.core.cache import cache
# ipware for getting ip address rather than relaying on django META headers
from ipware import get_client_ip


class FixedRateLimiter:
    def __init__(self,limit=15,seconds=50):
        self.rate_limit = limit
        self.window_time = seconds
    
    def __call__(self, function):
        def wrapper(view_self,request,*args,**kwargs):
            req_ip , _ = get_client_ip(request,request_header_order=['X_FORWARDED_FOR','REMOTE_ADDR'])
            key = f"user-{req_ip}"
            
            # print("time",cache.ttl(key))
            
            if cache.get(key) is None:
                cache.set(key,1,timeout=self.window_time)    
            else:
                cache.incr(key)
            # print("key",int(cache.get(key)))
            
            if cache.ttl(key) and cache.ttl(key) > 0 and int(cache.get(key)) >= self.rate_limit:
                    return JsonResponse(
                        {
                            'status': "error",
                            'error': 'rate limit exceeded'
                        },
                        status=429,
                    )

            return function(view_self,request,*args,**kwargs)

        return wrapper