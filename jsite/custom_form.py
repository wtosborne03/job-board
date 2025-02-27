from crispy_forms.layout import BaseInput
import django.forms as forms
from django.utils.safestring import mark_safe


class CustomSubmit(BaseInput):
    """
    Used to create a custom Submit button descriptor for the {% crispy %} template tag::
        submit = CustomSubmit('Search the Site', 'search this site')
    .. note:: The first argument is also slugified and turned into the id for the submit button.

    This is a customised version for Tailwind to add Tailwind CSS style by default
    """

    input_type = "submit"

    def __init__(self, *args, css_class=None, **kwargs):
        if css_class is None:
            self.field_classes = "bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer"
        else:
            self.field_classes = css_class
        super().__init__(*args, **kwargs)


class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=attrs, **kwargs)
        img_html = ''
        if value and hasattr(value, 'url'):

            img_html = mark_safe(f'<img src="{
                                 value.url}" alt="Image preview" style="margin-left: 10px; max-height: 100px;"/>')
        return mark_safe(f'<div class="flex flex-row w-full justify-between items-center">{input_html}{img_html}</div>')
