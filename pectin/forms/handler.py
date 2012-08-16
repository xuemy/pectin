class ValidationError(RuntimeError):
    """
    Raised when a validator fails to validate its form.
    catch this exception and render the error page.
    """
    pass


class FormsDict(dict):
    '''WTForms form object dict.'''
    def append(self, Form):
        self[Form.__name__] = Form()

    def update(self, *forms):
        for form in forms:
            self[form.__class__.__name__] = form


class AutoFormsMixin(object):
    '''Auto add form to `forms`dict in the templates.'''
    Form = None
    formset = []

    def __init__(self, *args, **kwargs):
        self.forms = FormsDict()
        if self.Form:
            self.forms.append(self.Form)
        for Form in self.formset:
            self.forms.append(Form)
        super(AutoFormsMixin, self).__init__(*args, **kwargs)

    def getform(self, key=None, validate=True):
        '''Get and validate a form.'''
        form = self.form_loader(key)
        if validate:
            if not self.form_validate(form):
                # form validate.
                raise ValidationError("This form is not pass the validation.")
        return form

    def form_loader(self, key):
        if not key:
            # return default form
            try:
                form = self.Form(self)
            except TypeError:
                raise RuntimeError("Not set default form.")
        else:
            form = self.forms[key].__class__(self)
        return form

    def form_validate(self, form, *args, **kwargs):
        '''Automated handle of Forms validate.'''
        if form.validate():
            return True
        else:
            self.forms.update(form)
            return False

    def render(self, *args, **context):
        if "forms" not in context:
            context["forms"] = self.forms
        super(AutoFormsMixin, self).render(*args, **context)
