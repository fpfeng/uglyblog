from django import template

register = template.Library()


@register.filter(name='addcls')
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='addpl')
def addpl(field, arg):
    if not arg:
        return field
    field.field.widget.attrs.update({'placeholder': arg})
    return field
