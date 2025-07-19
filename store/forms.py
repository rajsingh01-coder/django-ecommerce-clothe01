from django import forms
from .models import Order, CartItem, Contact, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CheckoutForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=[
            ('cod', 'Cash on Delivery'),
            ('razorpay', 'Razorpay'),
            ('stripe', 'Stripe'),
            ('paypal', 'PayPal'),
            ('upi', 'UPI'),
            ('other', 'Other'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label='Payment Method'
    )
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'country',
            'shipping_address', 'phone_number', 'payment_method'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'shipping_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your complete shipping address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shipping_address'].label = 'Shipping Address'
        self.fields['phone_number'].label = 'Phone Number'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['email'].label = 'Email'
        self.fields['phone'].label = 'Phone'
        self.fields['address'].label = 'Address'
        self.fields['city'].label = 'City'
        self.fields['state'].label = 'State'
        self.fields['zip_code'].label = 'ZIP Code'
        self.fields['country'].label = 'Country'
        # Make all new fields required
        for field in ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'country']:
            self.fields[field].required = True
        self.fields['shipping_address'].required = True
        self.fields['phone_number'].required = True


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity', 'size', 'color']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '99'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        
        if product:
            # Set size choices based on product
            if product.available_sizes:
                self.fields['size'].choices = [('', 'Select Size')] + [(size, size) for size in product.available_sizes]
            else:
                self.fields['size'].widget = forms.HiddenInput()
            
            # Set color choices based on product
            if product.available_colors:
                self.fields['color'].choices = [('', 'Select Color')] + [(color, color) for color in product.available_colors]
            else:
                self.fields['color'].widget = forms.HiddenInput()


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search products...',
            'aria-label': 'Search'
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Price',
            'step': '0.01'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Price',
            'step': '0.01'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email address'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your message'
            })
        } 