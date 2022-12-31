from rest_framework import serializers

from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from hospital.models import User, Hospital, Departments, Medical_areas, Medical_act, Doctor, Patient, \
    Expenses_nature, Storage_depots, Appointment, Ordinance, Cash, Cash_movement, Category, Shape, Product, \
    Suppliers, Supplies, DetailsSupplies, Bills, DetailsBills, PatientSettlement, DetailsStock, DetailsStock_movement, \
    Stock_movement, Inventory, DetailsInventory, Background, Consultation, Prescription, Examination, DCI


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DepartmentsSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost user writable nested serializer
    """

    class Meta:
        model = Departments
        fields = '__all__'


class DoctorSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost medical_areas writable nested serializer
    """
    department = DepartmentsSerializer(many=False, required=False, fields=('id', 'name',))

    class Meta:
        model = Doctor
        fields = '__all__'


class PatientSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost patient writable nested serializer
    """

    class Meta:
        model = Patient
        fields = '__all__'
class UserSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost user writable nested serializer
    """

    doctor = DoctorSerializer(many=False)
    patient = PatientSerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'createdAt', 'role', 'is_active', 'code', 'deleted', 'doctor', 'patient')

class Medical_areasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medical_areas
        fields = '__all__'


class Medical_actSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost medical_areas writable nested serializer
    """

    medical_areas = Medical_areasSerializer(many=False)

    class Meta:
        model = Medical_act
        fields = '__all__'


class CategorySerializer(DynamicFieldsModelSerializer):
    """
    Bifrost medical_areas writable nested serializer
    """

    medical_areas = Medical_areasSerializer(many=False)

    class Meta:
        model = Category
        fields = '__all__'


class ShapeSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost medical_areas writable nested serializer
    """

    class Meta:
        model = Shape
        fields = '__all__'
class DCISerializer(DynamicFieldsModelSerializer):
    """
    Bifrost medical_areas writable nested serializer
    """

    class Meta:
        model = DCI
        fields = '__all__'


class Expenses_natureSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost patient writable nested serializer
    """

    class Meta:
        model = Expenses_nature
        fields = '__all__'


class AppointmentSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost patient writable nested serializer
    """
    patient = PatientSerializer(many=False)
    doctor = DoctorSerializer(many=False)

    class Meta:
        model = Appointment
        fields = '__all__'


class ProductSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost patient writable nested serializer
    """
    category = CategorySerializer(many=False)
    shape = ShapeSerializer(many=False)
    dci1 = DCISerializer(many=False)
    dci2 = DCISerializer(many=False)

    class Meta:
        model = Product
        fields = '__all__'


class CashSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost patient writable nested serializer
    """
    user = UserSerializer(many=False, fields=('id', 'username'))
    open_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    close_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Cash
        fields = '__all__'


class SuppliersSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost patient writable nested serializer
    """

    class Meta:
        model = Suppliers
        fields = '__all__'


class Cash_movementSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost Cash_movement writable nested serializer
    """
    cash = CashSerializer(many=False)

    class Meta:
        model = Cash_movement
        fields = '__all__'


class OrdinanceSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost Ordinance writable nested serializer
    """
    patient = PatientSerializer(many=False)
    doctor = DoctorSerializer(many=False)

    class Meta:
        model = Ordinance
        fields = '__all__'

class PrescriptionSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost Prescription writable nested serializer
    """
    ordinance = OrdinanceSerializer(many=False)
    product = ProductSerializer(many=False)

    class Meta:
        model = Prescription
        fields = '__all__'

class ExaminationSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost Prescription writable nested serializer
    """
    patient = PatientSerializer(many=False)

    class Meta:
        model = Examination
        fields = '__all__'

class BackgroundSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost Background writable nested serializer
    """
    patient = PatientSerializer(many=False)

    class Meta:
        model = Background
        fields = '__all__'
class ConsultationSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost Consultation writable nested serializer
    """
    patient = PatientSerializer(many=False)
    doctor = DoctorSerializer(many=False)
    ordinance = OrdinanceSerializer(many=False)
    background = BackgroundSerializer(many=False)
    appointment = AppointmentSerializer(many=False)
    Examination = ExaminationSerializer(many=False)

    class Meta:
        model = Consultation
        fields = '__all__'

class HospitalSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost Hospital writable nested serializer
    """

    class Meta:
        model = Hospital
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class Storage_depotsSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost patient writable nested serializer
    """
    username = UserSerializer(many=False)

    class Meta:
        model = Storage_depots
        fields = '__all__'
class Stock_movementSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost Stock_movement writable nested serializer
    """
    storage_depots = Storage_depotsSerializer(many=False, fields=('id', 'name'))
    date_movement = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Stock_movement
        fields = ('id', 'storage_depots', 'type_movement', 'movement_value','reason_movement','code','date_movement')
class InventorySerializer(DynamicFieldsModelSerializer):
    """
    Bifrost Inventory writable nested serializer
    """
    storage_depots = Storage_depotsSerializer(many=False, fields=('id', 'name'))
    date_inventory = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Inventory
        fields = ('id','reason_inventory', 'storage_depots', 'code', 'date_inventory')


class SuppliesSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost Supplies writable nested serializer
    """
    suppliers = SuppliersSerializer(many=False, fields=('id', 'name'))
    storage_depots = Storage_depotsSerializer(many=False, fields=('id', 'name'))
    id = serializers.CharField(max_length=255)
    code = serializers.CharField(max_length=255)
    additional_info = serializers.CharField(max_length=255)
    reference_no = serializers.CharField(max_length=255)
    supply_amount = serializers.IntegerField()

    class Meta:
        model = Supplies
        fields = ('id','storage_depots','suppliers','arrival_date','code','additional_info', 'reference_no', 'supply_amount')
class BillsSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost Bills writable nested serializer
    """
    cash = CashSerializer(many=False, fields=('id','user'))
    doctor = DoctorSerializer(many=False, fields=('id', 'name'))
    patient = PatientSerializer(many=False, fields=('id', 'name', 'shape'))
    storage_depots=Storage_depotsSerializer(many=False, fields=('id', 'name'))

    class Meta:
        model = Bills
        fields = ['id','cash','doctor','patient','storage_depots','bills_date','code','patient_type','bill_shape','bill_type','additional_info','total_amount','balance','net_payable','advance']
class PatientSettlementSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost PatientSettlement writable nested serializer
    """
    cash = CashSerializer(many=False, fields=('id','code'))
    patient = PatientSerializer(many=False, fields=('id', 'name', 'code'))

    class Meta:
        model = PatientSettlement
        fields = '__all__'


class DetailsSuppliesSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost         model = DetailsSupplies
 writable nested serializer
    """
    supplies = SuppliesSerializer(many=False, fields=('id','code','createdAt'))
    product = ProductSerializer(many=False)

    class Meta:
        model = DetailsSupplies
        fields = '__all__'
class DetailsStockSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost DetailsStock writable nested serializer
    """
    storage_depots=Storage_depotsSerializer(many=False, fields=('id', 'name'))
    product = ProductSerializer(many=False)

    class Meta:
        model = DetailsStock
        fields = '__all__'

class DetailsBillsSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost patient writable nested serializer
    """
    bills = BillsSerializer(many=False, fields=('id','code','bills_date'))
    details_stock = DetailsStockSerializer(many=False)
    class Meta:
        model = DetailsBills
        fields = '__all__'

class DetailsStock_movementSerializer(DynamicFieldsModelSerializer):
    """
    Bifrost DetailsStock_movement writable nested serializer
    """
    storage_depots=Storage_depotsSerializer(many=False, fields=('id', 'name'))
    stock_movement=Stock_movementSerializer(many=False, fields=('id', 'name','code','date_movement'))
    details_stock = DetailsStockSerializer(many=False)

    class Meta:
        model = DetailsStock_movement
        fields = '__all__'
class DetailsInventorySerializer(DynamicFieldsModelSerializer):
    """
    Bifrost DetailsStock_movement writable nested serializer
    """
    storage_depots=Storage_depotsSerializer(many=False, fields=('id', 'name'))
    inventory=InventorySerializer(many=False, fields=('id', 'name'))
    details_stock = DetailsStockSerializer(many=False)

    class Meta:
        model = DetailsInventory
        fields = '__all__'
