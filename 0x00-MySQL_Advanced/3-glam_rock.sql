-- SQL script that ranks by longevity
-- SQL command
SELECT band_name, COALESCE(split, 2022)-formed AS lifespan
  FROM metal_bands
    WHERE style LIKE '%Glam rock%'
    ORDER BY lifespan DESC;
