# 
# 
# 
# 
'''
Server Connection Class
'''
from tkinter import messagebox
from kepconfig import connection, error


# Class for Kepware API Connection - extended for doc reads
class server_doc(connection.server):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_doc(self,url):
        if self.SSL_on:
            proto = 'https'
        else:
            proto = 'http'
        path =  '{}://{}:{}'.format(proto, self.host, self.port)
        r = self._config_get(path + url)
        return r.payload

    def ErrorHandler(self,err):
        # Generic Handler for exception errors
        if err.__class__ is error.KepError:
            print(err.msg)
            messagebox.showerror('Error', message=err.msg)
        elif err.__class__ is error.KepHTTPError:
            print(err.code)
            print(err.msg)
            print(err.url)
            print(err.hdrs)
            print(err.payload)
            messagebox.showerror(err.msg, message=err.payload['message'])
        elif err.__class__ is error.KepURLError:
            print(err.url)
            print(err.reason)
            messagebox.showerror('Error', message=err.msg)
        else:
            print(f'Different Exception Received: {err}')
            messagebox.showerror('Error', message=err)
