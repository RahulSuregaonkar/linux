from django import forms
from .models import sell_old_books

class NewSellingForm(forms.ModelForm):
    class Meta:
        model = sell_old_books
        fields = ["selling_prod","selling_user","category","description","regular_price","discount_price","discount_percentage","quantity","image1","image2","image3","status","slug","real_quantity","title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["selling_prod"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "selling product"}
        )
        self.fields["selling_user"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Phone"})
        self.fields["status"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address line 1"}
        )
        self.fields["category"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address Line 2"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "description"}
        )
        self.fields["regular_price"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "regular price"}
        )
        self.fields["discount_price"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Discount Price"}
        )
        self.fields["discount_percentage"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Discount Precentage"}
        )
        self.fields["quantity"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "quantity"}
        )
        self.fields["slug"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "slug"}
        )
        self.fields["real_quantity"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "real_quantity"}
        )
        self.fields["slug"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "title"}
        )
        

class NewSellingEditForm(forms.ModelForm):
    class Meta:
        model = sell_old_books
        fields = ["category","status","description","image1","image2","image3"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Status"}
        )
        self.fields["category"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Category"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "description"}
        )




