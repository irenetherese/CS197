CREATE OR REPLACE FUNCTION isinPH(tweet_lon varchar, tweet_lat varchar)
RETURNS boolean AS $$

BEGIN 
IF EXISTS (
    SELECT name_2
    FROM city_municipalities 
    WHERE ST_INTERSECTS(ST_PointFromText('POINT(' || tweet_lon || ' ' || tweet_lat || ')', 4326), city_municipalities.geom)
) THEN RETURN 1;
END IF;

RETURN 0;

END;

$$ LANGUAGE plpgsql;