-- Task 2: Sum of Exposure by VehBrand and Area
INSERT INTO exposure_summary (VehBrand, Area, total_exposure)
SELECT 
    VehBrand, 
    Area, 
    SUM(Exposure) AS total_exposure
FROM 
    insurance_claims
GROUP BY 
    VehBrand, Area;

-- Task 3: Min and Max Density by Area
INSERT INTO density_summary (Area, min_density, max_density)
SELECT 
    Area, 
    MIN(Density) AS min_density, 
    MAX(Density) AS max_density
FROM 
    insurance_claims
GROUP BY 
    Area;
