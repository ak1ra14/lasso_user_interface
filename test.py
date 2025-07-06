# main.py
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.recycleview import RecycleView
from screens.timezone import TimezoneListView
class CustomButton(Button):
    """
    A custom button class that extends Kivy's Button.
    It includes properties for text and image source, and its layout
    is defined entirely in Python.
    """
    button_text = StringProperty("Click Me!")  # Default text for the button
    button_image_source = StringProperty("placeholder.png")  # Default image source

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set the background color to blue with some transparency (RGBA)
        self.background_color = (0.1, 0.5, 0.9, 1)  # Blue color
        # Set the background normal to an empty string to allow custom background
        self.background_normal = ''
        # Set the background down to an empty string for consistency
        self.background_down = ''

        # Define the canvas instructions for drawing the button's background
        with self.canvas.before:
            # Use the background_color property for the button's color
            self.color_instruction = Color(rgba=self.background_color)
            # Draw a rounded rectangle that matches the button's size and position
            self.rounded_rect_instruction = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[20,]  # Adjust this value for more or less curvature
            )

        # Bind updates to the canvas instructions when pos or size changes
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.bind(background_color=self._update_color)

        # Create a BoxLayout to hold the image and text
        self.content_layout = BoxLayout(
            orientation='horizontal',
            padding=5,
            spacing=5
        )
        # Removed manual binding for pos and size of content_layout.
        # BoxLayout by default has size_hint=(1,1) and will fill its parent.

        # Image widget for the button logo
        self.image_widget = Image(
            source=self.button_image_source,
            keep_ratio=True,
            allow_stretch=True,
            width=60, # Initial width, will be adjusted by size_hint_x: None
            size_hint_x=None,
            size_hint_y=0.8
        )
        self.image_widget.bind(source=self._update_image_source)

        # Label for the button text
        self.label_widget = Label(
            text=self.button_text,
            color=(1, 1, 1, 1), # White color
            halign='center',
            valign='middle',
            font_size='20sp',
            size_hint_x=1
        )
        self.label_widget.bind(text=self._update_label_text)

        # Add the image and label to the content layout
        self.content_layout.add_widget(self.image_widget)
        self.content_layout.add_widget(self.label_widget)

        # Add the content layout as a child of the button
        # Kivy's layout system will automatically position and size this
        # BoxLayout within the CustomButton based on its default size_hint=(1,1).
        self.add_widget(self.content_layout)

    def _update_rect(self, instance, value):
        """Callback to update the position and size of the rounded rectangle."""
        self.rounded_rect_instruction.pos = instance.pos
        self.rounded_rect_instruction.size = instance.size

    def _update_color(self, instance, value):
        """Callback to update the color of the rounded rectangle."""
        self.color_instruction.rgba = value

    def _update_image_source(self, instance, value):
        """Callback to update the image source when button_image_source changes."""
        self.image_widget.source = value

    def _update_label_text(self, instance, value):
        """Callback to update the label text when button_text changes."""
        self.label_widget.text = value

    # Removed _update_content_layout_pos and _update_content_layout_size callbacks
    # as they are no longer needed.


class CustomButtonApp(App):
    """
    The main application class for demonstrating the custom button.
    """
    def build(self):
        """
        Builds the application's user interface.
        """
        # Create a BoxLayout to hold the custom button
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        # Create an instance of the CustomButton with specific text and image
        custom_btn = CustomButton(
            button_text="My Custom Button",
            button_image_source="https://placehold.co/60x60/000000/FFFFFF?text=Logo" # Placeholder image
        )
        # Bind a function to the button's on_press event
        custom_btn.bind(on_press=self.on_button_press)

        # Create another custom button to show different text and image
        another_btn = CustomButton(
            button_text="Another Button",
            button_image_source="https://placehold.co/60x60/FF0000/FFFFFF?text=Icon" # Another placeholder
        )
        another_btn.bind(on_press=self.on_button_press)

        # Add the custom buttons to the layout
        layout.add_widget(custom_btn)
        layout.add_widget(another_btn)

        return layout

    def on_button_press(self, instance):
        """
        Callback function for when a custom button is pressed.
        Prints the text of the pressed button to the console.
        """
        print(f"Button '{instance.button_text}' pressed!")

class TestApp(App):
    """
    A simple test application to run the CustomButtonApp.
    """
    def build(self):
            from kivy.uix.scrollview import ScrollView
            layout = BoxLayout(orientation='vertical', size=(400, 400), size_hint=(None,None))
            layout.bind(minimum_height=layout.setter('height'))

            for tz in ["UTC", "US/Eastern", "Asia/Tokyo"]:
                layout.add_widget(Button(text=tz, size_hint_y=None, height=200))
            scroll = ScrollView(size_hint=(1, None), size=(400,400), do_scroll_x=False)

            scroll.add_widget(layout)
            return scroll

if __name__ == '__main__':
    # Run the Kivy application
    # CustomButtonApp().run()
    from kivy.core.window import Window
   # Window.size = (800, 800)  # Set the window size for testing
    TestApp().run()
