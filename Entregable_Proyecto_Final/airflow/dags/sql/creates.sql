CREATE TABLE if not EXISTS exportaciones_productos_primarios_stg (
            date_from TIMESTAMP distkey,
            millones_dolares FLOAT,
            frequency VARCHAR,
            month INT
        )sortkey(date_from);

CREATE TABLE if not EXISTS exportaciones_productos_primarios (
            date_from TIMESTAMP distkey,
            millones_dolares FLOAT,
            frequency VARCHAR,
            month INT
        )sortkey(date_from);