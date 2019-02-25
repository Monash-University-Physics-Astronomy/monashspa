************
Installation
************
These installation instructions assume you already have Python installed. If you do not already have a copy of Python, we recommend you install `Anaconda Python 3`_. 

.. _`Anaconda Python 3`: https://www.continuum.io/downloads

----
PyPi
----
We recommend installing `monashspa` from the Python Package Index. To do this, open a terminal (linux/OSX) or command prompt (Windows) window (or if using Anaconda, an Anaconda Prompt), and run::

    pip install monashspa
    
-------------------
Upgrading monashspa
-------------------

To upgrade to the latest version of `monashspa`, open a terminal (linux/OSX) or command prompt (Windows) window (or if using Anaconda, an Anaconda Prompt), and run::

    pip install -U monashspa
    
To upgrade to a specific version of `monashspa` (or, alternatively, if you wish to downgrade), run::

    pip install -U monashspa==<version>
    
where :code:`<version>` is replaced by the version you wish (for example :code:`pip install -U monashspa==0.1.0`).

.. note:: After upgrading, you will need to **restart** any open Python or IPython terminals in order to ensure you are using the new version. This includes terminals within Spyder (restart the entire Spyder application if you are unsure how to restart a terminal). You can check which version of monashspa you are using by running :code:`import monashspa` followed by :code:`print(monashspa.__version__)` from with a Python script or terminal.
