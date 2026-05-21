# Cambios incluidos

- Al confirmar un pedido se envía automáticamente un email al cliente con dos adjuntos:
  - albarán individual del pedido
  - factura individual del pedido
- Se mantiene la opción de preparar un borrador editable de email desde el detalle del pedido.
- El resumen por proveedor permite:
  - descargar un albarán conjunto con todos los proveedores agrupados
  - descargar un albarán individual por proveedor
  - preparar un email editable para cada proveedor antes de enviarlo
- Los albaranes por proveedor se generan a partir de todos los pedidos confirmados del ciclo seleccionado.
- Se añadió servicio interno `reports/services.py` para el envío automático al cliente.
- Se añadió `render_pdf_bytes()` para adjuntar PDFs a emails sin depender de una respuesta HTTP.

Nota: para envío real de correos hay que configurar SMTP en `.env`. Si se usa backend de consola, Django imprimirá el email en la terminal.
