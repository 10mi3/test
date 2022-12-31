from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField

USER_CHOICES = [
    ('RESPONSIBLE', 'Responsible'),
    ('ADMIN', 'Admin'),
    ('DOCTOR', 'Doctor'),
    ('PATIENT', 'Patient'), ('CASHIER', 'Cashier'),
    ('RECEPTIONIST', 'Receptionist'),
    ('HR', 'HR')
]

DAYS_CHOICES = [
    ('MONDAY', 'MONDAY'),
    ('TUESDAY', 'TUESDAY'),
    ('WEDNESDAY', 'WEDNESDAY'),
    ('FRIDAY', 'FRIDAY'),
    ('THURSDAY', 'THURSDAY'),
    ('SATURDAY', 'SATURDAY'),
    ('SUNDAY', 'SUNDAY')
]
typeMOV_CHOICES = [
    ('ENTRY', 'Entry'),
    ('EXIT', 'Exit')
]
BILL_CHOICES = [
    ('YES', 'Yes'),
    ('NO', 'No')
]
BILLS_CHOICES = [
    ('PHARMACY', 'Pharmacy'),
    ('MEDICAL_ACT', 'Medical_act')
]
BILL_SHAPE_CHOICES = [
    ('ORDINANCE', 'Ordinance'),
    ('CLASSIC', 'Classic')
]

POSITION_CHOICES = [
    ('INTERNAL', 'INTERNAL'),
    ('EXTERNAL', 'EXTERNAL')
]
CAT_ANT_CHOICES = [
    ('MEDICAL', 'Medical'),
    ('SURGICAL', 'Surgical'),
    ('FAMILY', 'Family'),
    ('DRUG INTOLERANCE', 'Drug intolerance'),
    ('VACCINATION', 'Vaccination'),
    ('MENTION PART', 'Mention part')
]
PATIENT_SHAPE_CHOICES = [
    ('EMPLOYEE', 'EMPLOYEE'),
    ('INDIGENT', 'INDIGENT'),
    ('NORMAL', 'NORMAL'),
    ('COVERED', 'COVERED')
]


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    createdAt = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=255, blank=True)
    dateNaiss = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    child = models.CharField(max_length=255, blank=True)
    date_id = models.CharField(max_length=255, blank=True)
    number_id = models.CharField(max_length=255, blank=True)
    maritalStatus = models.CharField(max_length=255, blank=True)
    emergency_contact = models.CharField(max_length=255, blank=True)
    emergency_name = models.CharField(max_length=255, blank=True)
    mother_name = models.CharField(max_length=255, blank=True)
    type_id = models.CharField(max_length=255, blank=True)
    religion = models.CharField(max_length=255, blank=True)
    pathologies = models.CharField(max_length=255, blank=True)
    allergies = models.CharField(max_length=255, blank=True)
    blood_group = models.CharField(max_length=255, blank=True)
    weight = models.CharField(max_length=255, blank=True)
    electrophoresis = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=255, blank=True)
    bpm = models.CharField(max_length=255, blank=True)
    temperature = models.CharField(max_length=255, blank=True)
    padiasto = models.CharField(max_length=255, blank=True)
    pasysto = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    other_phone = models.CharField(max_length=255, blank=True)
    age = models.CharField(max_length=255, blank=True)
    insurance_name = models.CharField(max_length=255, blank=True)
    insurance_number = models.CharField(max_length=255, blank=True)
    shape = models.CharField(choices=PATIENT_SHAPE_CHOICES, max_length=255)
    address = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=255, blank=True, default="PAT0001")
    email = models.EmailField(max_length=255, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'patient'
        ordering = ('-createdAt',)


# Create your models here.


class Expenses_nature(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True, default="NAT0001")
    type = models.CharField(max_length=255, choices=typeMOV_CHOICES, )
    name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'expenses_nature'
        ordering = ('-createdAt',)


class Medical_areas(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True, default="DOM0001")
    name = models.CharField(max_length=255, null=True, blank=True)
    normal = models.CharField(max_length=255, null=True, blank=True)
    covered = models.CharField(max_length=255, null=True, blank=True)
    employee = models.CharField(max_length=255, null=True, blank=True)
    indigent = models.CharField(max_length=255, null=True, blank=True)
    number_account = models.CharField(max_length=255, null=True, blank=True)
    quote_internal = models.CharField(max_length=255, null=True, blank=True)
    quote_external = models.CharField(max_length=255, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'medical_areas'
        ordering = ('-createdAt',)


class Medical_act(models.Model):
    medical_areas = models.ForeignKey(Medical_areas, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="ACT0001")
    name = models.CharField(max_length=255, null=True, blank=True)
    coefficient = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    quote_internal = models.CharField(max_length=255, null=True, blank=True)
    quote_external = models.CharField(max_length=255, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'medical_act'
        ordering = ('-createdAt',)


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'manufacturer'
        ordering = ('-createdAt',)


class Provider(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'provider'
        ordering = ('-createdAt',)


class Category(models.Model):
    medical_areas = models.ForeignKey(Medical_areas, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="CAT0001")
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    billable = models.CharField(max_length=255, choices=BILL_CHOICES, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'categories'
        ordering = ('-createdAt',)


class Shape(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True, default="FOR0001")
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'shape'
        ordering = ('-createdAt',)


class DCI(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True, default="DCI0001")
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'dci'
        ordering = ('-createdAt',)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    shape = models.ForeignKey(Shape, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    barcode = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="PRD0001")
    dci1 = models.ForeignKey(DCI, on_delete=models.CASCADE, null=True, related_name='dci1')
    dci2 = models.ForeignKey(DCI, on_delete=models.CASCADE, null=True, related_name='dci2')
    dosage = models.CharField(max_length=255, null=True, blank=True)
    conditioning = models.CharField(max_length=255, null=True, blank=True)
    margin = models.FloatField(default=0, null=True, blank=True)
    public_price = models.FloatField(default=0, null=True, blank=True)
    purchase_price = models.FloatField(default=0, null=True, blank=True)
    # expiry_date = models.DateTimeField()
    cmup = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'products'
        ordering = ('-createdAt',)


class Hospital(models.Model):
    # depart = models.ManyToManyField(Departments, related_name='departments')
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField()
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    slogan = models.CharField(max_length=255, null=True, blank=True)
    taxpayer = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=1255, blank=True, null=True)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'hospital'
        ordering = ('-createdAt',)

class Departments(models.Model):
    # hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'departments'
        ordering = ('-createdAt',)
class Services(models.Model):
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'services'
        ordering = ('-createdAt',)

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    intervention_days = MultiSelectField(choices=DAYS_CHOICES, max_length=255)
    position = models.CharField(choices=POSITION_CHOICES, max_length=255)
    createdAt = models.DateTimeField(default=timezone.now)
    updateAt = models.DateTimeField(auto_now=True)
    coef = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=255, blank=True, default="DCT0001")
    name = models.CharField(max_length=255, blank=True)
    dateNaiss = models.CharField(max_length=255, blank=True)
    dateService = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    speciality = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True)
    deleted = models.BooleanField(default=False)
    deletedAt = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'doctor'
        ordering = ('-createdAt',)

class User(AbstractUser):
    code = models.CharField(max_length=255, null=False, default="USR0001")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=255, unique=True, null=False)
    is_active = models.BooleanField(default=True, db_column='is_active')
    role = models.CharField(choices=USER_CHOICES, max_length=255)
    createdAt = models.DateTimeField(default=timezone.now)
    updateAt = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deletedAt = models.DateTimeField(null=True, blank=True)

    # objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ('-createdAt',)

class Storage_depots(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True, default="DEP0001")
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    name_responsible = models.CharField(max_length=255, null=True, blank=True)
    default_depot = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'storage_depots'
        ordering = ('-createdAt',)


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="RDV0001")
    problem = models.CharField(max_length=255, null=True, blank=True)
    start_appointment_date = models.CharField(max_length=255, null=True, blank=True)
    end_appointment_date = models.CharField(max_length=255, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'appointment'
        ordering = ('-createdAt',)


class Ordinance(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="PRE0001")
    medication = models.CharField(max_length=255, null=True, blank=True)
    period_medication = models.CharField(max_length=255, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'ordinance'
        ordering = ('-createdAt',)

class Examination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="EXAM0001")
    description_exam = models.CharField(max_length=255, null=True, blank=True)
    results_exam = models.CharField(max_length=255, null=True, blank=True)
    temperature = models.CharField(max_length=255, null=True, blank=True)
    tension = models.CharField(max_length=255, null=True, blank=True)
    perimeter = models.CharField(max_length=255, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'Examination'
        ordering = ('-createdAt',)

class Background(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="BACK0001")
    description_back = models.CharField(max_length=255, null=True, blank=True)
    category_back = models.CharField(max_length=255, null=True, blank=True, choices=CAT_ANT_CHOICES)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'background'
        ordering = ('-createdAt',)
class Consultation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    ordinance = models.OneToOneField(Ordinance, on_delete=models.CASCADE, null=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True)
    background = models.ForeignKey(Background, on_delete=models.CASCADE, null=True)
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="CON0001")
    reason = models.CharField(max_length=255, null=True, blank=True)
    diagnostic = models.CharField(max_length=255, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'consultation'
        ordering = ('-createdAt',)


class Prescription(models.Model):
    ordinance = models.ForeignKey(Ordinance, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    product_qte = models.CharField(max_length=255, null=True, blank=True)
    product_nbr_fois = models.CharField(max_length=255, null=True, blank=True)
    product_form = models.CharField(max_length=255, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'Prescription'
        ordering = ('-createdAt',)


class Suppliers(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="FOU0001")
    phone_representative = models.CharField(max_length=255, null=True, blank=True)
    name_representative = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_column='is_active')
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'suppliers'
        ordering = ('-createdAt',)


class Stock_movement(models.Model):
    storage_depots = models.ForeignKey(Storage_depots, on_delete=models.CASCADE, null=True)
    type_movement = models.CharField(max_length=255, choices=typeMOV_CHOICES)
    movement_value = models.IntegerField(default=0)
    reason_movement = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="STM0001")
    date_movement = models.DateTimeField(verbose_name="Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'stock_movement'
        ordering = ('-id',)


class Inventory(models.Model):
    storage_depots = models.ForeignKey(Storage_depots, on_delete=models.CASCADE, null=True)
    reason_inventory = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="IVT0001")
    date_inventory = models.DateTimeField(verbose_name="Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'inventory'
        ordering = ('-id',)


class Supplies(models.Model):
    suppliers = models.ForeignKey(Suppliers, on_delete=models.CASCADE, null=True)
    storage_depots = models.ForeignKey(Storage_depots, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="APP0001")
    additional_info = models.CharField(max_length=255, null=True, blank=True)
    reference_no = models.CharField(max_length=255, null=True, blank=True)
    arrival_date = models.DateField()
    supply_amount = models.IntegerField(default=0)
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'supplies'
        ordering = ('-id',)


class DetailsSupplies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    storage_depots = models.ForeignKey(Storage_depots, on_delete=models.CASCADE, null=True)
    supplies = models.ForeignKey(Supplies, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    arrival_price = models.IntegerField(default=0)
    cmup = models.CharField(max_length=255, null=True, blank=True)
    createdAt = models.DateField()
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'details_supplies'
        ordering = ('-createdAt',)


class DetailsStock(models.Model):
    storage_depots = models.ForeignKey(Storage_depots, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    qte_stock = models.IntegerField(default=0, blank=True)
    cmup = models.FloatField(default=0, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'details_stock'
        ordering = ('-createdAt',)


class DetailsStock_movement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    storage_depots = models.ForeignKey(Storage_depots, on_delete=models.CASCADE, null=True)
    stock_movement = models.ForeignKey(Stock_movement, on_delete=models.CASCADE, null=True)
    details_stock = models.ForeignKey(DetailsStock, on_delete=models.CASCADE, null=True)
    total_amount = models.FloatField(default=0, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    unit_price = models.FloatField(default=0, null=True, blank=True)
    type_movement = models.CharField(max_length=255, choices=typeMOV_CHOICES, blank=True)
    createdAt = models.DateField()
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'details_stock_movement'
        ordering = ('-createdAt',)


class DetailsInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    storage_depots = models.ForeignKey(Storage_depots, on_delete=models.CASCADE, null=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)
    details_stock = models.ForeignKey(DetailsStock, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(default=0, null=True, blank=True)
    amount_adjusted = models.FloatField(default=0, null=True, blank=True)
    cmup = models.FloatField(default=0, null=True, blank=True)
    quantity_stock = models.IntegerField(default=0)
    quantity_adjusted = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'details_inventory'
        ordering = ('-createdAt',)


class Cash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="CSH0001")
    cash_fund = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_column='is_active')
    open_date = models.DateTimeField(auto_now_add=True, verbose_name="Open Date")
    close_date = models.DateTimeField(verbose_name="Close Date", null=True, blank=True)

    class Meta:
        db_table = 'cash'
        ordering = ('-id',)


class Cash_movement(models.Model):
    cash = models.ForeignKey(Cash, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="CMV0001")
    type = models.CharField(max_length=255, choices=typeMOV_CHOICES, )
    name = models.CharField(max_length=255, null=True, blank=True)
    motive = models.CharField(max_length=255, null=True, blank=True)
    name_movement = models.CharField(max_length=255, null=True, blank=True)
    amount_movement = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'cash_movement'
        ordering = ('-createdAt',)


class Bills(models.Model):
    storage_depots = models.ForeignKey(Storage_depots, on_delete=models.CASCADE, null=True, blank=True)
    cash = models.ForeignKey(Cash, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    advance = models.IntegerField(default=0)
    net_payable = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    additional_info = models.CharField(max_length=255, null=True, blank=True)
    bill_type = models.CharField(choices=BILLS_CHOICES, max_length=255)
    bill_shape = models.CharField(choices=BILL_SHAPE_CHOICES, max_length=255, null=True, blank=True)
    patient_type = models.CharField(choices=PATIENT_SHAPE_CHOICES, max_length=255)
    code = models.CharField(max_length=255, null=True, blank=True, default="FAC000001")
    bills_date = models.DateField()
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'bills'
        ordering = ('-id',)


class PatientSettlement(models.Model):
    cash = models.ForeignKey(Cash, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    payment = models.IntegerField(default=0)
    wordings = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True, default="RGP00001")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'patient_settlement'
        ordering = ('-id',)


class DetailsBills(models.Model):
    cash = models.ForeignKey(Cash, on_delete=models.CASCADE, null=True, blank=True)
    storage_depots = models.ForeignKey(Storage_depots, on_delete=models.CASCADE, null=True, blank=True)
    bills = models.ForeignKey(Bills, on_delete=models.CASCADE, null=True, blank=True)
    details_stock = models.ForeignKey(DetailsStock, on_delete=models.CASCADE, null=True)
    medical_act = models.ForeignKey(Medical_act, on_delete=models.CASCADE, null=True, blank=True)
    quantity_served = models.IntegerField(default=0)
    quantity_ordered = models.IntegerField(default=0)
    amount_net = models.IntegerField(default=0)
    amount_gross = models.IntegerField(default=0)
    pun = models.IntegerField(default=0)
    pub = models.IntegerField(default=0)
    delivery = models.FloatField(default=0, null=True, blank=True)
    createdAt = models.DateField()
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        db_table = 'details_bills'
        ordering = ('-id',)
