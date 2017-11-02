--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: jsonb_merge(jsonb, jsonb); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION jsonb_merge(jsonb1 jsonb, jsonb2 jsonb) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
    DECLARE
      result JSONB;
      v RECORD;
    BEGIN
       result = (
    SELECT json_object_agg(KEY,value)
    FROM
      (SELECT jsonb_object_keys(jsonb1) AS KEY,
              1::int AS jsb,
              jsonb1 -> jsonb_object_keys(jsonb1) AS value
       UNION SELECT jsonb_object_keys(jsonb2) AS KEY,
                    2::int AS jsb,
                    jsonb2 -> jsonb_object_keys(jsonb2) AS value ) AS t1
           );
       RETURN result;
    END;
    $$;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: advertisements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE advertisements (
    id integer NOT NULL,
    crawled_at timestamp without time zone NOT NULL,
    raw_data text NOT NULL,
    crawler character varying(100) NOT NULL,
    url character varying(255) NOT NULL,
    reference_no character varying(100),
    object_id character varying(100),
    living_area double precision,
    floor integer,
    price_brutto integer,
    additional_costs integer,
    street character varying(100),
    price_netto integer,
    description text,
    object_types_id integer NOT NULL,
    num_rooms double precision,
    num_floors integer,
    build_year integer,
    last_renovation_year integer,
    cubature double precision,
    room_height double precision,
    effective_area double precision,
    characteristics json,
    floors_house integer,
    additional_data json,
    longitude double precision,
    latitude double precision,
    owner text,
    plot_area double precision,
    available date,
    municipalities_id integer,
    last_seen date,
    municipality_unparsed character varying(200),
    quality_label character varying(255),
    tags json,
    last_reprocessed date,
    lv03_easting double precision,
    lv03_northing double precision,
    noise_level double precision
);


--
-- Name: municipalities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE municipalities (
    id integer NOT NULL,
    zip integer NOT NULL,
    bfsnr integer NOT NULL,
    name character varying(100) NOT NULL,
    canton_id integer NOT NULL,
    district_id integer NOT NULL,
    planning_region_id integer NOT NULL,
    mountain_region_id integer NOT NULL,
    ase integer NOT NULL,
    greater_region_id integer NOT NULL,
    language_region_id integer NOT NULL,
    ms_region_id integer NOT NULL,
    job_market_region_id integer NOT NULL,
    agglomeration_id integer NOT NULL,
    metropole_region_id integer NOT NULL,
    tourism_region_id integer NOT NULL,
    municipal_size_class_id integer NOT NULL,
    urban_character_id integer NOT NULL,
    agglomeration_size_class_id integer NOT NULL,
    is_town integer NOT NULL,
    degurba_id integer NOT NULL,
    municipal_type22_id integer NOT NULL,
    municipal_type9_id integer NOT NULL,
    ms_region_typology_id integer NOT NULL,
    alternate_names jsonb DEFAULT '[]'::json,
    lat double precision,
    long double precision,
    lv03_easting double precision,
    lv03_northing double precision,
    noise_level double precision,
    steuerfuss_gde double precision,
    steuerfuss_kanton double precision
);


--
-- Name: object_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE object_types (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    "grouping" character varying(50)
);


--
-- Name: ad_view; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--

CREATE MATERIALIZED VIEW ad_view AS
 SELECT a.id,
    a.living_area,
    a.floor,
    a.price_brutto,
    ((((a.price_brutto)::double precision / a.living_area))::numeric)::integer AS price_brutto_m2,
    a.build_year,
        CASE
            WHEN (a.last_renovation_year IS NULL) THEN 0
            ELSE 1
        END AS was_renovated,
        CASE
            WHEN ((a.build_year)::double precision >= date_part('year'::text, ('now'::text)::date)) THEN (0)::double precision
            WHEN ((a.last_renovation_year)::double precision >= date_part('year'::text, ('now'::text)::date)) THEN (0)::double precision
            WHEN (a.last_renovation_year IS NULL) THEN (date_part('year'::text, ('now'::text)::date) - (a.build_year)::double precision)
            ELSE (date_part('year'::text, ('now'::text)::date) - (a.last_renovation_year)::double precision)
        END AS last_construction,
    a.num_rooms,
    (a.living_area / a.num_rooms) AS avg_room_area,
    o.name AS otype,
    o."grouping" AS ogroup,
    ((m.zip || ' '::text) || (m.name)::text) AS municipality,
    m.canton_id,
    m.district_id,
    m.mountain_region_id,
    m.language_region_id,
    m.job_market_region_id,
    m.agglomeration_id,
    m.metropole_region_id,
    m.tourism_region_id,
    m.is_town,
    m.lat,
    m.long,
    a.crawler,
    a.tags
   FROM ((advertisements a
     JOIN object_types o ON ((o.id = a.object_types_id)))
     JOIN municipalities m ON ((m.id = a.municipalities_id)))
  WHERE ((a.price_brutto IS NOT NULL) AND (a.price_brutto > 10) AND ((o."grouping")::text <> 'ignore'::text) AND (a.living_area IS NOT NULL) AND (a.living_area > (0)::double precision) AND (a.build_year > 1200) AND (a.floor < 100) AND (a.num_rooms IS NOT NULL) AND (a.num_rooms > (0)::double precision) AND ((a.last_renovation_year IS NULL) OR ((a.last_renovation_year - a.build_year) > '-10'::integer)) AND ((date_part('year'::text, ('now'::text)::date) + (5)::double precision) > (a.build_year)::double precision))
  WITH NO DATA;


--
-- Name: advertisements_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE advertisements_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: advertisements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE advertisements_id_seq OWNED BY advertisements.id;


--
-- Name: avg_room_area_by_num_rooms; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--

CREATE MATERIALIZED VIEW avg_room_area_by_num_rooms AS
 SELECT ad_view.num_rooms,
    avg(ad_view.avg_room_area) AS avg_avg,
    count(*) AS cnt_ads
   FROM ad_view
  GROUP BY ad_view.num_rooms
  ORDER BY ad_view.num_rooms
  WITH NO DATA;


--
-- Name: object_types_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE object_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: object_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE object_types_id_seq OWNED BY object_types.id;


--
-- Name: advertisements id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY advertisements ALTER COLUMN id SET DEFAULT nextval('advertisements_id_seq'::regclass);


--
-- Name: object_types id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_types ALTER COLUMN id SET DEFAULT nextval('object_types_id_seq'::regclass);


--
-- Name: advertisements advertisements_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY advertisements
    ADD CONSTRAINT advertisements_pk PRIMARY KEY (id);


--
-- Name: municipalities municipalities_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY municipalities
    ADD CONSTRAINT municipalities_pk PRIMARY KEY (id);


--
-- Name: object_types object_type_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_types
    ADD CONSTRAINT object_type_pk PRIMARY KEY (id);


--
-- Name: iCrawler; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "iCrawler" ON advertisements USING hash (crawler varchar_ops);


--
-- Name: advertisements advertisements_municipalities; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY advertisements
    ADD CONSTRAINT advertisements_municipalities FOREIGN KEY (municipalities_id) REFERENCES municipalities(id);


--
-- Name: advertisements input_property_object_type; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY advertisements
    ADD CONSTRAINT input_property_object_type FOREIGN KEY (object_types_id) REFERENCES object_types(id);


--
-- PostgreSQL database dump complete
--

