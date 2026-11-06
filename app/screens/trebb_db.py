#!/usr/bin/env python3
"""Fetch listing data from the Grova listings DB and return a Listings_Dict for TREB automation.

Requires the SSM tunnel to be running before connecting:
  aws ssm start-session --target i-0d11f235a1ef43c20 \
    --document-name AWS-StartPortForwardingSessionToRemoteHost \
    --parameters '{"host":["listings-ai-dev-db.chquuumugagx.ca-central-1.rds.amazonaws.com"],
                   "portNumber":["5432"],"localPortNumber":["15432"]}' \
    --profile grova --region ca-central-1
"""

import os

import psycopg2
import psycopg2.extras

DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("DB_PORT", "15432"))
DB_NAME = os.environ.get("DB_NAME", "listings")
DB_USER = os.environ.get("DB_USER", "listings_admin")
DB_PASS = os.environ.get("DB_PASS", "")
DB_SSL  = os.environ.get("DB_SSL", "require")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS, sslmode=DB_SSL,
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


def _fetch_record(listing_id: str) -> dict:
    """Return the flattened latest-version field_value dict for one listing."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT field, value, version, status FROM field_value "
            "WHERE listing_id = %s ORDER BY field, version",
            (listing_id,),
        )
        rows = cur.fetchall()
    finally:
        conn.close()

    record: dict = {}
    for row in rows:
        key = row["field"]
        existing = record.get(key)
        if existing is None:
            record[key] = row
        elif row["version"] > existing["version"]:
            record[key] = row
        elif row["version"] == existing["version"] and row["status"] == "confirmed_two":
            record[key] = row

    return {k: (v["value"] or "") for k, v in record.items()}


# Maps one DB field name → one or more Listings_Dict keys.
# Field names verified against the real field_value table (334 distinct fields).
_FIELD_MAP: dict[str, list[str]] = {
    # ── AddListing ──────────────────────────────────────────────────────
    "listing.address":                  ["AddListing_Address"],
    "proptx.property_type":             ["AddListing_PropertyType", "DraftExterior_PropertyType"],
    "proptx.residential_or_vacant_land": ["AddListing_PropertyClass"],
    "proptx.street":                    ["AddListing_StreetNumber", "DraftLocation_StreetNumber"],
    "proptx.street_name":               ["AddListing_StreetName",   "DraftLocation_StreetName"],
    "proptx.abbrev":                    ["AddListing_Abbreviation", "DraftLocation_Abbreviation"],
    "proptx.street_direction":          ["AddListing_StreetDirection", "DraftLocation_StreetDirection"],
    "proptx.street_direction_prefix":   ["DraftLocation_StreetDirectionPrefix"],
    "proptx.apt_unit":                  ["AddListing_UnitNumber",   "DraftLocation_UnitNumber"],
    "proptx.municipality":              ["AddListing_Municipality", "DraftLocation_Muncipality"],
    "proptx.community":                 ["AddListing_Community",    "DraftLocation_Community"],
    "proptx.postal_code":               ["AddListing_PostalCode",   "DraftLocation_PostalCode"],
    "proptx.sale":                      ["AddListing_TransactionType", "DraftLocation_TransactionType"],
    "proptx.listing":                   ["AddListing_Member"],

    # ── DraftLocation ────────────────────────────────────────────────────
    "proptx.assessment_roll":           ["DraftLocation_ARN"],
    "proptx.pin":                       ["DraftLocation_PIN"],
    "proptx.additional_pin":            ["DraftLocation_AdditionalPIN"],
    "proptx.fronting_on":               ["DraftLocation_FrontingOn"],
    "proptx.legal_description":         ["DraftLocation_LegalDescription"],
    "proptx.lot_front":                 ["DraftLocation_LotFront"],
    "proptx.lot_depth":                 ["DraftLocation_LotDepth"],
    "proptx.lot_size_code":             ["DraftLocation_LotSizeCode"],
    "proptx.lot_irregularities":        ["DraftLocation_LotIrregularities"],
    "proptx.lot_shape":                 ["DraftLocation_LotShape"],
    "proptx.lot_size_source":           ["DraftLocation_LotSizeSource"],
    "proptx.lot_size_area":             ["DraftLocation_LotSizeArea"],
    "proptx.lot_size_area_code":        ["DraftLocation_LotSizeAreaCode"],
    "proptx.lot_building_unit_code":    ["DraftLocation_LotSizeCode"],
    "proptx.winterized":                ["DraftLocation_Winterized"],
    "proptx.acreage":                   ["DraftLocation_Acreage"],
    "proptx.waterfront":                ["DraftLocation_WaterFront"],
    "proptx.directions":                ["DraftLocation_Directions"],
    "proptx.main_cross_streets":        ["DraftLocation_MainCrossStreets"],
    "proptx.zoning":                    ["DraftLocation_Zoning"],
    "geo.lat":                          ["DraftLocation_Latitude"] if False else [],  # not in Listings_Dict

    # ── DraftAmountsDates ────────────────────────────────────────────────
    "agreement.list_price":             ["DraftAmountsDates_ListPrice"],
    "proptx.list_price":                ["DraftAmountsDates_ListPrice"],
    "proptx.possession_type":           ["DraftAmountsDates_PossessionType"],
    "proptx.possession_remarks":        ["DraftAmountsDates_PossessionRemarks"],
    "proptx.holdover_days":             ["DraftAmountsDates_HoldoverDays"],
    "agreement.holdover_days":          ["DraftAmountsDates_HoldoverDays"],
    "proptx.landlord_name":             ["DraftAmountsDates_LandlordName"],
    "proptx.landlord":                  ["DraftAmountsDates_LandlordName"],
    "proptx.lease_term":                ["DraftAmountsDates_LeaseTerm"],
    "proptx.payment_frequency":         ["DraftAmountsDates_PaymentFrequency"],
    "proptx.payment_method":            ["DraftAmountsDates_PaymentMethod"],
    "proptx.hst":                       ["DraftAmountsDates_ListPriceToReducedReflectHSTRebate"],
    "proptx.hst_applicable_to_sale_price": ["DraftAmountsDates_HSTApplicableToSamePrice"],
    "proptx.development_charges_paid":  ["DraftAmountsDates_DevelopmentChargesPaid"],
    "proptx.taxes":                     ["DraftAmountsDates_Taxes"],
    "proptx.tax_year":                  ["DraftAmountsDates_TaxYear"],
    "proptx.tax_type":                  ["DraftAmountsDates_TaxType"],
    "proptx.assessment":                ["DraftAmountsDates_Assessment"],
    "proptx.assessment_year":           ["DraftAmountsDates_AssessmentYear"],
    "agreement.commencement":           ["DraftAmountsDates_ContractCommencement"],
    "proptx.contract_commencement":     ["DraftAmountsDates_ContractCommencement"],
    "proptx.expiry_date":               ["DraftAmountsDates_ExpiryDate"],
    "agreement.expiry":                 ["DraftAmountsDates_ExpiryDate"],
    "proptx.mortgage_comments":         ["DraftAmountsDates_MortgageComments"],
    "proptx.phased_in_tax_assessed_value": ["DraftAmountsDates_PhasedInTaxAssessedValue"],
    "proptx.road_access_fee":           ["DraftAmountsDates_RoadAccessFee"],
    "proptx.leased_land_fee":           ["DraftAmountsDates_LeasedLandFee"],
    "proptx.local_improvements":        ["DraftAmountsDates_LocalImprovements"],
    "proptx.local_improvements_comments": ["DraftAmountsDates_LocalImprovementsComments"],
    "proptx.condo_maintenance_fees_monthly": ["DraftAmountsDates_Maintenance"],
    "proptx.minimum_rental_term_months": ["DraftAmountsDates_MinimumRentalTermMonths"],
    "proptx.maximum_rental_term_months": ["DraftAmountsDates_MaximumRentalMonthsTerm"],
    "proptx.list_price_code":           ["DraftAmountsDates_ListPriceCode"],
    "proptx.lease_price":               ["DraftAmountsDates_ListPrice"],
    "proptx.rental_application_required": ["DraftAmountsDates_RentalApplicationRequired"],
    "proptx.deposit_required":          ["DraftAmountsDates_DepositRequired"],
    "proptx.listing_agreement":         ["DraftAmountsDates_LeaseAgreement"],
    "proptx.references_required":       ["DraftAmountsDates_ReferencesRequired"],
    "proptx.credit_check":              ["DraftAmountsDates_CreditCheck"],
    "proptx.employment_letter":         ["DraftAmountsDates_EmploymentLetter"],
    "proptx.non_smoking_policy":        ["DraftAmountsDates_NonSmokingPolicy"],
    "proptx.buy_option":                ["DraftAmountsDates_BuyOption"],
    "proptx.included_in_lease_cost":    ["DraftAmountsDates_IncludedInLeaseCost"],

    # ── DraftExterior ────────────────────────────────────────────────────
    "proptx.link":                      ["DraftExterior_LINK"],
    "proptx.parcel_of_tied_land":       ["DraftExterior_ParcelofTiedLand"],
    "proptx.potl_monthly_fees":         ["DraftExterior_POTLMonthlyFee"],
    "proptx.vacant_land_condo":         ["DraftExterior_VacantLandCondo"],
    "proptx.assignment":                ["DraftExterior_Assignment"],
    "proptx.fractional_ownership":      ["DraftExterior_FractionalOwnership"],
    "proptx.portion_of_property_for_lease": ["DraftExterior_PortionofPropertyforLease"],
    "proptx.portion_of_property_comments": ["DraftExterior_PortionofPropertyComments"],
    "proptx.style":                     ["DraftExterior_Style"],
    "proptx.view":                      ["DraftExterior_View"],
    "proptx.views":                     ["DraftExterior_View"],
    "proptx.exterior_features":         ["DraftExterior_ExteriorFeatures"],
    "proptx.foundation_detail":         ["DraftExterior_FoundationDetail"],
    "proptx.roof":                      ["DraftExterior_Roof"],
    "proptx.topography":                ["DraftExterior_Topography"],
    "proptx.garage":                    ["DraftExterior_Garage"],
    "proptx.garage_type":               ["DraftExterior_GarageType"],
    "proptx.garage_parking_spaces":     ["DraftExterior_GarageParkingSpaces"],
    "proptx.parking_drive":             ["DraftExterior_ParkingDrive"],
    "proptx.drive_parking_spaces":      ["DraftExterior_DriveParkingSpaces"],
    "proptx.total_parking_spaces":      ["DraftExterior_TotalParkingSpaces"],
    "proptx.parking_cost_month":        ["DraftExterior_ParkingCostMonth"],
    "proptx.pool":                      ["DraftExterior_Pool"],
    "proptx.sewers":                    ["DraftExterior_Sewers"],
    "proptx.retirement_community":      ["DraftExterior_RetirementCommunity"],
    "proptx.physically_handicapped_equipped": ["DraftExterior_PhysicallyHandicappedEquipped"],
    "proptx.special_designation":       ["DraftExterior_SpecialDesignation"],
    "proptx.approximate_age":           ["DraftExterior_ApproximateAge"],
    "proptx.year_built":                ["DraftExterior_YearBuilt"],
    "proptx.year_built_source":         ["DraftExterior_YearBuiltSource"],
    "proptx.approximate_square_footage": ["DraftExterior_ApproximateSquareFootage"],
    "proptx.above_grade_finished_sqft": ["DraftExterior_AboveGradeFinishedSQFT"],
    "proptx.above_grade_finished_sqft_source": ["DraftExterior_AboveGradeFinishedSQFTSource"],
    "proptx.below_grade_finished_sqft": ["DraftExterior_BelowGradeFinishedSQFT"],
    "proptx.below_grade_finished_sqft_source": ["DraftExterior_BelowGradeFinishedSQFTSource"],
    "proptx.other_sqft":                ["DraftExterior_OtherSQFT"],
    "proptx.total_unfinished_sqft":     ["DraftExterior_TotalUnfinished"],
    "proptx.property_features_area_influences": ["DraftExterior_PropertyFeaturesAreaInfluences"],
    "proptx.area_influences":           ["DraftExterior_PropertyFeaturesAreaInfluences"],
    "proptx.security_features":         ["DraftExterior_SecurityFeatures"],
    "proptx.other_structures":          ["DraftExterior_OtherStructures"],
    "proptx.water_supply_type":         ["DraftExterior_WaterSupplyType"],
    "proptx.farm_agriculture":          ["DraftExterior_Farm/Agriculture"],
    "proptx.farm_features":             ["DraftExterior_FarmFeatures"],
    "proptx.soil_type":                 ["DraftExterior_SoilType"],
    "proptx.survey_type":               ["DraftExterior_SurveyType"],
    "proptx.survey_year":               ["DraftExterior_SurveyYear"],
    "proptx.water_meter":               ["DraftExterior_WaterMeter"],
    "proptx.well_capacity":             ["DraftExterior_WellCapacityGalMinute"],
    "proptx.well_depth":                ["DraftExterior_WellDepth"],
    "proptx.cable":                     ["DraftExterior_Cable"],
    "proptx.hydro":                     ["DraftExterior_Hydro"],
    "proptx.gas":                       ["DraftExterior_Gas(Natural)"],
    "proptx.municipal_water":           ["DraftExterior_MunicipalWater"],
    "proptx.telephone":                 ["DraftExterior_Telephone"],
    "proptx.water":                     ["DraftExterior_Water"],

    # ── DraftWaterfrontRural ─────────────────────────────────────────────
    "proptx.waterfront_type":           ["DraftWaterfrontRural_WaterfrontType"],
    "proptx.body_of_water_name":        ["DraftWaterfrontRural_BodyOfWaterName"],
    "proptx.water_body_type":           ["DraftWaterfrontRural_WaterBodyType"],
    "proptx.island":                    ["DraftWaterfrontRural_Island"],
    "proptx.water_view":                ["DraftWaterfrontRural_WaterView"],
    "proptx.channel_name":              ["DraftWaterfrontRural_ChannelName"],
    "proptx.water_frontage":            ["DraftWaterfrontRural_WaterFrontage"],
    "proptx.water_frontage_units":      ["DraftWaterfrontRural_WaterFrontageUnits"],
    "proptx.seasonal_dwelling":         ["DraftWaterfrontRural_SeasonalDwelling"],
    "proptx.access_to_property":        ["DraftWaterfrontRural_AccessToProperty"],
    "proptx.shoreline":                 ["DraftWaterfrontRural_Shoreline"],
    "proptx.waterfront_features":       ["DraftWaterfrontRural_WaterfrontFeatures"],
    "proptx.shoreline_exposure":        ["DraftWaterfrontRural_ShorelineExposure"],
    "proptx.shoreline_allowance":       ["DraftWaterfrontRural_ShorelineAllowance"],
    "proptx.alternative_power":         ["DraftWaterfrontRural_AlternativePower"],
    "proptx.sewage":                    ["DraftWaterfrontRural_Sewage"],
    "proptx.water_delivery_features":   ["DraftWaterfrontRural_WaterDeliveryFeatures"],
    "proptx.easements_restrictions":    ["DraftWaterfrontRural_EasementsRestrictions"],
    "proptx.rural_services":            ["DraftWaterfrontRural_RuralServices"],
    "proptx.waterfront_accessory_buildings": ["DraftWaterfrontRural_WaterfrontAccessoryBuildings"],
    "proptx.docking_type":              ["DraftWaterfrontRural_DockingType"],

    # ── DraftInterior ────────────────────────────────────────────────────
    "proptx.number_of_rooms":           ["DraftInterior_NumberofRooms"],
    "proptx.bonus_room":                ["DraftInterior_RoomsPlus"],
    "proptx.number_of_bedrooms":        ["DraftInterior_NumberofBedrooms"],
    "proptx.number_of_kitchens":        ["DraftInterior_NumberofKitchens"],
    "proptx.kitchens":                  ["DraftInterior_NumberofKitchens"],
    "proptx.baths":                     ["DraftInterior_Washrooms1"],
    "proptx.washrooms":                 ["DraftInterior_Washrooms1"],
    "proptx.interior_features":         ["DraftInterior_InteriorFeatures"],
    "proptx.family_room":               ["DraftInterior_FamilyRoomBonusRoom"],
    "proptx.basement":                  ["DraftInterior_Basement"],
    "proptx.fireplace_stove":           ["DraftInterior_FireplaceStove"],
    "proptx.fireplace_features":        ["DraftInterior_FireplaceFeatures"],
    "proptx.of_fireplaces":             ["DraftInterior_NumberofFireplaces"],
    "proptx.heat_source":               ["DraftInterior_HeatSource"],
    "proptx.heat_type":                 ["DraftInterior_HeatType"],
    "proptx.air_conditioning":          ["DraftInterior_AirConditioning"],
    "proptx.uffi":                      ["DraftInterior_UFFI"],
    "proptx.laundry_level":             ["DraftInterior_LaundryLevel"],
    "proptx.accessibility_features":    ["DraftInterior_AccessibilityFeatures"],
    "proptx.elevator_lift":             ["DraftInterior_ElevatorLift"],
    "proptx.rental_items_under_contract": ["DraftInterior_LeaseToOwnItems"],
    "proptx.furnished":                 ["DraftInterior_Furnished"],

    # ── DraftComments ────────────────────────────────────────────────────
    "proptx.remarks_for_clients":       ["DraftComments_RemarksForClients"],
    "proptx.offer_remarks":             ["DraftComments_OfferRemarks"],
    "proptx.offer_remarks_seller_direction": ["DraftComments_OfferRemarks"],
    "proptx.inclusions":                ["DraftComments_Inclusions"],
    "proptx.exclusions":                ["DraftComments_Exclusions"],
    "proptx.rental_items_under_contract": ["DraftComments_RentalItems"],
    "proptx.under_contract_monthly_costs": ["DraftComments_UnderContractMonthlyCosts"],
    "proptx.realtor_only_remarks":      ["DraftComments_RealtorOnlyRemarks"],

    # ── DraftOther ───────────────────────────────────────────────────────
    "proptx.listing_brokerage":         ["DraftOther_ListingBrokerage"],
    "proptx.listing_brokerage_phone":   ["DraftOther_ListingBrokeragePhone"],
    "proptx.listing_brokerage_fax":     ["DraftOther_ListingBrokerageFax"],
    "proptx.salesperson_1":             ["DraftOther_SalesPerson_1"],
    "proptx.salesperson_1_phone":       ["DraftOther_SalesPersonPhone_1"],
    "proptx.salesperson_2_brokerage":   ["DraftOther_SalesPersonBrokerage_2"],
    "proptx.salesperson_2":             ["DraftOther_SalesPerson_2"],
    "proptx.salesperson_2_phone":       ["DraftOther_SalesPersonPhone_2"],
    "proptx.salesperson_3_brokerage":   ["DraftOther_SalesPersonBrokerage_3"],
    "proptx.salesperson_3":             ["DraftOther_SalesPerson_3"],
    "proptx.salesperson_3_phone":       ["DraftOther_SalesPersonPhone_3"],
    "proptx.salesperson_4_brokerage":   ["DraftOther_SalesPersonBrokerage_4"],
    "proptx.salesperson_4":             ["DraftOther_SalesPerson_4"],
    "proptx.salesperson_4_phone":       ["DraftOther_SalesPersonPhone_4"],
    "agreement.commission_coop":        ["DraftOther_CommissionToCoOperatingBrokerage"],
    "proptx.commission_to_co_operating_brokerage": ["DraftOther_CommissionToCoOperatingBrokerage"],
    "proptx.seller_property_info_statement": ["DraftOther_SellerPropertyInfoInformation"],
    "proptx.energy_certificate":        ["DraftOther_EnergyCertificate"],
    "proptx.certificate_level":         ["DraftOther_CertificationLevel"],
    "proptx.green_property_info_statement": ["DraftOther_GreenPropertyInformationStatement"],
    "proptx.distribute_to_internet":    ["DraftOther_DistributeToInternet"],
    "proptx.display_address_on_internet": ["DraftOther_DisplayAddressOnInternet"],
    "proptx.distribute_to_ddf_idx":     ["DraftOther_DistributeToDDFIDX"],
    "proptx.sign_on_property":          ["DraftOther_RealtorSignOnProperty"],
    "proptx.sign_on":                   ["DraftOther_RealtorSignOnProperty"],
    "proptx.broker_open_house_date_and_time": ["DraftOther_BrokerOpenHouseDateAndTime"],
    "proptx.broker_open_house_notes":   ["DraftOther_AppointmentsShowingRemarks"],
    "proptx.appointments_showing_remarks": ["DraftOther_AppointmentsShowingRemarks"],
    "proptx.occupancy":                 ["DraftOther_Occupancy"],
    "proptx.showing_requirements":      ["DraftOther_ShowingRequirements"],
    "proptx.contact_after_expired":     ["DraftOther_ContactAfterExpired"],
    "proptx.unbranded_virtual_tour_url_1": ["DraftOther_UnbrandedVirtualTourURL1"],
    "proptx.unbranded_virtual_tour_url_2": ["DraftOther_UnbrandedVirtualTourURL2"],
    "proptx.branded_virtual_tour_url_1": ["DraftOther_BrandedVirtualTourURL1"],
    "proptx.branded_virtual_tour_url_2": ["DraftOther_BrandedVirtualTourURL2"],
    "proptx.sales_brochure_url":        ["DraftOther_SalesBrochureURL"],
    "proptx.additional_pictures_url":   ["DraftOther_AdditionalPicturesURL"],
    "proptx.alternate_feature_sheet_url": ["DraftOther_AlternateFeatureSheetURL"],
    "proptx.map_location_url":          ["DraftOther_MapLocationURL"],
    "proptx.sound_bite_url":            ["DraftOther_SoundBiteURL"],

    # ── DraftDetails (Commercial) ────────────────────────────────────────
    "proptx.category":                  ["DraftDetails_Category"],
    "proptx.freehold":                  ["DraftDetails_Freestanding"],
    "proptx.industrial_area_code":      ["DraftDetails_IndustrialAreaCode"],
    "proptx.sprinklers":                ["DraftDetails_Sprinklers"],
    "proptx.utilities":                 ["DraftDetails_Utilities"],
    "proptx.amps":                      ["DraftDetails_BaySizeAmps"],
    "proptx.volts":                     ["DraftDetails_BaySizeVolts"],
    "proptx.bay_size":                  ["DraftDetails_BaySizeWidthFeet"],
    "proptx.truck_level":               ["DraftDetails_TruckLevelShippingDoors"],
    "proptx.drive_in_level_shipping_doors": ["DraftDetails_DriveInLevelShippingDoors"],
    "proptx.drive_in_level_shipping_doors_dimensions": ["DraftDetails_DriveInDoorsHeightFeet"],
    "proptx.shipping_doors":            ["DraftDetails_GradeLevelShippingDoors"],
    "proptx.elevator":                  ["DraftDetails_Elevator"],
    "proptx.parking_spaces":            ["DraftDetails_ParkingSpaces"],
    "proptx.number_of_trailer_parking_spots": ["DraftDetails_NumberofTrailerParkingSpots"],
    "proptx.outside_storage":          ["DraftDetails_OutsideStorage"],
    "proptx.rail":                      ["DraftDetails_Rail"],
    "proptx.crane":                     ["DraftDetails_Crane"],
    "proptx.survey":                    ["DraftDetails_Survey"],
    "proptx.soil_test":                 ["DraftDetails_SoilTest"],

    # ── DraftFinancialInformation (Commercial) ───────────────────────────
    "proptx.chattels":                  ["DraftFinancial_Chattels"],
    "proptx.days_open":                 ["DraftFinancial_DaysOpen"],
    "proptx.hours_open":                ["DraftFinancial_HoursOpen"],
    "proptx.seats":                     ["DraftFinancial_Seats"],
    "proptx.lbo":                       ["DraftFinancial_LLBO"],
    "proptx.l_l_b_o":                   ["DraftFinancial_LLBO"],
    "proptx.gross_income_sales":        ["DraftFinancial_GrossRevenue"],
    "proptx.vacancy_allowance":         ["DraftFinancial_VacancyAllowance"],
    "proptx.operating_expense":         ["DraftFinancial_OperatingExpense"],
    "proptx.net_income_before_debt":    ["DraftFinancial_NetIncome"],
    "proptx.estimated_inventory_value_at_cost": ["DraftFinancial_Inventory"],
    "proptx.taxes_expense":             ["DraftFinancial_TaxesExpense"],
    "proptx.insurance_expense":         ["DraftFinancial_InsuranceExpense"],
    "proptx.management_expense":        ["DraftFinancial_ManagementExpense"],
    "proptx.maintenance_expense":       ["DraftFinancial_MaintenanceExpense"],
    "proptx.heat_expense":              ["DraftFinancial_HeatExpense"],
    "proptx.hydro_expense":             ["DraftFinancial_HydroExpense"],
    "proptx.water_expense":             ["DraftFinancial_WaterExpense"],
    "proptx.other_expense":             ["DraftFinancial_OtherExpense"],
    "proptx.common_area_upcharge":      ["DraftFinancial_CAMUpcharge"],
    "proptx.percentage_rent":           ["DraftFinancial_PercentRent"],
    "proptx.tmi":                       ["DraftFinancial_TMI"],
}

# Add per-room mappings for up to 20 rooms
for _i in range(1, 21):
    _FIELD_MAP.update({
        f"proptx.room_level_{_i}":          [f"DraftRoomsDetail_RoomLevel_{_i}"],
        f"proptx.room_type_{_i}":           [f"DraftRoomsDetail_RoomType_{_i}"],
        f"proptx.room_length_metres_{_i}":  [f"DraftRoomsDetail_LengthMetres_{_i}"],
        f"proptx.room_length_ftin_{_i}":    [f"DraftRoomsDetail_LengthFtIn_{_i}"],
        f"proptx.room_width_metres_{_i}":   [f"DraftRoomsDetail_WidthMetres_{_i}"],
        f"proptx.room_width_ftin_{_i}":     [f"DraftRoomsDetail_WidthFtIn_{_i}"],
        f"proptx.room_height_metres_{_i}":  [f"DraftRoomsDetail_HeightMetres_{_i}"],
        f"proptx.room_height_ftin_{_i}":    [f"DraftRoomsDetail_HeightFtIn_{_i}"],
        f"proptx.room_description1_{_i}":   [f"DraftRoomsDetail_Description1_{_i}"],
        f"proptx.room_description2_{_i}":   [f"DraftRoomsDetail_Description2_{_i}"],
        f"proptx.room_description3_{_i}":   [f"DraftRoomsDetail_Description3_{_i}"],
    })

# Add per-open-house mappings for up to 10 open houses
for _i in range(1, 11):
    _FIELD_MAP.update({
        f"proptx.open_house_status_{_i}":     [f"DraftPublicOpenHouse_OpenHouseStatus_{_i}"],
        f"proptx.open_house_type_{_i}":       [f"DraftPublicOpenHouse_OpenHouseType_{_i}"],
        f"proptx.open_house_format_{_i}":     [f"DraftPublicOpenHouse_OpenHouseFormat_{_i}"],
        f"proptx.open_house_date_{_i}":       [f"DraftPublicOpenHouse_OpenHouseDate_{_i}"],
        f"proptx.open_house_start_time_{_i}": [f"DraftPublicOpenHouse_StartTime_{_i}"],
        f"proptx.open_house_end_time_{_i}":   [f"DraftPublicOpenHouse_EndTime_{_i}"],
        f"proptx.open_house_notes_{_i}":      [f"DraftPublicOpenHouse_OpenHouseNotes_{_i}"],
    })

# Add per-photo and per-attachment description mappings for up to 50 items
for _i in range(1, 51):
    _FIELD_MAP[f"proptx.photo_description_{_i}"] = [f"DraftPhotos_Description_{_i}"]
    _FIELD_MAP[f"proptx.attachment_description_{_i}"] = [f"DraftAttachments_Description_{_i}"]


def get_listings_dict(listing_id: str) -> dict:
    """Fetch listing data from the DB and return a populated Listings_Dict.

    All keys in Listings_Dict are present in the returned dict; unmapped or
    missing DB fields default to an empty string so the Selenium screens don't
    KeyError on optional fields.
    """
    record = _fetch_record(listing_id)

    # Start with all keys defaulting to empty string
    result: dict[str, str] = {"AddListing_SearchBy": "Address"}

    for db_field, value in record.items():
        targets = _FIELD_MAP.get(db_field)
        if targets:
            for target in targets:
                result[target] = value

    return result
