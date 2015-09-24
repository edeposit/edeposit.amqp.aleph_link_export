Aleph link export poznámky
==========================

Žádost k exportu
----------------
Z hlediska Alephu funguje vše tak, že se přes SCP připojí na ``edeposit-aplikace``, kde si vyzvedne soubor ``edep2aleph.xml``. Ten je vytvořený podle `následujícího XSD <https://raw.githubusercontent.com/edeposit/edeposit.amqp.aleph_link_export/master/src/edeposit/amqp/aleph_link_export/xsd/link_export_notification.xsd>`_:

.. include:: ../../src/edeposit/amqp/aleph_link_export/xsd/link_export_notification.xsd
   :literal:

Ukázka
++++++

.. include:: ../examples/request_example.xml
   :literal:

Odpověď
-------
Script na straně Alephu XML zpracuje a výsledky zapíše do souboru ``aleph2edep.xml``, který poté nahraje zpět na SCP. Odpověď se skládá z jednotlivých ``<result>`` záznamů, které obsahují stejný parametr ``session_id``, jako záznam, na který je to odpověď a položku ``<status>``, nabírající hodnot buďto ``OK``, nebo ``ERROR``.

Soubor je vytvořen podle `schématu definovaného následujícím XSD <https://raw.githubusercontent.com/edeposit/edeposit.amqp.aleph_link_export/master/src/edeposit/amqp/aleph_link_export/xsd/link_export_result.xsd>`_:

.. include:: ../../src/edeposit/amqp/aleph_link_export/xsd/link_export_result.xsd
   :literal:


Ukázka
++++++

.. include:: ../examples/response_example.xml
   :literal:

Pozor, zde se nepoužívá **record**, ale **result**.

Poznámky
--------
Programové vybavení modulu `aleph_link_export` automaticky odstraní všechny záznamy ``<record>`` ze souboru ``edep2aleph.xml``, které již mají odpověď v ``aleph2edep.xml``.

Workflow na straně Alephu by tedy mělo vypadat následovně:

------------

    - Jednou za čas jsem spuštěn (čas je nutné domluvit).
    - Stáhnu ``edep2aleph.xml``
        - Procházím všechny ``<record>`` záznamy v něm, něco s nimi dělám.
        - Výsledky zapisuji do druhého souboru ``aleph2edep.xml`` jako ``<result>`` tagy.
            - Do ``<result>`` kopíruji ``session_id``.
    - Nově vzniklý ``aleph2edep.xml`` nahraji zpět na SCP.

------------

Díky tomu, že všechny ``<record>`` tagy jsou po přijetí odpovědi E-depositem z vstupního XML automaticky odstraněny, není nutné používat vícero souborů. Výstupní XMl může být pokaždé přepsáno.

XSD
---
XSD specifikace je zde a takto je také vkládána jako ``xsi:schemaLocation``:

    - http://edeposit-aplikace.nkp.cz/link_export_result.xsd
    - http://edeposit-aplikace.nkp.cz/link_export_notification.xsd
