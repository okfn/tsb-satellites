import ckan.plugins as p

from ckanext.spatial.interfaces import ISpatialHarvester


class TSBSatellitesPlugin(p.SingletonPlugin):

    p.implements(ISpatialHarvester)
    p.implements(p.IFacets)

    # ISpatialHarvester

    def get_package_dict(self, context, data_dict):

        package_dict = data_dict['package_dict']
        iso_values = data_dict['iso_values']

        # If we need to include fields which are not extracted by the default
        # ISO parser (ie not in iso_values), reparse the ISO doc to extract
        # them
        #from ckanext.tsbsatellites.iso import CustomISODocument
        #xml_string = data_dict['harvest_object'].content
        #custom_iso_values = CustomISODocument(xml_string).read_values()


        # These values are extracted by the ISO parser but not added to the
        # package_dict by default
        package_dict['extras'].append(
                {'key': 'spatial-resolution', 'value': iso_values.get('spatial-resolution')}
        )

        for key, iso_key in [
            ('topic-category', 'topic-category'),
            ('use-constraints', 'use-constraints'),

            # Copy the temporal extent so it can be indexed as date
            ('begin-collection_date', 'temporal-extent-begin'),
            ('end-collection_date', 'temporal-extent-end'),
        ]:
            value = iso_values.get(iso_key)[0] if len(iso_values.get(iso_key, [])) else ''
            package_dict['extras'].append(
                {'key': key, 'value': value}
            )

        data_format = iso_values.get('data-format', [])
        if len(data_format) and 'name' in data_format[0]:
            package_dict['extras'].append(
                {'key': 'data-format', 'value': data_format[0]['name']},
            )

        return package_dict

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        # We will actually remove all the core facets and add our own
        facets_dict.clear()

        facets_dict['topic-category'] = p.toolkit._('Topic Category')
        facets_dict['data-format'] = p.toolkit._('Data Format')
        facets_dict['use-constraints'] = p.toolkit._('Data Cost and Access')

        #TODO: handle these as number / date
        facets_dict['spatial-resolution'] = p.toolkit._('Spatial Resolution')

        facets_dict['begin-collection_date'] = p.toolkit._('Date of Collection')

        return facets_dict