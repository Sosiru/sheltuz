# Generated by Django 5.0 on 2023-12-25 10:49

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('synced', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('transaction_no', models.CharField(default=uuid.uuid4, max_length=50, unique=True)),
                ('phone_number', models.CharField(max_length=12)),
                ('checkout_request_id', models.CharField(max_length=200)),
                ('reference', models.CharField(blank=True, max_length=40)),
                ('description', models.TextField(blank=True, null=True)),
                ('amount', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[(1, 'Pending'), (0, 'Complete')], default=1, max_length=15)),
                ('receipt_no', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ip', models.CharField(blank=True, max_length=200, null=True)),
                ('state', models.ForeignKey(default=uuid.UUID('5ac61057-dce2-4d53-8dca-eff4e94c473d'), on_delete=django.db.models.deletion.CASCADE, to='base.state')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]