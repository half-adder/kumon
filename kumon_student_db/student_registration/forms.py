from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Button, Layout, HTML, Div, Field
from django import forms
from django.template.loader import render_to_string

from kumon_student_db.student_registration import models
from kumon_student_db.student_registration.models import HowChoice, WhyChoice
from crispy_forms.helper import FormHelper


class Row(Div):
    css_class = "form-row"


class DateField(Field):
    def __init__(self, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)
        self.type = "date"


class StudentForm(forms.ModelForm):
    how_other = forms.CharField(label="Other", required=False)
    why_other = forms.CharField(label="Other", required=False)

    how_choices = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=models.HowChoice.objects.all(),
        label="How did you learn about Kumon?",
        required=False,
    )
    why_choices = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=models.WhyChoice.objects.all(),
        label="Why did you enroll your child in Kumon?",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        # self.fields['registration_discount_percent'].initial = 0
        self.fields['instructor'].initial = 1

        custom_labels = {
            "registration_discount_percent": "Reg. Discount %",
            "math_ppd": "Math PPD",
            "reading_ppd": "Reading PPD",
            "debit_paid": "Bank Draft Paid",
        }

        for k, v in custom_labels.items():
            self.fields[k].label = v

        self.helper = FormHelper()
        cost_table_html = render_to_string(
            "student_registration/student_form_cost_table.html"
        )

        if self.instance.pk is not None:
            delete_button = Button(
                "delete",
                "Delete",
                onclick='window.location.href="delete"',
                css_class="btn btn-outline-danger",
            )
        else:
            delete_button = None

        self.helper.layout = Layout(
            Row(
                Field("name", wrapper_class="col"),
                Field("parent_name", wrapper_class="col"),
            ),
            Row(
                Field("email", wrapper_class="col"), Field("phone", wrapper_class="col")
            ),
            Row(
                DateField("start_date", wrapper_class="col cost-input"),
                Field("primary_day", wrapper_class="col cost-input"),
            ),
            Row(
                Field("math_level", wrapper_class="col cost-input"),
                Field("math_ppd", wrapper_class="col-2 cost-input"),
                Field("reading_level", wrapper_class="col cost-input"),
                Field("reading_ppd", wrapper_class="col-2 cost-input"),
            ),
            Row(
                Field("how_choices", "", wrapper_class="col"),
                Field("why_choices", "", wrapper_class="col"),
            ),
            Row(
                Field("how_other", wrapper_class="col"),
                Field("why_other", wrapper_class="col"),
            ),
            Row(
                Field(
                    "registration_discount_percent",
                    wrapper_class="col-3 cost-input",
                ),
                Field("registration_discount_reason", wrapper_class="col"),
            ),
            Row(HTML(cost_table_html)),
            Row(
                Field("cash_paid", wrapper_class="col"),
                Field("credit_paid", wrapper_class="col"),
                Field("debit_paid", wrapper_class="col"),
                Field("check_paid", wrapper_class="col"),
            ),
            Row(Field("check_number", wrapper_class="col-3 ml-auto")),
            Row(Field("instructor", wrapper_class="col")),
            FormActions(
                Submit("submit", "Submit Changes"),
                Button(
                    "printout",
                    "Print",
                    css_class="btn btn-info",
                    onclick="window.open('printout')",
                ),
                delete_button,
                Button(
                    "cancel",
                    "Cancel",
                    css_class="btn btn-outline-secondary",
                    onclick="window.history.back()",
                ),
            ),
        )

    class Meta:
        date_input_ = forms.DateInput()
        date_input_.input_type = "date"
        model = models.Student
        fields = "__all__"
        widgets = {"start_date": date_input_}

    def save(self, commit=True):
        if self.is_valid():
            instance = super().save()

            if self.cleaned_data.get("how_other", None):
                new_how_choice = HowChoice(description=self.cleaned_data["how_other"])
                new_how_choice.save()
                self.instance.how_choices.add(new_how_choice)

            if self.cleaned_data.get("why_other", None):
                new_why_choice = WhyChoice(description=self.cleaned_data["why_other"])
                new_why_choice.save()
                self.instance.why_choices.add(new_why_choice)

            return instance

        return super().save(commit)


class CostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        if self.instance.pk is not None:
            delete_button = Button(
                "delete",
                "Delete",
                onclick='window.location.href="delete"',
                css_class="btn btn-outline-danger",
            )
        else:
            delete_button = None
        self.helper.layout = Layout(
            Row(Field("cost", wrapper_class="col")),
            Row(DateField("effective_date", wrapper_class="col")),
            FormActions(
                Submit("submit", "Submit"),
                delete_button,
                Button(
                    "cancel",
                    "Cancel",
                    css_class="btn btn-outline-secondary",
                    onclick="window.history.back()",
                ),
            ),
        )


class MonthlyCostForm(CostForm):
    class Meta:
        model = models.MonthlyCost
        fields = "__all__"


class RegistrationCostForm(CostForm):
    class Meta:
        model = models.RegistrationCost
        fields = "__all__"


class ChoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        if self.instance.pk is not None:
            delete_button = Button(
                "delete",
                "Delete",
                onclick='window.location.href="delete"',
                css_class="btn btn-outline-danger",
            )
        else:
            delete_button = None
        self.helper.layout = Layout(
            Row(Field("description", wrapper_class="col")),
            FormActions(
                Submit("submit", "Submit"),
                delete_button,
                Button(
                    "cancel",
                    "Cancel",
                    css_class="btn btn-outline-secondary",
                    onclick="window.history.back()",
                ),
            ),
        )


class HowChoiceForm(ChoiceForm):
    class Meta:
        model = models.HowChoice
        fields = "__all__"


class WhyChoiceForm(ChoiceForm):
    class Meta:
        model = models.WhyChoice
        fields = "__all__"


class InstructorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InstructorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        if self.instance.pk is not None:
            delete_button = Button(
                "delete",
                "Delete",
                onclick='window.location.href="delete"',
                css_class="btn btn-outline-danger",
            )
        else:
            delete_button = None
        self.helper.layout = Layout(
            Row(Field("name", wrapper_class="col")),
            FormActions(
                Submit("submit", "Submit"),
                delete_button,
                Button(
                    "cancel",
                    "Cancel",
                    css_class="btn btn-outline-secondary",
                    onclick="window.history.back()",
                ),
            ),
        )

    class Meta:
        model = models.Instructor
        fields = "__all__"
