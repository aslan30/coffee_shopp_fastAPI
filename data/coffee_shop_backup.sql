--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: aerich; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.aerich (
    id integer NOT NULL,
    version character varying(255) NOT NULL,
    app character varying(100) NOT NULL,
    content jsonb NOT NULL
);


ALTER TABLE public.aerich OWNER TO postgres;

--
-- Name: aerich_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.aerich_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.aerich_id_seq OWNER TO postgres;

--
-- Name: aerich_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.aerich_id_seq OWNED BY public.aerich.id;


--
-- Name: basket; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.basket (
    id uuid NOT NULL,
    quantity smallint DEFAULT 0 NOT NULL,
    menu_item_id uuid NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.basket OWNER TO postgres;

--
-- Name: category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.category (
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    image character varying(255)
);


ALTER TABLE public.category OWNER TO postgres;

--
-- Name: establishment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.establishment (
    id uuid NOT NULL,
    location character varying(50) NOT NULL
);


ALTER TABLE public.establishment OWNER TO postgres;

--
-- Name: menuitem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menuitem (
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    image character varying(255),
    description text,
    price double precision,
    category_id uuid
);


ALTER TABLE public.menuitem OWNER TO postgres;

--
-- Name: order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."order" (
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "phoneNumb1" character varying(20) NOT NULL,
    "phoneNumb2" character varying(20),
    location character varying(120),
    "totalPrice" numeric(10,2) DEFAULT 0 NOT NULL,
    delivery_type character varying(10) DEFAULT 'delivery'::character varying NOT NULL,
    pickup_location character varying(120) NOT NULL,
    delivery_location character varying(120) NOT NULL,
    status character varying(10) DEFAULT 'pending'::character varying NOT NULL,
    courier_id uuid,
    establishment_id uuid,
    user_id uuid NOT NULL
);


ALTER TABLE public."order" OWNER TO postgres;

--
-- Name: COLUMN "order".delivery_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public."order".delivery_type IS 'DELIVERY: delivery\nPICKUP: pickup';


--
-- Name: COLUMN "order".status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public."order".status IS 'PENDING: pending\nACCEPTED: accepted\nREJECTED: rejected\nPREPARING: preparing\nREADY: ready\nDELIVERING: delivering\nCOMPLETED: completed\nCANCELLED: cancelled';


--
-- Name: orderelement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orderelement (
    id uuid NOT NULL,
    quantity smallint NOT NULL,
    menu_item_id uuid NOT NULL,
    order_id uuid NOT NULL
);


ALTER TABLE public.orderelement OWNER TO postgres;

--
-- Name: supportchat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.supportchat (
    id uuid NOT NULL,
    message text NOT NULL,
    message_type character varying(10) NOT NULL,
    response text,
    is_read boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.supportchat OWNER TO postgres;

--
-- Name: COLUMN supportchat.message_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.supportchat.message_type IS 'COMPLAINT: complaint\nQUESTION: question\nSUGGESTION: suggestion';


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id uuid NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    profile_picture character varying(255),
    role character varying(20),
    password character varying(255) NOT NULL,
    is_verified boolean DEFAULT false NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    verification_token character varying(255),
    deleted_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    phone character varying(20),
    additional_phone character varying(20),
    verification_code character varying(4)
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: COLUMN "user".role; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public."user".role IS 'customer: customer\ncourier: courier\nadmin: admin\nsupport: support';


--
-- Name: aerich id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aerich ALTER COLUMN id SET DEFAULT nextval('public.aerich_id_seq'::regclass);


--
-- Data for Name: aerich; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.aerich (id, version, app, content) FROM stdin;
1	0_20250309034304_init.py	models	{"models.User": {"app": "models", "name": "models.User", "table": "user", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "first_name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "first_name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(50)", "oracle": "NVARCHAR2(50)"}}, {"name": "last_name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "last_name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(50)", "oracle": "NVARCHAR2(50)"}}, {"name": "email", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "email", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(50)", "oracle": "NVARCHAR2(50)"}}, {"name": "profile_picture", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "profile_picture", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)", "oracle": "NVARCHAR2(255)"}}, {"name": "role", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "role", "docstring": null, "generated": false, "field_type": "CharEnumFieldInstance", "constraints": {"max_length": 20}, "description": "customer: customer\\ncourier: courier\\nadmin: admin\\nsupport: support", "python_type": "str", "db_field_types": {"": "VARCHAR(20)", "oracle": "NVARCHAR2(20)"}}, {"name": "password", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "password", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)", "oracle": "NVARCHAR2(255)"}}, {"name": "is_verified", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "is_verified", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "is_active", "unique": false, "default": true, "indexed": false, "nullable": false, "db_column": "is_active", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "verification_token", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "verification_token", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)", "oracle": "NVARCHAR2(255)"}}, {"name": "deleted_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": true, "db_column": "deleted_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {}, "description": null, "python_type": "datetime.datetime", "auto_now_add": false, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "phone", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "phone", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 20}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(20)", "oracle": "NVARCHAR2(20)"}}, {"name": "additional_phone", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "additional_phone", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 20}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(20)", "oracle": "NVARCHAR2(20)"}}, {"name": "verification_code", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "verification_code", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 4}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(4)", "oracle": "NVARCHAR2(4)"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "assigned_orders", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.Order", "db_constraint": true}, {"name": "orders", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.Order", "db_constraint": true}, {"name": "support_messages", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.SupportChat", "db_constraint": true}, {"name": "basket", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.Basket", "db_constraint": true}], "backward_o2o_fields": []}, "models.Order": {"app": "models", "name": "models.Order", "table": "order", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.User", "db_constraint": true}, {"name": "courier", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "SET NULL", "raw_field": "courier_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.User", "db_constraint": true}, {"name": "establishment", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "SET NULL", "raw_field": "establishment_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.Establishment", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "phoneNumb1", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "phoneNumb1", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "phoneNumb2", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "phoneNumb2", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "location", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "location", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 120}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(120)", "oracle": "NVARCHAR2(120)"}}, {"name": "totalPrice", "unique": false, "default": 0.0, "indexed": false, "nullable": false, "db_column": "totalPrice", "docstring": null, "generated": false, "field_type": "DecimalField", "constraints": {}, "description": null, "python_type": "decimal.Decimal", "db_field_types": {"": "DECIMAL(10,2)", "sqlite": "VARCHAR(40)"}}, {"name": "delivery_type", "unique": false, "default": "delivery", "indexed": false, "nullable": false, "db_column": "delivery_type", "docstring": null, "generated": false, "field_type": "CharEnumFieldInstance", "constraints": {"max_length": 10}, "description": "DELIVERY: delivery\\nPICKUP: pickup", "python_type": "str", "db_field_types": {"": "VARCHAR(10)", "oracle": "NVARCHAR2(10)"}}, {"name": "pickup_location", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "pickup_location", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 120}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(120)", "oracle": "NVARCHAR2(120)"}}, {"name": "delivery_location", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "delivery_location", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 120}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(120)", "oracle": "NVARCHAR2(120)"}}, {"name": "status", "unique": false, "default": "pending", "indexed": false, "nullable": false, "db_column": "status", "docstring": null, "generated": false, "field_type": "CharEnumFieldInstance", "constraints": {"max_length": 10}, "description": "PENDING: pending\\nACCEPTED: accepted\\nREJECTED: rejected\\nCOMPLETED: completed\\nCANCELLED: cancelled", "python_type": "str", "db_field_types": {"": "VARCHAR(10)", "oracle": "NVARCHAR2(10)"}}, {"name": "courier_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "courier_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, {"name": "establishment_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "establishment_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "order_elements", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.OrderElement", "db_constraint": true}], "backward_o2o_fields": []}, "models.Aerich": {"app": "models", "name": "models.Aerich", "table": "aerich", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "version", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "version", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)", "oracle": "NVARCHAR2(255)"}}, {"name": "app", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "app", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(100)", "oracle": "NVARCHAR2(100)"}}, {"name": "content", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "content", "docstring": null, "generated": false, "field_type": "JSONField", "constraints": {}, "description": null, "python_type": "Union[dict, list]", "db_field_types": {"": "JSON", "mssql": "NVARCHAR(MAX)", "oracle": "NCLOB", "postgres": "JSONB"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Basket": {"app": "models", "name": "models.Basket", "table": "basket", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [{"name": "menu_item", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "menu_item_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.MenuItem", "db_constraint": true}, {"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.User", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "quantity", "unique": false, "default": 0, "indexed": false, "nullable": false, "db_column": "quantity", "docstring": null, "generated": false, "field_type": "SmallIntField", "constraints": {"ge": -32768, "le": 32767}, "description": null, "python_type": "int", "db_field_types": {"": "SMALLINT"}}, {"name": "menu_item_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "menu_item_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Category": {"app": "models", "name": "models.Category", "table": "category", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "name", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(100)", "oracle": "NVARCHAR2(100)"}}, {"name": "image", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "image", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)", "oracle": "NVARCHAR2(255)"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "items", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.MenuItem", "db_constraint": true}], "backward_o2o_fields": []}, "models.MenuItem": {"app": "models", "name": "models.MenuItem", "table": "menuitem", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [{"name": "category", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "category_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.Category", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "name", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(100)", "oracle": "NVARCHAR2(100)"}}, {"name": "image", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "image", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)", "oracle": "NVARCHAR2(255)"}}, {"name": "description", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "description", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "price", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "price", "docstring": null, "generated": false, "field_type": "FloatField", "constraints": {}, "description": null, "python_type": "float", "db_field_types": {"": "DOUBLE PRECISION", "mysql": "DOUBLE", "sqlite": "REAL"}}, {"name": "category_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "category_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "orderelements", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.OrderElement", "db_constraint": true}, {"name": "basket", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.Basket", "db_constraint": true}], "backward_o2o_fields": []}, "models.SupportChat": {"app": "models", "name": "models.SupportChat", "table": "supportchat", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.User", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "message", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "message", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "message_type", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "message_type", "docstring": null, "generated": false, "field_type": "CharEnumFieldInstance", "constraints": {"max_length": 10}, "description": "COMPLAINT: complaint\\nQUESTION: question\\nSUGGESTION: suggestion", "python_type": "str", "db_field_types": {"": "VARCHAR(10)", "oracle": "NVARCHAR2(10)"}}, {"name": "response", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "response", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "is_read", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "is_read", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "updated_at", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "updated_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.OrderElement": {"app": "models", "name": "models.OrderElement", "table": "orderelement", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [{"name": "menu_item", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "menu_item_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.MenuItem", "db_constraint": true}, {"name": "order", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "order_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.Order", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "quantity", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "quantity", "docstring": null, "generated": false, "field_type": "SmallIntField", "constraints": {"ge": -32768, "le": 32767}, "description": null, "python_type": "int", "db_field_types": {"": "SMALLINT"}}, {"name": "menu_item_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "menu_item_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, {"name": "order_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "order_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Establishment": {"app": "models", "name": "models.Establishment", "table": "establishment", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "location", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "location", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(50)", "oracle": "NVARCHAR2(50)"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "orders", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.Order", "db_constraint": true}], "backward_o2o_fields": []}}
2	1_20250309233438_change_phone_fields_to_char.py	models	{"models.User": {"app": "models", "name": "models.User", "table": "user", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "first_name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "first_name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(50)", "oracle": "NVARCHAR2(50)"}}, {"name": "last_name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "last_name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(50)", "oracle": "NVARCHAR2(50)"}}, {"name": "email", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "email", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(50)", "oracle": "NVARCHAR2(50)"}}, {"name": "profile_picture", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "profile_picture", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)", "oracle": "NVARCHAR2(255)"}}, {"name": "role", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "role", "docstring": null, "generated": false, "field_type": "CharEnumFieldInstance", "constraints": {"max_length": 20}, "description": "customer: customer\\ncourier: courier\\nadmin: admin\\nsupport: support", "python_type": "str", "db_field_types": {"": "VARCHAR(20)", "oracle": "NVARCHAR2(20)"}}, {"name": "password", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "password", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)", "oracle": "NVARCHAR2(255)"}}, {"name": "is_verified", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "is_verified", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "is_active", "unique": false, "default": true, "indexed": false, "nullable": false, "db_column": "is_active", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "verification_token", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "verification_token", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)", "oracle": "NVARCHAR2(255)"}}, {"name": "deleted_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": true, "db_column": "deleted_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {}, "description": null, "python_type": "datetime.datetime", "auto_now_add": false, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "phone", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "phone", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 20}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(20)", "oracle": "NVARCHAR2(20)"}}, {"name": "additional_phone", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "additional_phone", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 20}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(20)", "oracle": "NVARCHAR2(20)"}}, {"name": "verification_code", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "verification_code", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 4}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(4)", "oracle": "NVARCHAR2(4)"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "assigned_orders", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.Order", "db_constraint": true}, {"name": "orders", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.Order", "db_constraint": true}, {"name": "support_messages", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.SupportChat", "db_constraint": true}, {"name": "basket", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.Basket", "db_constraint": true}], "backward_o2o_fields": []}, "models.Order": {"app": "models", "name": "models.Order", "table": "order", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.User", "db_constraint": true}, {"name": "courier", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "SET NULL", "raw_field": "courier_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.User", "db_constraint": true}, {"name": "establishment", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "SET NULL", "raw_field": "establishment_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.Establishment", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "phoneNumb1", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "phoneNumb1", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 20}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(20)", "oracle": "NVARCHAR2(20)"}}, {"name": "phoneNumb2", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "phoneNumb2", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 20}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(20)", "oracle": "NVARCHAR2(20)"}}, {"name": "location", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "location", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 120}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(120)", "oracle": "NVARCHAR2(120)"}}, {"name": "totalPrice", "unique": false, "default": 0.0, "indexed": false, "nullable": false, "db_column": "totalPrice", "docstring": null, "generated": false, "field_type": "DecimalField", "constraints": {}, "description": null, "python_type": "decimal.Decimal", "db_field_types": {"": "DECIMAL(10,2)", "sqlite": "VARCHAR(40)"}}, {"name": "delivery_type", "unique": false, "default": "delivery", "indexed": false, "nullable": false, "db_column": "delivery_type", "docstring": null, "generated": false, "field_type": "CharEnumFieldInstance", "constraints": {"max_length": 10}, "description": "DELIVERY: delivery\\nPICKUP: pickup", "python_type": "str", "db_field_types": {"": "VARCHAR(10)", "oracle": "NVARCHAR2(10)"}}, {"name": "pickup_location", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "pickup_location", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 120}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(120)", "oracle": "NVARCHAR2(120)"}}, {"name": "delivery_location", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "delivery_location", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 120}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(120)", "oracle": "NVARCHAR2(120)"}}, {"name": "status", "unique": false, "default": "pending", "indexed": false, "nullable": false, "db_column": "status", "docstring": null, "generated": false, "field_type": "CharEnumFieldInstance", "constraints": {"max_length": 10}, "description": "PENDING: pending\\nACCEPTED: accepted\\nREJECTED: rejected\\nCOMPLETED: completed\\nCANCELLED: cancelled", "python_type": "str", "db_field_types": {"": "VARCHAR(10)", "oracle": "NVARCHAR2(10)"}}, {"name": "courier_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "courier_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, {"name": "establishment_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "establishment_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "order_elements", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.OrderElement", "db_constraint": true}], "backward_o2o_fields": []}, "models.Aerich": {"app": "models", "name": "models.Aerich", "table": "aerich", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "version", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "version", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)", "oracle": "NVARCHAR2(255)"}}, {"name": "app", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "app", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(100)", "oracle": "NVARCHAR2(100)"}}, {"name": "content", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "content", "docstring": null, "generated": false, "field_type": "JSONField", "constraints": {}, "description": null, "python_type": "Union[dict, list]", "db_field_types": {"": "JSON", "mssql": "NVARCHAR(MAX)", "oracle": "NCLOB", "postgres": "JSONB"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Basket": {"app": "models", "name": "models.Basket", "table": "basket", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [{"name": "menu_item", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "menu_item_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.MenuItem", "db_constraint": true}, {"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.User", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "quantity", "unique": false, "default": 0, "indexed": false, "nullable": false, "db_column": "quantity", "docstring": null, "generated": false, "field_type": "SmallIntField", "constraints": {"ge": -32768, "le": 32767}, "description": null, "python_type": "int", "db_field_types": {"": "SMALLINT"}}, {"name": "menu_item_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "menu_item_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Category": {"app": "models", "name": "models.Category", "table": "category", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "name", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(100)", "oracle": "NVARCHAR2(100)"}}, {"name": "image", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "image", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)", "oracle": "NVARCHAR2(255)"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "items", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.MenuItem", "db_constraint": true}], "backward_o2o_fields": []}, "models.MenuItem": {"app": "models", "name": "models.MenuItem", "table": "menuitem", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [{"name": "category", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "category_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.Category", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "name", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(100)", "oracle": "NVARCHAR2(100)"}}, {"name": "image", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "image", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)", "oracle": "NVARCHAR2(255)"}}, {"name": "description", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "description", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "price", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "price", "docstring": null, "generated": false, "field_type": "FloatField", "constraints": {}, "description": null, "python_type": "float", "db_field_types": {"": "DOUBLE PRECISION", "mysql": "DOUBLE", "sqlite": "REAL"}}, {"name": "category_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "category_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "orderelements", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.OrderElement", "db_constraint": true}, {"name": "basket", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.Basket", "db_constraint": true}], "backward_o2o_fields": []}, "models.SupportChat": {"app": "models", "name": "models.SupportChat", "table": "supportchat", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.User", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "message", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "message", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "message_type", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "message_type", "docstring": null, "generated": false, "field_type": "CharEnumFieldInstance", "constraints": {"max_length": 10}, "description": "COMPLAINT: complaint\\nQUESTION: question\\nSUGGESTION: suggestion", "python_type": "str", "db_field_types": {"": "VARCHAR(10)", "oracle": "NVARCHAR2(10)"}}, {"name": "response", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "response", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "is_read", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "is_read", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "updated_at", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "updated_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.OrderElement": {"app": "models", "name": "models.OrderElement", "table": "orderelement", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [{"name": "menu_item", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "menu_item_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.MenuItem", "db_constraint": true}, {"name": "order", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "order_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.Order", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "quantity", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "quantity", "docstring": null, "generated": false, "field_type": "SmallIntField", "constraints": {"ge": -32768, "le": 32767}, "description": null, "python_type": "int", "db_field_types": {"": "SMALLINT"}}, {"name": "menu_item_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "menu_item_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, {"name": "order_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "order_id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Establishment": {"app": "models", "name": "models.Establishment", "table": "establishment", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function uuid.uuid4>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "UUIDField", "constraints": {}, "description": null, "python_type": "uuid.UUID", "db_field_types": {"": "CHAR(36)", "postgres": "UUID"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "location", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "location", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(50)", "oracle": "NVARCHAR2(50)"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "orders", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.Order", "db_constraint": true}], "backward_o2o_fields": []}}
\.


--
-- Data for Name: basket; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.basket (id, quantity, menu_item_id, user_id) FROM stdin;
\.


--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.category (id, name, image) FROM stdin;
\.


--
-- Data for Name: establishment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.establishment (id, location) FROM stdin;
\.


--
-- Data for Name: menuitem; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menuitem (id, name, image, description, price, category_id) FROM stdin;
\.


--
-- Data for Name: order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."order" (id, created_at, "phoneNumb1", "phoneNumb2", location, "totalPrice", delivery_type, pickup_location, delivery_location, status, courier_id, establishment_id, user_id) FROM stdin;
\.


--
-- Data for Name: orderelement; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orderelement (id, quantity, menu_item_id, order_id) FROM stdin;
\.


--
-- Data for Name: supportchat; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.supportchat (id, message, message_type, response, is_read, created_at, updated_at, user_id) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, first_name, last_name, email, profile_picture, role, password, is_verified, is_active, verification_token, deleted_at, created_at, phone, additional_phone, verification_code) FROM stdin;
\.


--
-- Name: aerich_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.aerich_id_seq', 2, true);


--
-- Name: aerich aerich_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aerich
    ADD CONSTRAINT aerich_pkey PRIMARY KEY (id);


--
-- Name: basket basket_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.basket
    ADD CONSTRAINT basket_pkey PRIMARY KEY (id);


--
-- Name: category category_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_name_key UNIQUE (name);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: establishment establishment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.establishment
    ADD CONSTRAINT establishment_pkey PRIMARY KEY (id);


--
-- Name: menuitem menuitem_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menuitem
    ADD CONSTRAINT menuitem_name_key UNIQUE (name);


--
-- Name: menuitem menuitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menuitem
    ADD CONSTRAINT menuitem_pkey PRIMARY KEY (id);


--
-- Name: order order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_pkey PRIMARY KEY (id);


--
-- Name: orderelement orderelement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orderelement
    ADD CONSTRAINT orderelement_pkey PRIMARY KEY (id);


--
-- Name: supportchat supportchat_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supportchat
    ADD CONSTRAINT supportchat_pkey PRIMARY KEY (id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: basket basket_menu_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.basket
    ADD CONSTRAINT basket_menu_item_id_fkey FOREIGN KEY (menu_item_id) REFERENCES public.menuitem(id) ON DELETE CASCADE;


--
-- Name: basket basket_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.basket
    ADD CONSTRAINT basket_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: menuitem menuitem_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menuitem
    ADD CONSTRAINT menuitem_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.category(id) ON DELETE CASCADE;


--
-- Name: order order_courier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_courier_id_fkey FOREIGN KEY (courier_id) REFERENCES public."user"(id) ON DELETE SET NULL;


--
-- Name: order order_establishment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_establishment_id_fkey FOREIGN KEY (establishment_id) REFERENCES public.establishment(id) ON DELETE SET NULL;


--
-- Name: order order_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: orderelement orderelement_menu_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orderelement
    ADD CONSTRAINT orderelement_menu_item_id_fkey FOREIGN KEY (menu_item_id) REFERENCES public.menuitem(id) ON DELETE CASCADE;


--
-- Name: orderelement orderelement_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orderelement
    ADD CONSTRAINT orderelement_order_id_fkey FOREIGN KEY (order_id) REFERENCES public."order"(id) ON DELETE CASCADE;


--
-- Name: supportchat supportchat_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supportchat
    ADD CONSTRAINT supportchat_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

