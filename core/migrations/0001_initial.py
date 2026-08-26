from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [("auth", "0012_alter_user_first_name_max_length")]
    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("donor","Donor"),("requester","Requester"),("both","Both")], default="both", max_length=20)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("city", models.CharField(blank=True, max_length=100)),
                ("bio", models.TextField(blank=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to="auth.user")),
            ],
        ),
        migrations.CreateModel(
            name="Listing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150)),
                ("description", models.TextField()),
                ("category", models.CharField(choices=[("food","Food"),("clothing","Clothing"),("medicine","Medicine"),("school","School Supplies"),("hygiene","Hygiene"),("household","Household"),("other","Other")], max_length=30)),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("city", models.CharField(max_length=100)),
                ("pickup_details", models.CharField(blank=True, max_length=255)),
                ("status", models.CharField(choices=[("available","Available"),("reserved","Reserved"),("completed","Completed")], default="available", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("donor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="listings", to="auth.user")),
            ],
            options={"ordering":["-created_at"]},
        ),
        migrations.CreateModel(
            name="Request",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("message", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("pending","Pending"),("accepted","Accepted"),("rejected","Rejected"),("completed","Completed")], default="pending", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("listing", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="requests", to="core.listing")),
                ("requester", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="requests", to="auth.user")),
            ],
            options={"ordering":["-created_at"]},
        ),
        migrations.AddConstraint(
            model_name="request",
            constraint=models.UniqueConstraint(fields=("listing","requester"), name="one_request_per_user_listing"),
        ),
    ]
