# Generated by Django 2.2.9 on 2020-02-12 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=255, verbose_name='카테고리명')),
                ('univ_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='account.Univ', verbose_name='대학')),
            ],
        ),
        migrations.CreateModel(
            name='Posting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('max_num', models.IntegerField()),
                ('timer', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=20)),
                ('posting_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag', to='core.Posting')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.URLField()),
                ('title', models.CharField(max_length=255, verbose_name='가게명')),
                ('star', models.CharField(max_length=255, verbose_name='별점')),
                ('min_price', models.PositiveIntegerField(verbose_name='최소주문금액')),
                ('del_time', models.PositiveIntegerField(verbose_name='배달시간')),
                ('store_url', models.URLField()),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store', to='core.Category', verbose_name='카테고리명')),
            ],
        ),
        migrations.AddField(
            model_name='posting',
            name='store_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posting', to='core.Store'),
        ),
        migrations.AddField(
            model_name='posting',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
