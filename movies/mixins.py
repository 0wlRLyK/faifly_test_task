from django.http import HttpResponseRedirect
from django.views.generic import FormView


class MultiFormView(FormView):
    """
    View to handle multiple form classes.
    """
    form_classes = {}

    def are_forms_valid(self, forms):
        """
        Check if all forms defined in `form_classes` are valid.
        """
        for form in forms.values():
            if not form.is_valid():
                return False
        return True

    def forms_valid(self, forms):  # pylint: disable=unused-argument
        """
        Redirects to get_success_url().
        """
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, forms):
        """
        Renders a response containing the form errors.
        """
        return self.render_to_response(super().get_context_data(forms=forms))

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the forms.
        """
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        """
        Add forms into the context dictionary.
        """
        if 'forms' not in kwargs:
            kwargs['forms'] = self.get_forms()
        # Override "form" if not present so the original FormView class doesn't try to get a singular form.
        if 'form' not in kwargs:
            kwargs['form'] = None
        return super(MultiFormView, self).get_context_data(**kwargs)

    def get_forms(self):
        """
        Initializes the forms defined in `form_classes` with initial data from `get_initial()` and
        kwargs from get_form_kwargs().
        """
        forms = {}
        initial = self.get_initial()
        form_kwargs = self.get_form_kwargs()
        for key, form_class in self.form_classes.items():
            forms[key] = form_class(initial=initial[key], **form_kwargs[key])
        return forms

    def get_form_kwargs(self):
        """
        Build the keyword arguments required to instantiate the form.
        """

        kwargs = {}
        for key in self.form_classes.keys():
            if self.request.method in ('POST', 'PUT'):
                kwargs[key] = {
                    'data': self.request.POST,
                    'files': self.request.FILES,
                }
            else:
                kwargs[key] = {}
        return kwargs

    def get_initial(self):
        """
        Returns a copy of `initial` with empty initial data dictionaries for each form.
        """
        initial = super(MultiFormView, self).get_initial()
        for key in self.form_classes.keys():
            initial[key] = {}
        return initial

    def post(self, request, **kwargs):
        """
        Uses `are_forms_valid()` to call either `forms_valid()` or * `forms_invalid()`.
        """
        forms = self.get_forms()
        if self.are_forms_valid(forms):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)
