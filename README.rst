
Ensembl-REST
============

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
    :target: https://saythanks.io/to/Ad115

A Python interface to the Ensembl REST APIs. A whole world of biological data 
at your fingertips.

The `Ensembl database <https://www.ensembl.org/index.html>`__ contains
reference biological data on almost any organism. Now it is easy to
access this data programatically through their REST API.

The full list of endpoints for the Ensembl REST API endpoints along with 
endpoint-specific documentation can be found on `their website 
<https://rest.ensembl.org/>`__.

This library also includes some utilities built on top of the APIs designed to
ease working with them, including an `AssemblyMapper 
<https://ad115.github.io/EnsemblRest/#ensembl_rest.AssemblyMapper>`__ class 
that helps in the conversion between different genome assemblies.


This project uses code from `RESTEasy <https://github.com/rapidstack/RESTEasy>`__,
which made my life much easier. Thanks!



Installation
------------

You can install from `PyPI <https://pypi.org/project/ensembl-rest/>`_::

    $ pip install ensembl_rest


Examples
========

The library exports methods that point to each endpoint of the
API, such as:

.. code-block:: python

    >>> import ensembl_rest

    >>> ensembl_rest.symbol_lookup(
            species='homo sapiens',
            symbol='BRCA2'
        )

::

   { 'species': 'human',
     'object_type': 'Gene',
     'description': 'BRCA2, DNA repair associated [Source:HGNC Symbol;Acc:HGNC:1101]',
     'assembly_name': 'GRCh38',
     'end': 32400266,
     ...
     ...
     ...
     'seq_region_name': '13',
     'strand': 1,
     'id': 'ENSG00000139618',
     'start': 32315474}

All the endpoints are listed on the `API website <http://rest.ensembl.org/>`__. 
A quick lookup of the methods can be obtained by calling help on the module:

.. code-block:: python

    >>> help(ensembl_rest)


If you want to use an endpoint from the ones enlisted in the `API website 
<http://rest.ensembl.org/>`__, say ``GET lookup/symbol/:species/:symbol`` , 
then the name of the corresponding method is in the endpoint documentation URL, 
in this case, the documentation links to 
http://rest.ensembl.org/documentation/info/symbol\_lookup so the 
corresponding method name is ``symbol_lookup``.

.. code-block:: python

    >>> help(ensembl_rest.symbol_lookup)

::

    Help on method symbol_lookup in module ensembl_rest.core.baseclient:
    
    symbol_lookup(*args, **kwargs) method of ensembl_rest.core.baseclient.EnsemblClient instance
        ``GET lookup/symbol/:species/:symbol``
        
        Find the species and database for a symbol in a linked external database
        - More info: https://rest.ensembl.org/documentation/info/symbol_lookup
    


We can see from the resource string ``GET lookup/symbol/:species/:symbol`` that
this method contains 2 parameters called species and symbol, so we can call the
method in the following way:

.. code-block:: python

    >>> ensembl_rest.symbol_lookup(
            species='homo sapiens',
            symbol='TP53'
        )
    
    # Or like this...
    >>> ensembl_rest.symbol_lookup('homo sapiens', 'TP53')

::

   {'source': 'ensembl_havana',
     'object_type': 'Gene',
     'logic_name': 'ensembl_havana_gene',
    ...
    ...
    ...
     'start': 32315474}

One can provide optional parameters with the ``params`` 
keyword (the specific parameters to pass depend on the specific endpoint, 
the official endpoints documentation can be found `here 
<http://rest.ensembl.org/>`_)_:

.. code-block:: python

        # Fetch also exons, transcripts, etc...
        >>> ensembl_rest.symbol_lookup('human', 'BRCA2', 
                                       params={'expand':True})

::

    {'source': 'ensembl_havana',
     'seq_region_name': '13',
     'Transcript': [{'source': 'ensembl_havana',
       'object_type': 'Transcript',
       'logic_name': 'ensembl_havana_transcript',
       'Exon': [{'object_type': 'Exon',
         'version': 4,
         'species': 'human',
         'assembly_name': 'GRCh38',
         ...
         ...
         ...
     'biotype': 'protein_coding',
     'start': 32315474}
         

The parameters for the POST endpoints are also provided via the ``params`` 
keyword  , such as in the next example:

.. code-block:: python

    >>> ensembl_rest.symbol_post(species='human',
                                 params={'symbols': ["BRCA2", 
                                                     "TP53", 
                                                     "BRAF" ]})

::

    {
        "BRCA2": {
            "source": "ensembl_havana",
            "object_type": "Gene",
            "logic_name": "ensembl_havana_gene",
            "description": "BRCA2, DNA repair associated [Source:HGNC Symbol;Acc:HGNC:1101]",
            ...
            ...
        },
        "TP53": {
            ...
            ...
        }.
        "BRAF": {
            ...
            ...
            "strand": -1,
            "id": "ENSG00000157764",
            "start": 140719327
        }
    }

Another common usage is to fetch sequences of known genes:

.. code-block:: python

    >>> ensembl_rest.sequence_id('ENSG00000157764')


::

    {'desc': 'chromosome:GRCh38:7:140719327:140924928:-1',
     'query': 'ENSG00000157764',
     'version': 13,
     'id': 'ENSG00000157764',
     'seq': 'TTCCCCCAATCCCCTCAGGCTCGG...ATTGACTGCATGGAGAAGTCTTCA',
     'molecule': 'dna'}

if you want it in FASTA, you can modify the ``headers``:

.. code-block:: python

    >>> ensembl_rest.sequence_id(
            'ENSG00000157764', 
            headers={'content-type': 'text/x-fasta'})


::

    >ENSG00000157764.13 chromosome:GRCh38:7:140719327:140924928:-1
    TTCCCCCAATCCCCTCAGGCTCGGCTGCGCCCGGGGCCGCGGGCCGGTACCTGAGGTGGC
    CCAGGCGCCCTCCGCCCGCGGCGCCGCCCGGGCCGCTCCTCCCCGCGCCCCCCGCGCCCC
    CCGCTCCTCCGCCTCCGCCTCCGCCTCCGCCTCCCCCAGCTCTCCGCCTCCCTTCCCCCT
    ...

Notice that, if left unchanged, the methods ask for data in dictionary (JSON) 
format so that they are easy to use. If the response cannot be decoded as such,
then it is returned as plain text, such as the above.

You can also map betweeen assemblies...

.. code-block:: python

    >>> ensembl_rest.assembly_map(species='human',
                                  asm_one='GRCh37',
                                  region='X:1000000..1000100:1',
                                  asm_two='GRCh38')
    
    
    # Or...
    >>> region_str = ensembl_rest.region_str(chrom='X',
                                             start=1000000,
                                             end=1000100)
    
    >>> ensembl_rest.assembly_map(species='human',
                                  asm_one='GRCh37',
                                  region=region_str,
                                  asm_two='GRCh38')

::

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


The above problem (mapping from one assembly to another) is so frequent that 
the library provides a specialized class ``AssemblyMapper`` to efficiently
mapping large amounts of regions between assemblies. This class avoids the 
time-consuming task of making a web request every time a mapping is needed by 
fetching the mapping of the whole assembly right from the instantiation. This 
is a time-consuming operation by itself, but it pays off when one has to 
transform repeatedly betweeen assemblies.::


        >>> mapper = ensembl_rest.AssemblyMapper(
                        species='human', 
                        from_assembly='GRCh37',
                        to_assembly='GRCh38'
                    )
        
        >>> mapper.map(chrom='1', pos=1000000)
        1064620

You can also find orthologs, paralogs and gene tree information, along with 
variation data and basically everything `Ensembl <http://rest.ensembl.org/>`__ 
has to offer.

If you want to instantiate your own client, you can do it by using the 
``ensembl_rest.EnsemblClient`` class, this class is the one that contains all 
the endpoint methods.

.. code-block:: python

    >>> client = ensembl_rest.EnsemblClient()

    >>> client.symbol_lookup('homo sapiens', 'TP53')


::

   {'source': 'ensembl_havana',
     'object_type': 'Gene',
     'logic_name': 'ensembl_havana_gene',
     'version': 14,
     'species': 'human',
     ...
     ...
     ...}
        

Finally, the library exposes the class ``ensembl_rest.HTTPError`` that allows to 
handle errors in the requests. An example of it's utility is when using the 
``GET genetree/member/symbol/:species/:symbol`` endpoint to query for gene trees 
in order to find ortholog and paralog proteins and genes. This endpoint returns 
an HTTP error when a gene tree is not found with code 400 and the error message 
``Lookup found nothing``. We can use this information to detect the error 
and handle it, or to simply ignore it if we expected it:


.. code-block:: python

    for gene in ['TP53', 'rare-new-gene', 'BRCA2']:
        try:
            gene_tree = ensembl_rest.genetree_member_symbol(
                            species='human',
                            symbol=gene,
                            params={'prune_species': 'human'}
                        )
            # Assuming we have a function to extract the paralogs
            paralogs = extract_paralogs(gene_tree['tree'])
            print(paralogs)

        # Handle the case when there's no gene tree
        except ensembl_rest.HTTPError as err:
            error_code = err.response.status_code
            error_message = err.response.json()['error']
            if (error_code == 400) \
               and ('Lookup found nothing' in error_message):
                # Skip the gene with no data
                pass
            else:
                # The exception was caused by another problem
                # Raise the exception again
                raise



Meta
====

**Author**: `Ad115 <https://agargar.wordpress.com/>`_ -
`Github <https://github.com/Ad115/>`_ – a.garcia230395@gmail.com

**Project pages**: 
`Docs <https://ensemblrest.readthedocs.io>`__ - `@GitHub <https://github.com/Ad115/EnsemblRest/>`__ - `@PyPI <https://pypi.org/project/ensembl-rest/>`__

Distributed under the MIT license. See
`LICENSE <https://github.com/Ad115/EnsemblRest/blob/master/LICENSE>`_
for more information.

Contributing
============

1. Check for open issues or open a fresh issue to start a discussion
   around a feature idea or a bug.
2. Fork `the repository <https://github.com/Ad115/EnsemblRest/>`_
   on GitHub to start making your changes to a feature branch, derived
   from the **master** branch.
3. Write a test which shows that the bug was fixed or that the feature
   works as expected.
4. Send a pull request and bug the maintainer until it gets merged and
   published.
