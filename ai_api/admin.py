from django.contrib import  admin
from  django.contrib.admin import  AdminSite
from  django.utils.translation import  ungettext_lazy
from authentication.models import User
from convertapi.models import Convert




class MyEmsAdminSite(AdminSite):

    site_title = 'AI'
    #
    site_header ='AI'
    #
    index_title = 'AI'




myems_admin_site = MyEmsAdminSite()

myems_admin_site.register(User)
myems_admin_site.register(Convert)
