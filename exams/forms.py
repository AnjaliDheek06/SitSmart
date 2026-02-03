from django import forms
from .models import Room, Exam 
from .models import InvigilatorAssignment
from users.models import CustomUser



class StudentUploadForm(forms.Form):
    excel_file = forms.FileField(
        label='Upload Excel File',
        widget=forms.ClearableFileInput(
            attrs={
                'accept': '.xls,.xlsx'
            }
        )
    )



class RoomForm(forms.ModelForm): 
    class Meta: 
        model = Room 
        fields = ['room_number', 'capacity', 'building', 'floor']


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'date', 'start_time', 'duration', 'course']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class InvigilatorAssignmentForm(forms.ModelForm): 
    class Meta: 
        model = InvigilatorAssignment 
        fields = ['invigilator', 'exam', 'room', 'duty_type'] 
     
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        # Show only invigilators in dropdown 
        self.fields['invigilator'].queryset = CustomUser.objects.filter(role='invigilator')