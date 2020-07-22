from rest_framework import generics
from rest_framework.generics import get_object_or_404


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    lookup_fields = []

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        lookup_fields = list(self.lookup_fields) if isinstance(self.lookup_fields, (tuple, list, set)) and len(
            self.lookup_fields) > 0 else [self.lookup_field]

        filter = {}
        for field in [lu for lu in lookup_fields if lu]:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class MultipleLookupListCreateView(MultipleFieldLookupMixin, generics.ListCreateAPIView):
    pass


class MultipleLookupRetrieveUpdateDestroyView(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
