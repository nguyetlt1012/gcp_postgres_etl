CREATE INDEX idx_insurance_claims_vehbrand_area ON insurance_claims(VehBrand, Area);
CREATE INDEX idx_insurance_claims_area_density ON insurance_claims(Area, Density);


REVOKE ALL ON TABLE insurance_claims FROM PUBLIC;
GRANT SELECT ON TABLE insurance_claims TO user_name;
GRANT INSERT, UPDATE ON TABLE exposure_summary, density_summary TO user_name;
