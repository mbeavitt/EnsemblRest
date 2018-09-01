EnsemblRest
===========

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
:target: https://saythanks.io/to/Ad115

An interface to the Ensembl REST APIs, a whole world of biological data
at your fingertips.

The `Ensembl database <https://www.ensembl.org/index.html>`__ contains
reference biological data on almost any organism. Now it is easy to
access this data programatically through their REST API.

The specific documentation on the Ensembl REST API is on `their
website <https://rest.ensembl.org/>`__.


Installation
------------

You can install from PyPI::

    $ pip install ensembl_rest


Examples
--------

The library exports two main classes: ``ensembl_rest.EnsemblClient`` and
``ensembl_rest.EnsemblGenomesClient`` that point respectively to the `main
REST API <http://rest.ensembl.org/>`__ and to the `Ensembl Genomes REST
API <http://rest.ensemblgenomes.org/>`__.

.. code-block:: python

    >>> import ensembl_rest
    
    >>> client = ensembl_rest.EnsemblClient()

If you want to use a method from the REST API, say:
``GET lookup/symbol/:species/:symbol``\ (http://rest.ensembl.org/documentation/info/symbol\_lookup)
then the corresponding method on the class is called after the last
string in the link to the documentation page, in this case,
``symbol_lookup``.

.. code-block:: python

    >>> help(client.symbol_lookup)


.. code-block:: python

    Help on method symbol_lookup in module pyensembl.core.base:
    
    symbol_lookup(*args, **kwargs) method of pyensembl.core.base.Ensembl instance
        GET lookup/symbol/:species/:symbol
        
        Find the species and database for a symbol in a linked external database
        More info: https://rest.ensembl.org/documentation/info/symbol_lookup
    


We can see from the resource string
``GET lookup/symbol/:species/:symbol`` that this method contains 2
parameters called species and symbol, so we can call the method in the
following way:

.. code-block:: python

    >>> client.symbol_lookup(species='homo sapiens',
                         symbol='TP53')
    
    # Or like this...
    >>> client.symbol_lookup('homo sapiens', 'TP53')


.. code-block:: python

    {'source': 'ensembl_havana',
     'object_type': 'Gene',
     'logic_name': 'ensembl_havana_gene',
     'version': 16,
     'species': 'homo sapiens',
     'description': 'tumor protein p53 [Source:HGNC Symbol;Acc:HGNC:11998]',
     'display_name': 'TP53',
     'assembly_name': 'GRCh38',
     'biotype': 'protein_coding',
     'end': 7687550,
     'seq_region_name': '17',
     'db_type': 'core',
     'strand': -1,
     'id': 'ENSG00000141510',
     'start': 7661779}



Another common usage is to fetch sequences of known genes:

.. code-block:: python

    >>> client.sequence_id('ENSG00000157764')


.. code-block:: python

    {'desc': 'chromosome:GRCh38:7:140719327:140924928:-1',
     'query': 'ENSG00000157764',
     'version': 13,
     'id': 'ENSG00000157764',
     'seq': 'TTCCCCCAATCCCCTCAGGCTCGGCTGCGCCCGGGGC...ACTGCTATAATAAAGATTGACTGCATGGAGAAGTCTTCA',
     'molecule': 'dna'}



Or to map betweeen assemblies...

.. code-block:: python

    >>> client.assembly_map(species='human',
                        asm_one='GRCh37',
                        region='X:1000000..1000100:1',
                        asm_two='GRCh38')


.. code-block:: python

    {'mappings': [{'original': {'seq_region_name': 'X',
        'strand': 1,
        'coord_system': 'chromosome',
        'end': 1000100,
        'start': 1000000,
        'assembly': 'GRCh37'},
       'mapped': {'seq_region_name': 'X',
        'strand': 1,
        'coord_system': 'chromosome',
        'end': 1039365,
        'start': 1039265,
        'assembly': 'GRCh38'}}]}


Meta
----

**Author**: ``Ad115 <https://agargar.wordpress.com/>``\ \_ -
``Github <https://github.com/Ad115/>``\ \_ – a.garcia230395@gmail.com

Distributed under the MIT license. See
``LICENSE <https://github.com/Ad115/PyEnsembl/blob/master/LICENSE>``\ \_
for more information.

Contributing
------------

1. Check for open issues or open a fresh issue to start a discussion
   around a feature idea or a bug.
2. Fork ``the repository <https://github.com/Ad115/EnsemblRest/>``\ \_
   on GitHub to start making your changes to a feature branch, derived
   from the **master** branch.
3. Write a test which shows that the bug was fixed or that the feature
   works as expected.
4. Send a pull request and bug the maintainer until it gets merged and
   published.
