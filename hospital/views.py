from datetime import datetime
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import re
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.db.models import Sum
# Create your views here.
from hospital.forms import UserForm, UserFormUpdate, HospitalForm, DepartmentsForm, Medical_areasForm, \
    Medical_actForm, DoctorForm, PatientForm, UserFormPatient, UserFormDoctor, Storage_depotsForm, Expenses_natureForm, \
    AppointmentForm, CashForm, Cash_movementForm, Medical_actFormUpdate, CategoryForm, ShapeForm, \
    ProductForm, SuppliesForm, SuppliersForm, DetailsSuppliesForm, BillsForm, DetailsBillsForm, PatientSettlementForm, \
    Stock_movementForm, DetailsStock_movementForm, DetailsInventoryForm, InventoryForm, ConsultationForm, \
    BackgroundForm, ExaminationForm, OrdinanceForm, PrescriptionForm, DCIForm
from hospital.models import User, Hospital, Departments, Medical_areas, Medical_act, Doctor, Patient, Storage_depots, \
    Expenses_nature, Appointment, Ordinance, Cash, Cash_movement, Category, Shape, Product, Supplies, Suppliers, \
    DetailsSupplies, Bills, DetailsBills, PatientSettlement, DetailsStock, Stock_movement, DetailsStock_movement, \
    Inventory, DetailsInventory, Consultation, Background, Prescription, Examination, DCI
from hospital.serializers import UserSerializer, ChangePasswordSerializer, HospitalSerializer, DepartmentsSerializer, \
    Medical_areasSerializer, Medical_actSerializer, DoctorSerializer, PatientSerializer, \
    Storage_depotsSerializer, Expenses_natureSerializer, AppointmentSerializer, CashSerializer, \
    Cash_movementSerializer, CategorySerializer, ShapeSerializer, ProductSerializer, SuppliesSerializer, \
    SuppliersSerializer, DetailsSuppliesSerializer, BillsSerializer, DetailsBillsSerializer, \
    PatientSettlementSerializer, DetailsStockSerializer, Stock_movementSerializer, DetailsStock_movementSerializer, \
    InventorySerializer, DetailsInventorySerializer, ConsultationSerializer, BackgroundSerializer, \
    PrescriptionSerializer, ExaminationSerializer, OrdinanceSerializer, DCISerializer
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from globals.pagination import CustomPagination
from rest_framework import status
from .filters import UserFilter, HospitalFilter, DepartmentsFilter, Medical_areasFilter, Medical_actFilter, \
    PatientFilter, DoctorFilter, Storage_depotsFilter, Expenses_natureFilter, AppointmentFilter, \
    CashFilter, Cash_movementFilter, CategoryFilter, ShapeFilter, ProductFilter, SuppliesFilter, \
    SuppliersFilter, DetailsSuppliesFilter, BillsFilter, DetailsBillsFilter, PatientSettlementFilter, \
    DetailsStockFilter, Stock_movementFilter, DetailsStock_movementFilter, InventoryFilter, DetailsInventoryFilter, \
    ConsultationFilter, BackgroundFilter, PrescriptionFilter, ExaminationFilter, OrdinanceFilter, DCIFilter
from rest_framework.decorators import action, permission_classes, api_view
from django.shortcuts import render
def home_view(request):
    return render(request, 'index.html')

class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.filter(deleted=False)
    serializer_class = HospitalSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = HospitalFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        """
        This view should return a list of all the enterprise
        for the currently authenticated user.
        """
        user = self.request.user
        if user.role == 'RESPONSIBLE':
            return Hospital.objects.filter(owner__id=user.id).filter(deleted=False)
        else:
            return Hospital.objects.filter(deleted=False)

    def create(self, request, *args, **kwargs):
        hospital_form = HospitalForm(request.data)
        if hospital_form.is_valid():
            hospital = hospital_form.save()
            hospital.save()
            serializer = HospitalSerializer(hospital, many=False)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**hospital_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        hospital = self.get_object()
        hospital_form = HospitalForm(request.data, instance=hospital)
        if hospital_form.is_valid():
            hospital = hospital_form.save()
            hospital.save()
            serializer = HospitalSerializer(hospital, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**hospital_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        hospital = self.get_object()
        hospital.deleted = True
        hospital.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists')
    def exists(self, request):
        data = request.data
        errors = {"name": ["This field is required."]}
        if 'name' in data:
            association = Hospital.objects.filter(name=data['name'])
            if association:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(deleted=False)
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = UserFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):

        """
        This view should return a list of all the users
        for the currently authenticated user.
        """
        user = self.request.user
        if user.role == 'RESPONSIBLE':
            hospital = Hospital.objects.filter(owner__id=user.id, deleted=False).first()
            if hospital:
                return User.objects.filter(hospitals__id=hospital.id, deleted=False,
                                           role__in=['DOCTOR', 'PATIENT', 'RECEPTIONIST', 'HR'])
            else:
                return User.objects.none()
        return User.objects.filter(deleted=False).exclude(
            role__in=['ADMIN'])
        # return User.objects.filter(deleted=False).exclude(
        #     role__in=['ADMIN', 'DOCTOR', 'PATIENT', 'RECEPTIONIST', 'HR'])

    def create(self, request, *args, **kwargs):
        print(request.data)
        user_form = UserForm(request.data)
        if user_form.is_valid():
            get_user = User.objects.first()
            if get_user:
                user = user_form.save()
                user.set_password(user_form.cleaned_data.get('password'))
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_user.code)
                code = str('%04d' % (int(find[0]) + 1))
                user.code = get_user.code[0:3] + code
                user.save()
                serializer = self.get_serializer(user, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                user = user_form.save()
                user.set_password(user_form.cleaned_data.get('password'))
                user.save()
                serializer = UserSerializer(user, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**user_form.errors, }
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user_form = UserFormUpdate(request.data, instance=user)
        if user_form.is_valid():
            """
            Active et desactiver un utilisateur proprietaire d'une entreprise ainsi que mettre a jour le champs deleted 
            de l'entreprise au quel il est 
            rattache, le status du numero court de l'entreprise et les numero de routage lie a cette entreprise.
            """
            user = user_form.save()
            user.save()
            serializer = UserSerializer(user, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**user_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.deleted = True
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='username/exists', permission_classes=[AllowAny])
    def check_username(self, request, *args, **kwargs):
        data = request.data
        errors = {"username": ["This field already exists."]}
        if 'username' in data:
            users = User.objects.filter(username=data['username'])
            if users:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='email/exists', permission_classes=[AllowAny])
    def check_email(self, request, *args, **kwargs):
        data = request.data
        errors = {"email": ["This field already exists."]}
        if 'email' in data:
            users = User.objects.filter(email=data['email'])
            if users:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='phone/exists', permission_classes=[AllowAny])
    def check_phone(self, request, *args, **kwargs):
        data = request.data
        errors = {"phone": ["This field already exists."]}
        if 'phone' in data:
            users = User.objects.filter(phone=data['phone'])
            if users:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='me')
    def get(self, request):
        return Response(self.serializer_class(request.user).data)

    @action(detail=False, methods=['PUT'], url_path='change_password')
    def change_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        message = {"password": ["Password updated successfully."]}
        error = {"error": ["Your old password was entered incorrectly. Please enter it again."]}
        if serializer.is_valid():
            if user.check_password(serializer.data.get("old_password")):
                user.set_password(serializer.data.get("new_password"))
                user.save()
                # print(user)
                return Response(data=message, status=status.HTTP_200_OK)
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentsViewSet(viewsets.ModelViewSet):
    queryset = Departments.objects.filter(deleted=False)
    serializer_class = DepartmentsSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = DepartmentsFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):

        """
        This view should return a list of all the users
        for the currently authenticated user.
        """
        user = self.request.user
        if user.role == 'RESPONSIBLE':

            hospital = Hospital.objects.filter(owner__id=user.id, deleted=False).first()
            if hospital:
                return Departments.objects.filter(departments__id=hospital.id, deleted=False)
            else:
                return Departments.objects.none()
        return Departments.objects.filter(deleted=False)

    def create(self, request, *args, **kwargs):
        departments_form = DepartmentsForm(request.data)
        if departments_form.is_valid():
            departments = departments_form.save()
            departments.save()
            if request.user.role == 'RESPONSIBLE':
                department = Hospital.objects.filter(owner__id=request.user.id).first()
                if department:
                    department.depart.add(departments)
            serializer = DepartmentsSerializer(departments, many=False)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**departments_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        departments = self.get_object()
        departments_form = DepartmentsForm(request.data, instance=departments)
        if departments_form.is_valid():
            departments = departments_form.save()
            departments.save()
            serializer = DepartmentsSerializer(departments, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**departments_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        departments = self.get_object()
        departments.deleted = True
        departments.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_depart(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            departments = Departments.objects.filter(name=data['name'])
            if departments:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class Expenses_natureViewSet(viewsets.ModelViewSet):
    queryset = Expenses_nature.objects.filter(deleted=False)
    serializer_class = Expenses_natureSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = Expenses_natureFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        expenses_nature_form = Expenses_natureForm(request.data)
        if expenses_nature_form.is_valid():
            get_expenses_nature = Expenses_nature.objects.first()
            if get_expenses_nature is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_expenses_nature.code)
                code = str('%04d' % (int(find[0]) + 1))
                expenses_nature = expenses_nature_form.save()
                expenses_nature.code = get_expenses_nature.code[0:3] + code
                expenses_nature.save()
                serializer = self.get_serializer(expenses_nature, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                expenses_nature = expenses_nature_form.save()
                expenses_nature.save()
                serializer = self.get_serializer(expenses_nature, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**expenses_nature_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        expenses_nature = self.get_object()
        expenses_nature_form = Expenses_natureForm(request.data, instance=expenses_nature)
        if expenses_nature_form.is_valid():
            expenses_nature = expenses_nature_form.save()
            expenses_nature.save()
            serializer = self.get_serializer(expenses_nature, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**expenses_nature_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        expenses_nature = self.get_object()
        expenses_nature.deleted = True
        expenses_nature.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_depart(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            departments = Departments.objects.filter(name=data['name'])
            if departments:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class OrdinanceViewSet(viewsets.ModelViewSet):
    queryset = Ordinance.objects.filter(deleted=False)
    serializer_class = OrdinanceSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = OrdinanceFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        ordinance_form = OrdinanceForm(request.data)
        if ordinance_form.is_valid():
            get_ordinance = Ordinance.objects.first()
            if get_ordinance is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_ordinance.code)
                code = str('%04d' % (int(find[0]) + 1))
                ordinance = ordinance_form.save()
                ordinance.code = get_ordinance.code[0:3] + code
                ordinance.save()
                serializer = self.get_serializer(ordinance, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                ordinance = ordinance_form.save()
                ordinance.save()
                serializer = self.get_serializer(ordinance, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**ordinance_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        ordinance = self.get_object()
        ordinance_form = OrdinanceForm(request.data, instance=ordinance)
        if ordinance_form.is_valid():
            ordinance = ordinance_form.save()
            ordinance.save()
            serializer = self.get_serializer(ordinance, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**ordinance_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        ordinance = self.get_object()
        ordinance.deleted = True
        ordinance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BackgroundViewSet(viewsets.ModelViewSet):
    queryset = Background.objects.filter(deleted=False)
    serializer_class = BackgroundSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = BackgroundFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        background_form = BackgroundForm(request.data)
        if background_form.is_valid():
            get_background = Background.objects.first()
            if get_background is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_background.code)
                code = str('%04d' % (int(find[0]) + 1))
                background = background_form.save()
                background.code = get_background.code[0:3] + code
                background.save()
                serializer = self.get_serializer(background, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                background = background_form.save()
                background.save()
                serializer = self.get_serializer(background, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**background_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        background = self.get_object()
        background_form = BackgroundForm(request.data, instance=background)
        if background_form.is_valid():
            background = background_form.save()
            background.save()
            serializer = self.get_serializer(background, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**background_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        background = self.get_object()
        background.deleted = True
        background.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExaminationViewSet(viewsets.ModelViewSet):
    queryset = Examination.objects.filter(deleted=False)
    serializer_class = ExaminationSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = ExaminationFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        examination_form = ExaminationForm(request.data)
        user = self.request.user
        if examination_form.is_valid():
            get_examination = Examination.objects.first()
            if get_examination is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_examination.code)
                code = str('%04d' % (int(find[0]) + 1))
                examination = examination_form.save()
                examination.code = get_examination.code[0:3] + code
                examination.user_id = user.id
                examination.save()
                serializer = self.get_serializer(Examination, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                examination = examination_form.save()
                examination.user_id = user.id
                examination.save()
                serializer = self.get_serializer(Examination, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**examination_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        examination = self.get_object()
        examination_form = ExaminationForm(request.data, instance=examination)
        if examination_form.is_valid():
            examination = examination_form.save()
            examination.save()
            serializer = self.get_serializer(Examination, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**examination_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        examination = self.get_object()
        examination.deleted = True
        examination.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.filter(deleted=False)
    serializer_class = PrescriptionSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = PrescriptionFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        prescription_form = PrescriptionForm(request.data)
        if prescription_form.is_valid():
            get_prescription = Prescription.objects.first()
            if get_prescription is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_prescription.code)
                code = str('%04d' % (int(find[0]) + 1))
                prescription = prescription_form.save()
                prescription.code = get_prescription.code[0:3] + code
                prescription.save()
                serializer = self.get_serializer(prescription, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                prescription = prescription_form.save()
                prescription.save()
                serializer = self.get_serializer(prescription, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**prescription_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        prescription = self.get_object()
        prescription_form = PrescriptionForm(request.data, instance=prescription)
        if prescription_form.is_valid():
            prescription = prescription_form.save()
            prescription.save()
            serializer = self.get_serializer(prescription, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**prescription_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        prescription = self.get_object()
        prescription.deleted = True
        prescription.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_depart(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            departments = Prescription.objects.filter(name=data['name'])
            if departments:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.filter(deleted=False)
    serializer_class = ConsultationSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = ConsultationFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        print(request.data)
        consultation_form = ConsultationForm(request.data)
        if consultation_form.is_valid():
            get_consultation = Consultation.objects.first()
            if get_consultation is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_consultation.code)
                code = str('%04d' % (int(find[0]) + 1))
                consultation = consultation_form.save()
                consultation.code = get_consultation.code[0:3] + code
                consultation.save()
                serializer = self.get_serializer(consultation, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:

                consultation = consultation_form.save()
                consultation.save()
                serializer = self.get_serializer(consultation, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**consultation_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        consultation = self.get_object()
        consultation_form = ConsultationForm(request.data, instance=consultation)
        if consultation_form.is_valid():
            consultation = consultation_form.save()
            consultation.save()
            serializer = self.get_serializer(consultation, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**consultation_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        consultation = self.get_object()
        consultation.deleted = True
        consultation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CashViewSet(viewsets.ModelViewSet):
    queryset = Cash.objects.filter(is_active=False, deleted=False)
    serializer_class = CashSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = CashFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        cash_form = CashForm(request.data)
        if user.role == 'CASHIER' and user.check_password(request.data['password']):
            if cash_form.is_valid():
                get_cash = Cash.objects.first()
                if get_cash is not None:
                    regex = re.compile(r'[\d]+')
                    find = re.findall(regex, get_cash.code)
                    code = str('%04d' % (int(find[0]) + 1))
                    cash = cash_form.save()
                    cash.code = get_cash.code[0:3] + code
                    cash.user_id = user.id
                    cash.save()
                    serializer = self.get_serializer(cash, many=False)
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    cash = cash_form.save()
                    cash.user_id = user.id
                    cash.save()
                    serializer = self.get_serializer(cash, many=False)
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            errors = {**cash_form.errors}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = {"password": ["Username/Password incorrect."]}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        cash = self.get_object()
        cash_form = CashForm(request.data, instance=cash)
        if cash_form.is_valid():
            cash = cash_form.save()
            if request.data['is_active'] == False:
                cash.close_date = timezone.now()
                cash.save()
            cash.save()
            serializer = self.get_serializer(cash, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**cash_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        cash = self.get_object()
        cash.deleted = True
        cash.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='close/(?P<pk>.+)')
    def close(self, request, *args, **kwargs):
        get_user = User.objects.filter(username=request.data['cashier']).last()
        if get_user.role in ['ADMIN', 'CASHIER'] and get_user.check_password(request.data['password']):
            get_cash = Cash.objects.filter(id=request.data['id'], is_active=True).last()
            get_cash.close_date = timezone.now()
            get_cash.is_active = False
            get_cash.save()
            return Response(status=status.HTTP_200_OK)

        else:
            errors = {"user": ["No permission allowed."]}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='sessions_analysis')
    def sessions_analysis(self, request, *args, **kwargs):
        get_cash_movement = Cash_movement.objects.filter(cash__id=self.request.query_params.get("id"),
                                                         cash__is_active=False).all()
        serializer = Cash_movementSerializer(get_cash_movement, many=True)
        content = {'content': serializer.data}
        return Response(data=content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='details_sessions_analysis')
    def details_sessions_analysis(self, request, *args, **kwargs):
        get_cash = Cash.objects.filter(id=request.query_params.get("id"), is_active=False).last()
        if get_cash:

            get_cash_movment = Cash_movement.objects.filter(cash_id=get_cash.id).all()

            serializer = Cash_movementSerializer(get_cash_movment, many=True)
            get_settlement = PatientSettlement.objects.filter(cash_id=get_cash.id)
            serializer_settle = PatientSettlementSerializer(get_settlement, many=True)
            content = {'content': {'cash_fund': get_cash.cash_fund, 'cash_movement': serializer.data,
                                   'settlement': serializer_settle.data}}
            return Response(data=content, status=status.HTTP_200_OK)
        else:
            content = {"content": []}
            return Response(data=content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='bills_analysis')
    def bills_analysis(self, request, *args, **kwargs):
        startdate = request.query_params.get("start_date")
        enddate = request.query_params.get("end_date")
        get_bills = Bills.objects.filter(bills_date__range=[startdate, enddate])
        serializer = BillsSerializer(get_bills, many=True)
        content = {'content': serializer.data}
        return Response(data=content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='movements_analysis')
    def movements_analysis(self, request, *args, **kwargs):
        startdate = request.query_params.get("start_date")
        enddate = request.query_params.get("end_date")
        get_cash_movement = Cash_movement.objects.filter(createdAt__range=[startdate, enddate])
        serializer = Cash_movementSerializer(get_cash_movement, many=True)
        get_settlement = PatientSettlement.objects.filter(createdAt__range=[startdate, enddate])
        serializer_settle = PatientSettlementSerializer(get_settlement, many=True)
        content = {'content': {'cash_movement': serializer.data, 'settlement': serializer_settle.data}}
        return Response(data=content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='export_movements_analysis')
    def export_movements_analysis(self, request, *args, **kwargs):
        startdate = request.query_params.get("start_date")
        enddate = request.query_params.get("end_date")
        get_cash = Cash.objects.filter(id=request.query_params.get(
            "id")).last()
        get_bills = Bills.objects.filter(cash_id=request.query_params.get(
            "id")).last()
        serializer_bills = BillsSerializer(get_bills, many=True)
        bills = serializer_bills.data
        html_render = get_template('export_item_movement.html')
        html_content = html_render.render(
            {'bills': bills, 'cash_code': get_cash.code, 'cashier': get_cash.user.username,
             'start_date': startdate, 'end_date': enddate,
             'date': datetime.today().strftime("%Y-%m-%d %H:%M:%S")})
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_content.encode("ISO-8859-1")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            filename = 'Export' + datetime.today().strftime("%Y-%m-%d %H:%M:%S") + '.pdf'
            response['Content-Disposition'] = 'inline; filename="' + filename + '"'
            response['Access-Control-Expose-Headers'] = 'Content-Disposition,X-Suggested-Filename'
            return response
        else:
            return None

    @action(detail=False, methods=['get'], url_path='export_bills_analysis')
    def export_bills_analysis(self, request, *args, **kwargs):
        startdate = request.query_params.get("start_date")
        enddate = request.query_params.get("end_date")
        get_cash = Cash.objects.filter(id=request.query_params.get(
            "id")).last()
        get_bills = Bills.objects.filter(cash_id=request.query_params.get(
            "id")).last()
        serializer_bills = BillsSerializer(get_bills, many=True)
        bills = serializer_bills.data
        html_render = get_template('export_item_movement.html')
        html_content = html_render.render(
            {'bills': bills, 'cash_code': get_cash.code, 'cashier': get_cash.user.username,
             'start_date': startdate, 'end_date': enddate,
             'date': datetime.today().strftime("%Y-%m-%d %H:%M:%S")})
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_content.encode("ISO-8859-1")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            filename = 'Export' + datetime.today().strftime("%Y-%m-%d %H:%M:%S") + '.pdf'
            response['Content-Disposition'] = 'inline; filename="' + filename + '"'
            response['Access-Control-Expose-Headers'] = 'Content-Disposition,X-Suggested-Filename'
            return response
        else:
            return None


class Stock_movementViewSet(viewsets.ModelViewSet):
    queryset = Stock_movement.objects.filter(deleted=False)
    serializer_class = Stock_movementSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = Stock_movementFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        # print(Stock_movement.objects.filter(id=self.request.GET.get("id")).all())
        return Stock_movement.objects.filter(storage_depots_id=self.request.GET.get("id"),deleted=False).all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        stock_movement_form = Stock_movementForm(request.data)
        if stock_movement_form.is_valid():
            get_stock_movement = Stock_movement.objects.first()
            if get_stock_movement is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_stock_movement.code)
                code = str('%04d' % (int(find[0]) + 1))
                stock_movement = stock_movement_form.save()
                stock_movement.code = get_stock_movement.code[0:3] + code
                get_details_stock_movement = DetailsStock_movement.objects.filter(stock_movement=None).all()
                for stock_mov in get_details_stock_movement:
                    stock_mov.stock_movement_id = stock_movement
                    stock_mov.save()
                stock_movement.save()
                serializer = self.get_serializer(stock_movement, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                stock_movement = stock_movement_form.save()
                get_details_stock_movement = DetailsStock_movement.objects.filter(stock_movement=None).all()
                for stock_mov in get_details_stock_movement:
                    stock_mov.stock_movement_id = stock_movement
                    stock_mov.save()
                stock_movement.save()
                serializer = self.get_serializer(stock_movement, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**stock_movement_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        cash = self.get_object()
        cash_form = CashForm(request.data, instance=cash)
        if cash_form.is_valid():
            cash = cash_form.save()
            if request.data['is_active'] == False:
                cash.close_date = timezone.now()
                cash.save()
            cash.save()
            serializer = self.get_serializer(cash, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**cash_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        stock_movement = self.get_object()
        stock_movement.deleted = True
        stock_movement.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='get_stock_movement')
    def get_stock_movement(self, request, *args, **kwargs):
        stock_movement = Stock_movement.objects.filter(
            storage_depots_id=request.query_params.get("id"))
        serializer = Stock_movementSerializer(stock_movement, many=True)
        content = {'content': serializer.data}
        return Response(data=content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='close')
    def close(self, request, *args, **kwargs):
        user = self.request.user
        print("ici")
        if user.role in ['ADMIN', 'CASHIER']:
            get_cash = Cash.objects.filter(user_id=user.id, is_active=True).last()
            get_cash.is_active = False
            get_cash.save()
            return Response(status=status.HTTP_200_OK)

        else:
            errors = {"user": ["No permission allowed."]}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


def inventory_update(user, inventory, request):
    get_details_inventory = DetailsInventory.objects.filter(inventory=None, user_id=user.id).all()
    for inventories in get_details_inventory:
        get_product_stock = DetailsStock.objects.filter(id=inventories.details_stock_id).last()
        if inventories.quantity_adjusted > get_product_stock.qte_stock:
            result = int(inventories.quantity_adjusted) - int(get_product_stock.qte_stock)
            total_amount = result * get_product_stock.cmup
            DetailsStock_movement.objects.create(storage_depots_id=inventories.storage_depots_id,
                                                 details_stock_id=inventories.details_stock_id,
                                                 total_amount=total_amount, quantity=result,
                                                 unit_price=get_product_stock.cmup, type_movement='ENTRY',
                                                 user_id=user.id)
            get_product_stock.qte_stock = inventories.quantity_adjusted
            get_product_stock.save()
        else:
            result = int(get_product_stock.qte_stock) - int(inventories.quantity_adjusted)
            total_amount = result * get_product_stock.cmup
            DetailsStock_movement.objects.create(storage_depots_id=inventories.storage_depots_id,
                                                 details_stock_id=inventories.details_stock_id,
                                                 total_amount=total_amount, quantity=result,
                                                 unit_price=get_product_stock.cmup, type_movement='EXIT',
                                                 user_id=user.id)
            get_product_stock.qte_stock = inventories.quantity_adjusted
            get_product_stock.save()
        inventories.inventory_id = inventory
        inventories.save()
    get_stock_movement = DetailsStock_movement.objects.filter(type_movement='ENTRY', user_id=user.id,
                                                              stock_movement=None).all()
    if get_stock_movement:
        sum = get_stock_movement.aggregate(Sum('total_amount'))['total_amount__sum']
        get_stock = Stock_movement.objects.first()
        if get_stock is not None:
            regex = re.compile(r'[\d]+')
            find = re.findall(regex, get_stock.code)
            code = str('%04d' % (int(find[0]) + 1))
            save_stock_movement = Stock_movement.objects.create(code=get_stock.code[0:3] + code,
                                                                storage_depots_id=request.data[
                                                                    'storage_depots'],
                                                                type_movement='ENTRY',
                                                                movement_value=sum,
                                                                reason_movement='inventory',
                                                                date_movement=request.data[
                                                                    'date_inventory'])
            for movement in get_stock_movement:
                movement.stock_movement_id = save_stock_movement
                movement.save()
        else:
            save_stock_movement = Stock_movement.objects.create(storage_depots_id=request.data[
                'storage_depots'],
                                                                type_movement='ENTRY',
                                                                movement_value=sum,
                                                                reason_movement='inventory',
                                                                date_movement=request.data[
                                                                    'date_inventory'])
            for movement in get_stock_movement:
                movement.stock_movement_id = save_stock_movement.id
                movement.save()
    else:
        get_stock_movement = DetailsStock_movement.objects.filter(type_movement='EXIT',
                                                                  user_id=user.id, stock_movement=None).all()
        if get_stock_movement:
            sum = get_stock_movement.aggregate(Sum('total_amount'))['total_amount__sum']
            get_stock = Stock_movement.objects.first()
            print(get_stock)
            if get_stock is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_stock.code)
                code = str('%04d' % (int(find[0]) + 1))
                save_stock_movement = Stock_movement.objects.create(code=get_stock.code[0:3] + code,
                                                                    storage_depots_id=request.data[
                                                                        'storage_depots'],
                                                                    type_movement='EXIT',
                                                                    movement_value=sum,
                                                                    reason_movement='inventory',
                                                                    date_movement=request.data[
                                                                        'date_inventory'])
                for movement in get_stock_movement:
                    movement.stock_movement_id = save_stock_movement.id
                    movement.save()
            else:
                save_stock_movement = Stock_movement.objects.create(storage_depots_id=request.data[
                    'storage_depots'],
                                                                    type_movement='EXIT',
                                                                    movement_value=sum,
                                                                    reason_movement='inventory',
                                                                    date_movement=request.data[
                                                                        'date_inventory'])
                for movement in get_stock_movement:
                    movement.stock_movement_id = save_stock_movement
                    movement.save()


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.filter(deleted=False)
    serializer_class = InventorySerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = InventoryFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        # print(Stock_movement.objects.filter(id=self.request.GET.get("id")).all())
        return Inventory.objects.filter(storage_depots_id=self.request.GET.get("id"), deleted=False).all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        inventory_form = InventoryForm(request.data)
        user = self.request.user
        if inventory_form.is_valid():
            get_inventory = Inventory.objects.first()
            if get_inventory is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_inventory.code)
                code = str('%04d' % (int(find[0]) + 1))
                inventory = inventory_form.save()
                inventory.code = get_inventory.code[0:3] + code
                inventory_update(user=user, inventory=inventory, request=request)
                inventory.save()
                serializer = self.get_serializer(inventory, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                inventory = inventory_form.save()
                inventory_update(user=user, inventory=inventory, request=request)
                inventory.save()
                serializer = self.get_serializer(inventory, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**inventory_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        inventory = self.get_object()
        inventory_form = InventoryForm(request.data, instance=inventory)
        if inventory_form.is_valid():
            inventory = inventory_form.save()
            inventory.save()
            serializer = self.get_serializer(inventory, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**inventory_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        inventory = self.get_object()
        inventory.deleted = True
        inventory.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='get_inventory')
    def get_inventory(self, request, *args, **kwargs):
        inventory = Inventory.objects.filter(storage_depots_id=request.query_params.get("id"))
        serializer = InventorySerializer(inventory, many=True)
        content = {'content': serializer.data}
        return Response(data=content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='close')
    def close(self, request, *args, **kwargs):
        user = self.request.user
        print("ici")
        if user.role in ['ADMIN', 'CASHIER']:
            get_cash = Cash.objects.filter(user_id=user.id, is_active=True).last()
            get_cash.is_active = False
            get_cash.save()
            return Response(status=status.HTTP_200_OK)

        else:
            errors = {"user": ["No permission allowed."]}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class Cash_movementViewSet(viewsets.ModelViewSet):
    queryset = Cash_movement.objects.filter(deleted=False)
    serializer_class = Cash_movementSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = Cash_movementFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        user = self.request.user
        return Cash_movement.objects.filter(cash__user_id=user.id,deleted=False).all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        print(request.data)
        cash_movement_form = Cash_movementForm(request.data)
        if cash_movement_form.is_valid():
            user = self.request.user
            if user.role in ['ADMIN', 'CASHIER']:
                get_cash = Cash.objects.filter(user_id=user.id, is_active=True).last()
                if get_cash:
                    get_cash_movement = Cash_movement.objects.first()
                    if get_cash_movement is not None:
                        regex = re.compile(r'[\d]+')
                        find = re.findall(regex, get_cash_movement.code)
                        code = str('%04d' % (int(find[0]) + 1))
                        cash_movement = cash_movement_form.save()
                        cash_movement.code = get_cash_movement.code[0:3] + code
                        cash_movement.save()
                        serializer = self.get_serializer(cash_movement, many=False)
                        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        cash_movement = cash_movement_form.save()
                        cash_movement.save()
                        serializer = self.get_serializer(cash_movement, many=False)
                        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    errors = {"cash": ["No Cash open."]}
                    return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                errors = {"cash": ["not permission allowed."]}
                return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        errors = {**cash_movement_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        cash_movement = self.get_object()
        cash_movement_form = Cash_movementForm(request.data, instance=cash_movement)
        if cash_movement_form.is_valid():
            cash_movement = cash_movement_form.save()
            cash_movement.save()
            serializer = self.get_serializer(cash_movement, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**cash_movement_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        cash_movement = self.get_object()
        cash_movement.deleted = True
        cash_movement.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_depart(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            departments = Ordinance.objects.filter(name=data['name'])
            if departments:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.filter(deleted=False)
    serializer_class = AppointmentSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = AppointmentFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        print(request.data)
        appointment_form = AppointmentForm(request.data)
        if appointment_form.is_valid():
            get_appointment = Appointment.objects.first()
            if get_appointment is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_appointment.code)
                code = str('%04d' % (int(find[0]) + 1))
                appointment = appointment_form.save()
                appointment.code = get_appointment.code[0:3] + code
                appointment.save()
                serializer = self.get_serializer(appointment, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                appointment = appointment_form.save()
                appointment.save()
                serializer = self.get_serializer(appointment, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**appointment_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        appointment = self.get_object()
        appointment_form = AppointmentForm(request.data, instance=appointment)
        if appointment_form.is_valid():
            appointment = appointment_form.save()
            appointment.save()
            serializer = self.get_serializer(appointment, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**appointment_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        appointment = self.get_object()
        appointment.deleted = True
        appointment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_depart(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            departments = Departments.objects.filter(name=data['name'])
            if departments:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class Storage_depotsViewSet(viewsets.ModelViewSet):
    queryset = Storage_depots.objects.filter(deleted=False)
    serializer_class = Storage_depotsSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = Storage_depotsFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        storage_depots_form = Storage_depotsForm(request.data)
        if storage_depots_form.is_valid():
            get_storage_depots = Storage_depots.objects.first()
            if get_storage_depots is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_storage_depots.code)
                code = str('%04d' % (int(find[0]) + 1))
                if request.data['default_depot'] == True:
                    get_depots = Storage_depots.objects.all()
                    for depot in get_depots:
                        depot.default_depot = False
                        depot.save()
                    storage_depots = storage_depots_form.save()
                    storage_depots.code = get_storage_depots.code[0:3] + code
                    storage_depots.save()
                else:
                    storage_depots = storage_depots_form.save()
                    storage_depots.code = get_storage_depots.code[0:3] + code
                    storage_depots.save()
                serializer = self.get_serializer(storage_depots, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                storage_depots = storage_depots_form.save()
                storage_depots.save()
                serializer = self.get_serializer(storage_depots, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**storage_depots_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        storage_depots = self.get_object()
        storage_depots_form = Storage_depotsForm(request.data, instance=storage_depots)
        if storage_depots_form.is_valid():
            if request.data['default_depot'] == True:
                get_depots = Storage_depots.objects.all()
                for depot in get_depots:
                    depot.default_depot = False
                    depot.save()
                storage_depots = storage_depots_form.save()
                storage_depots.save()
            else:
                storage_depots = storage_depots_form.save()
                storage_depots.save()

            serializer = self.get_serializer(storage_depots, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**storage_depots_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        storage_depots = self.get_object()
        storage_depots.deleted = True
        storage_depots.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_depart(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            storage_depots = Storage_depots.objects.filter(name=data['name'])
            if storage_depots:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class Medical_areasViewSet(viewsets.ModelViewSet):
    queryset = Medical_areas.objects.filter(deleted=False)
    serializer_class = Medical_areasSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = Medical_areasFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        medical_areas_form = Medical_areasForm(request.data)
        if medical_areas_form.is_valid():
            get_medical_areas = Medical_areas.objects.first()
            if get_medical_areas is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_medical_areas.code)
                code = str('%04d' % (int(find[0]) + 1))
                medical_areas = medical_areas_form.save()
                medical_areas.code = get_medical_areas.code[0:3] + code
                medical_areas.save()
                serializer = self.get_serializer(medical_areas, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                medical_areas = medical_areas_form.save()
                medical_areas.save()
                serializer = self.get_serializer(medical_areas, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**medical_areas_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        medical_areas = self.get_object()
        medical_areas_form = Medical_areasForm(request.data, instance=medical_areas)
        if medical_areas_form.is_valid():
            medical_areas = medical_areas_form.save()
            medical_areas.save()
            serializer = self.get_serializer(medical_areas, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**medical_areas_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        medical_areas = self.get_object()
        medical_areas.deleted = True
        medical_areas.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_medical_areas(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            medical_areas = Medical_areas.objects.filter(name=data['name'])
            if medical_areas:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(deleted=False)
    serializer_class = CategorySerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = CategoryFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        category_form = CategoryForm(request.data)
        if category_form.is_valid():
            get_category = Category.objects.first()
            if get_category is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_category.code)
                code = str('%04d' % (int(find[0]) + 1))
                category = category_form.save()
                category.code = get_category.code[0:3] + code
                category.save()
                serializer = self.get_serializer(category, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                category = category_form.save()
                category.save()
                serializer = self.get_serializer(category, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**category_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        category_form = CategoryForm(request.data, instance=category)
        if category_form.is_valid():
            category = category_form.save()
            category.save()
            serializer = self.get_serializer(category, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**category_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        category.deleted = True
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_category(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            category = Category.objects.filter(name=data['name'])
            if category:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class ShapeViewSet(viewsets.ModelViewSet):
    queryset = Shape.objects.filter(deleted=False)
    serializer_class = ShapeSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = ShapeFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        shape_form = ShapeForm(request.data)
        if shape_form.is_valid():
            get_shape = Shape.objects.first()
            if get_shape is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_shape.code)
                code = str('%04d' % (int(find[0]) + 1))
                shape = shape_form.save()
                shape.code = get_shape.code[0:3] + code
                shape.save()
                serializer = self.get_serializer(shape, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                shape = shape_form.save()
                shape.save()
                serializer = self.get_serializer(shape, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**shape_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        shape = self.get_object()
        shape_form = ShapeForm(request.data, instance=shape)
        if shape_form.is_valid():
            shape = shape_form.save()
            shape.save()
            serializer = self.get_serializer(shape, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**shape_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        shape = self.get_object()
        shape.deleted = True
        shape.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_category(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            shape = Shape.objects.filter(name=data['name'])
            if shape:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class DCIViewSet(viewsets.ModelViewSet):
    queryset = DCI.objects.filter(deleted=False)
    serializer_class = DCISerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = DCIFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        dci_form = DCIForm(request.data)
        if dci_form.is_valid():
            get_DCI = DCI.objects.first()
            if get_DCI is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_DCI.code)
                code = str('%04d' % (int(find[0]) + 1))
                dci = dci_form.save()
                dci.code = get_DCI.code[0:3] + code
                dci.save()
                serializer = self.get_serializer(dci, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                dci = dci_form.save()
                dci.save()
                serializer = self.get_serializer(dci, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**dci_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        dci = self.get_object()
        dci_form = DCIForm(request.data, instance=dci)
        if dci_form.is_valid():
            dci = dci_form.save()
            dci.save()
            serializer = self.get_serializer(DCI, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**dci_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        dci = self.get_object()
        dci.deleted = True
        dci.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_category(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            dci = DCI.objects.filter(name=data['name'])
            if dci:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(deleted=False)
    serializer_class = ProductSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = CustomPagination
    filterset_class = ProductFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        """
        This view should return a list of all the enterprise
        for the currently authenticated user.
        """

        return Product.objects.filter(deleted=False)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_class = [IsAuthenticated]
        if self.action in ['ocm_callback', 'mtn_callback', 'campost_callback', 'get_graph_test']:
            permission_class = [AllowAny]
        return [permission() for permission in permission_class]

    def create(self, request, *args, **kwargs):
        product_form = ProductForm(request.data)
        if product_form.is_valid():
            get_product = Product.objects.first()
            if get_product is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_product.code)
                code = str('%04d' % (int(find[0]) + 1))
                product = product_form.save()
                product.code = get_product.code[0:3] + code
                product.save()
                serializer = self.get_serializer(product, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                product = product_form.save()
                product.save()
                serializer = self.get_serializer(product, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**product_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        product_form = ProductForm(request.data, instance=product)
        if product_form.is_valid():
            product = product_form.save()
            product.save()
            serializer = self.get_serializer(product, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**product_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.deleted = True
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post', 'get'], url_path='get_product', permission_classes=[AllowAny])
    def get_product(self, request, *args, **kwargs):
        data = request.data
        product = Product.objects.filter(code=data['code']).last()
        if product:
            serializer = ProductSerializer(product, many=False)
            data = {'name': serializer.data['name'], 'code': serializer.data['code'],
                    'codebarre': serializer.data['barcode']}
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            error = {"Code": ["No data available for this code"]}
            return Response(data=error, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_category(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            product = Product.objects.filter(name=data['name'])
            if product:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='get_products')
    def get_products(self, request, *args, **kwargs):
        product = DetailsStock.objects.filter(product__name=request.query_params.get("name"),
                                              storage_depots_id=request.query_params.get("storage_depots"))
        serializer = DetailsStockSerializer(product, many=True)
        content = {}
        content['content'] = serializer.data
        if product:
            return Response(data=content, status=status.HTTP_200_OK)
        else:
            product = DetailsStock.objects.filter(
                storage_depots_id=request.query_params.get("storage_depots"))
            serializer = DetailsStockSerializer(product, many=True)
            content = {}
            content['content'] = serializer.data
            return Response(data=content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='export_items')
    def export_items(self, request, *args, **kwargs):
        # startdate = '2022-11-17'
        # enddate = '2022-11-22'
        # get_product = Product.objects.filter(id=5).last()
        startdate = request.query_params.get("start_date")
        enddate = request.query_params.get("end_date")
        get_product = Product.objects.filter(id=request.query_params.get(
            "product")).last()
        get_product_stock = DetailsStock_movement.objects.filter(storage_depots_id=request.query_params.get("id"),
                                                                 details_stock__product__id=request.query_params.get(
                                                                     "product"), createdAt__range=[startdate, enddate])
        serializer_stock = DetailsStock_movementSerializer(get_product_stock, many=True)
        stocks = serializer_stock.data
        get_product_bills = DetailsBills.objects.filter(storage_depots_id=request.query_params.get("id"),
                                                        details_stock__product__id=request.query_params.get(
                                                            "product"), createdAt__range=[startdate, enddate])
        serializer_bills = DetailsBillsSerializer(get_product_bills, many=True)
        bills = serializer_bills.data
        get_product_supplies = DetailsSupplies.objects.filter(storage_depots_id=request.query_params.get("id"),
                                                              product_id=request.query_params.get(
                                                                  "product"), createdAt__range=[startdate, enddate])
        serializer_supplies = DetailsSuppliesSerializer(get_product_supplies, many=True)
        supplies = serializer_supplies.data
        html_render = get_template('export_item_movement.html')
        html_content = html_render.render(
            {'bills': bills, 'supplies': supplies, 'stocks': stocks, 'product_name': get_product.name,
             'product_code': get_product.code, 'start_date': startdate, 'end_date': enddate,
             'date': datetime.today().strftime("%Y-%m-%d %H:%M:%S")})
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_content.encode("ISO-8859-1")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            filename = 'Export' + datetime.today().strftime("%Y-%m-%d %H:%M:%S") + '.pdf'
            response['Content-Disposition'] = 'inline; filename="' + filename + '"'
            response['Access-Control-Expose-Headers'] = 'Content-Disposition,X-Suggested-Filename'
            return response
        else:
            return None


class DetailsStockViewSet(viewsets.ModelViewSet):
    queryset = DetailsStock.objects.all()
    serializer_class = DetailsStockSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = DetailsStockFilter
    filter_backends = (filters.DjangoFilterBackend,)

    # def get_queryset(self):
    #     if self.request.query_params.get("supplies") == 'undefined':
    #         return DetailsBills.objects.none()
    #     else:
    #         user = self.request.user
    #         return DetailsBills.objects.filter(user_id=user.id, bills_id=None).all()
    #
    # def create(self, request, *args, **kwargs):
    #     detailsBills_form = DetailsBillsForm(data=request.data)
    #     print(request.data)
    #
    #     if detailsBills_form.is_valid():
    #         user = self.request.user
    #         if user.role in ['ADMIN', 'CASHIER']:
    #             get_cash = Cash.objects.filter(user_id=user.id, is_active=True).last()
    #             if get_cash:
    #                 # get_bills = Bills.objects.filter(id=request.data['bills']).last()
    #                 # if 'net_payable' in request.data and request.data['net_payable'] != 0:
    #                 #     get_bills.net_payable = request.data['net_payable']
    #                 #     get_bills.balance = request.data['balance']
    #                 #     get_bills.advance = request.data['advance']
    #                 #     get_bills.save()
    #                 #     return Response(status=status.HTTP_201_CREATED)
    #                 # else:
    #                 get_details = DetailsBills.objects.filter(product_id=request.data['product'],
    #                                                           storage_depots_id=request.data['storage_depots'], user_id=user.id, bills=None).last()
    #
    #                 if get_details:
    #                     get_details_stock = DetailsStock.objects.filter(product_id=request.data['product'],
    #                                                                     storage_depots_id=request.data[
    #                                                                         'storage_depots']).last()
    #                     get_details_stock.qte_stock = get_details_stock.qte_stock + get_details.quantity_served - int(
    #                         request.data['quantity_served'])
    #                     get_details_stock.save()
    #                     get_details.quantity_served = request.data['quantity_served']
    #                     get_details.pub = request.data['pub']
    #                     get_details.pun = request.data['pun']
    #                     get_details.amount_net = request.data['amount_net']
    #                     get_details.amount_gross = request.data['amount_gross']
    #                     get_details.save()
    #
    #                     return Response(status=status.HTTP_201_CREATED)
    #
    #                 else:
    #                     print(request.data)
    #                     detailsBills = detailsBills_form.save()
    #                     detailsBills.user_id = user.id
    #                     detailsBills.save()
    #                     get_details_stock = DetailsStock.objects.filter(product_id=request.data['product'], storage_depots_id=request.data['storage_depots']).last()
    #                     get_details_stock.qte_stock = get_details_stock.qte_stock - int(request.data['quantity_served'])
    #                     get_details_stock.save()
    #                     serializer = self.get_serializer(detailsBills, many=False)
    #                     return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    #             else:
    #                 errors = {"cash": ["No open checkout."]}
    #                 return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             errors = {"cash": ["No permission allowed."]}
    #             return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
    #     errors = {**detailsBills_form.errors}
    #     return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def update(self, request, *args, **kwargs):
    #     path = request.path
    #     end_path = path.rsplit('/', 1)[-1]
    #     get_details = DetailsSupplies.objects.filter(id=end_path).last()
    #     print(request.data)
    #     if get_details:
    #         get_details.supplies_id = request.data['supplies']
    #         get_details.product_id = get_details.product
    #         get_details.quantity = request.data['quantity']
    #         get_details.total_amount = request.data['total_amount']
    #         get_details.product_code = request.data['product_code']
    #         get_details.product_name = request.data['product_name']
    #         get_details.arrival_price = request.data['arrival_price']
    #         get_details.save()
    #         get_sum_details = DetailsSupplies.objects.filter(supplies_id=request.data['supplies']).aggregate(
    #             Sum('total_amount'))
    #         get_supplies = Supplies.objects.filter(id=get_details.supplies.id).last()
    #         get_supplies.supply_amount = get_sum_details['total_amount__sum']
    #         get_supplies.save()
    #         return Response(status=status.HTTP_201_CREATED)
    #     else:
    #         errors = {"errors": ["Already exist"]}
    #         return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def destroy(self, request, *args, **kwargs):
    #     path = request.path
    #     end_path = path.rsplit('/', 1)[-1]
    #     get_details = DetailsBills.objects.filter(id=end_path).last()
    #     get_product = Product.objects.filter(id=get_details.product.id).last()
    #     get_product.qte_stock = get_product.qte_stock + int(get_details.quantity_served)
    #     get_product.save()
    #     get_details.delete()
    #     return Response(status=status.HTTP_200_OK)
    #
    # @action(detail=False, methods=['get'], url_path='stock_available')
    # def stock_available(self, request):
    #     get_product = DetailsSupplies.objects.filter(supplies__storage_depot=request.query_params.get("id")).order_by(
    #         'product_id').distinct("product_id")
    #     productList = []
    #     for product in get_product:
    #         get_prod = Product.objects.filter(id=product.product_id).last()
    #         productList.append(get_prod)
    #     serializer = DetailsSuppliesSerializer(get_product, many=True)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)


class SuppliesViewSet(viewsets.ModelViewSet):
    queryset = Supplies.objects.filter(deleted=False)
    serializer_class = SuppliesSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = SuppliesFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        supplies_form = SuppliesForm(request.data)
        if supplies_form.is_valid():
            get_supplies = Supplies.objects.first()
            user = self.request.user
            if get_supplies is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_supplies.code)
                code = str('%04d' % (int(find[0]) + 1))
                supplies = supplies_form.save()
                supplies.code = get_supplies.code[0:3] + code
                get_details_stock = DetailsSupplies.objects.filter(user_id=user.id, supplies=None).all()
                for supplie in get_details_stock:
                    supplie.supplies_id = supplies
                    supplie.save()
                # get_sum_details = DetailsSupplies.objects.filter(
                #     supplies_id=request.data['supplies']).aggregate(
                #     Sum('total_amount'))
                # get_supplies.supply_amount = get_sum_details['total_amount__sum']
                # get_supplies.save()
                supplies.save()
                serializer = self.get_serializer(supplies, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                supplies = supplies_form.save()
                get_details_stock = DetailsSupplies.objects.filter(user_id=user.id, supplies=None).all()
                for supplie in get_details_stock:
                    supplie.supplies_id = supplies
                    supplie.save()
                supplies.save()
                serializer = self.get_serializer(supplies, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**supplies_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):

        supplies = self.get_object()
        print(supplies, request.data)
        supplies_form = SuppliesForm(request.data, instance=supplies)
        if supplies_form.is_valid():
            supplies = supplies_form.save()
            supplies.save()
            serializer = self.get_serializer(supplies, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**supplies_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        supplies = self.get_object()
        supplies.deleted = True
        supplies.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_category(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            product = Product.objects.filter(name=data['name'])
            if product:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=['get'], url_path='stock_available', permission_classes=[AllowAny])
    # def stock_available(self, request, *args, **kwargs):
    #     product={}
    #     get_stock_available = Supplies.objects.filter(storage_depot_id=request.query_params.get("id")).last()
    #     supplies = SuppliesSerializer(get_stock_available, many=False)
    #     product['supplie'] = supplies.data
    #     # print(supplies.data)
    #     get_product = Product.objects.filter(id=get_stock_available.id).all()
    #     serializer = ProductSerializer(get_product, many=True)
    #     product['product'] = serializer.data
    #     return Response(data=product, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get', 'post'], url_path='details', permission_classes=[AllowAny])
    def details(self, request, *args, **kwargs):
        if request.method == 'GET':
            get_product_supplies = DetailsSupplies.objects.filter(
                supplies_id=request.query_params.get("id_supplies")).all()
            details = DetailsSuppliesSerializer(get_product_supplies, many=True)
            return Response(data=details.data, status=status.HTTP_200_OK)
        else:
            print(request.data)
            get_details = DetailsSupplies.objects.create(supplies_id=request.data['id_supplies'],
                                                         product_id=request.data['product']['id'],
                                                         quantity=request.data['quantity'],
                                                         total_amount=request.data['total_amount'],
                                                         arrival_price=request.data['arrival_price'],
                                                         product_code=request.data['product_code'],
                                                         product_name=request.data['product_name'])
            details = DetailsSuppliesSerializer(get_details, many=False)
            return Response(data=details.data, status=status.HTTP_200_OK)


class DetailsBillsViewSet(viewsets.ModelViewSet):
    queryset = DetailsBills.objects.all()
    serializer_class = DetailsBillsSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = DetailsBillsFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        user = self.request.user
        if self.request.GET.get("bills"):
            if self.request.GET.get("bills") == 'undefined' or self.request.GET.get("bills") == 'null':
                return DetailsBills.objects.filter(cash__user_id=user.id, bills_id=None).all()
            else:
                return DetailsBills.objects.filter(cash__user_id=user.id, bills_id=self.request.GET.get("bills")).all()
        else:
            return DetailsBills.objects.filter(cash__user_id=user.id, bills_id=None).all()

    def create(self, request, *args, **kwargs):
        print(request.data)
        detailsBills_form = DetailsBillsForm(data=request.data)
        if detailsBills_form.is_valid():
            user = self.request.user
            if user.role in ['ADMIN', 'CASHIER']:
                get_cash = Cash.objects.filter(user_id=user.id, is_active=True).last()
                if get_cash:
                    # get_bills = Bills.objects.filter(id=request.data['bills']).last()
                    # if 'net_payable' in request.data and request.data['net_payable'] != 0:
                    #     get_bills.net_payable = request.data['net_payable']
                    #     get_bills.balance = request.data['balance']
                    #     get_bills.advance = request.data['advance']
                    #     get_bills.save()
                    #     return Response(status=status.HTTP_201_CREATED)
                    # else:
                    get_details = DetailsBills.objects.filter(id=request.data['details_stock'],
                                                              storage_depots_id=request.data['storage_depots'],
                                                              cash_id=get_cash.id, bills=None).last()

                    if get_details:
                        get_details_stock = DetailsStock.objects.filter(id=request.data['details_stock'],
                                                                        storage_depots_id=request.data[
                                                                            'storage_depots']).last()
                        get_details_stock.qte_stock = get_details_stock.qte_stock + get_details.quantity_served - int(
                            request.data['quantity_served'])
                        get_details_stock.save()
                        get_details.quantity_served = request.data['quantity_served']
                        get_details.pub = request.data['pub']
                        get_details.pun = request.data['pun']
                        get_details.amount_net = request.data['amount_net']
                        get_details.amount_gross = request.data['amount_gross']
                        get_details.save()

                        return Response(status=status.HTTP_201_CREATED)

                    else:
                        detailsBills = detailsBills_form.save()
                        detailsBills.cash_id = get_cash.id
                        detailsBills.createdAt = request.data['createdAt']
                        detailsBills.save()
                        get_details_stock = DetailsStock.objects.filter(id=request.data['details_stock'],
                                                                        storage_depots_id=request.data[
                                                                            'storage_depots']).last()
                        get_details_stock.qte_stock = get_details_stock.qte_stock - int(request.data['quantity_served'])
                        get_details_stock.save()
                        serializer = self.get_serializer(detailsBills, many=False)
                        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    errors = {"cash": ["No open checkout."]}
                    return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                errors = {"cash": ["No permission allowed."]}
                return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        errors = {**detailsBills_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        path = request.path
        end_path = path.rsplit('/', 1)[-1]
        get_details = DetailsSupplies.objects.filter(id=end_path).last()
        print(request.data)
        if get_details:
            get_details.supplies_id = request.data['supplies']
            get_details.product_id = get_details.product
            get_details.quantity = request.data['quantity']
            get_details.total_amount = request.data['total_amount']
            get_details.product_code = request.data['product_code']
            get_details.product_name = request.data['product_name']
            get_details.arrival_price = request.data['arrival_price']
            get_details.save()
            get_sum_details = DetailsSupplies.objects.filter(supplies_id=request.data['supplies']).aggregate(
                Sum('total_amount'))
            get_supplies = Supplies.objects.filter(id=get_details.supplies.id).last()
            get_supplies.supply_amount = get_sum_details['total_amount__sum']
            get_supplies.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            errors = {"errors": ["Already exist"]}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        path = request.path
        end_path = path.rsplit('/', 1)[-1]
        get_details = DetailsBills.objects.filter(id=end_path).last()
        get_product = Product.objects.filter(id=get_details.product.id).last()
        get_product.qte_stock = get_product.qte_stock + int(get_details.quantity_served)
        get_product.save()
        get_details.delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='stock_available')
    def stock_available(self, request):
        get_product = DetailsSupplies.objects.filter(supplies__storage_depot=request.query_params.get("id")).order_by(
            'product_id').distinct("product_id")
        productList = []
        for product in get_product:
            get_prod = Product.objects.filter(id=product.product_id).last()
            productList.append(get_prod)
        serializer = DetailsSuppliesSerializer(get_product, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='get_items')
    def get_items(self, request):
        startdate = request.query_params.get("start_date")
        enddate = request.query_params.get("end_date")
        get_product = DetailsBills.objects.filter(storage_depots_id=request.query_params.get("id"),
                                                  details_stock__product__id=request.query_params.get("product"),
                                                  createdAt__range=[startdate, enddate])
        serializer = DetailsBillsSerializer(get_product, many=True)
        content = {'content': serializer.data}
        return Response(data=content, status=status.HTTP_200_OK)


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bills.objects.filter(deleted=False)
    serializer_class = BillsSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = BillsFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        return Bills.objects.filter(cash__user_id=self.request.user.id,deleted=False).all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        bills_form = BillsForm(request.data)
        if bills_form.is_valid():
            user = self.request.user
            if user.role in ['ADMIN', 'CASHIER']:
                get_cash = Cash.objects.filter(user_id=request.data['cashier'], is_active=True).last()
                if get_cash:
                    get_bills = Bills.objects.first()
                    if get_bills is not None:
                        regex = re.compile(r'[\d]+')
                        find = re.findall(regex, get_bills.code)
                        code = str('%06d' % (int(find[0]) + 1))
                        bills = bills_form.save()
                        bills.code = get_bills.code[0:3] + code
                        bills.cash_id = get_cash.id
                        get_details_bills = DetailsBills.objects.filter(cash__user_id=request.data['cashier'],
                                                                        bills=None).all()
                        for bill in get_details_bills:
                            bill.bills_id = bills
                            bill.save()
                        bills.save()
                        if request.data['advance'] != '':
                            get_patient_settlement = PatientSettlement.objects.first()
                            if get_patient_settlement is not None:
                                regex = re.compile(r'[\d]+')
                                find = re.findall(regex, get_patient_settlement.code)
                                code = str('%05d' % (int(find[0]) + 1))

                                code_patient = get_patient_settlement.code[0:3] + code
                                PatientSettlement.objects.create(code=code_patient, patient_id=request.data['patient'],
                                                                 bills_id=bills.id, payment=request.data['advance'],
                                                                 cash_id=get_cash.id, wordings='')
                            else:
                                PatientSettlement.objects.create(patient_id=request.data['patient'], bills_id=bills,
                                                                 payment=request.data['advance'], cash_id=get_cash.id,
                                                                 wordings='')
                        else:
                            pass
                        if 'print' in request.query_params:
                            # get_details_bills = DetailsBills.objects.filter(cash__user_id=request.data['cashier'],
                            #                                                 bills_id=bills).all()
                            html_render = get_template('print.html')
                            # logo = settings.MEDIA_ROOT + '/logo.png'
                            html_content = html_render.render(
                                {'products': get_details_bills, 'bills': bills.code,
                                 'Hospital': "test",
                                 'Contact': "690438500",
                                 # 'logo': logo,
                                 'STP': bills.net_payable,
                                 'STL': 0,
                                 'MontantT': bills.net_payable,
                                 'Doctor': bills.doctor.name,
                                 'Left_to_pay': bills.balance,
                                 'date': request.data['bills_date']})
                            result = BytesIO()
                            pdf = pisa.pisaDocument(BytesIO(html_content.encode("ISO-8859-1")), result)
                            response = HttpResponse(content_type='application/pdf')
                            filename = 'Facture_' + str(bills.code) + '.pdf'
                            response['Content-Disposition'] = 'inline; filename="' + filename + '"'
                            response['Access-Control-Expose-Headers'] = 'Content-Disposition,X-Suggested-Filename'
                            response.write(result.getvalue())
                            return response
                        else:
                            serializer = self.get_serializer(bills, many=False)
                            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        bills = bills_form.save()
                        bills.cash_id = get_cash.id
                        get_details_bills = DetailsBills.objects.filter(cash__user_id=request.data['cashier'],
                                                                        bills=None).all()
                        for bill in get_details_bills:
                            bill.bills_id = bills
                            bill.save()
                        bills.save()
                        if request.data['advance'] != '':
                            get_patient_settlement = PatientSettlement.objects.first()
                            if get_patient_settlement is not None:
                                regex = re.compile(r'[\d]+')
                                find = re.findall(regex, get_patient_settlement.code)
                                code = str('%05d' % (int(find[0]) + 1))

                                code_patient = get_patient_settlement.code[0:3] + code
                                PatientSettlement.objects.create(code=code_patient, patient_id=request.data['patient'],
                                                                 bills_id=bills.id, payment=request.data['advance'],
                                                                 cash_id=get_cash.id, wordings='')
                            else:
                                PatientSettlement.objects.create(patient_id=request.data['patient'], bills_id=bills,
                                                                 payment=request.data['advance'], cash_id=get_cash.id,
                                                                 wordings='')
                        else:
                            pass
                        if 'print' in request.query_params:
                            html_render = get_template('print.html')
                            # logo = settings.MEDIA_ROOT + '/logo.png'
                            html_content = html_render.render(
                                {'products': get_details_bills, 'bills': 'FC00056',
                                 'Hospital': "Hopital Central de Yaounde",
                                 # 'logo': logo,
                                 'MontantT': '10000',
                                 'STP': '1000',
                                 'STL': '10000',
                                 'Advance': '6000',
                                 'DomainePharm': 'Pharmacie',
                                 'DomaineLab': 'Laboratoire',
                                 'Doctor': 'Dr.Takou',
                                 'casher': 'Dimitri',
                                 'Contact': '690738500', 'addresse': 'Bandra Kurla Complex, Bandra (E), Mumbai.',
                                 'Left_to_pay': '4000',
                                 'Repayment': '200',
                                 'customer_name': 'Dimitri',
                                 'date': timezone.now()})
                            result = BytesIO()
                            pdf = pisa.pisaDocument(BytesIO(html_content.encode("ISO-8859-1")), result)
                            response = HttpResponse(content_type='application/pdf')
                            filename = 'Facture_' + '.pdf'
                            # filename = 'Facture_' + str(bills.code) + '.pdf'
                            response['Content-Disposition'] = 'inline; filename="' + filename + '"'
                            response['Access-Control-Expose-Headers'] = 'Content-Disposition,X-Suggested-Filename'
                            response.write(result.getvalue())
                            return response
                        else:
                            serializer = self.get_serializer(bills, many=False)
                            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

                else:
                    errors = {"cash": ["No open checkout."]}
                    return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                errors = {"cash": ["No permission allowed."]}
                return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        errors = {**bills_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        bills = self.get_object()
        bills_form = BillsForm(request.data, instance=bills)
        if bills_form.is_valid():
            bills = bills_form.save()
            bills.save()
            serializer = self.get_serializer(bills, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**bills_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        bills = self.get_object()
        bills.deleted = True
        bills.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists')
    def check_category(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            product = Product.objects.filter(name=data['name'])
            if product:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post', 'get'], url_path='print')
    def print(self, request, *args, **kwargs):
        html_render = get_template('print.html')
        # logo = settings.MEDIA_ROOT + '/logo.png'
        user = self.request.user
        get_details_bills = DetailsBills.objects.filter(user_id=user.id, bills_id='54').all()
        html_content = html_render.render(
            {'products': get_details_bills, 'bills': 'FC00056',
             'Hospital': "Hopital Central de Yaounde",
             # 'logo': logo,
             'MontantT': '10000',
             'STP': '1000',
             'STL': '10000',
             'Advance': '6000',
             'DomainePharm': 'Pharmacie',
             'DomaineLab': 'Laboratoire',
             'Doctor': 'Dr.Takou',
             'casher': 'Dimitri',
             'Contact': '690738500', 'addresse': 'Bandra Kurla Complex, Bandra (E), Mumbai.',
             'Left_to_pay': '4000',
             'Repayment': '200',
             'customer_name': 'Dimitri',
             'date': timezone.now()})
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_content.encode("ISO-8859-1")), result)
        response = HttpResponse(content_type='application/pdf')
        filename = 'Facture_' + str('FC00056') + '.pdf'
        response['Content-Disposition'] = 'inline; filename="' + filename + '"'
        response['Access-Control-Expose-Headers'] = 'Content-Disposition,X-Suggested-Filename'
        response.write(result.getvalue())
        outputStream = response
        return response

    @action(detail=False, methods=['get', 'post'], url_path='cash_movements')
    def cash_movements(self, request, *args, **kwargs):
        user = self.request.user
        if user.role in ['ADMIN', 'CASHIER']:
            get_cash = Cash.objects.filter(user_id=user.id, is_active=True).last()
            if get_cash:

                get_cash_movment = Cash_movement.objects.filter(cash_id=get_cash.id).all()

                serializer = Cash_movementSerializer(get_cash_movment, many=True)
                get_settlement = PatientSettlement.objects.filter(cash_id=get_cash.id)
                serializer_settle = PatientSettlementSerializer(get_settlement, many=True)
                content = {'content': {'cash_movement': serializer.data, 'settlement': serializer_settle.data}}
                return Response(data=content, status=status.HTTP_200_OK)
            else:
                content = {"content": []}
                return Response(data=content, status=status.HTTP_200_OK)
        else:
            errors = {"cash": ["not permission allowed."]}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class PatientSettlementViewSet(viewsets.ModelViewSet):
    queryset = PatientSettlement.objects.filter(deleted=False)
    serializer_class = PatientSettlementSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = PatientSettlementFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        return PatientSettlement.objects.filter(cash__user_id=self.request.user.id, deleted=False).all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        print(request.data)
        patient_settlement_form = PatientSettlementForm(request.data)
        if patient_settlement_form.is_valid():

            user = self.request.user
            if user.role in ['ADMIN', 'CASHIER']:

                get_cash = Cash.objects.filter(user_id=user.id, is_active=True).last()
                if get_cash:
                    get_patient_settlement = PatientSettlement.objects.first()
                    if get_patient_settlement is not None:
                        regex = re.compile(r'[\d]+')
                        find = re.findall(regex, get_patient_settlement.code)
                        code = str('%05d' % (int(find[0]) + 1))
                        patient_settlement = patient_settlement_form.save()
                        patient_settlement.cash_id = get_cash.id
                        patient_settlement.code = get_patient_settlement.code[0:3] + code
                        patient_settlement.save()
                        get_bills = Bills.objects.filter(patient_id=request.data['patient']).all()
                        payment = request.data['payment']
                        for bills in get_bills:
                            if payment == 0:
                                break
                            else:
                                print(payment)
                                pre_payment = int(payment) - int(bills.balance)
                                if pre_payment < 0:
                                    bills.balance = int(bills.balance) - int(payment)
                                    advance = int(bills.net_payable)-int(bills.balance)
                                    bills.advance = int(bills.advance) + advance
                                    bills.save()
                                    payment = 0
                                else:
                                    payment = pre_payment
                                    bills.balance = 0
                                    bills.advance = bills.net_payable
                                    bills.save()
                        serializer = self.get_serializer(patient_settlement, many=False)
                        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        patient_settlement = patient_settlement_form.save()
                        patient_settlement.cash_id = get_cash.id
                        patient_settlement.save()
                        get_bills = Bills.objects.filter(patient_id=request.data['patient']).all()
                        payment = request.data['payment']
                        for bills in get_bills:
                            if payment == 0:
                                break
                            else:
                                pre_payment = int(payment) - int(bills.balance)
                                if pre_payment < 0:
                                    bills.balance = int(bills.balance) - int(payment)
                                    bills.save()
                                    payment = 0
                                else:
                                    payment = pre_payment
                                    bills.advance = int(bills.advance)+ int(bills.balance)
                                    bills.balance = 0
                                    bills.save()
                        serializer = self.get_serializer(patient_settlement, many=False)
                        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


                else:
                    errors = {"cash": ["No Cash open."]}
                    return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                errors = {"cash": ["not permission allowed."]}
                return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        errors = {**patient_settlement_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        patient_settlement = self.get_object()
        patient_settlement_form = PatientSettlementForm(request.data, instance=patient_settlement)
        if patient_settlement_form.is_valid():
            patient_settlement = patient_settlement_form.save()
            patient_settlement.save()
            serializer = self.get_serializer(patient_settlement, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**patient_settlement_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        patient_settlement = self.get_object()
        patient_settlement.deleted = True
        patient_settlement.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_category(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            product = Product.objects.filter(name=data['name'])
            if product:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'post'], url_path='details_patients_settlements',
            permission_classes=[AllowAny])
    def details(self, request, *args, **kwargs):
        if request.method == 'GET':
            if request.query_params.get("patient") != 'null':
                get_bills = Bills.objects.filter(patient_id=request.query_params.get("patient")).all()
                serializer = BillsSerializer(get_bills, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            get_details = DetailsSupplies.objects.create(supplies_id=request.data['id_supplies'],
                                                         product_id=request.data['product']['id'],
                                                         quantity=request.data['quantity'],
                                                         total_amount=request.data['total_amount'],
                                                         arrival_price=request.data['arrival_price'],
                                                         product_code=request.data['product_code'],
                                                         product_name=request.data['product_name'])
            details = DetailsSuppliesSerializer(get_details, many=False)
            return Response(data=details.data, status=status.HTTP_200_OK)


class DetailsSuppliesViewSet(viewsets.ModelViewSet):
    queryset = DetailsSupplies.objects.all()
    serializer_class = DetailsSuppliesSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = DetailsSuppliesFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        user = self.request.user
        if self.request.GET.get("supplies"):
            print(self.request.GET.get("supplies"))
            if self.request.GET.get("supplies") == 'undefined':
                return DetailsSupplies.objects.filter(user_id=user.id, supplies_id=None).all()
            else:
                return DetailsSupplies.objects.filter(user_id=user.id,
                                                      supplies_id=self.request.GET.get("supplies")).all()
        else:
            return DetailsSupplies.objects.filter(user_id=user.id, supplies_id=None).all()

    def create(self, request, *args, **kwargs):
        detailsSupplies_form = DetailsSuppliesForm(data=request.data)
        print(request.data)
        if detailsSupplies_form.is_valid():

            user = self.request.user
            # get_supplies = Supplies.objects.filter(id=request.data['supplies']).last()
            get_product = Product.objects.filter(id=request.data['product']).last()
            get_details = DetailsSupplies.objects.filter(product_id=request.data['product'],
                                                         storage_depots_id=request.data['storage_depots'],
                                                         user_id=user.id, supplies=None).last()
            if get_details:
                get_details_stock = DetailsStock.objects.filter(product_id=request.data['product'],
                                                                storage_depots_id=request.data[
                                                                    'storage_depots']).last()
                get_details_stock.qte_stock = get_details_stock.qte_stock - int(get_details.quantity) + int(
                    request.data['quantity'])
                get_details_stock.save()
                get_details.quantity = get_details.quantity - int(get_details.quantity) + int(request.data['quantity'])
                get_details.total_amount = get_details.total_amount - int(get_details.total_amount) + int(
                    request.data['total_amount'])
                get_details.arrival_price = request.data['arrival_price']
                get_details.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                get_details_stock = DetailsStock.objects.filter(product_id=request.data['product'],
                                                                storage_depots_id=request.data[
                                                                    'storage_depots']).last()
                if get_details_stock:
                    get_details_stock.qte_stock = get_details_stock.qte_stock + int(request.data['quantity'])
                    total_amount = get_details_stock.qte_stock * float(get_details_stock.cmup) + int(
                        request.data['total_amount'])
                    total_qte = get_details_stock.qte_stock + int(request.data['quantity'])
                    cmup = total_amount / total_qte
                    get_details_stock.cmup = round(cmup, 2)
                    get_details_stock.save()
                    detailsSupplies = detailsSupplies_form.save()
                    detailsSupplies.storage_depots_id = request.data['storage_depots']
                    detailsSupplies.cmup = cmup
                    detailsSupplies.user_id = user.id
                    detailsSupplies.createdAt = request.data['createdAt']
                    detailsSupplies.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    detailsSupplies = detailsSupplies_form.save()
                    detailsSupplies.storage_depots_id = request.data['storage_depots']
                    detailsSupplies.cmup = request.data['arrival_price']
                    detailsSupplies.user_id = user.id
                    detailsSupplies.createdAt = request.data['createdAt']
                    detailsSupplies.save()
                    DetailsStock.objects.create(product_id=request.data['product'],
                                                storage_depots_id=request.data[
                                                    'storage_depots'], product_name=get_product.name,
                                                qte_stock=request.data['quantity'], cmup=request.data['arrival_price'])

                    serializer = self.get_serializer(detailsSupplies, many=False)
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**detailsSupplies_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        path = request.path
        end_path = path.rsplit('/', 1)[-1]
        get_details = DetailsSupplies.objects.filter(id=end_path).last()
        if get_details:
            get_details.supplies_id = request.data['supplies']
            get_details.product_id = get_details.product
            get_details.quantity = request.data['quantity']
            get_details.total_amount = request.data['total_amount']
            get_details.product_code = request.data['product_code']
            get_details.product_name = request.data['product_name']
            get_details.arrival_price = request.data['arrival_price']
            get_details.save()
            get_sum_details = DetailsSupplies.objects.filter(supplies_id=request.data['supplies']).aggregate(
                Sum('total_amount'))
            get_supplies = Supplies.objects.filter(id=get_details.supplies.id).last()
            get_supplies.supply_amount = get_sum_details['total_amount__sum']
            get_supplies.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            errors = {"errors": ["Already exist"]}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        path = request.path
        end_path = path.rsplit('/', 1)[-1]
        get_details = DetailsSupplies.objects.filter(id=end_path).last()
        get_product = Product.objects.filter(id=get_details.product.id).last()
        get_product.qte_stock = get_product.qte_stock - int(get_details.quantity)
        get_product.save()
        get_supplies = Supplies.objects.filter(id=get_details.supplies.id).last()
        get_supplies.supply_amount = get_supplies.supply_amount - get_details.total_amount
        get_supplies.save()

        get_details.delete()

        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='stock_available')
    def stock_available(self, request):
        get_detail_depot = DetailsStock.objects.filter(storage_depots_id=request.query_params.get("id"))
        if get_detail_depot:
            serializer = DetailsStockSerializer(get_detail_depot, many=True)
            content = {'content': serializer.data}
            return Response(data=content, status=status.HTTP_200_OK)
        else:
            content = {'content': []}
            return Response(data=content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='get_items')
    def get_items(self, request):
        startdate = request.query_params.get("start_date")
        enddate = request.query_params.get("end_date")
        get_product = DetailsSupplies.objects.filter(storage_depots_id=request.query_params.get("id"),
                                                     product_id=request.query_params.get("product"),
                                                     createdAt__range=[startdate, enddate])
        serializer = DetailsSuppliesSerializer(get_product, many=True)
        content = {'content': serializer.data}
        return Response(data=content, status=status.HTTP_200_OK)


class DetailsStock_movementViewSet(viewsets.ModelViewSet):
    queryset = DetailsStock_movement.objects.all()
    serializer_class = DetailsStock_movementSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = DetailsStock_movementFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        if self.request.GET.get("stock_movement"):
            if self.request.GET.get("stock_movement") == 'undefined':
                return DetailsStock_movement.objects.filter(stock_movement_id=None).all()
            else:
                return DetailsStock_movement.objects.filter(
                    stock_movement_id=self.request.GET.get("stock_movement")).all()
        else:
            return DetailsStock_movement.objects.filter(stock_movement_id=None).all()

    def create(self, request, *args, **kwargs):
        print(request.data)
        user = self.request.user
        detailsStock_movement_form = DetailsStock_movementForm(data=request.data)
        if detailsStock_movement_form.is_valid():
            get_detailsStock_movement = DetailsStock_movement.objects.filter(
                details_stock_id=request.data['details_stock'],
                storage_depots_id=request.data[
                    'storage_depots'],
                stock_movement=None, user_id=user.id).last()
            if get_detailsStock_movement:
                get_details_stock = DetailsStock.objects.filter(id=request.data['details_stock'],
                                                                storage_depots_id=request.data[
                                                                    'storage_depots']).last()
                if request.data['type_movement'] == 'ENTRY':
                    get_details_stock.qte_stock = get_details_stock.qte_stock - int(
                        get_detailsStock_movement.quantity) + int(
                        request.data['quantity'])
                    get_details_stock.save()
                    get_detailsStock_movement.quantity = get_detailsStock_movement.quantity - int(
                        get_detailsStock_movement.quantity) + int(request.data['quantity'])
                    get_detailsStock_movement.total_amount = get_detailsStock_movement.total_amount - int(
                        get_detailsStock_movement.total_amount) + int(
                        request.data['total_amount'])
                    get_detailsStock_movement.unit_price = request.data['unit_price']
                    get_detailsStock_movement.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    get_details_stock.qte_stock = get_details_stock.qte_stock + int(
                        get_detailsStock_movement.quantity) - int(
                        request.data['quantity'])
                    get_details_stock.save()
                    get_detailsStock_movement.quantity = get_detailsStock_movement.quantity + int(
                        get_detailsStock_movement.quantity) - int(request.data['quantity'])
                    get_detailsStock_movement.total_amount = get_detailsStock_movement.total_amount + int(
                        get_detailsStock_movement.total_amount) - int(
                        request.data['total_amount'])
                    get_detailsStock_movement.unit_price = request.data['unit_price']
                    get_detailsStock_movement.save()
                    return Response(status=status.HTTP_201_CREATED)
            else:
                detailsStock_movement = detailsStock_movement_form.save()
                detailsStock_movement.user_id = user.id
                detailsStock_movement.createdAt = request.data['createdAt']
                detailsStock_movement.save()
                get_details_stock = DetailsStock.objects.filter(id=request.data['details_stock'],
                                                                storage_depots_id=request.data[
                                                                    'storage_depots']).last()
                if get_details_stock:
                    if request.data['type_movement'] == 'ENTRY':
                        get_details_stock.qte_stock = get_details_stock.qte_stock + int(request.data['quantity'])
                        get_details_stock.save()
                        return Response(status=status.HTTP_201_CREATED)
                    else:
                        get_details_stock.qte_stock = get_details_stock.qte_stock - int(request.data['quantity'])
                        get_details_stock.save()
                        return Response(status=status.HTTP_201_CREATED)
                else:
                    errors = {"errors": ["Product not exist"]}
                    return Response(data=errors, status=status.HTTP_201_CREATED)
        errors = {**detailsStock_movement_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        path = request.path
        end_path = path.rsplit('/', 1)[-1]
        get_details = DetailsSupplies.objects.filter(id=end_path).last()
        if get_details:
            get_details.supplies_id = request.data['supplies']
            get_details.product_id = get_details.product
            get_details.quantity = request.data['quantity']
            get_details.total_amount = request.data['total_amount']
            get_details.product_code = request.data['product_code']
            get_details.product_name = request.data['product_name']
            get_details.arrival_price = request.data['arrival_price']
            get_details.save()
            get_sum_details = DetailsSupplies.objects.filter(supplies_id=request.data['supplies']).aggregate(
                Sum('total_amount'))
            get_supplies = Supplies.objects.filter(id=get_details.supplies.id).last()
            get_supplies.supply_amount = get_sum_details['total_amount__sum']
            get_supplies.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            errors = {"errors": ["Already exist"]}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        path = request.path
        end_path = path.rsplit('/', 1)[-1]
        get_details = DetailsSupplies.objects.filter(id=end_path).last()
        get_product = Product.objects.filter(id=get_details.product.id).last()
        get_product.qte_stock = get_product.qte_stock - int(get_details.quantity)
        get_product.save()
        get_supplies = Supplies.objects.filter(id=get_details.supplies.id).last()
        get_supplies.supply_amount = get_supplies.supply_amount - get_details.total_amount
        get_supplies.save()

        get_details.delete()

        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='stock_available')
    def stock_available(self, request):
        get_detail_depot = DetailsStock.objects.filter(storage_depots_id=request.query_params.get("id"))
        serializer = DetailsStockSerializer(get_detail_depot, many=True)
        content = {'content': serializer.data}
        return Response(data=content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='get_items')
    def get_items(self, request):
        startdate = request.query_params.get("start_date")
        enddate = request.query_params.get("end_date")
        get_product = DetailsStock_movement.objects.filter(storage_depots_id=request.query_params.get("id"),
                                                           details_stock__product__id=request.query_params.get(
                                                               "product"), createdAt__range=[startdate, enddate])
        serializer = DetailsStock_movementSerializer(get_product, many=True)
        content = {'content': serializer.data}
        return Response(data=content, status=status.HTTP_200_OK)


class DetailsInventoryViewSet(viewsets.ModelViewSet):
    queryset = DetailsInventory.objects.all()
    serializer_class = DetailsInventorySerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = DetailsInventoryFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        if self.request.GET.get("inventory"):
            if self.request.GET.get("inventory") == 'undefined':
                return DetailsInventory.objects.filter(inventory_id=None).all()
            else:
                return DetailsInventory.objects.filter(inventory_id=self.request.GET.get("inventory")).all()
        else:
            return DetailsInventory.objects.filter(inventory_id=None).all()

    def create(self, request, *args, **kwargs):
        print(request.data)
        user = self.request.user
        details_inventory_form = DetailsInventoryForm(data=request.data)
        if details_inventory_form.is_valid():
            get_details_inventory = DetailsInventory.objects.filter(
                details_stock_id=request.data['details_stock'],
                storage_depots_id=request.data[
                    'storage_depots'],
                inventory=None, user_id=user.id).last()
            if get_details_inventory:
                get_details_inventory.amount = get_details_inventory.amount - int(
                    get_details_inventory.amount) + int(
                    request.data['amount'])
                get_details_inventory.amount_adjusted = get_details_inventory.amount_adjusted - int(
                    get_details_inventory.amount_adjusted) + int(
                    request.data['amount_adjusted'])
                get_details_inventory.quantity_adjusted = get_details_inventory.quantity_adjusted - int(
                    get_details_inventory.quantity_adjusted) + int(
                    request.data['quantity_adjusted'])
                get_details_inventory.save()

                return Response(status=status.HTTP_201_CREATED)
            else:
                details_inventory = details_inventory_form.save()
                details_inventory.user_id = user.id
                details_inventory.save()
                return Response(status=status.HTTP_201_CREATED)
        errors = {**details_inventory_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        path = request.path
        end_path = path.rsplit('/', 1)[-1]
        get_details = DetailsSupplies.objects.filter(id=end_path).last()
        if get_details:
            get_details.supplies_id = request.data['supplies']
            get_details.product_id = get_details.product
            get_details.quantity = request.data['quantity']
            get_details.total_amount = request.data['total_amount']
            get_details.product_code = request.data['product_code']
            get_details.product_name = request.data['product_name']
            get_details.arrival_price = request.data['arrival_price']
            get_details.save()
            get_sum_details = DetailsSupplies.objects.filter(supplies_id=request.data['supplies']).aggregate(
                Sum('total_amount'))
            get_supplies = Supplies.objects.filter(id=get_details.supplies.id).last()
            get_supplies.supply_amount = get_sum_details['total_amount__sum']
            get_supplies.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            errors = {"errors": ["Already exist"]}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        path = request.path
        end_path = path.rsplit('/', 1)[-1]
        get_details = DetailsSupplies.objects.filter(id=end_path).last()
        get_product = Product.objects.filter(id=get_details.product.id).last()
        get_product.qte_stock = get_product.qte_stock - int(get_details.quantity)
        get_product.save()
        get_supplies = Supplies.objects.filter(id=get_details.supplies.id).last()
        get_supplies.supply_amount = get_supplies.supply_amount - get_details.total_amount
        get_supplies.save()

        get_details.delete()

        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='stock_available')
    def stock_available(self, request):
        get_detail_depot = DetailsStock.objects.filter(storage_depots_id=request.query_params.get("id"))
        serializer = DetailsStockSerializer(get_detail_depot, many=True)
        # get_product = DetailsSupplies.objects.filter(supplies__storage_depots=request.query_params.get("id")).order_by(
        #     'product_id').distinct("product_id")
        # productList = []
        # for product in get_product:
        #     get_prod = Product.objects.filter(id=product.product_id).last()
        #     productList.append(get_prod)
        # serializer = DetailsSuppliesSerializer(get_product, many=True)
        content = {'content': serializer.data}
        return Response(data=content, status=status.HTTP_200_OK)


class SuppliersViewSet(viewsets.ModelViewSet):
    queryset = Suppliers.objects.filter(deleted=False)
    serializer_class = SuppliersSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = SuppliersFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        suppliers_form = SuppliersForm(request.data)
        if suppliers_form.is_valid():
            get_suppliers = Suppliers.objects.first()
            if get_suppliers is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_suppliers.code)
                code = str('%04d' % (int(find[0]) + 1))
                suppliers = suppliers_form.save()
                suppliers.code = get_suppliers.code[0:3] + code
                suppliers.save()
                serializer = self.get_serializer(suppliers, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                suppliers = suppliers_form.save()
                suppliers.save()
                serializer = self.get_serializer(suppliers, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**suppliers_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        suppliers = self.get_object()
        suppliers_form = SuppliersForm(request.data, instance=suppliers)
        if suppliers_form.is_valid():
            suppliers = suppliers_form.save()
            suppliers.save()
            serializer = self.get_serializer(suppliers, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**suppliers_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        suppliers = self.get_object()
        suppliers.deleted = True
        suppliers.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_category(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            suppliers = Suppliers.objects.filter(name=data['name'])
            if suppliers:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class Medical_actViewSet(viewsets.ModelViewSet):
    queryset = Medical_act.objects.filter(deleted=False)
    serializer_class = Medical_actSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = Medical_actFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        print(request.data)
        if request.data['medical_areas'] is not None:
            request_update = request.data
            request_update['medical_areas'] = request.data['medical_areas']['id']
            medical_act_form = Medical_actFormUpdate(request.data)
            if medical_act_form.is_valid():
                get_medical_act = Medical_act.objects.first()
                if get_medical_act is not None:
                    regex = re.compile(r'[\d]+')
                    find = re.findall(regex, get_medical_act.code)
                    code = str('%04d' % (int(find[0]) + 1))
                    medical_act = medical_act_form.save()
                    medical_act.code = get_medical_act.code[0:3] + code
                    medical_act.save()
                    serializer = self.get_serializer(medical_act, many=False)
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    medical_act = medical_act_form.save()
                    medical_act.save()
                    serializer = self.get_serializer(medical_act, many=False)
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            medical_act_form = Medical_actForm(request.data)
            if medical_act_form.is_valid():
                get_medical_act = Medical_act.objects.first()
                if get_medical_act is not None:
                    regex = re.compile(r'[\d]+')
                    find = re.findall(regex, get_medical_act.code)
                    code = str('%04d' % (int(find[0]) + 1))
                    medical_act = medical_act_form.save()
                    medical_act.code = get_medical_act.code[0:3] + code
                    medical_act.save()
                    serializer = self.get_serializer(medical_act, many=False)
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                else:
                    medical_act = medical_act_form.save()
                    medical_act.save()
                    serializer = self.get_serializer(medical_act, many=False)
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**medical_act_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        medical_act = self.get_object()
        medical_act_form = Medical_actForm(request.data, instance=medical_act)
        if medical_act_form.is_valid():
            medical_act = medical_act_form.save()
            medical_act.save()
            serializer = self.get_serializer(medical_act, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**medical_act_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        medical_act = self.get_object()
        medical_act.deleted = True
        medical_act.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists', permission_classes=[AllowAny])
    def check_medical_act(self, request, *args, **kwargs):
        data = request.data
        errors = {"name": ["This field already exists."]}
        if 'name' in data:
            medical_act = Medical_act.objects.filter(name=data['name'])
            if medical_act:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.filter(deleted=False)
    serializer_class = DoctorSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filterset_class = DoctorFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        doctor_form = DoctorForm(request.data)
        if doctor_form.is_valid():
            get_doctor = Doctor.objects.first()
            if get_doctor is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_doctor.code)
                code = str('%04d' % (int(find[0]) + 1))
                doctor = doctor_form.save()
                doctor.code = get_doctor.code[0:3] + code
                doctor.save()
                if request.data['password']:
                    print(request.data)
                    data_user = {'username':request.data['username'],'password':request.data['password']}
                    user_form = UserForm(data_user)
                    if user_form.is_valid():
                        get_user = User.objects.first()
                        if get_user:
                            user = user_form.save()
                            user.set_password(user_form.cleaned_data.get(data_user['password']))
                            regex = re.compile(r'[\d]+')
                            find = re.findall(regex, get_user.code)
                            code = str('%04d' % (int(find[0]) + 1))
                            user.code = get_user.code[0:3] + code
                            user.doctor = doctor
                            user.role = 'DOCTOR'
                            user.save()
                            serializer = self.get_serializer(doctor, many=False)
                            return Response( status=status.HTTP_201_CREATED)
                        else:
                            user = user_form.save()
                            user.set_password(user_form.cleaned_data.get('password'))
                            user.doctor = doctor
                            user.role = 'DOCTOR'
                            user.save()
                            serializer = self.get_serializer(doctor, many=False)
                            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        errors = {**user_form.errors, }
                        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer = self.get_serializer(doctor, many=False)
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                doctor = doctor_form.save()
                doctor.save()
                if request.data['password']:
                    user_form = UserForm(request.data)
                    if user_form.is_valid():
                        get_user = User.objects.first()
                        if get_user:
                            user = user_form.save()
                            user.set_password(user_form.cleaned_data.get('password'))
                            regex = re.compile(r'[\d]+')
                            find = re.findall(regex, get_user.code)
                            code = str('%04d' % (int(find[0]) + 1))
                            user.code = get_user.code[0:3] + code
                            user.doctor = doctor
                            user.role = 'DOCTOR'
                            user.save()
                            serializer = self.get_serializer(doctor, many=False)
                            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            user = user_form.save()
                            user.set_password(user_form.cleaned_data.get('password'))
                            user.doctor = doctor
                            user.role = 'DOCTOR'
                            user.save()
                            serializer = self.get_serializer(doctor, many=False)
                            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        errors = {**user_form.errors, }
                        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

                serializer = self.get_serializer(doctor, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**doctor_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        doctor = self.get_object()
        doctor_form = DoctorForm(request.data, instance=doctor)
        if doctor_form.is_valid():
            doctor = doctor_form.save()
            doctor.save()
            serializer = self.get_serializer(doctor, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**doctor_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        doctor = self.get_object()
        doctor.deleted = True
        doctor.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='name/exists')
    def get_doctor(self, request, *args, **kwargs):
        errors = {"name": ["This field already exists."]}
        if 'name' in request.data:
            doctor = Doctor.objects.filter(name=request.data['name'])
            if doctor:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='schedules')
    def schedules(self, request, *args, **kwargs):
        get_doctor = Doctor.objects.filter(id=request.data['doctor']).last()
        get_doctor.intervention_days = request.data['intervention_days']
        get_doctor.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='exports')
    def exports(self, request, *args, **kwargs):
        get_doctors = Doctor.objects.all()
        serializer_bills = DoctorSerializer(get_doctors, many=True)
        doctor = serializer_bills.data
        get_hospital = Hospital.objects.last()
        html_render = get_template('export_doctor.html')
        html_content = html_render.render(
            {'doctors': doctor, 'hospital': get_hospital.name, 'contact': get_hospital.phone,
             'address': get_hospital.address,
             'date': datetime.today().strftime("%Y-%m-%d %H:%M:%S")})
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_content.encode("ISO-8859-1")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            filename = 'Export' + datetime.today().strftime("%Y-%m-%d %H:%M:%S") + '.pdf'
            response['Content-Disposition'] = 'inline; filename="' + filename + '"'
            response['Access-Control-Expose-Headers'] = 'Content-Disposition,X-Suggested-Filename'
            return response
        else:
            return None


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.filter(deleted=False)
    serializer_class = PatientSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    # filterset_class = PatientFilter
    filter_backends = (filters.DjangoFilterBackend,)

    #
    # def get_queryset(self):
    #
    #     """
    #     This view should return a list of all the users
    #     for the currently authenticated user.
    #     """
    #
    #     patient = Patient.objects.filter(deleted=False)
    #     serializer = PatientSerializer(patient, many=True)
    #     print(serializer.data)
    #     return Patient.objects.filter(deleted=False)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            user = self.request.user
            if isinstance(user, User):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        patient_form = PatientForm(request.data)
        if patient_form.is_valid():
            get_patient = Patient.objects.first()
            if get_patient is not None:
                regex = re.compile(r'[\d]+')
                find = re.findall(regex, get_patient.code)
                code = str('%04d' % (int(find[0]) + 1))
                patient = patient_form.save()
                patient.code = get_patient.code[0:3] + code
                patient.save()
                if request.data['password']:
                    user_form = UserForm(request.data)
                    if user_form.is_valid():
                        get_user = User.objects.first()
                        if get_user:
                            user = user_form.save()
                            user.set_password(user_form.cleaned_data.get('password'))
                            regex = re.compile(r'[\d]+')
                            find = re.findall(regex, get_user.code)
                            code = str('%04d' % (int(find[0]) + 1))
                            user.code = get_user.code[0:3] + code
                            user.doctor = patient
                            user.role = 'PATIENT'
                            user.save()
                            serializer = self.get_serializer(patient, many=False)
                            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            user = user_form.save()
                            user.set_password(user_form.cleaned_data.get('password'))
                            user.doctor = patient
                            user.role = 'PATIENT'
                            user.save()
                            serializer = self.get_serializer(patient, many=False)
                            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        errors = {**user_form.errors, }
                        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

                serializer = self.get_serializer(patient, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                patient = patient_form.save()
                patient.save()
                if request.data['password']:
                    user_form = UserForm(request.data)
                    if user_form.is_valid():
                        get_user = User.objects.first()
                        if get_user:
                            user = user_form.save()
                            user.set_password(user_form.cleaned_data.get('password'))
                            regex = re.compile(r'[\d]+')
                            find = re.findall(regex, get_user.code)
                            code = str('%04d' % (int(find[0]) + 1))
                            user.code = get_user.code[0:3] + code
                            user.doctor = patient
                            user.role = 'PATIENT'
                            user.save()
                            serializer = self.get_serializer(patient, many=False)
                            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            user = user_form.save()
                            user.set_password(user_form.cleaned_data.get('password'))
                            user.doctor = patient
                            user.role = 'PATIENT'
                            user.save()
                            serializer = self.get_serializer(patient, many=False)
                            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        errors = {**user_form.errors, }
                        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
                serializer = self.get_serializer(patient, many=False)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        errors = {**patient_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        patient = self.get_object()
        patient_form = PatientForm(request.data, instance=patient)
        if patient_form.is_valid():
            patient = patient_form.save()
            patient.save()
            serializer = self.get_serializer(patient, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        errors = {**patient_form.errors}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        patient = self.get_object()
        patient.deleted = True
        patient.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='exports')
    def exports(self, request, *args, **kwargs):
        get_doctors = Doctor.objects.all()
        serializer_bills = PatientSerializer(get_doctors, many=True)
        patient = serializer_bills.data
        get_hospital = Hospital.objects.last()
        html_render = get_template('export_patient.html')
        html_content = html_render.render(
            {'patients': patient, 'hospital': get_hospital.name, 'contact': get_hospital.phone,
             'address': get_hospital.address,
             'date': datetime.today().strftime("%Y-%m-%d %H:%M:%S")})
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_content.encode("ISO-8859-1")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            filename = 'Export' + datetime.today().strftime("%Y-%m-%d %H:%M:%S") + '.pdf'
            response['Content-Disposition'] = 'inline; filename="' + filename + '"'
            response['Access-Control-Expose-Headers'] = 'Content-Disposition,X-Suggested-Filename'
            return response
        else:
            return None

    @action(detail=False, methods=['post'], url_path='name/exists')
    def check_name(self, request, *args, **kwargs):
        errors = {"name": ["This field already exists."]}
        if 'name' in request.data:
            users = Patient.objects.filter(name=request.data['name'])
            if users:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    if not isinstance(user, User):
        return Response(data={'message': _('Profile not found')}, status=status.HTTP_404_NOT_FOUND)
    profile = user.profile
    profile_form = ProfileForm(instance=profile, data=request.data or {})
    if profile_form.is_valid():
        profile = profile_form.save()
        serializer = ProfileSerializer(profile, many=False)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    return Response(
        data=profile_form.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
