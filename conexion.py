import psycopg2 as pg


class Conexion():
  def __init__(self):
    self.conexion = pg.connect(
      host="localhost",
      database="termifast",
      user="soporte",
      password="soporte1011",
      port="5432" 
    )
    self.cursor = self.conexion.cursor()

  def cerrar(self):
    self.cursor.close()
    self.conexion.close()


cnn = Conexion()