# Generated by Django 4.2.10 on 2024-05-07 18:12

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Administrator",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("email", models.CharField(max_length=200)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(default="", max_length=200)),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("credits", models.PositiveIntegerField()),
                ("department", models.CharField(default="", max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="CS_Major_Core",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("CSCI1101", models.CharField(default="CSCI1101", max_length=11)),
                ("CSCS1102", models.CharField(default="CSCS1102", max_length=11)),
                ("CSCI2243", models.CharField(default="CSCI2243", max_length=11)),
                ("CSCI2244", models.CharField(default="CSCI2244", max_length=11)),
                ("CSCI2271", models.CharField(default="CSCI2271", max_length=11)),
                ("CSCI2272", models.CharField(default="CSCI2272", max_length=11)),
                ("CSCI3383", models.CharField(default="CSCI3383", max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name="Econ_major",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ECON1101", models.CharField(default="ECON1101", max_length=11)),
                ("ECON1151", models.CharField(default="ECON1151", max_length=11)),
                (
                    "Micro",
                    models.CharField(
                        choices=[("ECON2201", "ECON2201"), ("ECON2203", "ECON2203")],
                        default="ECON2201",
                        max_length=11,
                    ),
                ),
                (
                    "Macro",
                    models.CharField(
                        choices=[("ECON2202", "ECON2202"), ("ECON2204", "ECON2204")],
                        default="ECON2202",
                        max_length=11,
                    ),
                ),
                ("ECON2228", models.CharField(default="ECON2228", max_length=11)),
                ("econ_2200_credits", models.IntegerField(default=6)),
                ("econ_3000_credits", models.IntegerField(default=12)),
                ("MATH1102", models.CharField(default="MATH1102", max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name="ScienceComponent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "Physics",
                    models.CharField(
                        choices=[
                            ("PHYS2100", "PHYS2100"),
                            ("PHYS2050", "PHYS2050"),
                            ("PHYS2101", "PHYS2101"),
                            ("PHYS2051", "PHYS2051"),
                        ],
                        default="",
                        max_length=11,
                    ),
                ),
                ("physics_credits", models.IntegerField(default=6)),
                (
                    "Biology",
                    models.CharField(
                        choices=[
                            ("BIOL2010", "BIOL2010"),
                            ("BIOL2000", "BIOL2000"),
                            ("BIOL2040", "BIOL2040"),
                            ("BIOL1300", "BIOL1300"),
                        ],
                        default="",
                        max_length=11,
                    ),
                ),
                ("biology_credits", models.IntegerField(default=9)),
                ("chemisyry_credits", models.IntegerField(default=8)),
                (
                    "Chemistry",
                    models.CharField(
                        choices=[
                            ("CHEM1011", "CHEM1011"),
                            ("CHEM1012", "CHEM1012"),
                            ("CHEM1013", "CHEM1013"),
                            ("CHEM1014", "CHEM1014"),
                            ("CHEM1117", "CHEM1117"),
                            ("CHEM1118", "CHEM1118"),
                            ("CHEM1119", "CHEM1119"),
                            ("CHEM1120", "CHEM1120"),
                        ],
                        default="",
                        max_length=11,
                    ),
                ),
                (
                    "Environmental",
                    models.CharField(
                        choices=[
                            ("EESC1132", "EESC1132"),
                            ("EESC2202", "EESC2202"),
                            ("EESC2203", "EESC2203"),
                            ("EESC2204", "EESC2204"),
                            ("EESC2205", "EESC2205"),
                            ("EESC2206", "EESC2206"),
                            ("EESC2207", "EESC2207"),
                            ("EESC2208", "EESC2208"),
                        ],
                        default="",
                        max_length=11,
                    ),
                ),
                ("environmental_credits", models.IntegerField(default=7)),
                ("environmental_elective_credits", models.IntegerField(default=3)),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("email", models.CharField(max_length=200)),
                ("school", models.CharField(max_length=200)),
                ("department", models.CharField(max_length=200)),
                ("start", models.CharField(max_length=200)),
                ("major1", models.CharField(max_length=200)),
                ("major2", models.CharField(blank=True, max_length=200)),
                ("minor1", models.CharField(blank=True, max_length=200)),
                ("minor2", models.CharField(blank=True, max_length=200)),
                ("first_login_completed", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Plan",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(default="Main", max_length=200)),
                ("freshman_fall", models.TextField(blank=True, default="")),
                ("freshman_spring", models.TextField(blank=True, default="")),
                ("sophomore_fall", models.TextField(blank=True, default="")),
                ("sophomore_spring", models.TextField(blank=True, default="")),
                ("junior_fall", models.TextField(blank=True, default="")),
                ("junior_spring", models.TextField(blank=True, default="")),
                ("senior_fall", models.TextField(blank=True, default="")),
                ("senior_spring", models.TextField(blank=True, default="")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.student"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CS_Major_BS",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("MATH1103", models.CharField(default="MATH1103", max_length=11)),
                ("MATH2202", models.CharField(default="MATH2202", max_length=11)),
                ("MATH2210", models.CharField(default="MATH2210", max_length=11)),
                ("CSCI2267", models.CharField(default="CSCI2267", max_length=11)),
                ("cs_3000", models.CharField(default="", max_length=11)),
                ("elective_credits", models.IntegerField(default=12)),
                ("math_elective_credits", models.IntegerField(default=3)),
                ("math_3000", models.CharField(default="", max_length=11)),
                ("ethics_credits", models.IntegerField(default=3)),
                (
                    "core",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.cs_major_core",
                    ),
                ),
                (
                    "science_component",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.sciencecomponent",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CS_Major_BA",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("MATH1103", models.CharField(default="MATH1103", max_length=11)),
                ("MATH2202", models.CharField(default="MATH2202", max_length=11)),
                ("cs_2000_credits", models.IntegerField(default=3)),
                ("cs_3000_credits", models.IntegerField(default=9)),
                (
                    "core",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.cs_major_core",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Advisor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("email", models.CharField(max_length=200)),
                ("school", models.CharField(max_length=200)),
                ("department", models.CharField(max_length=200)),
                (
                    "students",
                    models.ManyToManyField(
                        blank=True, related_name="advisors", to="user.student"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
