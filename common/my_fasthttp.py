from locust.contrib.fasthttp import FastHttpUser


class MyUser(FastHttpUser):

    def get(self, path, headers, **kwargs):
        """Sends a GET request"""
        response = self.request("GET", path, headers=headers, **kwargs)
        try:
            response.raise_for_status()
        except:
            print(path, headers)
        return response
