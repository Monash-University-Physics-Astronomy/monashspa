************
Installation
************
These installation instructions assume you already have Python installed. If you do not already have a copy of Python, we recommend you install `Anaconda Python 3`_. 

.. _`Anaconda Python 3`: https://www.anaconda.com/products/individual#Downloads

----
PyPi
----
We recommend installing `monashspa` from the Python Package Index. To do this, open Spyder and in the console window (bottom right) at the `In [1]` prompt type::

    !pip install monashspa

followed by return. The package should now install. You only need to do this once.

-------------------
Upgrading monashspa
-------------------

To upgrade to the latest version of `monashspa`, open Spyder and in the console window (bottom right) at the `In [1]` prompt type::

    !pip install -U monashspa
    
To upgrade to a specific version of `monashspa` (or, alternatively, if you wish to downgrade), run::

    pip install -U monashspa==<version>
    
where :code:`<version>` is replaced by the version you wish (for example :code:`pip install -U monashspa==0.1.0`).

.. note:: After upgrading, you will need to **restart** any open Python or IPython terminals in order to ensure you are using the new version. This includes terminals within Spyder (restart the entire Spyder application if you are unsure how to restart a terminal). You can check which version of monashspa you are using by running :code:`import monashspa` followed by :code:`print(monashspa.__version__)` from with a Python script or terminal.

-----------------------
Run inside Google Colab
-----------------------
If for some reason you have trouble installaing `Anaconda` on your local computer, it is possible to run everything inside your web browser using what is called `Google Colab`. Follow the directions below to get this up and working.

#. Go to `Google Colab <https://research.google.com/colaboratory/>`
#. In the window that comes up select `GitHub`
#. At the line that asks for a `GitHub URL` type `Monash-University-Physics-Astronomy` and press return
#. Pick one of the files that shows up (like the `PHS2062 one`)
#. Select `Copy to Drive` at the top of the code to get your own copy to work on
#. If your python code requires some data file, then pick the small folder icon to the left and then select the little icon with an up arrow to upload a file.
#. You are now ready to run. If you want to come back to your code later, simply go to your Google Drive, find the file inside the `Colab Notebooks` folder and double click it. Note that you might have to upload your data file again though.
