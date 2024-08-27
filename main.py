from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
import mysql.connector

class VerificadorDePrecios(App):
    def build(self):

        self.conexion_bd = mysql.connector.connect(
            host="192.168.0.117",
            user="user_jugueteria",
            password="12345",
            database="ventas"
        )
        self.cursor = self.conexion_bd.cursor()


        Window.clearcolor = (1,1,1,1)
        self.layout = BoxLayout(
            orientation='vertical',
            padding=10,
            spacing=10
        )

        self.image = Image(
            source='logo-casa-gonnet.jpg',
            size_hint=(1,0.6)
        )

        self.input_escaner = TextInput(
            hint_text='ESCANEE EL CODIGO DE BARRAS DEL PRODUCTO',
            multiline=False,
            font_size= 25,
            halign='center',
            size_hint=(1, 0.2)
        )
        self.input_escaner.bind(on_text_validate=self.on_enter)
        
        self.label_producto = Label(
            text='PRODUCTO: ',
            font_size= 35,
            color= (0,0,0,1),
            size_hint=(1, 0.4)
        )
        self.label_precio = Label(
            text='PRECIO: ',
            font_size= 35,
            color= (0,0,0,1),
            size_hint=(1, 0.4)
        )

        self.layout.add_widget(self.image)
        self.layout.add_widget(self.input_escaner)
        self.layout.add_widget(self.label_producto)
        self.layout.add_widget(self.label_precio)

        return self.layout

    def on_enter(self, instance):
        codigo_barras = instance.text

        nombre_producto, precio_producto = self.obtener_producto(codigo_barras)
        self.label_producto.text = f'PRODUCTO: {nombre_producto}'
        self.label_precio.text = f'PRECIO: ${precio_producto}'
        instance.text = ''
        Clock.schedule_once(lambda dt: self.focus_input(), 0.1)

    def focus_input(self):
        self.input_escaner.focus = True

    def obtener_producto(self, codigo_barras):

        self.cursor.execute('SELECT producto_nombre, producto_precio_venta FROM producto WHERE producto_codigo = %s', (codigo_barras,))
        producto = self.cursor.fetchone()
        while self.cursor.nextset():
            pass

        if producto:
            nombre_producto, precio_producto = producto
        else:
            nombre_producto, precio_producto = 'PRODUCTO NO ENCONTRADO', ''

        return nombre_producto, precio_producto
    
if __name__ == '__main__':
    VerificadorDePrecios().run()
