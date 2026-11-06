import logging,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from screens.trebb_allfunctions import get_traceback
from screens.trebb_db import get_listings_dict
from screens.trebb_main import trebb_main


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler()
    ],
    force=True
)


def create_chrome_driver() -> webdriver.Chrome:
    """Configures headless Chrome with production memory management flags."""
    options = Options()
    #.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(90)
    return driver


_HARDCODED_LISTINGS_DICT = {
    # ==================== ADD LISTING PAGE ====================
    "AddListing_SearchBy": "Address",
    "AddListing_Address": "123 Main Street",
    "AddListing_LRO": "",
    "AddListing_OwnerName": "",
    "AddListing_PIN": "",
    "AddListing_ARN": "",
    "AddListing_Member": "PEGGY HILL",
    "AddListing_TransactionType": "For Sale",
    "AddListing_PropertyClass": "Residential Freehold",
    "AddListing_PropertyType": "Detached",
    "AddListing_StreetNumber": "123",
    "AddListing_StreetName": "Main",
    "AddListing_Abbreviation": "Street",
    "AddListing_StreetDirection": "E",
    "AddListing_UnitNumber": "4B",
    "AddListing_Area": "Algoma",
    "AddListing_Municipality": "Algoma Remote Area",
    "AddListing_Community": "West",
    "AddListing_PostalCode": "P0S 1C0",

    # ==================== DRAFT Location ====================
    "DraftLocation_ARN": "",
    "DraftLocation_ReasonNoARN": "",
    "DraftLocation_PIN": "",
    "DraftLocation_ReasonNoPIN": "",
    "DraftLocation_AdditionalPIN": "",
    "DraftLocation_Area": "Algoma",
    "DraftLocation_Muncipality": "Algoma Remote Area",
    "DraftLocation_Community": "West",
    "DraftLocation_StreetDirectionPrefix": "E",
    "DraftLocation_StreetNumber": "123",
    "DraftLocation_StreetName": "Main",
    "DraftLocation_Abbreviation": "Street",
    "DraftLocation_StreetDirection": "E",
    "DraftLocation_UnitNumber": "4B",
    "DraftLocation_PostalCode": "P0S 1C0",
    "DraftLocation_FrontingOn": "West",
    "DraftLocation_LegalDescription": "PT LT 5 CON 3 INNISFIL PT 1 51R24103 ; INNISFIL",
    "DraftLocation_LotFront": "400.98",
    "DraftLocation_LotDepth": "400.89",
    "DraftLocation_LotSizeCode": "Feet",
    "DraftLocation_LotIrregularities": "662.21 ft x 752.18 ft x 462.06 ft",
    "DraftLocation_LotShape": "Rectangular",
    "DraftLocation_LotSizeSource": "GeoWarehouse",
    "DraftLocation_LotSizeArea": "3.49",
    "DraftLocation_LotSizeAreaCode": "Acres",
    "DraftLocation_Winterized": "Fully",
    "DraftLocation_Acreage": "2-4.99",
    "DraftLocation_WaterFront": "No",
    "DraftLocation_Directions": "Hwy 400/Hwy 89/5th Sideroad",
    "DraftLocation_MainCrossStreets": "5th Sideroad Between 3rd Line & 4th Line",
    "DraftLocation_Zoning": "RR & EP",
    "DraftLocation_TransactionType": "For Sale",

    # ==================== DRAFT AMOUNTS & DATES ====================

    "DraftAmountsDates_ListPrice": "100000",
    "DraftAmountsDates_PossessionDate": "12/28/2026",
    "DraftAmountsDates_PossessionRemarks": "Flexible",
    "DraftAmountsDates_PossessionType": "Flexible",
    "DraftAmountsDates_HoldoverDays": "90",

    "DraftAmountsDates_LandlordName": "Jakes Bejoy",
    "DraftAmountsDates_LeaseTerm": "",
    "DraftAmountsDates_PaymentFrequency": "",
    "DraftAmountsDates_PaymentMethod": "",

    "DraftAmountsDates_ListPriceToReducedReflectHSTRebate": "No",
    "DraftAmountsDates_HSTApplicableToSamePrice": "Not Subject to HST",
    "DraftAmountsDates_DevelopmentChargesPaid": "No,Unknown",

    "DraftAmountsDates_Taxes": "7676.3",
    "DraftAmountsDates_TaxYear": "2026",
    "DraftAmountsDates_TaxType": "",
    "DraftAmountsDates_Assessment": "Land Assessment",
    "DraftAmountsDates_AssessmentYear": "2026",

    "DraftAmountsDates_ContractCommencement": "12/01/2026",
    "DraftAmountsDates_ExpiryDate": "12/28/2027",
    "DraftAmountsDates_MortgageComments": "Mortagagee",

    "DraftAmountsDates_PhasedInTaxAssessedValue": "NA",
    "DraftAmountsDates_RoadAccessFee": "NA",

    "DraftAmountsDates_LandLease": "No",
    "DraftAmountsDates_LeasedLandFee": "NA",
    "DraftAmountsDates_LandLeaseAmountFrequency": "",
    "DraftAmountsDates_LandLeaseExpirationDate": "",

    "DraftAmountsDates_LocalImprovements": "",
    "DraftAmountsDates_LocalImprovementsComments": "NA",

    # Additional fields identified from Script 2
    "DraftAmountsDates_SharesPercent": "",
    "DraftAmountsDates_Maintenance": "",
    "DraftAmountsDates_MinimumRentalTermMonths": "",
    "DraftAmountsDates_MaximumRentalMonthsTerm": "",
    "DraftAmountsDates_ListPriceCode": "",
    "DraftAmountsDates_CommercialCondoFeeMonthly": "",

    "DraftAmountsDates_RentalApplicationRequired": "",
    "DraftAmountsDates_DepositRequired": "",
    "DraftAmountsDates_LeaseAgreement": "",
    "DraftAmountsDates_ReferencesRequired": "",
    "DraftAmountsDates_CreditCheck": "",
    "DraftAmountsDates_EmploymentLetter": "",
    "DraftAmountsDates_NonSmokingPolicy": "",
    "DraftAmountsDates_BuyOption": "",
    "DraftAmountsDates_IncludedInLeaseCost": "",

    # ==================== DRAFT EXTERIOR ====================

    "DraftExterior_PropertyType": "Detached",
    "DraftExterior_LINK": "No",
    "DraftExterior_ParcelofTiedLand": "No",
    "DraftExterior_POTLMonthlyFee": "100",
    "DraftExterior_VacantLandCondo": "No",
    "DraftExterior_VacantLandCondoMonthlyFee": "100",
    "DraftExterior_Assignment": "No",
    "DraftExterior_FractionalOwnership": "No",
    "DraftExterior_PortionofPropertyforLease": "Main",
    "DraftExterior_PortionofPropertyComments": "land",
    "DraftExterior_Style": "Bungalow",
    "DraftExterior_View": "Beach, City",
    "DraftExterior_Exterior": "Brick,Wood",
    "DraftExterior_ExteriorFeatures": "Deck,Canopy",
    "DraftExterior_FoundationDetail": "Block,Brick",
    "DraftExterior_Roof": "Flat,Green",
    "DraftExterior_Topography": "Rocky,Flat",
    "DraftExterior_Garage": "No",
    "DraftExterior_GarageType": "Attached",
    "DraftExterior_GarageParkingSpaces": "2",
    "DraftExterior_ParkingDrive": "Lane,None",
    "DraftExterior_DriveParkingSpaces": "10",
    "DraftExterior_TotalParkingSpaces": "12",

    # Parking 1
    "DraftExterior_ParkingType1": "Common",
    "DraftExterior_ParkingLevelUnit1": "1",
    "DraftExterior_ParkingSpot1": "3",

    # Parking 2
    "DraftExterior_ParkingType2": "Rental",
    "DraftExterior_ParkingLevelUnit2": "4",
    "DraftExterior_ParkingSpot2": "6",

    "DraftExterior_ParkingCostMonth": "4000",
    "DraftExterior_Exposure": "East",
    "DraftExterior_Balcony": "Open",
    "DraftExterior_Water": "Well",
    "DraftExterior_Pool": "Salt",
    "DraftExterior_Sewers": "Septic",
    "DraftExterior_RetirementCommunity": "No",
    "DraftExterior_PhysicallyHandicappedEquipped": "No",
    "DraftExterior_SpecialDesignation": "Other,Unknown",
    "DraftExterior_ApproximateAge": "16-30",
    "DraftExterior_YearBuilt": "2001",
    "DraftExterior_YearBuiltSource": "MPAC",
    "DraftExterior_Builder": "Peggy",
    "DraftExterior_ApproximateSquareFootage": "1500-2000",
    "DraftExterior_SQFTSourceComment": "MPAC",
    "DraftExterior_AboveGradeFinishedSQFT": "1613",
    "DraftExterior_AboveGradeFinishedSQFTSource": "MPAC",
    "DraftExterior_BelowGradeFinishedSQFT": "",
    "DraftExterior_BelowGradeFinishedSQFTSource": "MPAC",
    "DraftExterior_OtherSQFT": "12",
    "DraftExterior_TotalUnfinished": "13",
    "DraftExterior_PropertyFeaturesAreaInfluences": "Beach,Park",
    "DraftExterior_SecurityFeatures": "None",
    "DraftExterior_OtherStructures": "Arena,None",
    "DraftExterior_BuildingAmenities": "Gym,Playground",
    "DraftExterior_WaterSupplyType": "Cistern,Unknown",
    "DraftExterior_Farm/Agriculture": "Hog, Horse, Goat",
    "DraftExterior_FarmFeatures": "Quotas,Stalls",
    "DraftExterior_SoilType": "Clay,Heavy,Light",
    "DraftExterior_SurveyType": "None",
    "DraftExterior_SurveyYear": "2001",
    "DraftExterior_WaterMeter": "None",
    "DraftExterior_WellCapacityGalMinute": "",
    "DraftExterior_WellDepth": "No",
    "DraftExterior_Cable": "Yes",
    "DraftExterior_Hydro": "No",
    "DraftExterior_SewersYN": "Yes",
    "DraftExterior_Gas(Natural)": "No",
    "DraftExterior_MunicipalWater": "Yes",
    "DraftExterior_Telephone": "No",
    
    # ==================== DRAFT WATERFRONT/RURAL ====================

    "DraftWaterfrontRural_WaterfrontType": "Direct,None",
    "DraftWaterfrontRural_BodyOfWaterName": "Lake Simcoe",
    "DraftWaterfrontRural_WaterBodyType": "Lake",
    "DraftWaterfrontRural_Island": "No",
    "DraftWaterfrontRural_WaterView": "Direct",
    "DraftWaterfrontRural_ChannelName": "",
    "DraftWaterfrontRural_WaterFrontage": "78.25",
    "DraftWaterfrontRural_WaterFrontageUnits": "Feet",
    "DraftWaterfrontRural_SeasonalDwelling": "Yes",
    "DraftWaterfrontRural_AccessToProperty": "By Water,Water Only",
    "DraftWaterfrontRural_Shoreline": "Rocky, Shallow",
    "DraftWaterfrontRural_WaterfrontFeatures": "Island, Dock",
    "DraftWaterfrontRural_ShorelineExposure": "All,East,North",
    "DraftWaterfrontRural_ShorelineAllowance": "Owned",
    "DraftWaterfrontRural_AlternativePower": "Microfit,None",
    "DraftWaterfrontRural_Sewage": "Privy",
    "DraftWaterfrontRural_WaterDeliveryFeatures": "UV System",
    "DraftWaterfrontRural_EasementsRestrictions": "Easement,Moraine",
    "DraftWaterfrontRural_RuralServices": "Cell Services",
    "DraftWaterfrontRural_WaterfrontAccessoryBuildings": "Boat House, Single Slip",
    "DraftWaterfrontRural_DockingType": "None,Private",

    # ==================== DRAFT INTERIOR ====================

    "DraftInterior_NumberofRooms": "1",
    "DraftInterior_RoomsPlus": "3",
    "DraftInterior_NumberofBedrooms": "2",
    "DraftInterior_BedroomsPlus": "3",
    "DraftInterior_NumberofKitchens": "1",
    "DraftInterior_KitchensPlus": "2",

    # Washrooms 1
    "DraftInterior_Washrooms1": "1",
    "DraftInterior_NumberOfPieces1": "1",
    "DraftInterior_Level1": "Flat",

    # Washrooms 2
    "DraftInterior_Washrooms2": "1",
    "DraftInterior_NumberOfPieces2": "2",
    "DraftInterior_Level2": "Second",

    # Washrooms 3
    "DraftInterior_Washrooms3": "1",
    "DraftInterior_NumberOfPieces3": "2",
    "DraftInterior_Level3": "Third",

    # Washrooms 4
    "DraftInterior_Washrooms4": "3",
    "DraftInterior_NumberOfPieces4": "2",
    "DraftInterior_Level4": "Main",

    # Washrooms 5
    "DraftInterior_Washrooms5": "3",
    "DraftInterior_NumberOfPieces5": "2",
    "DraftInterior_Level5": "Lower",

    "DraftInterior_InteriorFeatures": "Atrium",
    "DraftInterior_FamilyRoomBonusRoom": "No",
    "DraftInterior_Basement": "Full, Half",
    "DraftInterior_FireplaceStove": "No",
    "DraftInterior_FireplaceFeatures": "Family Room, Natural Gas",
    "DraftInterior_NumberofFireplaces": "",
    "DraftInterior_HeatSource": "Gas,Oil",
    "DraftInterior_HeatType": "Water,Radiant",
    "DraftInterior_AirConditioning": "None,Central Air",
    "DraftInterior_UFFI": "Yes",
    "DraftInterior_LaundryLevel": "Lower Level",
    "DraftInterior_AccessibilityFeatures": "Elevator",
    "DraftInterior_ElevatorLift": "No",
    "DraftInterior_LeaseToOwnItems": "Boiler, None",
    "DraftInterior_UnderContract": "Internet, Freezer",

    # Additional fields from script
    "DraftInterior_PetsPermitted": "",
    "DraftInterior_LaundryFeatures": "",
    "DraftInterior_Furnished": "",
    "DraftInterior_Locker": "",
    "DraftInterior_LockerLevel": "",
    "DraftInterior_LockerUnit": "",
    "DraftInterior_LockerNumber": "",
    # ==================== DRAFT ROOMS/DETAIL ====================

    # ==================== DRAFT ROOMS/DETAIL ====================

    "DraftRoomsDetail_NumberOfRooms": "5",

    # Room 1
    "DraftRoomsDetail_RoomLevel_1": "Main",
    "DraftRoomsDetail_RoomType_1": "Living Room",
    "DraftRoomsDetail_LengthMetres_1": "5.2",
    "DraftRoomsDetail_LengthFtIn_1": "17",
    "DraftRoomsDetail_WidthMetres_1": "4.5",
    "DraftRoomsDetail_WidthFtIn_1": "14",
    "DraftRoomsDetail_HeightMetres_1": "2.7",
    "DraftRoomsDetail_HeightFtIn_1": "9",
    "DraftRoomsDetail_Description1_1": "Hardwood Floor",
    "DraftRoomsDetail_Description2_1": "Window",
    "DraftRoomsDetail_Description3_1": "Fireplace",

    # Room 2
    "DraftRoomsDetail_RoomLevel_2": "Main",
    "DraftRoomsDetail_RoomType_2": "Kitchen",
    "DraftRoomsDetail_LengthMetres_2": "3.8",
    "DraftRoomsDetail_LengthFtIn_2": "12",
    "DraftRoomsDetail_WidthMetres_2": "3.2",
    "DraftRoomsDetail_WidthFtIn_2": "10",
    "DraftRoomsDetail_HeightMetres_2": "2.7",
    "DraftRoomsDetail_HeightFtIn_2": "9",
    "DraftRoomsDetail_Description1_2": "Ceramic Floor",
    "DraftRoomsDetail_Description2_2": "Eat-in Kitchen",
    "DraftRoomsDetail_Description3_2": "Window",

    # Room 3
    "DraftRoomsDetail_RoomLevel_3": "Second",
    "DraftRoomsDetail_RoomType_3": "Primary Bedroom",
    "DraftRoomsDetail_LengthMetres_3": "4.5",
    "DraftRoomsDetail_LengthFtIn_3": "15",
    "DraftRoomsDetail_WidthMetres_3": "3.8",
    "DraftRoomsDetail_WidthFtIn_3": "12",
    "DraftRoomsDetail_HeightMetres_3": "2.7",
    "DraftRoomsDetail_HeightFtIn_3": "9",
    "DraftRoomsDetail_Description1_3": "Hardwood Floor",
    "DraftRoomsDetail_Description2_3": "Closet",
    "DraftRoomsDetail_Description3_3": "Window",

    # Room 4
    "DraftRoomsDetail_RoomLevel_4": "Second",
    "DraftRoomsDetail_RoomType_4": "Bedroom",
    "DraftRoomsDetail_LengthMetres_4": "3.5",
    "DraftRoomsDetail_LengthFtIn_4": "11",
    "DraftRoomsDetail_WidthMetres_4": "3.0",
    "DraftRoomsDetail_WidthFtIn_4": "10",
    "DraftRoomsDetail_HeightMetres_4": "2.7",
    "DraftRoomsDetail_HeightFtIn_4": "9",
    "DraftRoomsDetail_Description1_4": "Laminate",
    "DraftRoomsDetail_Description2_4": "Closet",
    "DraftRoomsDetail_Description3_4": "Window",

    # Room 5
    "DraftRoomsDetail_RoomLevel_5": "Lower",
    "DraftRoomsDetail_RoomType_5": "Recreation",
    "DraftRoomsDetail_LengthMetres_5": "5.0",
    "DraftRoomsDetail_LengthFtIn_5": "16",
    "DraftRoomsDetail_WidthMetres_5": "4.0",
    "DraftRoomsDetail_WidthFtIn_5": "13",
    "DraftRoomsDetail_HeightMetres_5": "2.4",
    "DraftRoomsDetail_HeightFtIn_5": "8",
    "DraftRoomsDetail_Description1_5": "Laminate",
    "DraftRoomsDetail_Description2_5": "Open Concept",
    "DraftRoomsDetail_Description3_5": "Window",


    # ==================== DRAFT COMMENTS ====================
    "DraftComments_RemarksForClients": "Beautifully maintained property featuring spacious rooms, plenty of natural light, and a functional layout. Conveniently located close to schools, parks, shopping, and public transit.",

    "DraftComments_OfferRemarks": "Please attach Schedule B and include a deposit cheque with all offers. Allow 24 hours irrevocable.",

    "DraftComments_Inclusions": "Refrigerator, stove, dishwasher, washer, dryer, all existing light fixtures, and window coverings.",

    "DraftComments_Exclusions": "Personal belongings, decorative mirrors, and staging furniture.",

    "DraftComments_RentalItems": "Hot water tank and furnace.",

    "DraftComments_UnderContractMonthlyCosts": "Hot water tank rental: $35/month.",

    "DraftComments_RealtorOnlyRemarks": "Please provide 24 hours notice for all showings. Remove shoes before entering. Kindly leave a business card after the showing.",

    "DraftComments_SystemRemarks": "Listing information is believed to be accurate but should be independently verified by the buyer or buyer's agent.",

    # ==================== DRAFT OTHER ====================

    "DraftOther_ListingBrokerage": "RE/MAX HALLMARK PEGGY HILL GROUP REALTY",
    "DraftOther_ListingBrokeragePhone": "705-739-4455",
    "DraftOther_ListingBrokerageFax": "866-919-5276",

    # Salesperson 1
    "DraftOther_SalesPerson_1": "PEGGY HILL",
    "DraftOther_SalesPersonPhone_1": "705-739-4450",
    "DraftOther_SalesPersonEmail_1": "john.smith@example.com",

    # Salesperson 2
    "DraftOther_SalesPersonBrokerage_2": "RE/MAX HALLMARK PEGGY HILL GROUP REALTY",
    "DraftOther_SalesPerson_2": "ABBEY MCINTYRE",
    "DraftOther_SalesPersonPhone_2": "416-555-0102",
    "DraftOther_SalesPersonEmail_2": "abbey@peggyhill.com",

    # Salesperson 3
    "DraftOther_SalesPersonBrokerage_3": "RE/MAX HALLMARK PEGGY HILL GROUP REALTY",
    "DraftOther_SalesPerson_3": "ABBEY MCINTYRE",
    "DraftOther_SalesPersonPhone_3": "416-555-0103",
    "DraftOther_SalesPersonEmail_3": "abbey@peggyhill.com",

    # Salesperson 4
    "DraftOther_SalesPersonBrokerage_4": "RE/MAX HALLMARK PEGGY HILL GROUP REALTY",
    "DraftOther_SalesPerson_4": "ABBEY MCINTYRE",
    "DraftOther_SalesPersonPhone_4": "416-555-0104",
    "DraftOther_SalesPersonEmail_4": "abbey@peggyhill.com",

    "DraftOther_CommissionToCoOperatingBrokerage": "2.5",

    "DraftOther_SellerPropertyInfoInformation": "Yes",
    "DraftOther_EnergyCertificate": "No",
    "DraftOther_CertificationLevel": "Gold",
    "DraftOther_GreenPropertyInformationStatement": "No",

    "DraftOther_DistributeToInternet": "Yes",
    "DraftOther_DisplayAddressOnInternet": "Yes",
    "DraftOther_DistributeToDDFIDX": "Yes",
    "DraftOther_PermissionToContactListingBrokerToAdvertise": "Yes",
    "DraftOther_RealtorSignOnProperty": "Yes",

    "DraftOther_BrokerOpenHouseDateAndTime": "11/15/2026",
    "DraftOther_StartTime": "10:00 AM",
    "DraftOther_EndTime": "12:00 PM",

    "DraftOther_AppointmentsShowingRemarks": "Please provide 24 hours notice. Remove shoes before entering. Lock all doors after showing.",

    "DraftOther_Occupancy": "Owner",
    "DraftOther_ShowingRequirements": "Lockbox,Showing System",

    "DraftOther_ContactAfterExpired": "No",

    "DraftOther_UnbrandedVirtualTourURL1": "https://example.com/virtual-tour",
    "DraftOther_UnbrandedVirtualTourURL2": "https://example.com/virtual-tour-2",
    "DraftOther_BrandedVirtualTourURL1": "https://example.com/branded-tour",
    "DraftOther_BrandedVirtualTourURL2": "https://example.com/branded-tour-2",

    "DraftOther_SalesBrochureURL": "https://example.com/sales-brochure",
    "DraftOther_AdditionalPicturesURL": "https://example.com/additional-pictures",
    "DraftOther_AlternateFeatureSheetURL": "https://example.com/feature-sheet",
    "DraftOther_MapLocationURL": "https://maps.google.com/?q=Toronto",
    "DraftOther_SoundBiteURL": "https://example.com/sound-bite",

    # ==================== DRAFT PHOTOS ====================
    "DraftPhotos_PhotoPaths":"/Users/kurmasrujan/Downloads/_ (9).jpeg$/Users/kurmasrujan/Downloads/_ (8).jpeg$/Users/kurmasrujan/Downloads/aca0f6e0-fe88-449e-843d-e3293dbcaf31.JPG$/Users/kurmasrujan/Downloads/ChatGPT Image Jun 19, 2026, 06_32_27 PM.png$/Users/kurmasrujan/Downloads/DAH Architects - DAH Architects added a new photo — in Thu_.jpeg",
    "DraftPhotos_Description_1": "Front exterior view of the property",
    "DraftPhotos_Description_2": "Spacious living room with natural light",
    "DraftPhotos_Description_3": "Modern kitchen with stainless steel appliances",
    "DraftPhotos_Description_4": "Primary bedroom with large windows",
    "DraftPhotos_Description_5": "Beautiful backyard with landscaped garden",

    # ==================== DRAFT ATTACHMENTS ====================
    "DraftAttachments_AttachmentPaths":"/Users/kurmasrujan/Downloads/week1_backend_plan.pdf$/Users/kurmasrujan/Downloads/FAANG_Roadmap_2026 - by Sai bargav (1).pdf$/Users/kurmasrujan/Downloads/Week 1 Revision Document.pdf",
    "DraftAttachments_Description_1": "Feature Sheets",
    "DraftAttachments_Description_2": "Feature Sheets",
    "DraftAttachments_Description_3": "Environmentals",

    # ==================== PUBLIC OPEN HOUSE 1 ====================
    "DraftPublicOpenHouse_NumberOfPublicOpenHouses": "2",

    "DraftPublicOpenHouse_OpenHouseStatus_1": "Active",
    "DraftPublicOpenHouse_OpenHouseType_1": "Public",
    "DraftPublicOpenHouse_OpenHouseFormat_1": "In Person",
    "DraftPublicOpenHouse_OpenHouseDate_1": "11/07/2026",
    "DraftPublicOpenHouse_StartTime_1": "1:00 PM",
    "DraftPublicOpenHouse_EndTime_1": "4:00 PM",
    "DraftPublicOpenHouse_OpenHouseNotes_1": "Please visit the property during the scheduled open house hours.",

    # ==================== PUBLIC OPEN HOUSE 2 ====================
    "DraftPublicOpenHouse_OpenHouseStatus_2": "Active",
    "DraftPublicOpenHouse_OpenHouseType_2": "Public",
    "DraftPublicOpenHouse_OpenHouseFormat_2": "In Person",
    "DraftPublicOpenHouse_OpenHouseDate_2": "11/07/2026",
    "DraftPublicOpenHouse_StartTime_2": "12:00 PM",
    "DraftPublicOpenHouse_EndTime_2": "3:00 PM",
    "DraftPublicOpenHouse_OpenHouseNotes_2": "Visitors are welcome. Please remove shoes before entering.",

    "DraftDetails_Type": "Farm",
    "DraftDetails_Category": "Agricultural",
    "DraftDetails_Use": "Hobby",
    "DraftDetails_Freestanding" : "No",
    "DraftDetails_TotalArea" : "124",
    "DraftDetails_TotalAreaCode" : "Acres",
    "DraftDetails_PercentBuilding" : "40%",
    "DraftDetails_OfficeApartmentArea" : "123",
    "DraftDetails_OfficeApartmentAreaCode" : "Sq Ft",
    "DraftDetails_IndustrialArea" : "123",
    "DraftDetails_IndustrialAreaCode" : "Sq Ft Divisible",
    "DraftDetails_RetailArea" : "12",
    "DraftDetails_RetailAreaCode" : "Sq Ft Divisible",
    "DraftDetails_ApproximateAge" : "31-50",
    "DraftDetails_AreaInfluences" : "Skiing",
    "DraftDetails_PhysicallyHandicappedEquipped" : "Yes",
    "DraftDetails_Basement" : "Yes",
    "DraftDetails_UFFI" : "Yes",
    "DraftDetails_ClearHeightFeet" : "80",
    "DraftDetails_ClearHeightInches" : "7",
    "DraftDetails_Sprinklers" : "No",
    "DraftDetails_Utilities" : "Yes",
    "DraftDetails_BaySizeWidthFeet" : "12",
    "DraftDetails_BaySizeWidthInches" : "9",
    "DraftDetails_BaySizeLengthFeet" :  "7",
    "DraftDetails_BaySizeLengthInches" : "7",
    "DraftDetails_BaySizeAmps" : "78",
    "DraftDetails_BaySizeVolts" : "650",
    "DraftDetails_BaySizeWater" : "Well",
    "DraftDetails_BaySizeWaterSupplyType" : "Drilled Well",
    "DraftDetails_BaySizeAirConditioning" : "No",
    "DraftDetails_BaySizeHeatType" : "Fan Coil",
    "DraftDetails_BaySizeWashrooms" : "12",
    "DraftDetails_TruckLevelShippingDoors" : "12",
    "DraftDetails_TrucklevelDoorsHeightFeet" : "3",
    "DraftDetails_TrucklevelDoorsHeightInches" : "4",
    "DraftDetails_TrucklevelDoorsWidthFeet" : "5",
    "DraftDetails_TrucklevelDoorsWidthInches" : "6",
    "DraftDetails_TrucklevelDoubleManShippingDoors" : "11",
    "DraftDetails_DoubleManDoorsHeightFeet" : "3",
    "DraftDetails_DoubleManDoorsHeightInches" : "2",
    "DraftDetails_DoubleManDoorsWidthFeet" : "4",
    "DraftDetails_DoubleManDoorsWidthInches" : "6",
    "DraftDetails_DriveInLevelShippingDoors" : "12",
    "DraftDetails_DriveInDoorsHeightFeet" : "7",
    "DraftDetails_DriveInDoorsHeightInches" : "6",
    "DraftDetails_DriveInDoorsWidthFeet" : "2",
    "DraftDetails_DriveInDoorsWidthInches" : "6",
    "DraftDetails_GradeLevelShippingDoors" : "4",
    "DraftDetails_GradeLevelDoorsHeightFeet" : "5",
    "DraftDetails_GradeLevelDoorsHeightInches" : "7",
    "DraftDetails_GradeLevelDoorsWidthFeet" : "6",
    "DraftDetails_GradeLevelDoorsWidthInches" : "6",
    "DraftDetails_Elevator" : "Public",
    "DraftDetails_GarageType" : "Pay, Plaza",
    "DraftDetails_ParkingSpaces" : "4",
    "DraftDetails_NumberofTrailerParkingSpots" : "2", 
    "DraftDetails_OutsideStorage" : "Yes",
    "DraftDetails_Rail" : "No",
    "DraftDetails_Crane" : "Yes",
    "DraftDetails_Survey" : "Yes",
    "DraftDetails_SoilTest" : "Environmental Audit",
    "DraftDetails_Sewers" : "Sanitary Available",
    "DraftDetails_FarmFeatures" : "None , Other",
    "DraftDetails_YearBuilt" : "1995",
    "DraftDetails_YearBuiltSource" : "MPAC"
    
}

def run_selenium_workflow(recordId,trebbUrl,trebbUsername,trebbPassword):
    try:
        driver=None
        exceptionDict={"Status":"","Exception type":"","Exception Message":""}

        listings_dict = get_listings_dict(recordId)
        logger.info(f"Loaded listings dict for record {recordId} ({len(listings_dict)} fields)")

        driver = create_chrome_driver()
        logger.info("Selenium Chrome Driver is Created")
        existingListingFlag=False
        trebb_main(recordId,existingListingFlag,driver,listings_dict,trebbUrl,trebbUsername,trebbPassword,exceptionDict,logger)
        
    except Exception as e:
        logger.error(e)
        exceptionDict["Status"]="Failed"
        if exceptionDict["Exception type"]=="":
            exceptionDict["Exception type"]="Application"
        if exceptionDict["Exception Message"]=="":
            exceptionDict["Exception Message"]=get_traceback(e)
        
    finally:
        # Guarantees browser termination even on crash or unhandled error
        driver.quit()


# trebbUrl, trebbUsername, trebbPassword are passed in via environment / API — do not hardcode here
#run_selenium_workflow("",trebbUrl,trebbUsername,trebbPassword)

