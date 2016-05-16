#!/usr/bin/python
import os
import datetime


from lxml import etree


start = datetime.datetime.now()
print('\n\nStart time:\t{}'.format(start))


# print etree.ErrorLevels._names
# print etree.ErrorTypes._names
# print etree.ErrorDomains._names


# schema_file = r'E:\thredds\junk01\InvCatalog.1.0.7.xsd'
# print('\n\nschema_file:\t{}'.format(schema_file))


schema_url = r'http://www.unidata.ucar.edu/schemas/thredds/InvCatalog.1.0.7.xsd'
print('\n\nschema_url:\t{}'.format(schema_url))


print('\tValidating schema...')
schema_doc = etree.parse(schema_url)
try:
    schema = etree.XMLSchema(schema_doc)
except etree.XMLSchemaParseError as e:
    print e
    exit(1)
print('\tSchema OK.')


root_folder = r'E:\thredds\junk02'
print('\n\nroot_folder:\t{}'.format(root_folder))


exclude_folders = set(['compass', 'palettes', 'public', 'root', 'tomcat-conf'])
# exclude_folders = set(['compass', 'palettes', 'public', 'root', 'tomcat-conf', 'catalog-eidc', 'catalog-public'])
print('\n\nexclude_folders:')
for exclude_folder in exclude_folders:
    print('\t\t{}'.format(exclude_folder))


exclude_files = set(['threddsConfig.xml', 'wmsConfig.xml'])
print('\n\nexclude_files:')
for exclude_file in exclude_files:
    print('\t\t{}'.format(exclude_file))


# include_files = set(['chessdetail.xml'])
# print('\n\ninclude_files:')
# for include_file in include_files:
#     print('\t\t{}'.format(include_file))


print('\n\nWalking through folder structure...')
for path, subdirs, files in os.walk(root_folder):
    subdirs[:] = [d for d in subdirs if d not in exclude_folders]
    for x in files:
        if x.endswith('.xml') and x not in exclude_files:
        # if x.endswith('.xml') and x in include_files:
            xml_file = os.path.join(path, x)
            print('\n\n\txml_file:\t{}'.format(xml_file))
            print('\t\tTesting for well-formedness...')
            try:
                xml_doc = etree.parse(xml_file)
            except etree.XMLSyntaxError as e:
                print('\t\tDocument not well-formed!')
                print('\t\t\t{}'.format(e))
            else:
                print('\t\tDocument is well-formed.')
                print('\t\tValidating document...')
                # xml_doc = etree.parse(xml_file)
                try:
                    print('\t\t\tschema.validate(xml_doc):\t{}'.format(schema.validate(xml_doc)))
                    schema.assertValid(xml_doc)
                except etree.DocumentInvalid as e:
                    print('\t\tDocument not valid!')
                    # print('\t\t{0}'.format(e))
                    print('\t\t\tErrors found:\t{:>3}'.format(len(schema.error_log)))
                    error_count = 0
                    for error in schema.error_log:
                        error_count += 1
                        print('\t\t\t\tError:\t{:>3}'.format(error_count))
                        # print('\t\t\t\terror:\t{}'.format(error))
                        print('\t\t\t\t\tMessage:\t{}'.format(error.message))
                        # print('\t\t\t\t\tDomain:\t{}'.format(error.domain))
                        # print('\t\t\t\t\tType:\t{}'.format(error.type))
                        # print('\t\t\t\t\tLevel:\t{}'.format(error.level))
                        print('\t\t\t\t\tLine number:\t{}'.format(error.line))
                        print('\t\t\t\t\tColumn:\t{}'.format(error.column))
                        print('\t\t\t\t\tFilename:\t{}'.format(error.filename))
                        # print('\t\t\t\t\tDomain name:\t{}'.format(error.domain_name))
                        # print('\t\t\t\t\tType name:\t{}'.format(error.type_name))
                        # print('\t\t\t\t\tLevel name:\t{}'.format(error.level_name))
                    # exit(1)
                else:
                    print('\t\tDocument is valid.')
print('\n\nWalked through folder structure.')


end = datetime.datetime.now()
print('\n\nEnd time:\t{}'.format(end))


elapsed = end - start
print('\n\nElapsed time:\t{}'.format(elapsed))


print('\n\nDone.\n\n')

