from locust.contrib.fasthttp import FastHttpUser



class MyUser(FastHttpUser):

    def get(self, path, headers, **kwargs):
        """Sends a GET request"""
        response = super(MyUser,self).request("GET", path, headers=headers, **kwargs)
        print(1)
        try:
            response.raise_for_status()
        except:
            print(path, headers)
        return response
