from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import math

class SmartCalculator(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        history_scroll = ScrollView(size_hint=(1, 0.2))
        self.history_label = Label(
            text='',
            size_hint_y=None,
            halign='right',
            valign='top',
            font_size='16sp',
            color=(0.7, 0.7, 1, 1)
        )
        self.history_label.bind(texture_size=self.history_label.setter('size'))
        history_scroll.add_widget(self.history_label)
        main_layout.add_widget(history_scroll)
        
        self.input_display = TextInput(
            text='',
            multiline=False,
            readonly=True,
            halign='right',
            font_size='32sp',
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            size_hint=(1, 0.15)
        )
        main_layout.add_widget(self.input_display)
        
        self.result_display = TextInput(
            text='0',
            multiline=False,
            readonly=True,
            halign='right',
            font_size='48sp',
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(0, 1, 0.5, 1),
            size_hint=(1, 0.15)
        )
        main_layout.add_widget(self.result_display)
        
        buttons_layout = GridLayout(cols=5, rows=5, spacing=5, size_hint=(1, 0.5))
        
        buttons = [
            ('C', self.clear_all), ('(', self.add_char), (')', self.add_char), 
            ('⌫', self.backspace), ('±', self.toggle_sign),
            ('sin', self.add_function), ('cos', self.add_function), 
            ('tan', self.add_function), ('√', self.add_char), ('^', self.add_char),
            ('7', self.add_char), ('8', self.add_char), ('9', self.add_char), 
            ('÷', self.add_char), ('π', self.add_constant),
            ('4', self.add_char), ('5', self.add_char), ('6', self.add_char), 
            ('×', self.add_char), ('e', self.add_constant),
            ('1', self.add_char), ('2', self.add_char), ('3', self.add_char), 
            ('-', self.add_char), ('log', self.add_function),
            ('0', self.add_char), ('.', self.add_char), ('=', self.calculate), 
            ('+', self.add_char), ('!', self.factorial),
            ('Hist', self.show_history), ('M+', self.memory_add), 
            ('M-', self.memory_subtract), ('MR', self.memory_recall), ('MC', self.memory_clear)
        ]
        
        for text, func in buttons:
            btn = Button(
                text=text,
                font_size='20sp',
                background_color=self.get_button_color(text),
                on_press=func
            )
            buttons_layout.add_widget(btn)
        
        main_layout.add_widget(buttons_layout)
        
        self.history = []
        self.memory = 0
        
        return main_layout
    
    def get_button_color(self, text):
        if text in ['C', '⌫', '±']:
            return (1, 0.5, 0, 1)
        elif text in ['=', 'Hist']:
            return (0, 0.7, 0.3, 1)
        elif text in ['sin', 'cos', 'tan', 'log', '√', '^', '!', 'π', 'e']:
            return (0.4, 0.6, 1, 1)
        elif text in ['M+', 'M-', 'MR', 'MC']:
            return (0.8, 0.4, 0.8, 1)
        elif text in ['÷', '×', '-', '+']:
            return (1, 0.6, 0, 1)
        else:
            return (0.3, 0.3, 0.3, 1)
    
    def add_char(self, instance):
        current = self.input_display.text
        char = instance.text
        
        if char == '×':
            char = '*'
        elif char == '÷':
            char = '/'
        elif char == '^':
            char = '**'
        
        self.input_display.text = current + char
    
    def add_function(self, instance):
        func = instance.text
        self.input_display.text = self.input_display.text + func + '('
    
    def add_constant(self, instance):
        const = instance.text
        if const == 'π':
            self.input_display.text = self.input_display.text + '3.141592653589793'
        elif const == 'e':
            self.input_display.text = self.input_display.text + '2.718281828459045'
    
    def toggle_sign(self, instance):
        current = self.result_display.text
        if current and current != '0':
            if current[0] == '-':
                self.result_display.text = current[1:]
            else:
                self.result_display.text = '-' + current
    
    def backspace(self, instance):
        self.input_display.text = self.input_display.text[:-1]
    
    def clear_all(self, instance):
        self.input_display.text = ''
        self.result_display.text = '0'
    
    def factorial(self, instance):
        try:
            current = self.input_display.text
            if current:
                num = float(current)
                result = math.factorial(int(num))
                self.result_display.text = str(result)
                self.add_to_history(f"{current}! = {result}")
        except:
            self.result_display.text = "Error"
    
    def calculate(self, instance):
        try:
            expression = self.input_display.text
            
            expression = expression.replace('×', '*').replace('÷', '/').replace('^', '**')
            expression = expression.replace('sin', 'math.sin')
            expression = expression.replace('cos', 'math.cos')
            expression = expression.replace('tan', 'math.tan')
            expression = expression.replace('log', 'math.log10')
            expression = expression.replace('√', 'math.sqrt')
            
            result = eval(expression, {"__builtins__": {}}, {"math": math})
            
            self.result_display.text = str(result)
            self.add_to_history(f"{self.input_display.text} = {result}")
            
        except Exception as e:
            self.result_display.text = "Error"
    
    def add_to_history(self, entry):
        self.history.append(entry)
        if len(self.history) > 10:
            self.history.pop(0)
        
        self.history_label.text = '\n'.join(self.history[-5:])
    
    def show_history(self, instance):
        if not self.history:
            content = Label(text="لا توجد عمليات سابقة", font_size='20sp')
        else:
            history_text = "\n".join([f"{i+1}. {op}" for i, op in enumerate(self.history)])
            content = Label(text=history_text, font_size='18sp', halign='left', valign='top')
            content.bind(texture_size=content.setter('size'))
        
        scroll = ScrollView()
        scroll.add_widget(content)
        
        popup = Popup(
            title='الحسابات السابقة',
            content=scroll,
            size_hint=(0.9, 0.7),
            background_color=(0.2, 0.2, 0.3, 1)
        )
        popup.open()
    
    def memory_add(self, instance):
        try:
            self.memory += float(self.result_display.text)
        except:
            pass
    
    def memory_subtract(self, instance):
        try:
            self.memory -= float(self.result_display.text)
        except:
            pass
    
    def memory_recall(self, instance):
        self.input_display.text = self.input_display.text + str(self.memory)
    
    def memory_clear(self, instance):
        self.memory = 0

if __name__ == '__main__':
    SmartCalculator().run()