import django_filters

from hospital.models import User, Hospital, Departments, Medical_areas, Medical_act, Patient, Doctor, Expenses_nature, \
    Storage_depots, Ordinance, Appointment, Cash, Cash_movement, Category, Shape, Product, DetailsSupplies, Bills, \
    DetailsBills, PatientSettlement, DetailsStock, Stock_movement, DetailsStock_movement, Inventory, DetailsInventory, \
    Consultation, Background, Prescription, Examination, DCI

from hospital.models import Supplies, Suppliers


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    role = django_filters.CharFilter(lookup_expr='iexact')
    is_active = django_filters.BooleanFilter(lookup_expr='exact')
    createAt = django_filters.NumberFilter(lookup_expr='year')
    p_id = django_filters.NumberFilter(field_name='profile__id', lookup_expr='exact')
    p_position_held = django_filters.CharFilter(field_name='profile__position_held', lookup_expr='icontains')
    p_code = django_filters.CharFilter(field_name='profile__code', lookup_expr='icontains')

    class Meta:
        model = User
        fields = {'id': ['exact']}


class DepartmentsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    createAt = django_filters.NumberFilter(lookup_expr='year')

    class Meta:
        model = Departments
        fields = {'id': ['exact']}


class HospitalFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    user_type = django_filters.CharFilter(lookup_expr='iexact')
    is_active = django_filters.BooleanFilter(lookup_expr='exact')
    createAt = django_filters.NumberFilter(lookup_expr='year')
    address = django_filters.CharFilter(field_name='address', lookup_expr='icontains')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')
    slogan = django_filters.CharFilter(field_name='slogan', lookup_expr='icontains')
    taxpayer = django_filters.CharFilter(field_name='taxpayer', lookup_expr='icontains')

    class Meta:
        model = Hospital
        fields = {'id': ['exact']}
class DetailsSuppliesFilter(django_filters.FilterSet):
    createAt = django_filters.NumberFilter(lookup_expr='year')
    product_name = django_filters.CharFilter(lookup_expr='iexact')
    product_code = django_filters.CharFilter(lookup_expr='iexact')
    quantity = django_filters.CharFilter(lookup_expr='iexact')
    total_amount = django_filters.CharFilter(lookup_expr='iexact')
    createdAt = django_filters.CharFilter(lookup_expr='iexact')
    arrival_price = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = DetailsSupplies
        fields = {'id': ['exact']}


class DoctorFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='iexact')
    createdAt = django_filters.CharFilter(lookup_expr='iexact')
    intervention_days = django_filters.CharFilter(lookup_expr='iexact')
    position = django_filters.CharFilter(lookup_expr='iexact')
    updateAt = django_filters.CharFilter(lookup_expr='iexact')
    coef = django_filters.CharFilter(lookup_expr='iexact')
    code = django_filters.CharFilter(lookup_expr='iexact')
    name = django_filters.CharFilter(lookup_expr='iexact')
    dateNaiss = django_filters.CharFilter(lookup_expr='iexact')
    dateService = django_filters.CharFilter(lookup_expr='iexact')
    phone = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Doctor
        fields = {'id': ['exact']}


class PatientFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='iexact')
    createdAt = django_filters.CharFilter(lookup_expr='iexact')
    updateAt = django_filters.CharFilter(lookup_expr='iexact')
    phone = django_filters.CharFilter(lookup_expr='iexact')
    name = django_filters.CharFilter(lookup_expr='iexact')
    dateNaiss = django_filters.CharFilter(lookup_expr='iexact')
    child = django_filters.CharFilter(lookup_expr='iexact')
    date_id = django_filters.CharFilter(lookup_expr='iexact')
    number_id = django_filters.CharFilter(lookup_expr='iexact')
    maritalStatus = django_filters.CharFilter(lookup_expr='iexact')
    emergency_contact = django_filters.CharFilter(lookup_expr='iexact')
    emergency_name = django_filters.CharFilter(lookup_expr='iexact')
    mother_name = django_filters.CharFilter(lookup_expr='iexact')
    type_id = django_filters.CharFilter(lookup_expr='iexact')
    religion = django_filters.CharFilter(lookup_expr='iexact')
    pathologies = django_filters.CharFilter(lookup_expr='iexact')
    allergies = django_filters.CharFilter(lookup_expr='iexact')
    blood_group = django_filters.CharFilter(lookup_expr='iexact')
    weight = django_filters.CharFilter(lookup_expr='iexact')
    electrophoresis = django_filters.CharFilter(lookup_expr='iexact')
    size = django_filters.CharFilter(lookup_expr='iexact')
    bpm = django_filters.CharFilter(lookup_expr='iexact')
    temperature = django_filters.CharFilter(lookup_expr='iexact')
    padiasto = django_filters.CharFilter(lookup_expr='iexact')
    pasysto = django_filters.CharFilter(lookup_expr='iexact')
    gender = django_filters.CharFilter(lookup_expr='iexact')
    other_phone = django_filters.CharFilter(lookup_expr='iexact')
    age = django_filters.CharFilter(lookup_expr='iexact')
    insurance_name = django_filters.CharFilter(lookup_expr='iexact')
    insurance_number = django_filters.CharFilter(lookup_expr='iexact')
    shape = django_filters.CharFilter(lookup_expr='iexact')
    address = django_filters.CharFilter(lookup_expr='iexact')
    code = django_filters.CharFilter(lookup_expr='iexact')
    deletedAt = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Patient
        fields = {'id': ['exact']}


class Medical_areasFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    coefficient = django_filters.CharFilter(lookup_expr='iexact')
    is_active = django_filters.BooleanFilter(lookup_expr='exact')
    createAt = django_filters.NumberFilter(lookup_expr='year')
    quote_internal = django_filters.CharFilter(lookup_expr='icontains')
    quote_external = django_filters.CharFilter(lookup_expr='icontains')
    number_account = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Medical_areas
        fields = {'id': ['exact']}


class Expenses_natureFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    nature_code = django_filters.CharFilter(lookup_expr='iexact')
    is_active = django_filters.BooleanFilter(lookup_expr='exact')
    createAt = django_filters.NumberFilter(lookup_expr='year')
    type = django_filters.CharFilter(lookup_expr='icontains')
    nature = django_filters.CharFilter(lookup_expr='icontains')
    account_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Expenses_nature
        fields = {'id': ['exact']}


class Cash_movementFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='iexact')
    createAt = django_filters.NumberFilter(lookup_expr='year')
    type = django_filters.CharFilter(lookup_expr='icontains')
    name_movement = django_filters.CharFilter(lookup_expr='icontains')
    motive = django_filters.CharFilter(lookup_expr='icontains')
    amount_movement = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Cash_movement
        fields = {'id': ['exact']}


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='iexact')
    createAt = django_filters.NumberFilter(lookup_expr='year')
    billable = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = {'id': ['exact']}


class ShapeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='iexact')
    createAt = django_filters.NumberFilter(lookup_expr='year')

    class Meta:
        model = Shape
        fields = {'id': ['exact']}
class DCIFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='iexact')
    createAt = django_filters.NumberFilter(lookup_expr='year')

    class Meta:
        model = DCI
        fields = {'id': ['exact']}


class ProductFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    dci1 = django_filters.CharFilter(lookup_expr='icontains')
    dosage = django_filters.CharFilter(lookup_expr='icontains')
    dci2 = django_filters.CharFilter(lookup_expr='icontains')
    public_price = django_filters.CharFilter(lookup_expr='icontains')
    purchase_price = django_filters.CharFilter(lookup_expr='icontains')
    margin = django_filters.CharFilter(lookup_expr='icontains')
    # quantity = django_filters.CharFilter(lookup_expr='icontains')
    conditioning = django_filters.CharFilter(lookup_expr='icontains')
    # expiry_date = django_filters.NumberFilter(lookup_expr='year')
    createAt = django_filters.NumberFilter(lookup_expr='year')

    class Meta:
        model = Product
        fields = {'id': ['exact']}
class SuppliesFilter(django_filters.FilterSet):
    storage_depot = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    total_amount = django_filters.CharFilter(lookup_expr='icontains')
    quantity = django_filters.CharFilter(lookup_expr='icontains')
    additional_info = django_filters.CharFilter(lookup_expr='icontains')
    reference_no = django_filters.CharFilter(lookup_expr='icontains')
    arrival_price = django_filters.CharFilter(lookup_expr='icontains')
    supply_amount = django_filters.CharFilter(lookup_expr='icontains')
    arrival_date = django_filters.NumberFilter(lookup_expr='year')
    createdAt = django_filters.NumberFilter(lookup_expr='year')

    class Meta:
        model = Supplies
        fields = {'id': ['exact']}
class BillsFilter(django_filters.FilterSet):
    doctor = django_filters.CharFilter(lookup_expr='icontains')
    cashier = django_filters.CharFilter(lookup_expr='icontains')
    storage_depot = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='icontains')
    advance = django_filters.CharFilter(lookup_expr='icontains')
    total_amount = django_filters.CharFilter(lookup_expr='icontains')
    bill_shape = django_filters.CharFilter(lookup_expr='icontains')
    additional_info = django_filters.CharFilter(lookup_expr='icontains')
    bill_type = django_filters.CharFilter(lookup_expr='icontains')
    patient = django_filters.CharFilter(lookup_expr='icontains')
    net_payable = django_filters.CharFilter(lookup_expr='icontains')
    balance = django_filters.CharFilter(lookup_expr='icontains')
    patient_type = django_filters.NumberFilter(lookup_expr='year')
    createdAt = django_filters.NumberFilter(lookup_expr='year')

    class Meta:
        model = Bills
        fields = {'id': ['exact']}
class PatientSettlementFilter(django_filters.FilterSet):
    cashier = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='icontains')
    payment = django_filters.CharFilter(lookup_expr='icontains')
    wordings = django_filters.CharFilter(lookup_expr='icontains')
    patient = django_filters.CharFilter(lookup_expr='icontains')
    createdAt = django_filters.NumberFilter(lookup_expr='year')
    date = django_filters.NumberFilter(lookup_expr='year')

    class Meta:
        model = PatientSettlement
        fields = {'id': ['exact']}
class SuppliersFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    phone_representative = django_filters.CharFilter(lookup_expr='icontains')
    name_representative = django_filters.CharFilter(lookup_expr='icontains')
    createdAt = django_filters.NumberFilter(lookup_expr='year')

    class Meta:
        model = Suppliers
        fields = {'id': ['exact']}


class CashFilter(django_filters.FilterSet):
    wording = django_filters.CharFilter(lookup_expr='icontains')
    session = django_filters.CharFilter(lookup_expr='icontains')
    open_date = django_filters.CharFilter(lookup_expr='iexact')
    close_date = django_filters.CharFilter(lookup_expr='iexact')
    is_active = django_filters.BooleanFilter(lookup_expr='exact')
    createAt = django_filters.NumberFilter(lookup_expr='year')
    cash_fund = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Cash
        fields = {'id': ['exact']}


class Storage_depotsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='iexact')
    is_active = django_filters.BooleanFilter(lookup_expr='exact')
    createAt = django_filters.NumberFilter(lookup_expr='year')
    name_responsible = django_filters.CharFilter(lookup_expr='icontains')
    username = django_filters.CharFilter(lookup_expr='icontains')
    default_depot = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Storage_depots
        fields = {'id': ['exact']}


class AppointmentFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    appointment_date = django_filters.CharFilter(lookup_expr='icontains')
    time = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Appointment
        fields = {'id': ['exact']}
class PrescriptionFilter(django_filters.FilterSet):

    class Meta:
        model = Prescription
        fields = {'id': ['exact']}


class OrdinanceFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    medication = django_filters.CharFilter(lookup_expr='icontains')
    period_medication = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Ordinance
        fields = {'id': ['exact']}

class ExaminationFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Examination
        fields = {'id': ['exact']}

class BackgroundFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    medication = django_filters.CharFilter(lookup_expr='icontains')
    period_medication = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Background
        fields = {'id': ['exact']}

class ConsultationFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Consultation
        fields = {'id': ['exact']}


class Medical_actFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    coefficient = django_filters.CharFilter(lookup_expr='iexact')
    is_active = django_filters.BooleanFilter(lookup_expr='exact')
    createAt = django_filters.NumberFilter(lookup_expr='year')
    quote_internal = django_filters.CharFilter(lookup_expr='icontains')
    quote_external = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.CharFilter(lookup_expr='icontains')
    medical_areas = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Medical_act
        fields = {'id': ['exact']}
class Stock_movementFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    movement_value = django_filters.CharFilter(lookup_expr='icontains')
    date_movement = django_filters.NumberFilter(lookup_expr='year')
    type_movement = django_filters.CharFilter(lookup_expr='icontains')
    reason_movement = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Stock_movement
        fields = {'id': ['exact']}
class InventoryFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    date_inventory = django_filters.NumberFilter(lookup_expr='year')
    reason_inventory = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Inventory
        fields = {'id': ['exact']}

class DetailsBillsFilter(django_filters.FilterSet):
    quantity_ordered = django_filters.CharFilter(lookup_expr='iexact')
    amount_net = django_filters.CharFilter(lookup_expr='iexact')
    amount_gross = django_filters.CharFilter(lookup_expr='iexact')
    pun = django_filters.CharFilter(lookup_expr='iexact')
    pub = django_filters.CharFilter(lookup_expr='iexact')
    delivery = django_filters.CharFilter(lookup_expr='iexact')
    createdAt = django_filters.CharFilter(lookup_expr='iexact')
    updatedAt = django_filters.CharFilter(lookup_expr='iexact')
    createAt = django_filters.NumberFilter(lookup_expr='year')

    class Meta:
        model = DetailsBills
        fields = {'id': ['exact']}
class DetailsStockFilter(django_filters.FilterSet):
    product_name = django_filters.CharFilter(lookup_expr='icontains')


    class Meta:
        model = DetailsStock
        fields = {'id': ['exact']}
class DetailsStock_movementFilter(django_filters.FilterSet):
    total_amount = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = DetailsStock_movement
        fields = {'id': ['exact']}
class DetailsInventoryFilter(django_filters.FilterSet):
    amount = django_filters.CharFilter(lookup_expr='icontains')
    amount_adjusted = django_filters.CharFilter(lookup_expr='icontains')
    quantity_adjusted = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = DetailsInventory
        fields = {'id': ['exact']}
