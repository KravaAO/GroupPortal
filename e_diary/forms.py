from django.forms import ModelForm , Form,IntegerField,CharField

class add_grade(ModelForm):
    grade = IntegerField()
    messege = CharField()

