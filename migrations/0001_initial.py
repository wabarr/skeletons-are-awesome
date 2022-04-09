# Generated by Django 3.2.12 on 2022-04-09 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('axial_appendicular', models.CharField(choices=[('axial', 'Axial'), ('appendicular', 'Appendicular')], max_length=100)),
                ('region', models.CharField(blank=True, choices=[('skull', 'Skull'), ('thorax', 'Thorax'), ('forelimb', 'Forelimb'), ('hindlimb', 'Hindlimb')], max_length=100)),
                ('subregion', models.CharField(blank=True, choices=[('cranium', 'Cranium'), ('middle ear', 'Middle ear'), ('mandible', 'Mandible'), ('ribs', 'Ribs'), ('hyoid', 'Hyoid'), ('sternum', 'Sternum'), ('vertebral Column', 'Vertebral Column'), ('shoulder Girdle', 'Shoulder Girdle'), ('proximal Forelimb', 'Proximal Forelimb'), ('distal Forelimb', 'Distal Forelimb'), ('wrist', 'Wrist'), ('manus (hand)', 'Manus (Hand)'), ('pelvic girdle', 'Pelvic Girdle'), ('proximal hindlimb', 'Proximal Hindlimb'), ('distal hindlimb', 'Distal Hindlimb'), ('ankle', 'Ankle'), ('pes (foot)', 'Pes (Foot)')], max_length=100)),
                ('numerical_identifier', models.PositiveIntegerField(blank=True, null=True)),
                ('positional_identifier', models.CharField(blank=True, choices=[('proximal', 'Proximal'), ('intermediate', 'Intermediate'), ('distal', 'Distal')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorshortstring', models.CharField(help_text='Author name as it would appear in an in-text citation.', max_length=100)),
                ('year', models.IntegerField()),
                ('journal', models.CharField(blank=True, max_length=100)),
                ('volume', models.IntegerField(blank=True, null=True)),
                ('issue', models.IntegerField(blank=True, null=True)),
                ('pages', models.CharField(blank=True, max_length=20)),
                ('doi', models.CharField(blank=True, max_length=100)),
                ('dataEntryComplete', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'repositories',
            },
        ),
        migrations.CreateModel(
            name='Scanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('nickname', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Skeleton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_code', models.CharField(blank=True, max_length=100)),
                ('specimen_number', models.PositiveIntegerField()),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skeletons.repository')),
            ],
        ),
        migrations.CreateModel(
            name='Taxon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kingdom', models.CharField(blank=True, choices=[('Animalia', 'Animalia')], default='Animalia', max_length=100)),
                ('phylum', models.CharField(blank=True, choices=[('Chordata', 'Chordata')], default='Chordata', max_length=100)),
                ('tclass', models.CharField(blank=True, choices=[('Mammalia', 'Mammalia'), ('Reptilia', 'Reptilia'), ('Pisces', 'Pisces'), ('Aves', 'Aves'), ('Amphibia', 'Amphibia')], max_length=100, verbose_name='class')),
                ('order', models.CharField(blank=True, choices=[('AFROSORICIDA', 'AFROSORICIDA'), ('ARTIODACTYLA', 'ARTIODACTYLA'), ('CARNIVORA', 'CARNIVORA'), ('PERISSODACTYLA', 'PERISSODACTYLA'), ('PRIMATES', 'PRIMATES'), ('PROBOSCIDEA', 'PROBOSCIDEA'), ('RODENTIA', 'RODENTIA'), ('AFROSORICIDA', 'AFROSORICIDA'), ('CETACEA', 'CETACEA'), ('CHIROPTERA', 'CHIROPTERA'), ('CINGULATA', 'CINGULATA'), ('DASYUROMORPHIA', 'DASYUROMORPHIA'), ('DERMOPTERA', 'DERMOPTERA'), ('DIDELPHIMORPHIA', 'DIDELPHIMORPHIA'), ('DIPROTODONTIA', 'DIPROTODONTIA'), ('ERINACEOMORPHA', 'ERINACEOMORPHA'), ('HYRACOIDEA', 'HYRACOIDEA'), ('LAGOMORPHA', 'LAGOMORPHA'), ('MACROSCELIDEA', 'MACROSCELIDEA'), ('MICROBIOTHERIA', 'MICROBIOTHERIA'), ('MONOTREMATA', 'MONOTREMATA'), ('NOTORYCTEMORPHIA', 'NOTORYCTEMORPHIA'), ('PAUCITUBERCULATA', 'PAUCITUBERCULATA'), ('PERAMELEMORPHIA', 'PERAMELEMORPHIA'), ('PHOLIDOTA', 'PHOLIDOTA'), ('PILOSA', 'PILOSA'), ('SCANDENTIA', 'SCANDENTIA'), ('SIRENIA', 'SIRENIA'), ('SORICOMORPHA', 'SORICOMORPHA'), ('TUBULIDENTATA', 'TUBULIDENTATA')], max_length=100)),
                ('family', models.CharField(blank=True, max_length=100)),
                ('subfamily', models.CharField(blank=True, max_length=100)),
                ('tribe', models.CharField(blank=True, choices=[('Tragelaphini', 'Tragelaphini'), ('Cephalophini', 'Cephalophini'), ('Bovini', 'Bovini'), ('Hippotragini', 'Hippotragini'), ('Reduncini', 'Reduncini'), ('Alcelaphini', 'Alcelaphini'), ('Antilopini', 'Antilopini'), ('Aepycerotini', 'Aepycerotini'), ('Neotragini', 'Neotragini'), ('Colobini', 'Colobini'), ('Papionini', 'Papionini'), ('Hominini', 'Hominini'), ('Boselaphini', 'Boselaphini'), ('Caprini', 'Caprini'), ('Giraffini', 'Giraffini'), ('Palaeotragini', 'Palaeotragini'), ('Sivatheriini', 'Sivatheriini'), ('Kubanochoerini', 'Kubanochoerini'), ('Nyanzachoerini', 'Nyanzachoerini'), ('Phacochoerini', 'Phacochoerini'), ('Potamochoerini', 'Potamochoerini'), ('Homotheriini', 'Homotheriini'), ('Metailurini', 'Metailurini'), ('Smilodontini', 'Smilodontini'), ('Enhydrini', 'Enhydrini'), ('Protoxerini', 'Protoxerini')], max_length=100)),
                ('genus', models.CharField(blank=True, max_length=100, verbose_name='genus')),
                ('species', models.CharField(blank=True, max_length=100, verbose_name='species')),
                ('infraspecificEpithet', models.CharField(blank=True, max_length=100)),
                ('identificationQualifier', models.CharField(blank=True, help_text='e.g. aff. or cf.', max_length=100)),
                ('extant', models.BooleanField(default=True)),
                ('commonName', models.CharField(blank=True, max_length=100)),
                ('synonyms', models.CharField(blank=True, max_length=2000)),
                ('taxonRank', models.CharField(choices=[('tclass', 'class'), ('order', 'order'), ('family', 'family'), ('subfamily', 'subfamily'), ('tribe', 'tribe'), ('genus', 'genus'), ('species', 'species'), ('subspecies', 'subspecies'), ('infraorder', 'infraorder'), ('subgenus', 'subgenus'), ('suborder', 'suborder'), ('superfamily', 'superfamily')], max_length=100)),
                ('ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='skeletons.reference')),
            ],
            options={
                'verbose_name_plural': 'Taxa',
            },
        ),
        migrations.CreateModel(
            name='Specimen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('side', models.CharField(blank=True, choices=[('left', 'Left'), ('right', 'Right')], max_length=100)),
                ('specimen_label', models.CharField(blank=True, help_text='identifying label physically inked on specimen', max_length=100)),
                ('scan_filename', models.CharField(blank=True, max_length=200)),
                ('scanned_by', models.CharField(help_text='the name of the person who did the scan', max_length=100)),
                ('date_scanned', models.DateField(blank=True, null=True)),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skeletons.element')),
                ('machine', models.ForeignKey(help_text='the scanner used to make the scan', on_delete=django.db.models.deletion.CASCADE, to='skeletons.scanner')),
                ('skeleton', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skeletons.skeleton')),
            ],
        ),
        migrations.AddField(
            model_name='skeleton',
            name='taxon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skeletons.taxon'),
        ),
        migrations.AddConstraint(
            model_name='element',
            constraint=models.UniqueConstraint(fields=('positional_identifier', 'name', 'numerical_identifier', 'subregion'), name='unique element'),
        ),
        migrations.AddConstraint(
            model_name='taxon',
            constraint=models.UniqueConstraint(fields=('tclass', 'order', 'family', 'subfamily', 'tribe', 'genus', 'species', 'infraspecificEpithet', 'taxonRank', 'identificationQualifier'), name='unique taxon'),
        ),
    ]
