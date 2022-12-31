from django.urls import path
from django.conf.urls import include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework import routers
from hospital.views import UserViewSet, HospitalViewSet, home_view, DepartmentsViewSet, profile_view, Medical_areasViewSet, \
    Medical_actViewSet, DoctorViewSet, PatientViewSet, Storage_depotsViewSet, Expenses_natureViewSet, \
    AppointmentViewSet, OrdinanceViewSet, CashViewSet, Cash_movementViewSet, CategoryViewSet, ShapeViewSet, \
    ProductViewSet, SuppliersViewSet, SuppliesViewSet, DetailsSuppliesViewSet, BillViewSet, DetailsBillsViewSet, \
    PatientSettlementViewSet, Stock_movementViewSet, DetailsStock_movementViewSet, InventoryViewSet, \
    DetailsInventoryViewSet, ConsultationViewSet, BackgroundViewSet, PrescriptionViewSet, ExaminationViewSet, DCIViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'bills', BillViewSet)
router.register(r'patients_settlements', PatientSettlementViewSet)
router.register(r'users', UserViewSet)
router.register(r'hospitals', HospitalViewSet)
router.register(r'departments', DepartmentsViewSet)
router.register(r'medical_areas', Medical_areasViewSet)
router.register(r'medical_act', Medical_actViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'storage_depots', Storage_depotsViewSet)
router.register(r'expenses_nature', Expenses_natureViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'ordinances', OrdinanceViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'backgrounds', BackgroundViewSet)
router.register(r'examinations', ExaminationViewSet)
router.register(r'cashs', CashViewSet)
router.register(r'cash_movements', Cash_movementViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'shapes', ShapeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'suppliers', SuppliersViewSet)
router.register(r'supplies', SuppliesViewSet)
router.register(r'details_supplies', DetailsSuppliesViewSet)
router.register(r'details_bills', DetailsBillsViewSet)
router.register(r'details_stock_movement', DetailsStock_movementViewSet)
router.register(r'stock_movements', Stock_movementViewSet)
router.register(r'inventories', InventoryViewSet)
router.register(r'dcis', DCIViewSet)
router.register(r'details_inventories', DetailsInventoryViewSet)

urlpatterns = [
    path('', home_view),
    path('api/v1/', include(router.urls)),
    path('api/v1/profile', profile_view),
    path('api/v1/login', TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('api/v1/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
