# Generated by Django 4.0.6 on 2022-08-07 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name']},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title', 'author']},
        ),
        migrations.AddField(
            model_name='bookinstance',
            name='borrower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(blank=True, null=True, verbose_name='Дата смерти'),
        ),
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.TextField(help_text='Введите краткое описание книги', max_length=1000, verbose_name='Аннотация'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название книги'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='due_back',
            field=models.DateField(blank=True, null=True, verbose_name='Дата возврата'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Уникальный идентификатор этого экземпляра книги во всей библиотеке', primary_key=True, serialize=False, verbose_name='ID в библиотеке'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='imprint',
            field=models.CharField(max_length=200, verbose_name='Импринт'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('т', 'Техническое обслуживание'), ('в', 'Взято'), ('д', 'Доступно'), ('з', 'Зарезервировано')], default='т', help_text='Статус книги', max_length=1, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Введите жанр книги (научная фантастика, фэнтази, юмор и т.д.)', max_length=200, verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(help_text='Введите язык книги (русский, английский, немецкий, французский и т. д.)', max_length=200, verbose_name='Язык'),
        ),
    ]