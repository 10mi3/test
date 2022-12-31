from django import forms
from hospital.models import User, Hospital, Departments, Medical_areas, Medical_act, Patient, Doctor, \
    Ordinance, Appointment, Cash, Storage_depots, Expenses_nature, Cash_movement, Category, Shape, Product, \
    Supplies, Suppliers, DetailsSupplies, DetailsBills, PatientSettlement, DetailsStock, Stock_movement, \
    DetailsStock_movement, Inventory, DetailsInventory, Consultation, Background, Ordinance, Prescription, Examination, \
    DCI
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField
from hospital.models import Bills

DAYS_CHOICES = [
    ('MONDAY', 'MONDAY'),
    ('TUESDAY', 'TUESDAY'),
    ('WEDNESDAY', 'WEDNESDAY'),
    ('FRIDAY', 'FRIDAY'),
    ('THURSDAY', 'THURSDAY'),
    ('SATURDAY', 'SATURDAY'),
    ('SUNDAY', 'SUNDAY')
]


class UserForm(forms.ModelForm):
    is_active = forms.BooleanField(initial=True, required=False)
    username = forms.CharField(required=True)
    createdAt = forms.CharField(required=False)
    code = forms.CharField(required=False)
    role = forms.CharField(required=False)
    password = forms.CharField(required=True, widget=forms.PasswordInput, min_length=5, max_length=255)

    class Meta:
        model = User
        fields = ('username', 'role', 'is_active', 'password', 'deleted','code')


class CashForm(forms.ModelForm):
    code = forms.CharField(required=False)
    is_active = forms.BooleanField(initial=True, required=False)
    cash_fund = forms.CharField(required=True)
    createdAt = forms.CharField(required=False)

    class Meta:
        model = Cash
        fields = ('code', 'cash_fund', 'is_active', 'deleted')


class UserFormDoctor(forms.ModelForm):
    is_active = forms.BooleanField(initial=True, required=False)
    username = forms.CharField(required=True)
    createdAt = forms.CharField(required=False)
    role = forms.CharField(required=False)
    password = forms.CharField(required=True, widget=forms.PasswordInput, min_length=5, max_length=255)

    class Meta:
        model = User
        fields = ('username', 'role', 'is_active', 'password', 'deleted', 'doctor')


class UserFormPatient(forms.ModelForm):
    is_active = forms.BooleanField(initial=True, required=False)
    username = forms.CharField(required=True)
    createdAt = forms.CharField(required=False)
    role = forms.CharField(required=False)
    password = forms.CharField(required=True, widget=forms.PasswordInput, min_length=5, max_length=255)

    class Meta:
        model = User
        fields = ('username', 'role', 'is_active', 'password', 'deleted', 'patient')


class Expenses_natureForm(forms.ModelForm):
    code = forms.CharField(required=False)
    name = forms.CharField(required=False)
    nature = forms.CharField(required=False)
    account_number = forms.CharField(required=False)
    type = forms.CharField(required=False)

    class Meta:
        model = Expenses_nature
        fields = ('code', 'type', 'name', 'nature', 'account_number')


class Cash_movementForm(forms.ModelForm):
    code = forms.CharField(required=False)
    motive = forms.CharField(required=False)
    name = forms.CharField(required=False)
    name_movement = forms.CharField(required=False)
    amount_movement = forms.IntegerField(required=False)
    type = forms.CharField(required=False)

    class Meta:
        model = Cash_movement
        fields = ('code', 'type', 'name', 'motive', 'name_movement', 'amount_movement')


class AppointmentForm(forms.ModelForm):
    code = forms.CharField(required=False)
    problem = forms.CharField(required=False)
    start_appointment_date = forms.CharField(required=False)
    end_appointment_date = forms.CharField(required=False)

    class Meta:
        model = Appointment
        fields = ('code','patient', 'doctor', 'problem', 'start_appointment_date','end_appointment_date')


class PrescriptionForm(forms.ModelForm):
    code = forms.CharField(required=False)
    createdAt = forms.CharField(required=False)
    product_qte = forms.CharField(required=False)
    product_nbr_fois = forms.CharField(required=False)
    product_form = forms.CharField(required=False)

    class Meta:
        model = Prescription
        fields = ('code','product', 'ordinance', 'product_qte', 'product_nbr_fois','product_form')
class ExaminationForm(forms.ModelForm):
    code = forms.CharField(required=False)
    createdAt = forms.CharField(required=False)
    tension = forms.CharField(required=False)
    perimeter = forms.CharField(required=False)
    temperature = forms.CharField(required=False)
    description_exam = forms.CharField(required=False)
    results_exam = forms.CharField(required=False)

    class Meta:
        model = Examination
        fields = ('code','user','patient', 'perimeter', 'tension', 'temperature','description_exam','results_exam')


class OrdinanceForm(forms.ModelForm):
    code = forms.CharField(required=False)
    createdAt = forms.CharField(required=False)
    medication = forms.CharField(required=False)
    period_medication = forms.CharField(required=False)

    class Meta:
        model = Ordinance
        fields = ('code','patient', 'doctor', 'medication', 'period_medication')
class BackgroundForm(forms.ModelForm):
    code = forms.CharField(required=False)
    createdAt = forms.CharField(required=False)
    description_back = forms.CharField(required=False)
    category_back = forms.CharField(required=False)

    class Meta:
        model = Background
        fields = ('code','patient', 'category_back', 'description_back')

class ConsultationForm(forms.ModelForm):
    code = forms.CharField(required=False)
    createdAt = forms.CharField(required=False)
    reason = forms.CharField(required=False)
    diagnostic = forms.CharField(required=False)

    class Meta:
        model = Consultation
        fields = ('code','patient', 'doctor','background','ordinance','appointment', 'reason', 'diagnostic')


class Storage_depotsForm(forms.ModelForm):
    createdAt = forms.CharField(required=False)
    code = forms.CharField(required=False)
    name = forms.CharField(required=False)
    name_responsible = forms.CharField(required=False)
    default_depot = forms.BooleanField(initial=False, required=False)


    class Meta:
        model = Storage_depots
        fields = ('code', 'name', 'name_responsible', 'username','default_depot')


class DoctorForm(forms.ModelForm):
    address = forms.CharField(max_length=255,required=False)
    speciality = forms.CharField(max_length=255,required=False)
    email = forms.EmailField(required=False)
    createdAt = forms.CharField(max_length=255,required=False)
    intervention_days = MultiSelectField(choices=DAYS_CHOICES, max_length=255)
    position = forms.CharField(max_length=255, required=False)
    coef = forms.CharField(max_length=255, required=False)
    code = forms.CharField(max_length=255, required=False)
    name = forms.CharField(max_length=255, required=False)
    dateNaiss = forms.CharField(max_length=255, required=False)
    dateService = forms.CharField(max_length=255, required=False)
    phone = forms.CharField(required=True, min_length=9, max_length=12, validators=[
        RegexValidator('^((6([5-9][0-9]{7})))$',
                       _('Enter a valid phone format'))
    ])

    class Meta:
        model = Doctor
        fields = (
            'email', 'position', 'phone', 'coef', 'department',
            'name', 'dateNaiss', 'dateService', 'intervention_days', 'address', 'speciality')


class ProductForm(forms.ModelForm):
    barcode = forms.CharField(required=False)
    code = forms.CharField(required=False)
    name = forms.CharField(required=False)
    dosage = forms.CharField(required=False)
    createdAt = forms.CharField(required=False)
    public_price = forms.FloatField(required=False)
    purchase_price = forms.FloatField(required=False)
    margin = forms.FloatField(required=False)
    qte_stock = forms.IntegerField(required=False)
    conditioning = forms.CharField(max_length=255, required=False)
    # expiry_date = forms.CharField(max_length=255, required=False)
    is_active = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = Product
        fields = (
            'code', 'barcode','name', 'qte_stock','dci1', 'dci2', 'dosage',
            'conditioning', 'margin', 'category', 'shape', 'public_price', 'purchase_price', 'is_active')


class SuppliersForm(forms.ModelForm):
    code = forms.CharField(required=False)
    name = forms.CharField(required=False)
    phone = forms.CharField(required=False, min_length=9, max_length=12, validators=[
        RegexValidator('^((6([5-9][0-9]{7})))$',
                       _('Enter a valid phone format'))
    ])
    phone_representative = forms.CharField(required=False, min_length=9, max_length=12, validators=[
        RegexValidator('^((6([5-9][0-9]{7})))$',
                       _('Enter a valid phone format'))
    ])
    name_representative = forms.CharField(required=False)
    createdAt = forms.CharField(required=False)
    is_active = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = Suppliers
        fields = ('code', 'name', 'name_representative', 'phone_representative', 'phone', 'is_active')


class SuppliesForm(forms.ModelForm):
    code = forms.CharField(required=False)
    reference_no = forms.CharField(required=False)
    createdAt = forms.CharField(required=False)
    arrival_date = forms.DateTimeField(required=False)
    supply_amount = forms.IntegerField(required=False)
    additional_info = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Supplies
        fields = (
            'code', 'storage_depots','suppliers',
            'additional_info', 'reference_no', 'supply_amount',
            'arrival_date')
class Stock_movementForm(forms.ModelForm):
    code = forms.CharField(required=False)
    type_movement = forms.CharField(required=False)
    reason_movement = forms.CharField(required=False)
    date_movement = forms.DateTimeField(required=False)
    movement_value = forms.IntegerField(required=False)

    class Meta:
        model = Stock_movement
        fields = (
            'code', 'type_movement','reason_movement','storage_depots',
            'date_movement','movement_value')
class InventoryForm(forms.ModelForm):
    code = forms.CharField(required=False)
    reason_inventory = forms.CharField(required=False)
    date_inventory = forms.DateTimeField(required=False)

    class Meta:
        model = Inventory
        fields = (
            'code','reason_inventory','storage_depots',
            'date_inventory')
class BillsForm(forms.ModelForm):
    advance = forms.IntegerField(required=False)
    net_payable = forms.IntegerField(required=False)
    balance = forms.IntegerField(required=False)
    total_amount = forms.IntegerField(required=False)
    additional_info = forms.CharField(required=False)
    bill_type = forms.CharField(max_length=255, required=False)
    bill_shape = forms.CharField(max_length=255, required=False)
    patient_type = forms.CharField(max_length=255, required=False)
    bills_date = forms.CharField(max_length=255, required=False)
    code = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Bills
        fields = (
            'code', 'balance', 'net_payable', 'advance','patient','storage_depots','doctor','total_amount',
            'additional_info', 'patient_type', 'bill_shape','bills_date',
            'bill_type')
class PatientSettlementForm(forms.ModelForm):
    payment = forms.IntegerField(required=False)
    wordings = forms.CharField(required=False)
    code = forms.CharField(max_length=255, required=False)

    class Meta:
        model = PatientSettlement
        fields = (
            'code', 'payment', 'wordings', 'patient')


class DetailsSuppliesForm(forms.ModelForm):
    quantity = forms.IntegerField(required=False)
    total_amount = forms.IntegerField(required=False)
    arrival_price = forms.IntegerField(required=False)
    cmup = forms.CharField(required=False)
    createdAt = forms.CharField(required=False)

    class Meta:
        model = DetailsSupplies
        fields = (
            'quantity',
            'cmup', 'total_amount',
            'arrival_price' , 'product', 'supplies','createdAt')

class DetailsStockForm(forms.ModelForm):
    product_name = forms.CharField(required=False)
    class Meta:
        model = DetailsStock
        fields = ('product_name',)
class DetailsStock_movementForm(forms.ModelForm):
    total_amount = forms.CharField(required=False)
    unit_price = forms.CharField(required=False)
    quantity = forms.CharField(required=False)
    type_movement = forms.CharField(required=False)
    createdAt = forms.CharField(required=False)

    class Meta:
        model = DetailsStock_movement
        fields = ('total_amount','storage_depots','details_stock','type_movement','quantity', 'unit_price','createdAt')
class DetailsInventoryForm(forms.ModelForm):
    amount = forms.CharField(required=False)
    amount_adjusted = forms.CharField(required=False)
    quantity_stock = forms.CharField(required=False)
    quantity_adjusted = forms.CharField(required=False)
    cmup = forms.CharField(required=False)
    class Meta:
        model = DetailsInventory
        fields = ('amount','amount_adjusted','storage_depots','details_stock','quantity_adjusted','quantity_stock','cmup')
class DetailsBillsForm(forms.ModelForm):
    quantity_served = forms.IntegerField(required=False)
    quantity_ordered = forms.IntegerField(required=False)
    amount_net = forms.IntegerField(required=False)
    amount_gross = forms.IntegerField(required=False)
    pun = forms.IntegerField(required=False)
    pub = forms.IntegerField(required=False)
    delivery = forms.CharField(required=False)
    createdAt = forms.CharField(required=False)
    class Meta:
        model = DetailsBills
        fields = (
            'quantity_served','details_stock','storage_depots','medical_act','quantity_ordered','amount_gross',
            'pub','pun', 'delivery', 'createdAt',
            'amount_net')


class PatientForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    createdAt = forms.CharField(required=False)
    phone = forms.CharField(required=True, min_length=9, max_length=12, validators=[
        RegexValidator('^((6([5-9][0-9]{7})))$',
                       _('Enter a valid phone format'))
    ])
    name = forms.CharField(max_length=255, required=True)
    dateNaiss = forms.CharField(max_length=255, required=True)
    child = forms.CharField(max_length=255, required=False)
    date_id = forms.CharField(max_length=255, required=False)
    number_id = forms.CharField(max_length=255, required=False)
    maritalStatus = forms.CharField(max_length=255, required=False)
    emergency_contact = forms.CharField(max_length=255, required=False)
    emergency_name = forms.CharField(max_length=255, required=False)
    mother_name = forms.CharField(max_length=255, required=True)
    type_id = forms.CharField(max_length=255, required=False)
    religion = forms.CharField(max_length=255, required=True)
    pathologies = forms.CharField(max_length=255, required=False)
    allergies = forms.CharField(max_length=255, required=False)
    blood_group = forms.CharField(max_length=255, required=False)
    weight = forms.CharField(max_length=255, required=False)
    electrophoresis = forms.CharField(max_length=255, required=False)
    size = forms.CharField(max_length=255, required=False)
    bpm = forms.CharField(max_length=255, required=False)
    temperature = forms.CharField(max_length=255, required=False)
    padiasto = forms.CharField(max_length=255, required=False)
    pasysto = forms.CharField(max_length=255, required=False)
    gender = forms.CharField(max_length=255, required=False)
    other_phone = forms.CharField(required=False, min_length=9, max_length=12, validators=[
        RegexValidator('^((6([5-9][0-9]{7})))$',
                       _('Enter a valid phone format'))
    ])
    age = forms.CharField(max_length=255, required=False)
    insurance_name = forms.CharField(max_length=255, required=False)
    insurance_number = forms.CharField(max_length=255, required=False)
    shape = forms.CharField(max_length=255, required=True)
    address = forms.CharField(max_length=255, required=True)
    code = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Patient
        fields = (
            'email', 'shape', 'code', 'phone', 'address',
            'name', 'dateNaiss', 'insurance_name', 'age', 'other_phone', 'gender',
            'pasysto', 'padiasto', 'temperature', 'bpm', 'size', 'electrophoresis', 'weight', 'blood_group',
            'allergies', 'pathologies', 'religion', 'type_id', 'mother_name', 'emergency_name', 'emergency_contact',
            'maritalStatus', 'number_id', 'date_id', 'child')


class HospitalForm(forms.ModelForm):
    # depart = forms.CharField(max_length=255, required=False)
    taxpayer = forms.CharField(required=False)
    address = forms.CharField(required=True)
    slogan = forms.CharField(required=False)
    zip_code = forms.CharField(required=False)
    logo = forms.CharField(required=False)
    phone = forms.CharField(required=True, min_length=9, max_length=12, validators=[
        RegexValidator('^((6([5-9][0-9]{7})))$',
                       _('Enter a valid phone format'))
    ])

    class Meta:
        model = Hospital
        fields = (
            'name', 'address', 'phone', 'deleted', 'logo', 'zip_code', 'slogan', 'taxpayer', 'email')



class DepartmentsForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Departments
        fields = ('name',)


class Medical_areasForm(forms.ModelForm):
    code = forms.CharField(required=False)
    name = forms.CharField(max_length=255, required=False)
    normal = forms.CharField(max_length=255, required=False)
    covered = forms.CharField(max_length=255, required=False)
    employee = forms.CharField(max_length=255, required=False)
    indigent = forms.CharField(max_length=255, required=False)
    quote_internal = forms.CharField(max_length=255, required=False)
    quote_external = forms.CharField(max_length=255, required=False)
    number_account = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Medical_areas
        fields = ('code','name', 'normal','employee','indigent','covered', 'quote_internal', 'quote_external', 'number_account')


class Medical_actFormUpdate(forms.ModelForm):
    code = forms.CharField(required=False)
    name = forms.CharField(max_length=255, required=False)
    coefficient = forms.CharField(max_length=255, required=False)
    quote_internal = forms.CharField(max_length=255, required=False)
    quote_external = forms.CharField(max_length=255, required=False)
    price = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Medical_act
        fields = ('code','name', 'coefficient', 'quote_internal', 'quote_external', 'price', 'medical_areas')


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=False)
    code = forms.CharField(max_length=255, required=False)
    billable = forms.CharField(max_length=255, required=False)
    is_active = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = Category
        fields = ('name', 'code', 'billable', 'medical_areas', 'is_active')


class ShapeForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=False)
    code = forms.CharField(max_length=255, required=False)
    is_active = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = Shape
        fields = ('name', 'code', 'is_active')
class DCIForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=False)
    code = forms.CharField(max_length=255, required=False)

    class Meta:
        model = DCI
        fields = ('name', 'code')


class Medical_actForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=False)
    coefficient = forms.CharField(max_length=255, required=False)
    quote_internal = forms.CharField(max_length=255, required=False)
    quote_external = forms.CharField(max_length=255, required=False)
    price = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Medical_act
        fields = ('name', 'coefficient', 'quote_internal', 'quote_external', 'price')


class UserFormUpdate(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput, min_length=3, max_length=15)
    is_active = forms.BooleanField(initial=True, required=False)
    username = forms.CharField(required=False)
    role = forms.CharField(required=False)
    deleted = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'role', 'is_active', 'deleted')

    def save(self, commit=True):
        user = super(UserFormUpdate, self).save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class HospitalUserForm(forms.Form):
    hospitals = forms.ModelMultipleChoiceField(Hospital.objects.filter(deleted=False))


class HospitalDepartmentForm(forms.Form):
    departments = forms.ModelMultipleChoiceField(Hospital.objects.filter(deleted=False))
