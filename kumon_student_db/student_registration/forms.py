from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Button, Layout, HTML, ButtonHolder, Div, Field
from django import forms
from django.template.loader import render_to_string

from kumon_student_db.student_registration import models
from crispy_forms.helper import FormHelper


class Row(Div):
    css_class = "form-row"


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        cost_table_html = render_to_string('student_registration/student_form_cost_table.html')
        self.helper.layout = Layout(
            Row(
                Field("name", wrapper_class="col"),
                Field("parent_name", wrapper_class="col"),
            ),
            Row(
                Field("email", wrapper_class='col')
            ),
            Row(
                Field("start_date", wrapper_class='col cost-input'),
                Field("primary_day", wrapper_class='col cost-input'),
            ),
            Row(
                Field("math_level", wrapper_class='col'),
                Field("reading_level", wrapper_class='col'),
            ),
            Row(
                Field("how_choices", wrapper_class='col'),
                Field("why_choices", wrapper_class='col'),
            ),
            Row(
                Field("registration_discount_percent", wrapper_class='col-4 cost-input'),
                Field("registration_discount_reason", wrapper_class='col')
            ),
            Row(
                HTML(cost_table_html)
            ),
            Row(
                Field('cash_paid', wrapper_class='col'),
                Field('credit_paid', wrapper_class='col'),
                Field('debit_paid', wrapper_class='col'),
                Field('check_paid', wrapper_class='col'),
            ),
            Row(
                Field('check_number', wrapper_class='col-3 ml-auto')
            ),
            FormActions(
                Submit("submit", "Submit"),
                Button("cancel", "Cancel", css_class="btn btn-outline-secondary"),
            ),
        )
        if self.instance.pk is not None:
            self.helper.add_input(
                Button(
                    "delete",
                    "Delete",
                    onclick='window.location.href="{}"'.format("delete"),
                )
            )

    class Meta:
        model = models.Student
        fields = "__all__"
