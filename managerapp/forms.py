from django import forms
from .models import Course, Trainer, Student, Country, State, District
from trainerapp.models import Rating

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'trainer', 'price']

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['name', 'email', 'username','password', 'type', 'skype_id','whatsapp']

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select Country")
    state = forms.ModelChoiceField(queryset=State.objects.none(), empty_label="Select State")
    district = forms.ModelChoiceField(queryset=District.objects.none(), empty_label="Select District")

    class Meta:
        model = Student
        fields = ['name', 'email', 'username', 'password', 'confirm_password', 'country', 'state', 'district']
    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['state'].queryset = Country.objects.none()
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id)
            except (ValueError, TypeError):
                self.fields['state'].queryset = State.objects.none()
        elif self.instance.pk:
            self.fields['state'].queryset = State.objects.filter(country_id=self.instance.country_id)

        self.fields['district'].queryset = Country.objects.none()
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['district'].queryset = District.objects.filter(state_id=state_id)
            except (ValueError, TypeError):
                self.fields['district'].queryset = District.objects.none()
        elif self.instance.pk:
            self.fields['district'].queryset = District.objects.filter(state_id=self.instance.state_id)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        return cleaned_data

class RatingForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)],
                                label="Rate your trainer")

    class Meta:
        model = Rating
        fields = ['rating', 'review']