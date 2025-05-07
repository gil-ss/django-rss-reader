from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    existing_classes = field.field.widget.attrs.get("class", "")
    classes = f"{existing_classes} {css}".strip()
    return field.as_widget(attrs={"class": classes})
