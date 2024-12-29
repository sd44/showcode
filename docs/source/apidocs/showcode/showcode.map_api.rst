:py:mod:`showcode.map_api`
==========================

.. py:module:: showcode.map_api

.. autodoc2-docstring:: showcode.map_api
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`Address <showcode.map_api.Address>`
     - .. autodoc2-docstring:: showcode.map_api.Address
          :summary:

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`pos_to_bai_coord <showcode.map_api.pos_to_bai_coord>`
     - .. autodoc2-docstring:: showcode.map_api.pos_to_bai_coord
          :summary:
   * - :py:obj:`pos_to_gaode_coord <showcode.map_api.pos_to_gaode_coord>`
     - .. autodoc2-docstring:: showcode.map_api.pos_to_gaode_coord
          :summary:
   * - :py:obj:`ret_bai_gps <showcode.map_api.ret_bai_gps>`
     - .. autodoc2-docstring:: showcode.map_api.ret_bai_gps
          :summary:
   * - :py:obj:`ret_gao_gps <showcode.map_api.ret_gao_gps>`
     - .. autodoc2-docstring:: showcode.map_api.ret_gao_gps
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`BAIDU_AK <showcode.map_api.BAIDU_AK>`
     - .. autodoc2-docstring:: showcode.map_api.BAIDU_AK
          :summary:
   * - :py:obj:`GAO_AK <showcode.map_api.GAO_AK>`
     - .. autodoc2-docstring:: showcode.map_api.GAO_AK
          :summary:

API
~~~

.. py:data:: BAIDU_AK
   :canonical: showcode.map_api.BAIDU_AK
   :value: 'replace me to your key'

   .. autodoc2-docstring:: showcode.map_api.BAIDU_AK

.. py:data:: GAO_AK
   :canonical: showcode.map_api.GAO_AK
   :value: 'replace me to your key'

   .. autodoc2-docstring:: showcode.map_api.GAO_AK

.. py:class:: Address(name, is_baidu=False, lng=0.0, lat=0.0, precise=False, comprehension=0)
   :canonical: showcode.map_api.Address

   .. autodoc2-docstring:: showcode.map_api.Address

   .. rubric:: Initialization

   .. autodoc2-docstring:: showcode.map_api.Address.__init__

   .. py:method:: __str__()
      :canonical: showcode.map_api.Address.__str__

.. py:function:: pos_to_bai_coord(name, city)
   :canonical: showcode.map_api.pos_to_bai_coord

   .. autodoc2-docstring:: showcode.map_api.pos_to_bai_coord

.. py:function:: pos_to_gaode_coord(name, city)
   :canonical: showcode.map_api.pos_to_gaode_coord

   .. autodoc2-docstring:: showcode.map_api.pos_to_gaode_coord

.. py:function:: ret_bai_gps(name, city='宁阳')
   :canonical: showcode.map_api.ret_bai_gps

   .. autodoc2-docstring:: showcode.map_api.ret_bai_gps

.. py:function:: ret_gao_gps(name, city='泰安')
   :canonical: showcode.map_api.ret_gao_gps

   .. autodoc2-docstring:: showcode.map_api.ret_gao_gps
