CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS barangays (
    "id_0" int,
    "iso" varchar,
    "name_0" varchar,
    "id_1" int,
    "name_1" varchar,
    "id_2" int,
    "name_2" varchar,
    "id_3" int,
    "name_3" varchar,
    "nl_name_3" varchar,
    "varname_3" varchar,
    "type_3" varchar,
    "engtype_3" varchar,
    "province" varchar,
    "region" varchar,
    "geom" geography(multipolygon, 4326),
   	PRIMARY KEY(id_3)
);

CREATE TABLE IF NOT EXISTS city_municipalities (
    "id_0" int,
    "iso" varchar,
    "name_0" varchar,
    "id_1" int,
    "name_1" varchar,
    "id_2" int,
    "name_2" varchar,
    "nl_name_2" varchar,
    "varname_2" varchar,
    "type_2" varchar,
    "engtype_2" varchar,
    "province" varchar,
    "region" varchar,
    "geom" geography(multipolygon, 4326),
    PRIMARY KEY(id_2)
);

 CREATE TABLE IF NOT EXISTS countries (
	"id_0" int,
	"iso" varchar,
	"name_engli" varchar,
	"name_iso" varchar,
	"name_fao" varchar,
	"name_local" varchar,
	"name_obsol" varchar,
	"name_varia" varchar,
	"name_nonla" varchar,
	"name_frenc" varchar,
	"name_spani" varchar,
	"name_russi" varchar,
	"name_arabi" varchar,
	"name_chine" varchar,
	"waspartof" varchar,
	"contains" varchar,
	"sovereign" varchar,
	"iso2" varchar,
	"www" varchar,
	"fips" varchar,
	"ison" decimal,
	"validfr" varchar,
	"validto" varchar,
	"eumember" decimal,
	"geom" geography(multipolygon, 4326), 
	PRIMARY KEY(id_0)
);

CREATE TABLE IF NOT EXISTS provinces (
    "id_0" int,
    "iso" varchar,
    "name_0" varchar,
    "id_1" int,
    "name_1" varchar,
    "nl_name_1" varchar,
    "varname_1" varchar,
    "type_1" varchar,
    "engtype_1" varchar,
    "province" varchar,
    "region" varchar,
    "geom" geography(multipolygon, 4326),
    PRIMARY KEY(id_1)
);


CREATE TABLE IF NOT EXISTS tweets (
	"id" bigint PRIMARY KEY not null,
	"created_at" varchar not null,
	"user" varchar not null,
	"text" text not null,
	"language" varchar, 
	"lat" float,
	"lng" float,
	"user_location" varchar,
	"user_utc_offset" varchar,
	"user_timezone" varchar ,
    "radius" int
);


