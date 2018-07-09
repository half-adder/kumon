from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Button, Layout, HTML, ButtonHolder, Div, Field
from django import forms
from django.template.loader import render_to_string

from kumon_student_db.student_registration import models
from crispy_forms.helper import FormHelper


class Row(Div):
    css_class = "form-row"


class DateField(Field):
    def __init__(self, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)
        self.type = "date"


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        self.fields["registration_discount_percent"].label = "Reg. Discount %"

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
            Row(Field("email", wrapper_class="col")),
            Row(
                DateField("start_date", wrapper_class="col cost-input"),
                Field("primary_day", wrapper_class="col cost-input"),
            ),
            Row(
                Field("math_level", wrapper_class="col cost-input"),
                Field("reading_level", wrapper_class="col cost-input"),
            ),
            Row(
                Field("how_choices", wrapper_class="col"),
                Field("why_choices", wrapper_class="col"),
            ),
            Row(
                Field(
                    "registration_discount_percent", wrapper_class="col-3 cost-input"
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
            FormActions(
                Submit("submit", "Submit"),
                delete_button,
                Button("cancel", "Cancel", css_class="btn btn-outline-secondary"),
            ),
        )

    class Meta:
        date_input_ = forms.DateInput()
        date_input_.input_type = "date"
        model = models.Student
        fields = "__all__"
        widgets = {"start_date": date_input_}


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
            Row(
                Field("cost", wrapper_class="col"),
            ),
            Row(
                DateField("effective_date", wrapper_class="col"),
            ),
            FormActions(
                Submit("submit", "Submit"),
                delete_button,
                Button("cancel", "Cancel", css_class="btn btn-outline-secondary"),
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
