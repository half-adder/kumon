import logging
from datetime import date

from crispy_forms.bootstrap import FormActions, PrependedText
from crispy_forms.layout import Submit, Button, Layout, HTML, Div, Field
from django import forms
from django.forms import ChoiceField
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

        self.fields["instructor"].initial = 1
        self.fields["application"].widget = forms.HiddenInput()

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
                Field("email", wrapper_class="col"),
                Field("phone", wrapper_class="col", css_class="phone"),
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
                Field("how_choices", wrapper_class="col"),
                Field("why_choices", wrapper_class="col"),
            ),
            Row(
                Field("how_other", wrapper_class="col"),
                Field("why_other", wrapper_class="col"),
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
            Row(Field("instructor", wrapper_class="col")),
            Row(Field("application")),
            FormActions(
                Submit("submit", "Submit Changes"),
                Submit("print", "Print", css_class="btn btn-info"),
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


class StudentApplicationForm(forms.ModelForm):
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

    class Meta:
        model = models.LobbyStudent
        fields = "__all__"
        date_input_ = forms.DateInput()
        date_input_.input_type = "date"
        widgets = {"birth_date": date_input_}

    def __init__(self, *args, **kwargs):
        super(StudentApplicationForm, self).__init__(*args, **kwargs)

        if self.instance.pk is not None:
            delete_button = Button(
                "delete",
                "Delete",
                onclick='window.location.href="delete"',
                css_class="btn btn-outline-danger",
            )
        else:
            delete_button = None

        custom_labels = {
            "name": "Student Name",
            "apt_or_suite": "Apt. or Suite No.",
            "student_city": "City",
            "student_state_province": "State/Province",
            "student_zip_code": "Zip Code",
            "phone_number": "Student Phone #",
            "student_email": "Student Email",
            "parent_address": "Address",
            "parent_apt_or_suite": "Apt. or Suite No.",
            "parent_state_province": "State/Province",
            "parent_city": "City",
            "parent_zip_code": "Zip Code",
        }

        for k, v in custom_labels.items():
            self.fields[k].label = v

        next_five_years = [date.today().year + i for i in range(5)]
        school_year_choices = [
            "%d - %d" % (year, year_plus_one)
            for year, year_plus_one in zip(
                next_five_years, map(lambda x: x + 1, next_five_years)
            )
        ]
        SCHOOL_YEAR_CHOICES = list(zip(school_year_choices, school_year_choices))
        self.fields["school_year"] = ChoiceField(choices=SCHOOL_YEAR_CHOICES)
        self.fields["school_year"].default = SCHOOL_YEAR_CHOICES[0][0]

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("<h4>Student Info</h4><hr>"),
            Row(
                Field("name", wrapper_class="col"),
                DateField("birth_date", wrapper_class="col"),
            ),
            Row(
                Field("gender", wrapper_class="col"),
                Field("school_year", wrapper_class="col-3"),
                Field("grade", wrapper_class="col"),
            ),
            Row(Field("home_address", wrapper_class="col")),
            Row(
                Field("apt_or_suite", wrapper_class="col"),
                Field("student_city", wrapper_class="col"),
                Field("student_state_province", wrapper_class="col"),
                Field("student_zip_code", wrapper_class="col"),
            ),
            Row(
                Field("phone_number", wrapper_class="col", css_class="phone"),
                Field("student_email", wrapper_class="col"),
            ),
            Row(Field("school", wrapper_class="col")),
            HTML("<h4>Parent / Guardian Info</h4><hr>"),
            Row(
                Field("parent_relation", wrapper_class="col-3"),
                Field("parent_name", wrapper_class="col"),
            ),
            Row(
                Field("parent_email", wrapper_class="col"),
                Field("parent_home_phone_number", wrapper_class="col", css_class="phone"),
                Field("parent_mobile_phone_number", wrapper_class="col", css_class="phone"),
            ),
            HTML(
                """
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="id-checkbox-same-address">
                  <label class="form-check-label" for="id-checkbox-same-address">Address same as above</label>
                </div>
                """
            ),
            Row(Field("parent_address", wrapper_class="col parentAddressField")),
            Row(
                Field("parent_apt_or_suite", wrapper_class="col parentAddressField"),
                Field("parent_city", wrapper_class="col parentAddressField"),
                Field("parent_state_province", wrapper_class="col parentAddressField"),
                Field("parent_zip_code", wrapper_class="col parentAddressField"),
            ),
            HTML("<br><h4>Emergency Contact Info</h4><hr>"),
            Row(
                Field("emergency_name", wrapper_class="col"),
                Field("emergency_phone_number", wrapper_class="col", css_class="phone"),
            ),
            HTML("<hr>"),
            Row(
                Field("how_choices", wrapper_class="col"),
                Field("why_choices", wrapper_class="col"),
            ),
            Row(
                Field("how_other", wrapper_class="col"),
                Field("why_other", wrapper_class="col"),
            ),
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
