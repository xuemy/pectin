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


class AutoFormsMixin(object):
    '''Auto add form to `forms`dict in the templates.'''
    Form = None
    formset = []

    @property
    def forms(self):
        forms = FormsDict()
        if self.Form:
            forms.append(self.Form)
        for Form in self.formset:
            forms.append(Form)
        return forms

    def form_loader(self, key=None, validate=True):
        '''Get and validate a form.'''
        if not key:
            # return default form
            try:
                form = self.Form(self)
            except TypeError:
                raise RuntimeError("Not set default form.")
        else:
            form = self.forms[key].__class__(self)
        if validate:
            if not self.form_validate(form):
                # form validate.
                raise ValidationError("This form is not pass the validation.")
        return form

    def form_validate(self, form, *args, **kwargs):
        '''Automated handle of Forms validate.'''
        if form.validate():
            return form
        self.forms.update({form.__class__.__name__: form})
        self.render(*args, **kwargs)
        return False

    def render(self, *args, **context):
        if "forms" not in context:
            context["forms"] = self.forms
        super(AutoFormsMixin, self).render(*args, **context)
