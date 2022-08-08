from django import forms
from django.core.exceptions import ValidationError
# gettext_lazy возвращает объект, который со временем можно превратить в строку и перевести.
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _  # Пока не работает, переводить не хочет. Разобраться позже.
import datetime     # Для проверки диапазона дат продления.
from .models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Введите дату между сегодняшним днём и 4 неделями позже (по умолчанию 3).")


    def clean_renewal_date(self):
        # form.cleaned_data возвращает словарь валидируемых полей ввода формы и их значений,
        # где в качестве объектов возвращаются строковые первичные ключи.
        data = self.cleaned_data['renewal_date']

        # Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
        if data < datetime.date.today():
            raise ValidationError(_('Неверная дата - Продление в прошое'))
            # raise ValidationError(_('Invalid date - renewal in past'))

        # Проверка того, что дата не выходит за "верхнюю" границу (+4 недели).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Неверная дата - Указано продление более, чем на 4 недели вперёд'))
            # raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Возвращаем "очищенные", проверенные, а затем приведённые к стандартным типам данные.
        return data




class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
       data = self.cleaned_data['due_back']

       #Проверка того, что дата не в прошлом
       if data < datetime.date.today():
           raise ValidationError(_('Неверная дата - Продление в прошое'))

       # Проверка того, что дата не выходит за "верхнюю" границу (+4 недели).
       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Неверная дата - Указано продление более, чем на 4 недели вперёд'))

       # Возвращаем "очищенные", проверенные, а затем приведённые к стандартным типам данные.
       return data

    class Meta:
        model = BookInstance
        fields = ['due_back', ]
        labels = {'due_back': _('Новая дата возврата '), }
        help_texts = {'due_back': _('Введите дату между сегодняшним днём и 4 неделями позже (по умолчанию 3).'), }