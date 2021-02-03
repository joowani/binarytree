Graphviz and Jupyter Notebook
-----------------------------

From version 6.0.0, binarytree can integrate with Graphviz_ to render trees in image
viewers, browsers and Jupyter notebooks using the python-graphviz_ library.

In order to use this feature, you must first install the Graphviz software in your OS
and ensure its executables are on your PATH system variable (usually done automatically
during installation):

.. code-block:: bash

    # Ubuntu and Debian
    $ sudo apt install graphviz

    # Fedora and CentOS
    $ sudo yum install graphviz

    # Windows using choco (or winget)
    $ choco install graphviz

Use :func:`binarytree.Node.graphviz` to generate `graphviz.Digraph`_ objects:

.. code-block:: python

    from binarytree import tree

    t = tree()

    # Generate a graphviz.Digraph object
    # Arguments to this method are passed into Digraph.__init__
    graph = t.graphviz()

    # Get DOT (graph description language) body
    graph.body

    # Render the binary tree
    graph.render()

With Graphviz you can also visualize binary trees in `Jupyter notebooks`_:

.. image:: https://user-images.githubusercontent.com/2701938/107016813-3c818600-6753-11eb-8140-6b7a95791c08.gif
    :alt: Jupyter Notebook GIF

.. _DOT: https://graphviz.org/doc/info/lang.html
.. _Graphviz: https://graphviz.org/
.. _python-graphviz: https://github.com/xflr6/graphviz
.. _graphviz.Digraph: https://graphviz.readthedocs.io/en/stable/api.html#digraph
.. _Jupyter notebooks: https://jupyter.org/
