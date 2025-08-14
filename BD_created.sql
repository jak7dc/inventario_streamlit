-- TABLA DE CATEGORIAS

CREATE TABLE public.categoria
(
    id_categoria serial NOT NULL,
    nombre_categoria character varying(150) NOT NULL DEFAULT 'NA',
    descripcion_categoria character varying(250) NOT NULL DEFAULT 'NA',
    PRIMARY KEY (id_categoria)
);

ALTER TABLE IF EXISTS public.categoria
    OWNER to soporte;

-- TABLA DE PRODUCTOS

CREATE TABLE public.producto
(
    id_producto serial NOT NULL,
    referencia_producto character varying(50) NOT NULL,
    nombre_producto character varying(100) NOT NULL,
    unidades_producto INTEGER NOT NULL,
    peso_producto double precision NOT NULL,
    unmedida_producto character varying(15) NOT NULL,
    id_categoria integer NOT NULL,
    PRIMARY KEY (id_producto),
    CONSTRAINT producto_categoria FOREIGN KEY (id_categoria)
        REFERENCES public.categoria (id_categoria) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT
        NOT VALID
);

ALTER TABLE IF EXISTS public.producto
    OWNER to soporte;

COMMENT ON CONSTRAINT producto_categoria ON public.producto
    IS 'conexión entre producto y categoría ';


