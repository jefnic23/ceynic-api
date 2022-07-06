from flask import redirect, url_for, current_app
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from app.forms import *
from app.models import *
from werkzeug.utils import secure_filename
# from app import bucket

class AdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))

class LogoutView(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated

class ProductModelView(ModelView):
    column_exclude_list = ('purchase_id') # does this need to be visible?
    form_excluded_columns = ('purchase_id')
    # edit_template = 'admin/edit.html'
    extra_css = ["https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.9.3/min/dropzone.min.css"]
    extra_js = ["https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.9.3/min/dropzone.min.js"]

    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))

    def create_form(self):
        form = ProductForm()
        return form

    def edit_form(self, obj=None):
        return super(ProductModelView, self).edit_form(obj)

    def get_edit_form(self):
        form = super(ProductModelView, self).get_edit_form() 
        form.images = MultipleFileField('Upload image(s)')
        return form

    def edit_form(self, obj=None):
        form = super(ProductModelView, self).edit_form(obj) 
        images = Product.query.filter_by(id=obj.id).first()
        form.images.data = images.images
        return form

    def on_model_change(self, form, model, is_created=False):
        file_title = form.title.data.replace(" ", "_")
        file_path = 'public/' + file_title + '/'
        current_app.bucket.Object(file_path)
        files = [f for f in form.images.data]
        if files:
            model.images = []
            for f in files:
                if f:
                    try:
                        secured_file = secure_filename(f.filename.replace(" ", "_"))
                        model.images.append(secured_file)
                        current_app.bucket.Object(file_path + secured_file).put(Body=f)
                    except AttributeError:
                        model.images.append(f)


# keep images in bucket so they can be sold as prints?

# @event.listens_for(Product, 'after_delete')
# def _handle_image_delete(mapper, conn, target):
#     try:
#         if target.images:
#             for image in target.images:
#                 path = 'public/' + target.title.replace(" ", "_") + '/' + image
#                 resource.Object(app.config['BUCKET_NAME'], path).delete()
#             bucket.Object('public/' + target.title.replace(" ", "_") + '/').delete()
#     except:
#         pass
