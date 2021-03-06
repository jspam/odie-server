from django.db import models

class Cart(models.Model):
    name = models.CharField(max_length=200)
    creation_time = models.DateTimeField(auto_now_add=True)

    @property
    def document_ids(self):
        return [cartdocument.document_id for cartdocument in self.cartdocument_set.all()]

class CartDocument(models.Model):
    cart = models.ForeignKey(Cart)
    # cannot be a relation since it's cross-db _and_ id-transformed
    document_id = models.IntegerField()
